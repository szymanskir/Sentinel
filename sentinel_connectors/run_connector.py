import click
import logging
import json
import os
import os.path
import sys

from datetime import datetime
from sentinel_connectors.historical import HistoricalConnectorFactory
from sentinel_connectors.stream import StreamConnectorFactory
from sentinel_connectors.keyword_manager import (
    ConstKeywordManager,
    DynamicKeywordManager,
)
from sentinel_connectors.utils import read_config
from sentinel_connectors.sinks import (
    IDataSink,
    KafkaSink,
    KinesisSink,
    SinkNotAvailableError,
)

LOGGER = logging.getLogger("main")
LOG_DIRECTORY = "logs"
CURRENT_DATETIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def setup_logger(filename: str):
    logging.basicConfig(
        level=logging.DEBUG,
        filename=filename,
        filemode="w",
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("main").addHandler(logging.StreamHandler(sys.stdout))
    logging.getLogger(f"{DynamicKeywordManager.__name__}").addHandler(
        logging.StreamHandler(sys.stdout)
    )


def get_sink(sink: str):
    if sink == "kafka":
        return KafkaSink()
    elif sink == "kinesis":
        return KinesisSink()
    else:
        raise ValueError(f"Unsupported sink: {sink}")


@click.group()
def main():
    if not os.path.isdir(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--source", required=True)
@click.option("--keywords", type=click.STRING, required=True)
@click.option("--since", type=click.DateTime(), required=True)
@click.option("--until", type=click.DateTime(), default=str(datetime.today().date()))
@click.option("--sink", type=click.Choice(["kafka", "kinesis"]))
def historical(config_file, source, keywords, since, until, sink):
    setup_logger(
        os.path.join(LOG_DIRECTORY, f"logs_historical_{source}_{CURRENT_DATETIME}.log")
    )
    config = read_config(config_file)
    keywords = keywords.split(",")
    factory = HistoricalConnectorFactory()
    connector = factory.create_historical_connector(source, config)
    sink = get_sink(sink)

    try:
        for mention in connector.download_mentions(keywords, since, until):
            sink.put(mention)
            LOGGER.info(f"TEXT:{mention.text}")
    except Exception as e:
        LOGGER.error(e)


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--source", required=True)
@click.option("--keywords", type=click.STRING)
@click.option("--sink", type=click.Choice(["kafka", "kinesis"]))
def stream(config_file, source, keywords, sink):
    setup_logger(
        os.path.join(LOG_DIRECTORY, f"logs_stream_{source}_{CURRENT_DATETIME}.log")
    )

    config = read_config(config_file)
    factory = StreamConnectorFactory()
    connector = factory.create_stream_connector(source, config)
    sink = get_sink(sink)

    def stream_mentions():
        while True:
            try:
                for mention in connector.stream_comments():
                    if keyword_manager.any_match(mention.text):
                        sink.put(mention)
                        LOGGER.info(f"HIT: {mention.text[:30]}")
                    else:
                        LOGGER.info(f"MISS: {mention.text[:30]}")
            except SinkNotAvailableError as e:
                raise RuntimeError from e
            except Exception as e:
                LOGGER.error(e)

    if keywords is not None:
        keyword_manager = ConstKeywordManager(keywords.split(","))
        stream_mentions()
    else:
        keyword_manager = DynamicKeywordManager()
        try:
            keyword_manager.run()
            stream_mentions()
        finally:
            keyword_manager.exit()


if __name__ == "__main__":
    main()

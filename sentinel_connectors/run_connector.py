import click
import logging
import logging.handlers
import json
import math
import os
import os.path
import sys
import watchtower

from datetime import datetime
from sentinel_connectors.historical import HistoricalConnectorFactory
from sentinel_connectors.stream import StreamConnectorFactory
from sentinel_connectors.keyword_manager import (
    ConstKeywordManager,
    DynamicKeywordManager,
)
from sentinel_connectors.metric_logger import (
    IMetricLogger,
    DevNullMetricLogger,
    CloudWatchMetricLogger,
)
from sentinel_connectors.sinks import (
    IDataSink,
    KafkaSink,
    KinesisSink,
    DevNullSink,
    SinkNotAvailableError,
)

LOGGER = logging.getLogger("sentinel")
LOG_DIRECTORY = "logs"
CURRENT_DATETIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
MAX_BACKUPS = 7


def setup_logger(filename: str):
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=filename, when="midnight", backupCount=MAX_BACKUPS
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    cloud_watch_handler = watchtower.CloudWatchLogHandler()
    cloud_watch_handler.setFormatter(formatter)
    cloud_watch_handler.setLevel(logging.ERROR)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(cloud_watch_handler)
    root_logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.DEBUG)

    LOGGER.addHandler(stdout_handler)
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(cloud_watch_handler)
    LOGGER.setLevel(logging.DEBUG)


def get_sink(sink: str):
    if sink == "kafka":
        return KafkaSink()
    elif sink == "kinesis":
        return KinesisSink()
    elif sink == "dev-null":
        return DevNullSink()
    else:
        raise ValueError(f"Unsupported sink: {sink}")


@click.group()
def main():
    if not os.path.isdir(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)


@main.command()
@click.option("--source", required=True)
@click.option("--keywords", type=click.STRING, required=True)
@click.option("--since", type=click.DateTime(), required=True)
@click.option("--until", type=click.DateTime(), default=str(datetime.today().date()))
@click.option("--sink", type=click.Choice(["kafka", "kinesis", "dev-null"]))
def historical(source, keywords, since, until, sink):
    setup_logger(
        os.path.join(LOG_DIRECTORY, f"logs_historical_{source}_{CURRENT_DATETIME}.log")
    )
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
@click.option("--source", required=True)
@click.option("--keywords", type=click.STRING)
@click.option("--sink", type=click.Choice(["kafka", "kinesis", "dev-null"]))
def stream(source, keywords, sink):
    setup_logger(
        os.path.join(LOG_DIRECTORY, f"logs_stream_{source}_{CURRENT_DATETIME}.log")
    )

    factory = StreamConnectorFactory()
    connector = factory.create_stream_connector(source)
    sink = get_sink(sink)

    if keywords is not None:
        keyword_manager = ConstKeywordManager(keywords.split(","))
    else:
        keyword_manager = DynamicKeywordManager()
        keyword_manager.start()

    if sink == "dev-null":
        metric_logger = DevNullMetricLogger()
    else:
        metric_logger = CloudWatchMetricLogger(source)
        metric_logger.start()
    LOGGER.error("TESTERROR-SENTINEL")
    while True:
        try:
            for mention in connector.stream_comments():
                metric_logger.increment_data()
                if keyword_manager.any_match(mention.text):
                    sink.put(mention)
                    LOGGER.debug(f"HIT: {mention.text[:30]}")
                    metric_logger.increment_hits()
                else:
                    LOGGER.debug(f"MISS: {mention.text[:30]}")
        except SinkNotAvailableError as e:
            raise RuntimeError from e
        except Exception as e:
            LOGGER.error(e)


if __name__ == "__main__":
    main()

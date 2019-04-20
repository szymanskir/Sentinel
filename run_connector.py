import click
import logging

from datetime import datetime
from sentinel.connectors.historical import HistoricalConnectorFactory
from sentinel.connectors.stream import StreamConnectorFactory
from sentinel.utils import read_config

LOGGER = logging.getLogger("main")


@click.group()
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M:%S",
    )


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--source", required=True)
@click.option("--keywords", type=click.STRING, required=True)
@click.option("--since", type=click.DateTime(), required=True)
@click.option("--until", type=click.DateTime(), default=str(datetime.today().date()))
def historical(config_file, source, keywords, since, until):
    config = read_config(config_file)
    keywords = keywords.split(",")
    factory = HistoricalConnectorFactory()
    connector = factory.create_historical_connector(source, config)

    for mention in connector.download_mentions(keywords, since, until):
        LOGGER.info(f"TEXT:{mention.text}")


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--source", required=True)
@click.option("--keywords", type=click.STRING, required=True)
def stream(config_file, source, keywords):
    config = read_config(config_file)
    keywords = keywords.split(",")
    factory = StreamConnectorFactory()
    connector = factory.create_stream_connector(source, config)
    for mention in connector.stream_comments():
        LOGGER.info(f"TEXT: {mention}")


if __name__ == "__main__":
    main()

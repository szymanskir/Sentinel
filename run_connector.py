import click
import logging

from datetime import datetime
from sentinel.connectors.historical import HistoricalConnectorFactory
from sentinel.connectors.stream import StreamConnectorFactory

LOGGER = logging.getLogger("main")


@click.group()
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M:%S",
    )


@main.command()
@click.option("--source", required=True)
@click.option("--keywords", type=click.STRING, required=True)
@click.option("--since", type=click.DateTime(), required=True)
@click.option("--until", type=click.DateTime(), default=str(datetime.today().date()))
def historical(source, keywords, since, until):
    keywords = keywords.split(",")
    factory = HistoricalConnectorFactory()
    connector = factory.create_historical_connector(source)

    for mention in connector.download_mentions(keywords, since, until):
        LOGGER.info(f"TEXT:{mention.text}")


@main.command()
@click.option("--source", required=True)
@click.option("--keywords", type=click.STRING, required=True)
def stream(source, keywords):
    keywords = keywords.split(",")
    factory = StreamConnectorFactory()
    connector = factory.create_stream_connector(source)
    for mention in connector.stream_comments():
        LOGGER.info(f"TEXT: {mention}")


if __name__ == "__main__":
    main()

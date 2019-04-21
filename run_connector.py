import click
import logging

from datetime import datetime
from sentinel.connectors.historical import HistoricalConnectorFactory
from sentinel.connectors.stream import StreamConnectorFactory
from sentinel.keyword_manager import ConstKeywordManager, DynamicKeywordManager

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
@click.option("--keywords", type=click.STRING)
def stream(source, keywords):
    factory = StreamConnectorFactory()
    connector = factory.create_stream_connector(source)

    def stream_mentions():
        for mention in connector.stream_comments():
            if keyword_manager.any_match(mention.text):
                LOGGER.info(f"HIT: {mention.text[:30]}")
            else:
                LOGGER.info(f"MISS: {mention.text[:30]}")

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

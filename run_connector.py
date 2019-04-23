import click
import logging
import kafka
import json

from datetime import datetime
from sentinel.connectors.historical import HistoricalConnectorFactory
from sentinel.connectors.stream import StreamConnectorFactory
from sentinel.keyword_manager import ConstKeywordManager, DynamicKeywordManager
from sentinel.utils import read_config

KAFKA_URL = "sandbox-hdp.hortonworks.com:6667"


def ensure_topics_exist():
    all_topics = ["reddit", "twitter", "google-news", "hacker-news"]

    admin = kafka.admin.KafkaAdminClient(bootstrap_servers=[KAFKA_URL])
    client = kafka.KafkaClient([KAFKA_URL])
    existing_topics = client.topics
    topics = [
        kafka.admin.NewTopic(topic, 1, 1)
        for topic in all_topics
        if topic not in existing_topics
    ]
    admin.create_topics(topics)


LOGGER = logging.getLogger("main")
producer = kafka.KafkaProducer(
    bootstrap_servers=[KAFKA_URL],
    value_serializer=lambda m: json.dumps(m).encode("utf8"),
)


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
@click.option("--keywords", type=click.STRING)
def stream(config_file, source, keywords):
    config = read_config(config_file)
    factory = StreamConnectorFactory()
    connector = factory.create_stream_connector(source, config)
    ensure_topics_exist()

    def stream_mentions():
        for mention in connector.stream_comments():
            if keyword_manager.any_match(mention.text):
                producer.send(mention.source, mention.to_json())
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

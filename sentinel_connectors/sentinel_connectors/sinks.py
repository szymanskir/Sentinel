from kinesis.producer import KinesisProducer
import kafka
import json
from sentinel_common.mentions import Mention
from abc import ABCMeta


class IDataSink(metaclass=ABCMeta):
    def put(self, mention: Mention):
        pass


class SinkNotAvailableError(Exception):
    pass


class KafkaSink(IDataSink):
    KAFKA_URL = "sandbox-hdp.hortonworks.com:6667"

    def __init__(self):
        self._producer = None

    def put(self, mention: Mention):
        if self._producer is None:
            self._ensure_topics_exist()
            self._producer = kafka.KafkaProducer(
                bootstrap_servers=[self.KAFKA_URL],
                value_serializer=lambda m: json.dumps(m).encode("utf8"),
            )

        self._producer.send(mention.source, mention.to_json())

    def _ensure_topics_exist(self):
        all_topics = ["reddit", "twitter", "google-news", "hacker-news"]

        try:
            admin = kafka.admin.KafkaAdminClient(bootstrap_servers=[self.KAFKA_URL])
            client = kafka.KafkaClient([self.KAFKA_URL])
            existing_topics = client.topics
            topics = [
                kafka.admin.NewTopic(topic, 1, 1)
                for topic in all_topics
                if topic not in existing_topics
            ]
            admin.create_topics(topics)
        except Exception as e:
            raise SinkNotAvailableError from e


class KinesisSink(IDataSink):
    def __init__(self):
        self._producer = None

    def put(self, mention: Mention):
        if self._producer is None:
            try:
                self._producer = KinesisProducer(stream_name="sentinel-stream")
            except Exception as e:
                raise SinkNotAvailableError from e

        self._producer.put(mention.to_json())


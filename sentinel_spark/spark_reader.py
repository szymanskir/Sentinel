from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import os
from sentinel_common.mentions import Mention
import json
from textblob import TextBlob

sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 3)

kafka_params = {"bootstrap.servers": "sandbox-hdp.hortonworks.com:6667"}


def to_mention(data_tuple):
    _, mention_raw = data_tuple
    return Mention.from_json(json.loads(mention_raw))


kafka_stream = KafkaUtils.createDirectStream(ssc, ["hacker-news"], kafka_params)

parsed_stream = kafka_stream.map(lambda x: to_mention(x))

text_counts = parsed_stream.map(
    lambda mention: (mention.text, TextBlob(mention.text).sentiment)
)
text_counts.pprint()

ssc.start()
ssc.awaitTermination()

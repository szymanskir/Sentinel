from pyspark.sql.types import *
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import os
from sentinel_common.mentions import Mention
from sentinel_spark.data_manipulation.text_preprocessing import clean_comment_text
from sentinel_spark.data_manipulation.stream_utils import to_mention, clean_mention_text
from textblob import TextBlob


sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 3)

kafka_params = {"bootstrap.servers": "sandbox-hdp.hortonworks.com:6667"}

kafka_stream = KafkaUtils.createDirectStream(ssc, ["twitter"], kafka_params)
twitter_mentions_cleaned = kafka_stream.map(lambda x: to_mention(x)).map(lambda x: clean_mention_text(x, clean_comment_text))
twitter_mentions_enriched = twitter_mentions_cleaned.map(lambda x: (x, TextBlob(x.text).sentiment.polarity))

twitter_mentions_enriched.pprint()

ssc.start()
ssc.awaitTermination()

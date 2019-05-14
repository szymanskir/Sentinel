from pyspark.sql.types import *
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import os
from sentinel.models.mentions import Mention
from sentinel.data_manipulation.text_preprocessing import clean_article_text
from sentinel.data_manipulation.stream_utils import to_mention, clean_mention_text
from textblob import TextBlob


sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 3)

kafka_params = {"bootstrap.servers": "sandbox-hdp.hortonworks.com:6667"}

kafka_stream = KafkaUtils.createDirectStream(ssc, ["google-news"], kafka_params)
google_news_mentions_cleaned = kafka_stream.map(lambda x: to_mention(x)).map(lambda x: clean_mention_text(x, clean_article_text))
google_news_mentions_enriched = google_news_mentions_cleaned.map(lambda x: (x, TextBlob(x.text).sentiment.polarity))

google_news_mentions_enriched.pprint()

ssc.start()
ssc.awaitTermination()

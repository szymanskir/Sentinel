from pyspark.sql.types import *
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
import os
from sentinel.models.mentions import Mention
from sentinel.data_manipulation.text_preprocessing import clean_article_text
from textblob import TextBlob
from stream_utils import to_mention, clean_mention_text


sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 3)

kafka_stream = KafkaUtils.createDirectStream(ssc, ["hacker-news"], kafka_params)
hacker_news_mentions_cleaned = kafka_stream.map(lambda x: to_mention(x)).map(lambda x: clean_mention_text(x, clean_article_text))
hacker_news_mentions_enriched = hacker_news_mentions_cleaned.map(lambda x: (x, TextBlob(x.text).sentiment.polarity))

pprint(hacker_news_mentions_enriched)

ssc.start()
ssc.awaitTermination()

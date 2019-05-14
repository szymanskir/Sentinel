from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import os
from sentinel.models.mentions import Mention
import json
from textblob import TextBlob
import datetime

sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 500)

kafka_params = {"bootstrap.servers": "sandbox-hdp.hortonworks.com:6667"}


def to_mention(data_tuple):
    _, mention_raw = data_tuple
    return json.loads(mention_raw)


kafka_stream = KafkaUtils.createDirectStream(ssc, ["hacker-news", "reddit", "twitter", "google-news"], kafka_params)


parsed_stream = kafka_stream.window(500, 500) \
                            .map(lambda x: to_mention(x)) \

def tpprint(val):
    """
    Print the first num elements of each RDD generated in this DStream.
    @param num: the number of elements from the first will be printed.
    """
    def takeAndPrint(time, rdd):
        print("########################")
        print("Time: %s" % time)
        print("########################")
        rdd.saveAsPickleFile(f"hdfs:///user/root/data/mentions-{time.timestamp()}", 500)
        print("...")
        print("")
    val.foreachRDD(takeAndPrint)

tpprint(parsed_stream)

ssc.start()
ssc.awaitTermination()

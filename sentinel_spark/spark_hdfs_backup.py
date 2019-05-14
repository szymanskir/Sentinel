from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from sentinel_spark.data_manipulation.stream_utils import to_mention

sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 500)

kafka_params = {"bootstrap.servers": "sandbox-hdp.hortonworks.com:6667"}
kafka_stream = KafkaUtils.createDirectStream(ssc,
                                             ["hacker-news",
                                              "google-news",
                                              "twitter",
                                              "reddit"],
                                             kafka_params
                                             )

parsed_stream = kafka_stream.window(500, 500).map(lambda x: to_mention(x))


def dump_to_hdfs(val):
    """
    Dump dstream content to hdfs
    """
    def save_as_pickle(time, rdd):
        print("########################")
        print("Time: %s" % time)
        print("########################")
        rdd.saveAsPickleFile(
            f"hdfs:///user/root/pickles/mentions-{time.timestamp()}", 500
            )
        print("...")
        print("")
    val.foreachRDD(save_as_pickle)


dump_to_hdfs(parsed_stream)

ssc.start()
ssc.awaitTermination()

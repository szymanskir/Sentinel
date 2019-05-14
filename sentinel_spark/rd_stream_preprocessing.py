from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from sentinel_spark.data_manipulation.text_preprocessing \
    import clean_comment_text
from sentinel_spark.data_manipulation.stream_utils \
    import to_mention, clean_mention_text
from textblob import TextBlob

from sentinel_spark.db_writer import save_to_db

sc = SparkContext.getOrCreate()
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 3)

kafka_params = {"bootstrap.servers": "sandbox-hdp.hortonworks.com:6667"}

kafka_stream = KafkaUtils.createDirectStream(ssc, ["reddit"], kafka_params)
reddit_mentions_cleaned = kafka_stream.map(lambda x: to_mention(x)).map(
    lambda x: clean_mention_text(x, clean_comment_text)
)
reddit_mentions_enriched = reddit_mentions_cleaned.map(
    lambda x: (x, TextBlob(x.text).sentiment.polarity)
)

output = reddit_mentions_enriched.mapPartitions(lambda x: save_to_db(x))

output.pprint()

ssc.start()
ssc.awaitTermination()

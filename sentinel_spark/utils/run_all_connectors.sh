# Use `killall -9 python3.6` to stop all processes
declare -a topics=("google-news" "hacker-news" "reddit" "twitter")
KEYWORDS="the"
REPO_DIR=/shared/Sentinel

PYTHON_INTERPRETER=python3.6

source $REPO_DIR/sentinel_connectors/.env/bin/activate
echo Starting producers...
for topic in "${topics[@]}"; do
    echo Starting $topic producer
    $PYTHON_INTERPRETER $REPO_DIR/sentinel_connectors/run_connector.py stream $REPO_DIR/sentinel_connectors/config.ini --source $topic --keywords $KEYWORDS &> /dev/null &
done
deactivate

echo Starting consumers...
# /bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.3 /shared/Sentinel/sentinel_spark/gn_stream_preprocessing.py &
# /bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.3 /shared/Sentinel/sentinel_spark/hn_stream_preprocessing.py &
# /bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.3 /shared/Sentinel/sentinel_spark/rd_stream_preprocessing.py &
# /bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.3 /shared/Sentinel/sentinel_spark/tw_stream_preprocessing.py &
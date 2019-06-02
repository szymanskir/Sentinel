# Use `killall -9 python3.6` to stop all processes
declare -a topics=("google-news" "hacker-news" "reddit" "twitter")
KEYWORDS="the"

PYTHON_INTERPRETER=python3.6

echo Starting producers...
for topic in "${topics[@]}"; do
    echo Starting $topic producer
    $PYTHON_INTERPRETER run_connector.py stream --source $topic --sink kinesis &
done

echo Starting consumers...
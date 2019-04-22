echo Setting up Sentinel...

git clone https://github.com/szymanskir/Sentinel
cd Sentinel
git checkout dev
make create_environment
source .env/bin/activate
pip install -r requirements.txt

echo Creating kafka topics...
for topic in "${topics[@]}"; do
    echo Creating $topic topic...
    bin/kafka-topics.sh --create --zookeeper sandbox.hortonworks.com 2181 --replication-factor 1 --partitions 1 --topic $topic
done
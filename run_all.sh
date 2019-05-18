echo Setting up DynamoDb...
cd dynamo-dev
docker-compose up &

echo Starting flask server...
cd ../sentinel_backend
source test_config.sh
# venv/bin/python import_db.py
make run &
echo -e '\nexport PYSPARK_PYTHON=/shared/Sentinel/sentinel_spark/.env/bin/python3.6' >> /usr/hdp/current/spark2-client/conf/spark-env.sh
echo -e '\nspark.executorEnv.AWS_ACCESS_KEY_ID KEY_ID\nspark.executorEnv.AWS_SECRET_ACCESS_KEY ACCESS_KEY\nspark.executorEnv.DYNAMO_DB_REGION eu-central-1\nspark.executorEnv.AWS_DEFAULT_REGION eu-central-1\n' >> /usr/hdp/current/spark2-client/conf/spark-defaults.conf
var="log4j.rootCategory=WARN, console"
sed -i "3s/.*/$var/" /usr/hdp/current/spark2-client/conf/log4j.properties
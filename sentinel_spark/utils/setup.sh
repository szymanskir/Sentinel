echo -e '\nexport PYSPARK_PYTHON=/shared/Sentinel/sentinel_spark/.env/bin/python3.6' >> /usr/hdp/current/spark2-client/conf/spark-env.sh
var="log4j.rootCategory=WARN, console"
sed -i "3s/.*/$var/" /usr/hdp/current/spark2-client/conf/log4j.properties
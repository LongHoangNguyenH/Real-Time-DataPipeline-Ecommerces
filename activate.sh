#/bin/bash
ContainerSpark="spark_master"

spark-submit --jars jars/kafka-clients-3.4.0.jar,ars/spark-cassandra-connector-assembly_2.12-3.3.0.jar,jars/mysql-connector-java-8.0.28.jar consumer.py

docker exec -u 0 spark_master bash -c "spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector:10.0.0 /data/Aggregate_Country.py"
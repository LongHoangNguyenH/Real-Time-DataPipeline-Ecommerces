from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

KAFKA_TOPIC_NAME_CONS = 'Ecommerce_topic'
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

if __name__ == '__main__':
    print('Streaming country')
    #Create SparkSession
    spark = SparkSession \
        .builder \
        .appName('Pyspark streaming with Kafka') \
        .config('spark.jars.packages','org.mongodb.spark:mongo-spark-connector:10.0.0') \
        .config('spark.jars.packages','org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0') \
        .master('spark://spark:7077') \
        .getOrCreate()
    #Create Schema
    Schema = StructType() \
        .add("id", IntegerType())\
        .add("first_name", StringType()) \
        .add("last_name", StringType()) \
        .add("country", StringType()) \
        .add("Product_name", StringType()) \
        .add("gender", StringType()) \
        .add("quantity", IntegerType()) 

    alter_schema = StructType([
        StructField('id',StringType()),
        StructField('first_name',StringType()),
        StructField('last_name',StringType()),
        StructField('country',StringType()),
        StructField('Product_name',StringType()),
        StructField('gender',StringType()),
        StructField('quantity',IntegerType()),
    ])
    #read Data from kafka topic
    df = spark \
        .readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers',KAFKA_BOOTSTRAP_SERVERS_CONS) \
        .option('subscribe',KAFKA_TOPIC_NAME_CONS) \
        .option('startingOffsets','latest') \
        .load()\
        .selectExpr('CAST(value AS STRING)')
    #convert JSON to dataframe
    converted_df = df \
        .select(from_json(col('value'),alter_schema)\
        .alias('orders'))\
        .select('orders.*')
    #Query
    query_1 = converted_df.groupby('country')\
                .agg({'quantity':'sum'})\
                .select('country',col('sum(quantity)')\
                .alias('total_order_amount')
                )
                
    query_1.writeStream \
        .format('mongodb')\
        .queryName('query_1')\
        .option("checkpointLocation", "/tmp/pyspark6/")\
        .option("forceDeleteTempCheckpointLocation", "true")\
        .option('spark.mongodb.connection.uri', 'mongodb://root:password@mongo:27017/?authSource=admin')\
        .option('spark.mongodb.database', 'Ecommerce')\
        .option('spark.mongodb.collection', 'CountryAnalytic')\
        .trigger(processingTime="10 seconds")\
        .outputMode("complete")\
        .start().awaitTermination()
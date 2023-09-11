


spark-submit --jars Stream/jars/spark-sql-kafka-0-10_2.12-3.0.0.jar,Stream/jars/mongo-spark-connector-10.0.0.jar Aggregate_Country.py
spark-submit --jars Stream/jars/spark-sql-kafka-0-10_2.12-3.0.0.jar,Stream/jars/mongo-spark-connector-10.0.0.jar Aggregate_Gender.py
spark-submit --jars Stream/jars/spark-sql-kafka-0-10_2.12-3.0.0.jar,Stream/jars/mongo-spark-connector-10.0.0.jar Aggregate_Product.py

cd Data-Generator
python3 producer.py

python3 -m streamlit run Dashboard/dashboard.py
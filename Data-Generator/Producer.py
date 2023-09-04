from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
import csv
import json
from datetime import datetime
import random

KAFKA_TOPIC_NAME_CONS = 'Ecommerce_topic'
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS_CONS],
                         value_serializer=serializer)

def producer_message(message):
    try:
       producer.send(KAFKA_TOPIC_NAME_CONS, message)
       producer.flush()
    #    record_metadata = notice.get(timeout=10)
    #    print(record_metadata)
    except KafkaError as e:
       print(e)

with open("./dataset.csv") as f:
    fdict = csv.DictReader(f, delimiter=",")
    for row in fdict:
        message = dict(row)
        producer_message(message)
        print(f'Producing message @ {datetime.now()} | Message = {str(message)}')
        time_to_sleep = random.randint(1, 7)
        time.sleep(time_to_sleep)

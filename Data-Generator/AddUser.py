from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
import json
import random
from faker import Faker
import numpy as np
from datetime import datetime

KAFKA_TOPIC_NAME_CONS = 'Ecommerce_topic'
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

def serializer(message):
    return json.dumps(message).encode('utf-8')

if __name__ == '__main__':
    fake = Faker()
    producer_obj = KafkaProducer(bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS_CONS],
                            value_serializer=serializer)
    while True:
            message = {}
            message["first_name"]= fake.name()
            message["last_name"]= fake.name()
            message["Product_name"] = fake.company_suffix()
            message["country"] = fake.country()
            message["gender"]=np.random.choice(["M", "F"], p=[0.5, 0.5])
            message["Qte"]= random.randint(1, 9)
            try:
                producer_obj.send(KAFKA_TOPIC_NAME_CONS,value=message) 
                producer_obj.flush()

                print(f'Producing message @ {datetime.now()} | Message = {str(message)}')
                time_to_sleep = random.randint(1, 7)
                time.sleep(time_to_sleep)
            except KafkaError as e:
                 print(e)
            

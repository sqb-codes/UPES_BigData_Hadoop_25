from kafka import KafkaProducer
import json
import time
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.CONSTANTS import *

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v : json.dumps(v).encode()
)

users = [101,102,103,104,105]
products = [9001,9002,9003,9004,9005]
events = ["view", "click", "add_to_cart", "search"]

while True:
    data = {
        "user_id": random.choice(users),
        "product_id": random.choice(products),
        "event_type": random.choice(events),
        "timestamp": time.time()
    }
    producer.send(TOPIC_NAME, value=data)
    print("Sent:",data)
    time.sleep(30)






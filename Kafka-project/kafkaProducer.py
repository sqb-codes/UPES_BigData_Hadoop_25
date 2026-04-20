from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    # Address of kafka broker
    bootstrap_servers='localhost:9092',
    # convert python dict -> JSON -> bytes (Kafka needs bytes)
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    # key used for partitioning
    key_serializer=lambda k: str(k).encode()
)

user_id = [101,102,103,105]

def generate_transaction():
    return {
        "user_id": random.choice(user_id),
        "amount": random.randint(100,50000),
        "location": random.choice(["Delhi", "Mumbai", "Noida", "DDN"]),
        "timestamp": time.time()
    }

while True:
    txn = generate_transaction()
    key = txn["user_id"]
    producer.send(
        topic='transactions',
        key=key,
        value=txn
    )

    print("Transaction done:",txn)
    time.sleep(1)
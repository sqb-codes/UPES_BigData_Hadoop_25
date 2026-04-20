from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers="localhost:9092",
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fraud-detector-group',
    value_deserializer=lambda x : json.loads(x.decode())
)

def detect_fraud(txn):
    if txn['amount'] > 40000:
        return True
    return False

for message in consumer:
    txn = message.value
    if detect_fraud(txn):
        print("Fraud detected:",txn)
    else:
        print("Normal transaction", txn)
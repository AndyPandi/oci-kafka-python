from kafka import KafkaConsumer
import json
import os

BOOTSTRAP_SERVERS = os.getenv("OCI_KAFKA_BOOTSTRAP")
USERNAME = os.getenv("OCI_KAFKA_USER")
PASSWORD = os.getenv("OCI_KAFKA_PASSWORD")
TOPIC = os.getenv("OCI_KAFKA_TOPIC")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_plain_username=USERNAME,
    sasl_plain_password=PASSWORD,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="python-consumer-group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print("### Waiting for messages...")
for message in consumer:
    print(f"Received: {message.value}")
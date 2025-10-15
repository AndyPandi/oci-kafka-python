from kafka import KafkaConsumer
import json
import os

def safe_json_deserializer(data):
    """안전한 JSON 역직렬화 함수"""
    if data is None:
        return None
    try:
        return json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError) as e:
        print(f"Warning: Failed to deserialize message: {e}")
        print(f"Raw data: {data}")
        return {"error": "deserialization_failed", "raw_data": str(data)}

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
    auto_offset_reset="latest", """ earliest : 토픽의 처음부터 모든 메시지 읽기"""
    enable_auto_commit=True,
    group_id="python-consumer-group-v2",
    value_deserializer=safe_json_deserializer,
)

print("### Waiting for messages...")
try:
    for message in consumer:
        print(f"Received: {message.value}")
        print(f"Topic: {message.topic}, Partition: {message.partition}, Offset: {message.offset}")
        print("-" * 50)
except KeyboardInterrupt:
    print("\nConsumer stopped by user")
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    consumer.close()
    print("Consumer closed")
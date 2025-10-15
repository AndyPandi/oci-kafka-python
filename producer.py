from kafka import KafkaProducer
import json
import os
from datetime import datetime

# 환경 변수에서 Kafka 접속 정보 가져오기
BOOTSTRAP_SERVERS = os.getenv("OCI_KAFKA_BOOTSTRAP")
USERNAME = os.getenv("OCI_KAFKA_USER")
PASSWORD = os.getenv("OCI_KAFKA_PASSWORD")
TOPIC = os.getenv("OCI_KAFKA_TOPIC")

# Kafka Producer 생성
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_plain_username=USERNAME,
    sasl_plain_password=PASSWORD,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# 5개의 메시지 전송
for i in range(5):
    # 현재 시각 (밀리초 단위)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # 메시지 생성 (특수문자 제거된 텍스트)
    msg = {
        "id": i,
        "message": f"Hello OCI Kafka {i}",
        "timestamp": timestamp
    }

    producer.send(TOPIC, value=msg)
    print(f"Sent: {msg}")

# 메시지 전송 완료 후 정리
producer.flush()
producer.close()
print("Done producing messages.")
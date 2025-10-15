# 환경변수 등록
export OCI_KAFKA_BOOTSTRAP="bootstrap-clstr-xxxxxxxxxxxxxx.kafka.ap-chuncheon-1.oci.oraclecloud.com:9092" && \
export OCI_KAFKA_USER="super-user-o6zxkfmtekqncrpt" && \
export OCI_KAFKA_PASSWORD="your_user" && \
export OCI_KAFKA_TOPIC="your_password"

# 환경변수 등록 확인
echo $OCI_KAFKA_BOOTSTRAP
# 또는
env | grep OCI_KAFKA

# nc (netcat) 테스트
# nc 설치
sudo dnf install -y nmap-ncat
# 설치 확인
nc --version

# Kafka 브로커 접속 테스트
nc -zv bootstrap-clstr-o6zxkfmtekqncrpt.kafka.ap-chuncheon-1.oci.oraclecloud.com 9092
# 성공예시
# Connection to bootstrap-clstr-o6zxkfmtekqncrpt.kafka.ap-chuncheon-1.oci.oraclecloud.com 9092 port [tcp/*] succeeded!
# 실패예시
# nc: connect to ... port 9092 (tcp) failed: Connection timed out

# 실행
python producer.py
python consumer.py
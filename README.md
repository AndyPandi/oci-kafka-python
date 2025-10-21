# OCI Managed Kafka - Python Demo

Oracle Cloud Infrastructure (OCI) Kafka를 사용한 Python 기반 메시지 프로듀서/컨슈머 데모 프로젝트입니다.

## 프로젝트 구조

```
kafka-demo-python/
├── producer.py    # Kafka 메시지 프로듀서
├── consumer.py    # Kafka 메시지 컨슈머
├── script.sh      # 환경 설정 및 실행 스크립트
└── README.md      # 프로젝트 문서
```

## 주요 기능

### Producer (producer.py)
- OCI Kafka 클러스터에 메시지를 전송하는 프로듀서
- JSON 형태의 메시지를 5개 생성하여 전송
- 각 메시지에는 ID, 메시지 내용, 타임스탬프가 포함됨
- SASL_SSL 보안 프로토콜과 SCRAM-SHA-512 인증 메커니즘 사용

### Consumer (consumer.py)
- OCI Kafka 클러스터에서 메시지를 수신하는 컨슈머
- `python-consumer-group-v2` 컨슈머 그룹으로 동작
- 최신 메시지부터 읽기 시작 (`auto_offset_reset="latest"`)
- 안전한 JSON 역직렬화 기능으로 오류 방지
- 실시간으로 메시지를 수신하고 상세 정보 출력 (토픽, 파티션, 오프셋)
- 우아한 종료 처리 (Ctrl+C)

## 환경 설정

### 필수 환경 변수

다음 환경 변수들을 설정해야 합니다:

```bash
export OCI_KAFKA_BOOTSTRAP="your-bootstrap-server:9092"
export OCI_KAFKA_USER="your-username"
export OCI_KAFKA_PASSWORD="your-password"
export OCI_KAFKA_TOPIC="your-topic-name"
```

### 의존성 설치

```bash
pip install kafka-python
```

## 사용 방법

### 1. 환경 변수 설정

`script.sh` 파일을 참고하여 환경 변수를 설정합니다:

```bash
# script.sh 파일 수정 후 실행
source script.sh
```

또는 직접 환경 변수를 설정:

```bash
export OCI_KAFKA_BOOTSTRAP="bootstrap-clstr-xxxxxxxxxxxxxx.kafka.ap-chuncheon-1.oci.oraclecloud.com:9092"
export OCI_KAFKA_USER="super-user-o6zxkfmtekqncrpt"
export OCI_KAFKA_PASSWORD="your_password"
export OCI_KAFKA_TOPIC="your_topic"
```

### 2. 연결 테스트 (선택사항)

Kafka 브로커 연결을 테스트하려면:

```bash
# netcat 설치 (CentOS/RHEL)
sudo dnf install -y nmap-ncat

# 연결 테스트
nc -zv your-bootstrap-server 9092
```

### 3. 프로듀서 실행

메시지를 전송하려면:

```bash
python producer.py
```

예상 출력:
```
Sent: {'id': 0, 'message': 'Hello OCI Kafka 0', 'timestamp': '2024-10-15 19:33:45.123'}
Sent: {'id': 1, 'message': 'Hello OCI Kafka 1', 'timestamp': '2024-10-15 19:33:45.124'}
...
Done producing messages.
```

### 4. 컨슈머 실행

메시지를 수신하려면:

```bash
python consumer.py
```

예상 출력:
```
### Waiting for messages...
Received: {'id': 0, 'message': 'Hello OCI Kafka 0', 'timestamp': '2024-10-15 19:33:45.123'}
Topic: your-topic, Partition: 0, Offset: 12345
--------------------------------------------------
Received: {'id': 1, 'message': 'Hello OCI Kafka 1', 'timestamp': '2024-10-15 19:33:45.124'}
Topic: your-topic, Partition: 0, Offset: 12346
--------------------------------------------------
...
```

## 보안 설정

이 프로젝트는 다음 보안 설정을 사용합니다:

- **보안 프로토콜**: SASL_SSL
- **인증 메커니즘**: SCRAM-SHA-512
- **데이터 직렬화**: JSON 형태로 UTF-8 인코딩

## 오프셋 설정 옵션

### auto_offset_reset 설정

- **`latest`** (기본값): 컨슈머 시작 이후의 새로운 메시지만 읽기
- **`earliest`**: 토픽의 처음부터 모든 메시지 읽기

```python
# 새로운 메시지만 읽기 (현재 설정)
auto_offset_reset="latest"

# 모든 메시지 읽기
auto_offset_reset="earliest"
```

## 주요 개선사항

### 안전한 메시지 처리
- JSON 파싱 오류 방지를 위한 `safe_json_deserializer` 함수
- 잘못된 형식의 메시지도 안전하게 처리
- 상세한 오류 로그 제공

### 향상된 출력 정보
- 메시지 내용과 함께 토픽, 파티션, 오프셋 정보 표시
- 메시지 구분을 위한 구분선 출력

### 우아한 종료 처리
- Ctrl+C로 안전한 종료 가능
- 예외 처리 및 리소스 정리

## 주의사항

1. 환경 변수에 실제 인증 정보를 설정해야 합니다
2. `script.sh` 파일의 예시 값들을 실제 OCI Kafka 클러스터 정보로 변경해야 합니다
3. 컨슈머는 무한 루프로 동작하므로 Ctrl+C로 종료할 수 있습니다
4. 프로듀서는 5개의 메시지를 전송한 후 자동으로 종료됩니다
5. 컨슈머 그룹 이름이 `python-consumer-group-v2`로 업데이트되었습니다

## 트러블슈팅

### 연결 실패 시
- 환경 변수가 올바르게 설정되었는지 확인
- 네트워크 연결 상태 확인
- OCI Kafka 클러스터의 보안 그룹 및 방화벽 설정 확인

### 인증 실패 시
- 사용자명과 비밀번호가 올바른지 확인
- SASL 메커니즘이 클러스터 설정과 일치하는지 확인

### JSON 역직렬화 오류 시
- 토픽에 JSON이 아닌 메시지가 있을 때 발생
- 수정된 `safe_json_deserializer`가 이 문제를 자동으로 처리
- 오류 메시지와 원본 데이터가 로그에 출력됨

### 메시지를 받지 못할 때
- `auto_offset_reset="earliest"`로 변경하여 모든 메시지 확인
- 새로운 컨슈머 그룹 이름 사용 (`group_id` 변경)
- 프로듀서가 올바른 토픽에 메시지를 보내는지 확인

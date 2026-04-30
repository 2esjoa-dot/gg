# Performance Test Instructions

## Purpose
시스템이 NFR 성능 요구사항을 충족하는지 검증합니다.

## Performance Requirements (NFR-01)
| 항목 | 목표 |
|---|---|
| 일반 API 응답 시간 | 500ms 이내 |
| 복잡한 쿼리 응답 시간 | 1초 이내 |
| SSE 이벤트 전달 | 2초 이내 |
| 동시 접속자 | 500명 이상 |

## Test Tool
- **권장**: [Locust](https://locust.io/) (Python 기반, 프로젝트 스택과 일치)
- **대안**: k6, Apache JMeter

## Setup

### 1. Locust 설치
```bash
pip install locust
```

### 2. Locust 테스트 파일 생성
```python
# backend/tests/performance/locustfile.py
from locust import HttpUser, task, between

class CustomerUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # 태블릿 로그인
        response = self.client.post("/api/customer/auth/login", json={
            "store_code": "perf-store",
            "table_number": 1,
            "password": "testpass"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def get_session(self):
        self.client.get("/api/customer/session/current", headers=self.headers)

class AdminUser(HttpUser):
    wait_time = between(2, 5)
    
    def on_start(self):
        response = self.client.post("/api/admin/auth/login", json={
            "store_code": "perf-store",
            "username": "admin",
            "password": "testpass"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(2)
    def list_tables(self):
        self.client.get("/api/admin/tables", headers=self.headers)
```

### 3. 테스트 데이터 준비
```bash
# 성능 테스트용 매장/테이블/사용자 데이터 사전 생성 필요
```

## Run Performance Tests

### 1. 기본 부하 테스트 (500 동시 사용자)
```bash
locust -f tests/performance/locustfile.py --host=http://localhost:8000 \
  --users 500 --spawn-rate 50 --run-time 5m --headless
```

### 2. 점진적 부하 테스트
```bash
# 100 → 300 → 500 → 700 사용자 단계별 증가
locust -f tests/performance/locustfile.py --host=http://localhost:8000 \
  --users 700 --spawn-rate 10 --run-time 10m --headless
```

### 3. Web UI로 실행 (시각적 모니터링)
```bash
locust -f tests/performance/locustfile.py --host=http://localhost:8000
# 브라우저에서 http://localhost:8089 접속
```

## Analyze Results

### 확인 항목
| 메트릭 | 목표 | 확인 방법 |
|---|---|---|
| Median Response Time | < 500ms | Locust 결과 |
| 95th Percentile | < 1000ms | Locust 결과 |
| Error Rate | < 1% | Locust 결과 |
| RPS (Requests/sec) | > 100 | Locust 결과 |

### 병목 지점 확인
1. DB 쿼리 시간: `LOG_LEVEL=DEBUG`로 슬로우 쿼리 확인
2. Connection Pool: `pool_size` 부족 시 타임아웃 에러
3. SSE 연결: 동시 구독자 수 모니터링

## Note
성능 테스트는 운영 환경과 유사한 환경에서 실행해야 정확한 결과를 얻을 수 있습니다.
MVP 단계에서는 기본 부하 테스트로 충분합니다.

# NFR Design - 테이블오더 서비스

## 1. 성능 패턴

### 1.1 커넥션 풀 설정
```python
# database.py
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # 기본 커넥션 수
    max_overflow=10,       # 초과 허용 수
    pool_timeout=30,       # 커넥션 대기 타임아웃
    pool_recycle=3600,     # 1시간마다 커넥션 재생성
    echo=False,
)
```

### 1.2 SSE 이벤트 관리
```
구조:
- 매장별 독립 채널 (store_id → Queue 리스트)
- asyncio.Queue 기반 (메모리 효율적)
- 구독자 연결 끊김 시 자동 정리
- keep-alive: 15초 간격 빈 이벤트 전송

성능 목표:
- 이벤트 발행 → 구독자 수신: < 100ms (네트워크 제외)
- 매장당 최대 구독자: 10명 (관리자 동시 접속)
```

### 1.3 쿼리 최적화
```
적용된 인덱스:
- ix_active_session: (store_id, table_id, status) → 활성 세션 조회
- ix_session_orders: (session_id, created_at) → 세션별 주문 시간순
- ix_table_active_orders: (store_id, table_id, status) → 테이블별 활성 주문
- uq_store_table_number: (store_id, table_number) → 테이블 중복 방지
- uq_store_username: (store_id, username) → 계정 중복 방지

N+1 방지:
- 주문 조회 시 OrderItem을 joinedload로 함께 로드
- 메뉴 조회 시 Category를 selectinload로 로드
```

### 1.4 폴링 최적화 (고객)
```
전략:
- 30초 간격 폴링 (요구사항 준수)
- Last-Modified 헤더로 변경 없으면 304 반환 (대역폭 절약)
- 응답 크기 최소화: 필요한 필드만 반환
```

---

## 2. 확장성 패턴

### 2.1 Stateless API 설계
```
원칙:
- 서버에 세션 상태 저장 안 함
- 모든 인증 정보는 JWT에 포함
- 요청 간 독립성 보장

효과:
- 로드밸런서 뒤에 여러 인스턴스 배치 가능
- 인스턴스 추가/제거 시 영향 없음
```

### 2.2 멀티테넌시 격리
```
패턴: Row-Level Security (논리적 격리)
- 모든 테이블에 store_id 컬럼
- 모든 쿼리에 store_id 필터 자동 적용
- JWT에서 store_id 추출 → 미들웨어에서 검증

장점:
- 단일 DB로 다수 매장 운영
- 매장 추가 시 스키마 변경 불필요
- 쿼리 성능: 인덱스에 store_id 포함
```

### 2.3 SSE 확장 전략 (MVP 이후)
```
현재 (MVP): 인메모리 asyncio.Queue
- 단일 인스턴스에서만 동작
- 매장당 10명 이하 관리자면 충분

향후 (Scale-out): Redis Pub/Sub
- 다중 인스턴스 간 이벤트 공유
- Redis Channel = store_id
- 변경 범위: SSEService만 교체 (인터페이스 동일)
```

---

## 3. 가용성 패턴

### 3.1 에러 복구
```
API 레벨:
- 전역 ExceptionHandler로 500 에러 방지
- DB 트랜잭션 실패 시 자동 롤백
- SSE 연결 끊김 시 구독자 자동 정리

클라이언트 레벨:
- SSE: EventSource 자동 재연결 (브라우저 기본)
- 폴링: 실패 시 다음 주기에 재시도
- 장바구니: 로컬 스토리지 (서버 장애 무관)
```

### 3.2 Graceful Shutdown
```
uvicorn 설정:
- SIGTERM 수신 시 새 요청 거부
- 진행 중 요청 완료 대기 (timeout 30초)
- DB 커넥션 풀 정리
- SSE 연결 종료
```

### 3.3 헬스체크
```
GET /health → {"status": "ok"}

모니터링 항목 (향후):
- DB 연결 상태
- 활성 SSE 연결 수
- 메모리 사용량
```

---

## 4. 보안 패턴

### 4.1 인증 흐름
```
1. 로그인 → JWT 발급 (16시간)
2. 요청마다 Authorization: Bearer {token}
3. 미들웨어에서 검증:
   - 서명 유효성
   - 만료 시간
   - 역할 (tablet/store_admin/hq_admin)
   - store_id 일치 (멀티테넌시)
```

### 4.2 비밀번호 정책
```
- bcrypt cost factor: 12 (해싱 ~250ms)
- 최소 길이: 4자 (MVP, 향후 강화)
- 저장: password_hash만 DB에 저장
- 비교: passlib.verify (timing-safe)
```

### 4.3 Rate Limiting (MVP 이후)
```
현재: 로그인 시도 제한만 (5회 → 15분 잠금)
향후: 전체 API rate limit (IP 기반, 분당 100회)
```

---

## 5. 모니터링 (MVP 수준)

| 항목 | 방법 |
|---|---|
| 서버 상태 | /health 엔드포인트 |
| 에러 로깅 | Python logging → 파일/stdout |
| 접근 로그 | uvicorn access log |
| DB 모니터링 | RDS CloudWatch 메트릭 |

향후 확장:
- Structured logging (JSON)
- CloudWatch Logs 연동
- 커스텀 메트릭 (주문 수, SSE 연결 수)
- 알림 (에러율 임계치 초과 시)

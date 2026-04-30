# NFR Design Patterns - Unit 1: Backend API

## 1. 성능 패턴

### PAT-PERF-01: Async-First 패턴
모든 I/O 작업을 비동기로 처리하여 동시 처리량을 극대화합니다.

```
요청 → async Router → async Service → async Repository → asyncpg (비동기 DB)
```

**적용 범위:**
- Router: 모든 엔드포인트 `async def`
- Service: 모든 비즈니스 로직 `async def`
- Repository: 모든 DB 접근 `async def`
- DB 세션: `AsyncSession` 사용

**구현 원칙:**
- `sync_to_async` 래퍼 사용 금지 (순수 async만)
- 블로킹 I/O 발생 시 `asyncio.to_thread()` 사용 (파일 업로드 등)

### PAT-PERF-02: Connection Pool 관리 패턴
DB 연결을 효율적으로 재사용합니다.

```python
# database.py
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,        # 기본 연결 수
    max_overflow=30,     # 초과 허용 연결 수
    pool_timeout=30,     # 연결 대기 타임아웃 (초)
    pool_recycle=1800,   # 연결 재활용 주기 (30분)
    pool_pre_ping=True,  # 연결 유효성 사전 확인
)
```

### PAT-PERF-03: Eager Loading 패턴
N+1 쿼리 문제를 방지합니다.

**적용 대상:**
| 조회 | 전략 | 설명 |
|---|---|---|
| 주문 + 주문항목 | `selectinload(Order.items)` | 주문 조회 시 항목 함께 로드 |
| 세션 + 주문 | `selectinload(Session.orders)` | 세션 조회 시 주문 함께 로드 |
| 카테고리 + 메뉴 | `selectinload(Category.menu_items)` | 카테고리별 메뉴 조회 |

---

## 2. 확장성 패턴

### PAT-SCALE-01: Publisher 추상화 패턴 (Strategy)
SSE 이벤트 발행을 추상화하여 구현체 교체를 용이하게 합니다.

```
+---------------------+
| EventPublisher      |  <<interface>>
|---------------------|
| + publish(event)    |
| + subscribe(id)     |
| + unsubscribe(id)   |
+---------------------+
        ^         ^
        |         |
+------------+ +---------------+
| InMemory   | | Redis         |
| Publisher   | | Publisher     |
+------------+ +---------------+
  (MVP 사용)    (향후 확장)
```

**InMemoryPublisher 구현:**
- `dict[int, list[asyncio.Queue]]` — store_id별 구독자 큐 목록
- `publish()`: 해당 store_id의 모든 큐에 이벤트 전송
- `subscribe()`: 새 큐 생성 후 목록에 추가, AsyncGenerator 반환
- `unsubscribe()`: 큐 제거 (연결 종료 시)

### PAT-SCALE-02: Storage 추상화 패턴 (Strategy)
파일 저장소를 추상화하여 로컬 → S3 전환을 용이하게 합니다.

```
+---------------------+
| FileStorage         |  <<interface>>
|---------------------|
| + save(file) -> url |
| + delete(url)       |
| + exists(url)       |
+---------------------+
        ^         ^
        |         |
+------------+ +---------------+
| Local      | | S3            |
| Storage    | | Storage       |
+------------+ +---------------+
  (MVP 사용)    (향후 확장)
```

---

## 3. 신뢰성 패턴

### PAT-REL-01: Global Exception Handler 패턴
모든 예외를 일관된 형식으로 처리합니다.

```
예외 발생 → ExceptionHandler 미들웨어
  ├─ AppException (커스텀) → 정의된 에러 코드/메시지 반환
  ├─ ValidationError (Pydantic) → 422 + 필드별 에러 상세
  ├─ HTTPException (FastAPI) → 해당 HTTP 상태 코드
  └─ Exception (미처리) → 500 + 로그 기록 + 일반 에러 메시지
```

**에러 응답 형식:**
```json
{
  "error": {
    "code": "INVALID_STATUS",
    "message": "완료된 주문은 변경할 수 없습니다",
    "details": null
  }
}
```

### PAT-REL-02: Request ID 추적 패턴
모든 요청에 고유 ID를 부여하여 로그 추적을 용이하게 합니다.

```
요청 수신 → RequestIDMiddleware
  → X-Request-ID 헤더 확인 (있으면 사용, 없으면 UUID 생성)
  → ContextVar에 저장
  → 모든 로그에 request_id 포함
  → 응답 헤더에 X-Request-ID 포함
```

### PAT-REL-03: Unit of Work 패턴 (트랜잭션)
Service 레이어에서 트랜잭션 경계를 관리합니다.

```python
# Service 메서드 패턴
async def create_order(self, db: AsyncSession, data: OrderCreate):
    async with db.begin():  # 트랜잭션 시작
        order = await self.order_repo.create(db, ...)
        items = await self.order_repo.create_items(db, ...)
        await self.sse_publisher.publish(...)
        return order
    # 예외 시 자동 롤백
```

### PAT-REL-04: 구조화 로깅 패턴
JSON 형식의 구조화된 로그를 생성합니다.

```
로그 이벤트 → JSON Formatter
  → 필드: timestamp, level, request_id, method, path, 
          status_code, duration_ms, store_id, message
  → 출력: 파일 (일별 로테이션, 30일 보관) + 콘솔
```

---

## 4. 보안 패턴

### PAT-SEC-01: Authentication Middleware 패턴 (Chain of Responsibility)
요청 인증을 계층적으로 처리합니다.

```
요청 수신 → AuthMiddleware
  1. 공개 경로 확인 (/docs, /redoc, /openapi.json, /health)
     → 공개: 통과
  2. Authorization 헤더 추출
     → 없음: 401 AUTH_INVALID
  3. JWT 토큰 검증 (서명 + 만료)
     → 실패: 401 AUTH_EXPIRED 또는 AUTH_INVALID
  4. 역할 기반 경로 접근 확인
     → /api/customer/* : role=tablet
     → /api/admin/* : role=store_admin
     → /api/hq/* : role=hq_admin
     → 불일치: 403 FORBIDDEN
  5. store_id 컨텍스트 설정 (멀티테넌시)
  6. 요청 처리 진행
```

### PAT-SEC-02: Multi-Tenancy Isolation 패턴
모든 데이터 접근에 store_id 필터를 강제합니다.

```
Repository 메서드 패턴:
  query = select(Model).where(Model.store_id == store_id)
  
  → 모든 CRUD 메서드에 store_id 파라미터 필수
  → hq_admin은 store_id 필터 없이 전체 접근 가능
```

### PAT-SEC-03: File Upload Validation Chain 패턴
파일 업로드를 3단계로 검증합니다.

```
파일 수신 → Validation Chain
  1. 확장자 검증 (화이트리스트: .jpg, .jpeg, .png, .webp)
     → 실패: 422 VALIDATION
  2. MIME 타입 검증 (python-magic으로 파일 헤더 확인)
     → 실패: 422 VALIDATION
  3. 파일 크기 검증 (최대 5MB)
     → 실패: 422 VALIDATION
  4. UUID 파일명 생성 → uploads/{store_id}/{uuid}.{ext} 저장
```

---

## 5. 설정 패턴

### PAT-CFG-01: Centralized Settings 패턴
Pydantic Settings로 모든 설정을 중앙 관리합니다.

```
.env 파일 → Pydantic Settings 클래스
  → 타입 검증 (자동)
  → 기본값 제공
  → 환경별 오버라이드 (환경변수 우선)
  
Settings 인스턴스 → FastAPI Depends로 주입
  → Router/Service에서 사용
```

---

## 6. 패턴 적용 매트릭스

| 패턴 | NFR 카테고리 | 적용 계층 | 우선순위 |
|---|---|---|---|
| Async-First | 성능 | 전체 | 필수 |
| Connection Pool | 성능 | Infrastructure | 필수 |
| Eager Loading | 성능 | Repository | 필수 |
| Publisher 추상화 | 확장성 | Service/Infra | 필수 |
| Storage 추상화 | 확장성 | Service/Infra | 필수 |
| Global Exception | 신뢰성 | Middleware | 필수 |
| Request ID | 신뢰성 | Middleware | 필수 |
| Unit of Work | 신뢰성 | Service | 필수 |
| 구조화 로깅 | 신뢰성 | 전체 | 필수 |
| Auth Middleware | 보안 | Middleware | 필수 |
| Multi-Tenancy | 보안 | Repository | 필수 |
| File Validation | 보안 | Service | 필수 |
| Centralized Settings | 유지보수 | Infrastructure | 필수 |

# Logical Components - Unit 1: Backend API

## 1. 컴포넌트 아키텍처 개요

```
+------------------------------------------------------------------+
|                        FastAPI Application                        |
+------------------------------------------------------------------+
|  Middleware Layer                                                  |
|  +-------------+ +----------------+ +------------------+          |
|  | AuthMiddle  | | RequestID      | | ExceptionHandler |          |
|  | ware        | | Middleware     | | Middleware       |          |
|  +-------------+ +----------------+ +------------------+          |
+------------------------------------------------------------------+
|  Router Layer                                                     |
|  +----------+ +----------+ +----------+                           |
|  | customer | | admin    | | hq       |                           |
|  +----------+ +----------+ +----------+                           |
+------------------------------------------------------------------+
|  Service Layer                                                    |
|  +------+ +-------+ +-------+ +---------+ +------+ +-----+      |
|  | Auth | | Store | | Table | | Session | | Menu | | Ord |      |
|  +------+ +-------+ +-------+ +---------+ +------+ +-----+      |
|  +------+ +------+                                                |
|  | SSE  | | File |                                                |
|  +------+ +------+                                                |
+------------------------------------------------------------------+
|  Repository Layer                                                 |
|  +-------+ +------+ +-------+ +---------+ +------+ +-----+      |
|  | Store | | User | | Table | | Session | | Menu | | Ord |      |
|  +-------+ +------+ +-------+ +---------+ +------+ +-----+      |
+------------------------------------------------------------------+
|  Infrastructure Layer                                             |
|  +----------+ +----------+ +---------+ +----------+ +--------+   |
|  | Database | | Settings | | Logging | | EventPub | | FileSt |   |
|  +----------+ +----------+ +---------+ +----------+ +--------+   |
+------------------------------------------------------------------+
```

---

## 2. Middleware 컴포넌트

### COMP-MW-01: AuthMiddleware
| 항목 | 내용 |
|---|---|
| **위치** | `app/middleware/auth.py` |
| **패턴** | PAT-SEC-01 (Chain of Responsibility) |
| **책임** | JWT 검증, 역할 기반 접근 제어, store_id 컨텍스트 설정 |
| **의존성** | Settings (SECRET_KEY), SecurityUtils |

**처리 흐름:**
1. 공개 경로 바이패스 (`/docs`, `/redoc`, `/openapi.json`, `/health`)
2. Bearer 토큰 추출 및 JWT 디코딩
3. 역할-경로 매핑 검증
4. `request.state.user` 에 사용자 정보 저장
5. `request.state.store_id` 에 매장 ID 저장

### COMP-MW-02: RequestIDMiddleware
| 항목 | 내용 |
|---|---|
| **위치** | `app/middleware/request_id.py` |
| **패턴** | PAT-REL-02 (Request ID 추적) |
| **책임** | 요청별 고유 ID 생성/전파, 로그 컨텍스트 설정 |
| **의존성** | 없음 |

**처리 흐름:**
1. `X-Request-ID` 헤더 확인 (있으면 사용)
2. 없으면 UUID4 생성
3. `ContextVar`에 저장 (로깅에서 참조)
4. 응답 헤더에 `X-Request-ID` 포함

### COMP-MW-03: ExceptionHandlerMiddleware
| 항목 | 내용 |
|---|---|
| **위치** | `app/middleware/exception_handler.py` |
| **패턴** | PAT-REL-01 (Global Exception Handler) |
| **책임** | 모든 예외를 일관된 JSON 형식으로 변환 |
| **의존성** | Logging |

**예외 매핑:**
| 예외 타입 | HTTP 코드 | 처리 |
|---|---|---|
| `AppException` | 에러별 상이 | 정의된 code/message 반환 |
| `RequestValidationError` | 422 | 필드별 에러 상세 |
| `HTTPException` | 해당 코드 | FastAPI 기본 처리 |
| `Exception` | 500 | 로그 기록 + 일반 메시지 |

---

## 3. Infrastructure 컴포넌트

### COMP-INFRA-01: Database
| 항목 | 내용 |
|---|---|
| **위치** | `app/database.py` |
| **패턴** | PAT-PERF-02 (Connection Pool) |
| **책임** | AsyncEngine 생성, AsyncSession 팩토리, DB 의존성 주입 |

**주요 요소:**
```
AsyncEngine
  ├─ pool_size=20
  ├─ max_overflow=30
  ├─ pool_timeout=30
  ├─ pool_recycle=1800
  └─ pool_pre_ping=True

AsyncSessionLocal = async_sessionmaker(engine)

get_db() → AsyncGenerator[AsyncSession]  # FastAPI Depends용
```

### COMP-INFRA-02: Settings
| 항목 | 내용 |
|---|---|
| **위치** | `app/config.py` |
| **패턴** | PAT-CFG-01 (Centralized Settings) |
| **책임** | 환경 설정 중앙 관리, 타입 검증 |

**설정 그룹:**
| 그룹 | 설정 항목 |
|---|---|
| Database | DATABASE_URL, DB_POOL_SIZE, DB_MAX_OVERFLOW |
| JWT | SECRET_KEY, ACCESS_TOKEN_EXPIRE_HOURS |
| CORS | ALLOWED_ORIGINS |
| File | UPLOAD_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS |
| Logging | LOG_LEVEL, LOG_DIR, LOG_MAX_DAYS |
| App | APP_NAME, DEBUG, API_PREFIX |

### COMP-INFRA-03: Logging
| 항목 | 내용 |
|---|---|
| **위치** | `app/utils/logging_config.py` |
| **패턴** | PAT-REL-04 (구조화 로깅) |
| **책임** | JSON 로거 설정, 파일 로테이션, Request ID 포함 |

**로거 구성:**
```
Root Logger
  ├─ StreamHandler (콘솔, JSON 형식)
  └─ TimedRotatingFileHandler
       ├─ 파일: logs/app.log
       ├─ 로테이션: 일별 (midnight)
       └─ 보관: 30일
```

### COMP-INFRA-04: EventPublisher (SSE)
| 항목 | 내용 |
|---|---|
| **위치** | `app/services/sse_service.py` |
| **패턴** | PAT-SCALE-01 (Publisher 추상화) |
| **책임** | SSE 이벤트 발행/구독 관리 |

**인터페이스:**
```
EventPublisher (ABC)
  ├─ publish(store_id, event_type, data) → None
  ├─ subscribe(store_id) → AsyncGenerator[SSEEvent]
  └─ unsubscribe(store_id, subscriber_id) → None

InMemoryEventPublisher(EventPublisher)
  └─ _subscribers: dict[int, dict[str, asyncio.Queue]]
```

**이벤트 타입:**
| 이벤트 | 데이터 |
|---|---|
| `new_order` | order_id, table_id, table_number, items, total, created_at |
| `order_status_changed` | order_id, table_id, old_status, new_status |
| `order_deleted` | order_id, table_id |
| `table_completed` | table_id, table_number |

### COMP-INFRA-05: FileStorage
| 항목 | 내용 |
|---|---|
| **위치** | `app/services/file_service.py` |
| **패턴** | PAT-SCALE-02 (Storage 추상화) |
| **책임** | 파일 저장/삭제, 검증 체인 실행 |

**인터페이스:**
```
FileStorage (ABC)
  ├─ save(store_id, file) → str (URL)
  ├─ delete(url) → bool
  └─ exists(url) → bool

LocalFileStorage(FileStorage)
  └─ base_dir: str = "uploads"
```

**검증 체인 (PAT-SEC-03):**
```
validate_extension() → validate_mime_type() → validate_file_size() → save()
```

---

## 4. 유틸리티 컴포넌트

### COMP-UTIL-01: SecurityUtils
| 항목 | 내용 |
|---|---|
| **위치** | `app/utils/security.py` |
| **책임** | 비밀번호 해싱/검증, JWT 생성/디코딩 |

**메서드:**
| 메서드 | 설명 |
|---|---|
| `hash_password(plain)` | bcrypt 해싱 (cost=12) |
| `verify_password(plain, hashed)` | bcrypt 검증 |
| `create_access_token(data, expires)` | JWT 생성 (HS256) |
| `decode_access_token(token)` | JWT 디코딩 + 검증 |

### COMP-UTIL-02: CustomExceptions
| 항목 | 내용 |
|---|---|
| **위치** | `app/utils/exceptions.py` |
| **책임** | 비즈니스 예외 정의, 에러 코드 매핑 |

**예외 클래스 계층:**
```
AppException (base)
  ├─ AuthenticationError (401)
  ├─ AuthorizationError (403)
  ├─ NotFoundError (404)
  ├─ DuplicateError (409)
  ├─ ValidationError (422)
  └─ InvalidStatusError (400)
```

### COMP-UTIL-03: OrderNumberGenerator
| 항목 | 내용 |
|---|---|
| **위치** | `app/utils/order_number.py` |
| **패턴** | PostgreSQL SEQUENCE 활용 |
| **책임** | 매장별 일별 주문 번호 생성 |

**생성 로직:**
```
1. PostgreSQL SEQUENCE: order_number_seq (매장별)
2. 형식: ORD-{YYYYMMDD}-{4자리 순번}
3. 일별 리셋: 날짜 변경 시 순번 초기화
```

---

## 5. 컴포넌트 의존성 매트릭스

| 컴포넌트 | 의존 대상 |
|---|---|
| AuthMiddleware | Settings, SecurityUtils |
| RequestIDMiddleware | (없음) |
| ExceptionHandler | Logging |
| Router | Service, AuthMiddleware |
| Service | Repository, EventPublisher, FileStorage, SecurityUtils |
| Repository | Database (AsyncSession) |
| Database | Settings |
| Logging | Settings |
| EventPublisher | (없음, 독립) |
| FileStorage | Settings |
| Settings | .env 파일 |

---

## 6. 미들웨어 실행 순서

```
요청 수신
  → 1. RequestIDMiddleware (ID 생성/전파)
  → 2. ExceptionHandlerMiddleware (예외 캐치)
  → 3. CORSMiddleware (CORS 헤더)
  → 4. AuthMiddleware (인증/인가)
  → 5. Router 처리
  → 응답 반환
```

**등록 순서 (FastAPI):** 역순으로 등록 (마지막 등록 = 먼저 실행)
```python
app.add_middleware(AuthMiddleware)        # 4번째 실행
app.add_middleware(CORSMiddleware, ...)   # 3번째 실행
app.add_middleware(ExceptionHandlerMiddleware)  # 2번째 실행
app.add_middleware(RequestIDMiddleware)   # 1번째 실행
```

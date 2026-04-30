# Tech Stack Decisions - Unit 1: Backend API

## 1. 핵심 프레임워크

| 기술 | 버전 | 선택 근거 |
|---|---|---|
| **Python** | 3.11+ | async/await 성능 개선, 타입 힌트 강화 |
| **FastAPI** | 0.110+ | 비동기 지원, 자동 문서화, Pydantic 통합 |
| **Uvicorn** | 0.29+ | ASGI 서버, FastAPI 공식 권장 |

---

## 2. 데이터베이스

| 기술 | 버전 | 선택 근거 |
|---|---|---|
| **PostgreSQL** | 15+ | SEQUENCE 지원, JSON 타입, 안정성 |
| **SQLAlchemy** | 2.0+ | AsyncSession 지원, 타입 안전 ORM |
| **Alembic** | 1.13+ | SQLAlchemy 공식 마이그레이션 도구 |
| **asyncpg** | 0.29+ | PostgreSQL 비동기 드라이버 (최고 성능) |

---

## 3. 인증/보안

| 기술 | 용도 | 선택 근거 |
|---|---|---|
| **python-jose[cryptography]** | JWT 생성/검증 | HS256 지원, 널리 사용 |
| **passlib[bcrypt]** | 비밀번호 해싱 | bcrypt cost factor 설정 가능 |
| **python-multipart** | 폼 데이터/파일 업로드 | FastAPI 파일 업로드 필수 의존성 |

---

## 4. 설정/환경 관리

| 기술 | 용도 | 선택 근거 |
|---|---|---|
| **pydantic-settings** | 환경 설정 관리 | 타입 검증, .env 자동 로드, 기본값 지원 |

### Settings 클래스 구조
```python
class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 30
    
    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_HOURS: int = 16
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    
    model_config = SettingsConfigDict(env_file=".env")
```

---

## 5. 로깅

| 기술 | 용도 | 선택 근거 |
|---|---|---|
| **Python logging** | 로깅 프레임워크 | 표준 라이브러리, 추가 의존성 없음 |
| **python-json-logger** | JSON 포맷 | 구조화된 로그 출력 |
| **RotatingFileHandler** | 파일 로테이션 | 일별 로테이션, 30일 보관 |

### 로그 형식
```json
{
  "timestamp": "2026-04-30T12:00:00Z",
  "level": "INFO",
  "request_id": "uuid-here",
  "method": "POST",
  "path": "/api/customer/orders",
  "status_code": 201,
  "duration_ms": 45,
  "store_id": 1,
  "message": "Order created"
}
```

---

## 6. 파일 업로드 보안

| 기술 | 용도 | 선택 근거 |
|---|---|---|
| **python-magic** 또는 **filetype** | MIME 타입 검증 | 파일 헤더 기반 실제 타입 확인 |
| **uuid** | 파일명 생성 | 충돌 방지, 원본 파일명 노출 방지 |

### 허용 파일 타입
| 확장자 | MIME 타입 |
|---|---|
| .jpg, .jpeg | image/jpeg |
| .png | image/png |
| .webp | image/webp |

---

## 7. 테스트

| 기술 | 용도 | 선택 근거 |
|---|---|---|
| **pytest** | 테스트 프레임워크 | Python 표준, 풍부한 플러그인 |
| **pytest-asyncio** | 비동기 테스트 | async 테스트 함수 지원 |
| **httpx** | HTTP 클라이언트 | AsyncClient로 FastAPI 테스트 |
| **pytest-cov** | 커버리지 | 코드 커버리지 측정 (목표 80%+) |
| **factory_boy** | 테스트 데이터 | 모델별 팩토리 패턴 |

### 테스트 구조
```
tests/
├── conftest.py          # 공통 fixture (DB, client, factories)
├── factories/           # factory_boy 팩토리
│   ├── __init__.py
│   ├── store_factory.py
│   ├── user_factory.py
│   ├── table_factory.py
│   ├── menu_factory.py
│   └── order_factory.py
├── unit/                # 단위 테스트
│   ├── services/
│   ├── repositories/
│   └── utils/
└── integration/         # 통합 테스트
    ├── routers/
    └── middleware/
```

---

## 8. API 문서화

| 기능 | 경로 | 설명 |
|---|---|---|
| Swagger UI | /docs | 인터랙티브 API 테스트 |
| ReDoc | /redoc | 읽기 전용 API 문서 |
| OpenAPI JSON | /openapi.json | 스펙 파일 (프론트엔드 연동용) |

### 태그 분류
| 태그 | 설명 |
|---|---|
| Customer - Auth | 태블릿 인증 |
| Customer - Menu | 메뉴 조회 |
| Customer - Order | 주문 생성/조회 |
| Admin - Auth | 관리자 인증 |
| Admin - Order | 주문 관리 (상태변경, 삭제) |
| Admin - Table | 테이블 관리 |
| Admin - Menu | 메뉴 CRUD |
| Admin - Account | 계정 관리 |
| Admin - SSE | 실시간 이벤트 |
| HQ - Store | 매장 관리 |

---

## 9. 전체 의존성 목록 (requirements.txt)

```
# Core
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.6.0
pydantic-settings>=2.2.0

# Database
sqlalchemy[asyncio]>=2.0.28
asyncpg>=0.29.0
alembic>=1.13.0

# Auth
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.9

# Logging
python-json-logger>=2.0.7

# File Upload
python-magic>=0.4.27

# Dev/Test
pytest>=8.1.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
pytest-cov>=5.0.0
factory-boy>=3.3.0
```

---

## 10. 결정 요약

| 영역 | 결정 | 대안 (향후 확장) |
|---|---|---|
| SSE 관리 | In-memory (인터페이스 추상화) | Redis Pub/Sub |
| DB Pool | pool_size=20, max_overflow=30 | PgBouncer 도입 |
| 로깅 | JSON + 파일 로테이션 | CloudWatch 연동 |
| Rate Limit | 인증 API만 (앱 레벨) | 전체 API (미들웨어) |
| 파일 저장 | 로컬 파일시스템 | AWS S3 |
| 주문 번호 | PostgreSQL SEQUENCE | Redis INCR |
| 설정 관리 | Pydantic Settings + .env | AWS Parameter Store |

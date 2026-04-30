# Code Generation Summary - Unit 1: Backend API (Foundation)

## 생성 파일 목록

### 프로젝트 설정 (4 files)
- `backend/requirements.txt` — Python 의존성
- `backend/.env.example` — 환경 변수 템플릿
- `backend/app/config.py` — Pydantic Settings 중앙 설정
- `backend/app/database.py` — AsyncEngine, AsyncSession, get_db

### 애플리케이션 진입점 (1 file)
- `backend/app/main.py` — FastAPI 앱 생성, 미들웨어/라우터 등록

### 유틸리티 (4 files)
- `backend/app/utils/security.py` — bcrypt, JWT 유틸리티
- `backend/app/utils/exceptions.py` — 커스텀 예외 계층 (9개 예외 클래스)
- `backend/app/utils/logging_config.py` — JSON 구조화 로깅, 파일 로테이션
- `backend/app/utils/order_number.py` — PostgreSQL SEQUENCE 기반 주문 번호 생성

### 미들웨어 (3 files)
- `backend/app/middleware/auth.py` — JWT 인증 + 역할 기반 접근 제어
- `backend/app/middleware/request_id.py` — Request ID 추적
- `backend/app/middleware/exception_handler.py` — 글로벌 예외 핸들러

### Domain Models (8 files)
- `backend/app/models/store.py` — Store 엔티티
- `backend/app/models/user.py` — User 엔티티 (UserRole enum)
- `backend/app/models/table.py` — Table 엔티티
- `backend/app/models/session.py` — TableSession 엔티티 (SessionStatus enum)
- `backend/app/models/category.py` — Category 엔티티
- `backend/app/models/menu_item.py` — MenuItem 엔티티
- `backend/app/models/order.py` — Order 엔티티 (OrderStatus enum)
- `backend/app/models/order_item.py` — OrderItem 엔티티

### Pydantic Schemas (4 files)
- `backend/app/schemas/auth.py` — 인증 요청/응답
- `backend/app/schemas/store.py` — 매장 CRUD
- `backend/app/schemas/table.py` — 테이블 CRUD
- `backend/app/schemas/session.py` — 세션 조회/종료

### Repository Layer (5 files)
- `backend/app/repositories/base.py` — BaseRepository (Generic CRUD)
- `backend/app/repositories/store_repository.py`
- `backend/app/repositories/user_repository.py`
- `backend/app/repositories/table_repository.py`
- `backend/app/repositories/session_repository.py`

### Service Layer (5 files)
- `backend/app/services/auth_service.py` — 관리자/태블릿 인증
- `backend/app/services/store_service.py` — 매장 CRUD
- `backend/app/services/table_service.py` — 테이블 CRUD
- `backend/app/services/session_service.py` — 세션 라이프사이클
- `backend/app/services/sse_service.py` — EventPublisher 추상화 + InMemory 구현

### Router Layer (6 files)
- `backend/app/routers/health.py` — Health Check
- `backend/app/routers/hq.py` — 본사 매장 관리 (US-H01, US-H02)
- `backend/app/routers/admin_auth.py` — 관리자 인증 (US-A01, US-A10)
- `backend/app/routers/admin_tables.py` — 테이블 관리 (US-A04, US-A06)
- `backend/app/routers/customer_auth.py` — 태블릿 인증 (US-C01)
- `backend/app/routers/customer_session.py` — 세션 조회 (US-C02)

### Alembic 마이그레이션 (3 files)
- `backend/alembic.ini`
- `backend/migrations/env.py`
- `backend/migrations/script.py.mako`

### 테스트 (16 files)
- `backend/tests/conftest.py` — 공통 fixture
- `backend/tests/unit/test_security.py` — 보안 유틸 테스트 (8 tests)
- `backend/tests/unit/test_exceptions.py` — 예외 클래스 테스트 (10 tests)
- `backend/tests/unit/test_order_number.py` — 주문 번호 테스트 (3 tests)
- `backend/tests/unit/services/test_auth_service.py` — 인증 서비스 (7 tests)
- `backend/tests/unit/services/test_store_service.py` — 매장 서비스 (4 tests)
- `backend/tests/unit/services/test_table_service.py` — 테이블 서비스 (4 tests)
- `backend/tests/unit/services/test_session_service.py` — 세션 서비스 (6 tests)
- `backend/tests/unit/repositories/test_store_repository.py` — 매장 리포 (4 tests)
- `backend/tests/unit/repositories/test_user_repository.py` — 사용자 리포 (2 tests)
- `backend/tests/unit/repositories/test_table_repository.py` — 테이블 리포 (2 tests)
- `backend/tests/unit/repositories/test_session_repository.py` — 세션 리포 (3 tests)
- `backend/tests/integration/test_health_router.py` — Health (1 test)
- `backend/tests/integration/test_hq_router.py` — 본사 API (4 tests)
- `backend/tests/integration/test_admin_auth_router.py` — 관리자 인증 (3 tests)
- `backend/tests/integration/test_admin_tables_router.py` — 테이블 관리 (3 tests)
- `backend/tests/integration/test_customer_auth_router.py` — 태블릿 인증 (2 tests)
- `backend/tests/integration/test_customer_session_router.py` — 세션 조회 (2 tests)

### 테스트 팩토리 (4 files)
- `backend/tests/factories/store_factory.py`
- `backend/tests/factories/user_factory.py`
- `backend/tests/factories/table_factory.py`
- `backend/tests/factories/session_factory.py`

### 배포 아티팩트 (3 files)
- `backend/.gitignore`
- `backend/pytest.ini`
- `backend/Dockerfile`

---

## 스토리 커버리지

| 스토리 | 구현 상태 |
|---|---|
| US-H01 (매장 등록) | ✅ Router + Service + Repository + 테스트 |
| US-H02 (매장 조회) | ✅ Router + Service + Repository + 테스트 |
| US-A01 (관리자 로그인) | ✅ Router + Service + 잠금 로직 + 테스트 |
| US-A10 (계정 등록) | ✅ Router + Service + 테스트 |
| US-A04 (테이블 등록) | ✅ Router + Service + Repository + 테스트 |
| US-C01 (태블릿 로그인) | ✅ Router + Service + 테스트 |
| US-C02 (세션 관리) | ✅ Router + Service + Repository + 테스트 |
| US-A06 (이용 완료) | ✅ Router + Service + 테스트 |

## 총계
- **생성 파일**: 62개
- **테스트 케이스**: ~53개
- **스토리 커버리지**: 8/8 (100%)

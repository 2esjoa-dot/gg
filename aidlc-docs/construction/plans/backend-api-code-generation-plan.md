# Code Generation Plan - Unit 1: Backend API (Foundation)

## Unit 컨텍스트
- **Unit**: Unit 1 - 인증 + 매장/테이블 기반 (Foundation)
- **담당 스토리**: US-H01, US-H02, US-A01, US-A10, US-A04, US-C01, US-C02, US-A06
- **의존성**: 없음 (Foundation Unit)
- **기술**: FastAPI + SQLAlchemy + PostgreSQL + Alembic
- **코드 위치**: `backend/` (워크스페이스 루트)

## 의존성 및 인터페이스
- Unit 2, 3, 4가 이 Unit의 DB 구조, 인증 미들웨어, 설정을 사용
- SessionService 인터페이스를 Unit 3에 제공
- 공통 인프라 (database.py, config.py, exceptions.py, security.py) 제공

---

## 실행 계획

### Step 1: 프로젝트 구조 및 설정 파일 생성
- [x] `backend/` 디렉토리 구조 생성
- [x] `backend/requirements.txt` 생성
- [x] `backend/.env.example` 생성
- [x] `backend/app/__init__.py` 생성
- [x] `backend/app/config.py` 생성 (Pydantic Settings)
- [x] `backend/app/database.py` 생성 (AsyncEngine, AsyncSession, get_db)
- [x] `backend/app/main.py` 생성 (FastAPI 앱, 미들웨어 등록, 라우터 포함)

### Step 2: 공통 유틸리티 생성
- [x] `backend/app/utils/__init__.py` 생성
- [x] `backend/app/utils/security.py` 생성 (bcrypt, JWT)
- [x] `backend/app/utils/exceptions.py` 생성 (AppException 계층, 에러 코드)
- [x] `backend/app/utils/logging_config.py` 생성 (JSON 로거, 파일 로테이션)
- [x] `backend/app/utils/order_number.py` 생성 (주문 번호 생성기)

### Step 3: 미들웨어 생성
- [x] `backend/app/middleware/__init__.py` 생성
- [x] `backend/app/middleware/auth.py` 생성 (AuthMiddleware)
- [x] `backend/app/middleware/request_id.py` 생성 (RequestIDMiddleware)
- [x] `backend/app/middleware/exception_handler.py` 생성 (ExceptionHandlerMiddleware)

### Step 4: Domain Models 생성
- [x] `backend/app/models/__init__.py` 생성 (Base 선언)
- [x] `backend/app/models/store.py` 생성 (Store 엔티티)
- [x] `backend/app/models/user.py` 생성 (User 엔티티)
- [x] `backend/app/models/table.py` 생성 (Table 엔티티)
- [x] `backend/app/models/session.py` 생성 (TableSession 엔티티)
- [x] `backend/app/models/category.py` 생성 (Category 엔티티)
- [x] `backend/app/models/menu_item.py` 생성 (MenuItem 엔티티)
- [x] `backend/app/models/order.py` 생성 (Order 엔티티)
- [x] `backend/app/models/order_item.py` 생성 (OrderItem 엔티티)

### Step 5: Pydantic Schemas 생성
- [x] `backend/app/schemas/__init__.py` 생성
- [x] `backend/app/schemas/auth.py` 생성 (로그인 요청/응답)
- [x] `backend/app/schemas/store.py` 생성 (매장 CRUD)
- [x] `backend/app/schemas/table.py` 생성 (테이블 CRUD)
- [x] `backend/app/schemas/session.py` 생성 (세션 조회/종료)

### Step 6: Repository Layer 생성
- [x] `backend/app/repositories/__init__.py` 생성
- [x] `backend/app/repositories/base.py` 생성 (BaseRepository)
- [x] `backend/app/repositories/store_repository.py` 생성
- [x] `backend/app/repositories/user_repository.py` 생성
- [x] `backend/app/repositories/table_repository.py` 생성
- [x] `backend/app/repositories/session_repository.py` 생성

### Step 7: Service Layer 생성
- [x] `backend/app/services/__init__.py` 생성
- [x] `backend/app/services/auth_service.py` 생성 (관리자/태블릿 로그인)
- [x] `backend/app/services/store_service.py` 생성 (매장 CRUD)
- [x] `backend/app/services/table_service.py` 생성 (테이블 CRUD)
- [x] `backend/app/services/session_service.py` 생성 (세션 생성/종료/만료)
- [x] `backend/app/services/sse_service.py` 생성 (EventPublisher 인터페이스 + InMemory 구현)

### Step 8: Router Layer 생성
- [x] `backend/app/routers/__init__.py` 생성
- [x] `backend/app/routers/hq.py` 생성 (본사: 매장 등록/조회) — US-H01, US-H02
- [x] `backend/app/routers/admin_auth.py` 생성 (관리자 로그인/계정등록) — US-A01, US-A10
- [x] `backend/app/routers/admin_tables.py` 생성 (테이블 관리/이용완료) — US-A04, US-A06
- [x] `backend/app/routers/customer_auth.py` 생성 (태블릿 로그인) — US-C01
- [x] `backend/app/routers/customer_session.py` 생성 (세션 조회) — US-C02
- [x] `backend/app/routers/health.py` 생성 (Health Check)

### Step 9: Alembic 마이그레이션 설정
- [x] `backend/alembic.ini` 생성
- [x] `backend/migrations/env.py` 생성
- [x] `backend/migrations/script.py.mako` 생성
- [x] `backend/migrations/versions/` 디렉토리 생성

### Step 10: 단위 테스트 — 유틸리티
- [x] `backend/tests/__init__.py` 생성
- [x] `backend/tests/conftest.py` 생성 (공통 fixture: DB, client, factories)
- [x] `backend/tests/unit/__init__.py` 생성
- [x] `backend/tests/unit/test_security.py` 생성 (bcrypt, JWT 테스트)
- [x] `backend/tests/unit/test_exceptions.py` 생성 (예외 클래스 테스트)
- [x] `backend/tests/unit/test_order_number.py` 생성 (주문 번호 생성 테스트)

### Step 11: 단위 테스트 — Service Layer
- [x] `backend/tests/unit/services/__init__.py` 생성
- [x] `backend/tests/unit/services/test_auth_service.py` 생성
- [x] `backend/tests/unit/services/test_store_service.py` 생성
- [x] `backend/tests/unit/services/test_table_service.py` 생성
- [x] `backend/tests/unit/services/test_session_service.py` 생성

### Step 12: 단위 테스트 — Repository Layer
- [x] `backend/tests/unit/repositories/__init__.py` 생성
- [x] `backend/tests/unit/repositories/test_store_repository.py` 생성
- [x] `backend/tests/unit/repositories/test_user_repository.py` 생성
- [x] `backend/tests/unit/repositories/test_table_repository.py` 생성
- [x] `backend/tests/unit/repositories/test_session_repository.py` 생성

### Step 13: 통합 테스트 — Router Layer
- [x] `backend/tests/integration/__init__.py` 생성
- [x] `backend/tests/integration/test_hq_router.py` 생성 (매장 API)
- [x] `backend/tests/integration/test_admin_auth_router.py` 생성 (관리자 인증 API)
- [x] `backend/tests/integration/test_admin_tables_router.py` 생성 (테이블 관리 API)
- [x] `backend/tests/integration/test_customer_auth_router.py` 생성 (태블릿 인증 API)
- [x] `backend/tests/integration/test_customer_session_router.py` 생성 (세션 API)
- [x] `backend/tests/integration/test_health_router.py` 생성 (Health Check)

### Step 14: 테스트 팩토리 생성
- [x] `backend/tests/factories/__init__.py` 생성
- [x] `backend/tests/factories/store_factory.py` 생성
- [x] `backend/tests/factories/user_factory.py` 생성
- [x] `backend/tests/factories/table_factory.py` 생성
- [x] `backend/tests/factories/session_factory.py` 생성

### Step 15: 배포 아티팩트 생성
- [x] `backend/.gitignore` 생성
- [x] `backend/Dockerfile` 생성 (선택, 개발 편의)
- [x] `backend/pytest.ini` 생성 (pytest 설정)

### Step 16: 코드 생성 요약 문서
- [x] `aidlc-docs/construction/backend-api/code/code-generation-summary.md` 생성

---

## 스토리 추적

| 스토리 | 구현 Step | 상태 |
|---|---|---|
| US-H01 (매장 등록) | Step 4-8 | [x] |
| US-H02 (매장 조회) | Step 4-8 | [x] |
| US-A01 (관리자 로그인) | Step 2, 4-8 | [x] |
| US-A10 (계정 등록) | Step 4-8 | [x] |
| US-A04 (테이블 등록) | Step 4-8 | [x] |
| US-C01 (태블릿 로그인) | Step 2, 4-8 | [x] |
| US-C02 (세션 관리) | Step 4-8 | [x] |
| US-A06 (이용 완료) | Step 4-8 | [x] |

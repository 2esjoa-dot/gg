# Integration Test Instructions

## Purpose
Router 레이어를 통한 전체 API 흐름을 테스트합니다. 실제 DB와 연동하여 엔드투엔드 동작을 검증합니다.

## Prerequisites
- 테스트 DB 생성 완료 (`table_order_test`)
- 의존성 설치 완료

## Run Integration Tests

### 1. 전체 통합 테스트 실행
```bash
cd backend
pytest tests/integration/ -v
```

### 2. 커버리지 포함 실행
```bash
pytest tests/integration/ -v --cov=app --cov-report=term-missing
```

### 3. 특정 라우터 테스트
```bash
# Health Check
pytest tests/integration/test_health_router.py -v

# 본사 매장 관리 API
pytest tests/integration/test_hq_router.py -v

# 관리자 인증 API
pytest tests/integration/test_admin_auth_router.py -v

# 관리자 테이블 관리 API
pytest tests/integration/test_admin_tables_router.py -v

# 고객 태블릿 인증 API
pytest tests/integration/test_customer_auth_router.py -v

# 고객 세션 API
pytest tests/integration/test_customer_session_router.py -v
```

## Test Scenarios

### Scenario 1: 매장 등록 → 관리자 로그인 (US-H01 → US-A01)
1. HQ 관리자가 매장 등록 (`POST /api/hq/stores`)
2. 매장 관리자 계정 등록 (`POST /api/admin/auth/register`)
3. 관리자 로그인 (`POST /api/admin/auth/login`)
4. JWT 토큰으로 관리자 API 접근

### Scenario 2: 테이블 등록 → 태블릿 로그인 → 세션 (US-A04 → US-C01 → US-C02)
1. 관리자가 테이블 등록 (`POST /api/admin/tables`)
2. 태블릿 로그인 (`POST /api/customer/auth/login`)
3. 현재 세션 조회 (`GET /api/customer/session/current`)

### Scenario 3: 이용 완료 (US-A06)
1. 활성 세션이 있는 테이블
2. 관리자가 이용 완료 (`POST /api/admin/tables/{id}/complete`)
3. 세션 상태 completed 확인

### Scenario 4: 인증 실패 시나리오
1. 잘못된 비밀번호로 로그인 시도 → 401
2. 5회 실패 후 계정 잠금 → 401 (AUTH_LOCKED)
3. 토큰 없이 API 접근 → 401
4. 다른 역할로 API 접근 → 403

## Expected Results

| 테스트 파일 | 테스트 수 | 설명 |
|---|---|---|
| test_health_router.py | 1 | Health Check 200 |
| test_hq_router.py | 4 | 매장 CRUD + 인증 |
| test_admin_auth_router.py | 3 | 로그인/실패/등록 |
| test_admin_tables_router.py | 3 | 테이블 등록/목록/이용완료 |
| test_customer_auth_router.py | 2 | 태블릿 로그인/실패 |
| test_customer_session_router.py | 2 | 세션 조회/없음 |
| **합계** | **15** | |

## Cleanup
테스트는 각 함수마다 DB를 초기화하므로 별도 정리 불필요 (conftest.py의 db_session fixture).

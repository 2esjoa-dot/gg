# Unit Test Execution Instructions

## Prerequisites
- 가상환경 활성화 및 의존성 설치 완료
- 테스트 DB 생성 완료 (`table_order_test`)

## Run Unit Tests

### 1. 전체 단위 테스트 실행
```bash
cd backend
pytest tests/unit/ -v
```

### 2. 커버리지 포함 실행
```bash
pytest tests/unit/ -v --cov=app --cov-report=term-missing
```

### 3. 특정 모듈 테스트
```bash
# 유틸리티 테스트
pytest tests/unit/test_security.py -v
pytest tests/unit/test_exceptions.py -v
pytest tests/unit/test_order_number.py -v

# Service 테스트
pytest tests/unit/services/ -v

# Repository 테스트 (DB 필요)
pytest tests/unit/repositories/ -v
```

## Expected Results

### 유틸리티 테스트 (~21 tests)
| 테스트 파일 | 테스트 수 | 설명 |
|---|---|---|
| test_security.py | 8 | bcrypt 해싱, JWT 생성/검증 |
| test_exceptions.py | 10 | 커스텀 예외 클래스 속성 |
| test_order_number.py | 3 | 주문 번호 형식/순번 |

### Service 테스트 (~21 tests)
| 테스트 파일 | 테스트 수 | 설명 |
|---|---|---|
| test_auth_service.py | 7 | 로그인 성공/실패/잠금, 계정 등록 |
| test_store_service.py | 4 | 매장 생성/조회/중복 |
| test_table_service.py | 4 | 테이블 생성/조회/중복/매장 격리 |
| test_session_service.py | 6 | 세션 생성/만료/종료 |

### Repository 테스트 (~11 tests)
| 테스트 파일 | 테스트 수 | 설명 |
|---|---|---|
| test_store_repository.py | 4 | CRUD, 코드 조회, 활성 필터 |
| test_user_repository.py | 2 | 생성, 매장+사용자명 조회 |
| test_table_repository.py | 2 | 생성, 매장별 조회 |
| test_session_repository.py | 3 | 활성/만료 세션 조회 |

## Test Coverage Target
- **목표**: 80% 이상
- **핵심 모듈**: Service, Repository 90% 이상

## Fix Failing Tests
1. 테스트 출력에서 실패 원인 확인
2. `pytest tests/unit/path/to/test.py::TestClass::test_method -v` 로 개별 실행
3. 코드 수정 후 재실행

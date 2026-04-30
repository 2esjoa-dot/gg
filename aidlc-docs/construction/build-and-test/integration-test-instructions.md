# Integration Test Instructions - Unit 2: Menu

## 목적
Unit 2 (Menu)와 다른 Unit 간의 상호작용을 검증합니다.

## 통합 테스트 시나리오

### Scenario 1: Unit 1 (Auth) → Unit 2 (Menu) 인증 연동
- **설명**: 관리자 로그인 후 메뉴 CRUD API 접근 가능 여부 확인
- **사전 조건**: Unit 1 (Auth) 구현 완료
- **테스트 단계**:
  1. 관리자 로그인 API 호출 → JWT 토큰 획득
  2. 토큰으로 카테고리 생성 API 호출
  3. 토큰으로 메뉴 생성 API 호출
  4. 토큰 없이 API 호출 → 401 확인
  5. 태블릿 토큰으로 관리자 API 호출 → 403 확인
- **예상 결과**: 인증/인가가 올바르게 동작

### Scenario 2: Unit 2 (Menu) → Unit 3 (Order) 메뉴-주문 연동
- **설명**: 메뉴 생성 후 해당 메뉴로 주문 생성 가능 여부 확인
- **사전 조건**: Unit 3 (Order) 구현 완료
- **테스트 단계**:
  1. 관리자가 카테고리 + 메뉴 생성
  2. 고객이 메뉴 조회 → 생성된 메뉴 확인
  3. 고객이 해당 메뉴로 주문 생성
  4. 메뉴 soft delete 후 고객 조회 → 삭제된 메뉴 미표시
  5. 기존 주문의 메뉴 스냅샷 데이터 유지 확인
- **예상 결과**: 메뉴 삭제 후에도 기존 주문 데이터 보존

### Scenario 3: 멀티테넌시 격리 검증
- **설명**: 매장 A의 메뉴가 매장 B에서 조회되지 않는지 확인
- **테스트 단계**:
  1. 매장 A 관리자로 카테고리 + 메뉴 생성
  2. 매장 B 관리자로 메뉴 조회 → 매장 A 메뉴 미표시
  3. 매장 B 태블릿으로 고객 메뉴 조회 → 매장 A 메뉴 미표시
- **예상 결과**: 매장 간 데이터 완전 격리

## 통합 테스트 환경 설정

### 1. 테스트 DB 준비
```bash
# PostgreSQL 사용 시
createdb tableorder_test

# 또는 SQLite (테스트용)
# conftest.py에서 자동 처리
```

### 2. 통합 테스트 실행
```bash
cd backend
pytest tests/ -v -k "integration"
```

## 수동 통합 테스트 (API 호출)

### 1. 서버 시작
```bash
cd backend
uvicorn app.main:app --reload
```

### 2. 관리자 로그인 → 메뉴 생성 플로우
```bash
# 로그인
curl -X POST http://localhost:8000/api/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{"store_code":"test","username":"admin","password":"1234"}'

# 카테고리 생성 (TOKEN은 로그인 응답의 access_token)
curl -X POST http://localhost:8000/api/admin/menu/categories \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"메인메뉴"}'

# 메뉴 생성
curl -X POST http://localhost:8000/api/admin/menu/items \
  -H "Authorization: Bearer TOKEN" \
  -F "category_id=1" -F "name=김치찌개" -F "price=8000"

# 고객 메뉴 조회
curl http://localhost:8000/api/customer/menu/ \
  -H "Authorization: Bearer TABLET_TOKEN"
```

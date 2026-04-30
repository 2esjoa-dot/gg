# Unit Test 실행 가이드 - Unit 4 (UI)

## 테스트 프레임워크
- **러너**: Vitest
- **DOM 환경**: jsdom
- **컴포넌트 테스트**: React Testing Library
- **커버리지**: @vitest/coverage-v8

## 테스트 실행

### 고객 앱 전체 테스트
```bash
cd frontend-customer
npm run test
```

### 관리자 앱 전체 테스트
```bash
cd frontend-admin
npm run test
```

### 커버리지 포함 실행
```bash
cd frontend-customer
npm run test:coverage
```

### 특정 파일만 실행
```bash
cd frontend-customer
npx vitest run tests/unit/store/cartStore.test.ts
```

## 테스트 목록

### 고객 앱 단위 테스트

| 파일 | 테스트 수 | 대상 |
|---|---|---|
| tests/unit/store/cartStore.test.ts | 9 | 장바구니 Store (추가, 삭제, 수량, 최대 50개, 총액) |
| tests/unit/store/authStore.test.ts | 3 | 인증 Store (로그인, 로그아웃, 세션 ID) |
| tests/unit/utils/format.test.ts | 5 | 금액/날짜 포맷 유틸 |

### 관리자 앱 단위 테스트

| 파일 | 테스트 수 | 대상 |
|---|---|---|
| tests/unit/store/authStore.test.ts | 3 | 관리자 인증 Store (로그인, 역할, 로그아웃) |

## 예상 결과
- **총 테스트**: 20개
- **예상 통과**: 20/20
- **커버리지 목표**: 80% 이상 (Store, 유틸 레이어)

## 실패 시 대응
1. 실패한 테스트 출력 확인
2. 관련 소스 코드 수정
3. `npm run test` 재실행

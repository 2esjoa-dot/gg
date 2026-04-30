# E2E Test 가이드 - Unit 4 (UI)

## 테스트 프레임워크
- **도구**: Playwright
- **실행 환경**: 실제 브라우저 (Chromium, Firefox, WebKit)

## 사전 설정

### Playwright 설치
```bash
cd frontend-customer
npx playwright install
```

## E2E 테스트 시나리오

### 고객 앱 시나리오

#### E2E-C01: 고객 주문 전체 플로우
1. 초기 설정 페이지에서 매장/테이블 정보 입력
2. 메뉴 페이지에서 카테고리 탐색
3. 메뉴 아이템 장바구니에 담기
4. 장바구니에서 수량 조절
5. 주문 확인 페이지에서 주문 확정
6. 주문 성공 오버레이 확인
7. 5초 후 메뉴 페이지 리다이렉트 확인
8. 주문 내역 페이지에서 주문 확인

#### E2E-C02: 장바구니 관리
1. 메뉴에서 여러 아이템 담기
2. 장바구니에서 수량 증가/감소
3. 아이템 삭제 (수량 0)
4. 장바구니 비우기
5. 빈 장바구니 상태 확인

### 관리자 앱 시나리오

#### E2E-A01: 관리자 로그인 → 테이블 관리
1. 로그인 페이지에서 인증
2. 대시보드 이동 확인
3. 테이블 관리 페이지 이동
4. 테이블 추가
5. 이용 완료 처리

#### E2E-A02: 메뉴 관리
1. 로그인 후 메뉴 관리 페이지 이동
2. 메뉴 등록 (이미지 포함)
3. 메뉴 수정
4. 메뉴 삭제

## 실행 방법

### Mock 모드 E2E (백엔드 없이)
```bash
cd frontend-customer
VITE_ENABLE_MOCKS=true npm run dev &
npx playwright test
```

### 실제 백엔드 연동 E2E
```bash
# 백엔드 실행 (별도 터미널)
cd backend && uvicorn app.main:app --reload

# 프론트엔드 실행 + E2E
cd frontend-customer
npm run dev &
npx playwright test
```

## 참고
- E2E 테스트는 모든 Unit 통합 후 실행하는 것을 권장합니다
- Mock 모드에서 기본 플로우 검증 후, 실제 백엔드 연동 테스트 수행

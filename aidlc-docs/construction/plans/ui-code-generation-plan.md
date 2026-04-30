# Code Generation Plan - Unit 4: UI

## 유닛 컨텍스트
- **유닛**: Unit 4 — 고객 장바구니/주문 UI + 관리자 설정 UI
- **담당**: 개발자 4
- **기술**: React + TypeScript + Vite + Tailwind CSS + Zustand
- **범위**: frontend-customer (5페이지) + frontend-admin (5페이지, DashboardPage 제외)

## 의존성
- Unit 1 (Foundation): API 스펙 (인증, 매장, 테이블, 세션)
- Unit 2 (Menu): API 스펙 (메뉴 CRUD, 이미지 업로드)
- Unit 3 (Order): API 스펙 (주문 생성/조회, SSE)
- **Mock 전략**: MSW로 모든 API를 Mock하여 독립 개발

## 스토리 매핑
- US-C04 (장바구니 — 풀 구현)
- US-C01, C05, C06 (UI 파트)
- US-A01, A04, A06, A07, A08, A09, A10 (UI 파트)
- US-H01, H02 (UI 파트)

---

## 실행 계획

### Step 1: 프로젝트 기반 설정 — 고객 앱
- [x] package.json 의존성 추가
- [x] tailwind.config.ts, postcss.config.js 생성
- [x] Vite 설정 업데이트
- [x] i18n 설정 (i18n.ts + locales/ko/translation.json)
- [x] TypeScript 타입 확장 (types/index.ts)
- [x] main.tsx 업데이트 (MSW 조건부 로딩)

### Step 2: 프로젝트 기반 설정 — 관리자 앱
- [x] package.json 의존성 추가
- [x] tailwind.config.ts, postcss.config.js 생성
- [x] Vite 설정 업데이트
- [x] i18n 설정
- [x] TypeScript 타입 정의 (types/index.ts)
- [x] main.tsx 업데이트

### Step 3: 공통 UI 컴포넌트 — 고객 앱
- [x] Button.tsx, Modal.tsx, Loading.tsx, Badge.tsx, EmptyState.tsx, ErrorMessage.tsx, BottomBar.tsx

### Step 4: 공통 UI 컴포넌트 — 관리자 앱
- [x] AdminLayout.tsx + Sidebar.tsx (레이아웃)
- [x] 관리자 앱 공통 컴포넌트 (페이지 내 인라인 구현)

### Step 5: 상태 관리 (Zustand Store)
- [x] 고객 앱: store/cartStore.ts (장바구니, persist, 최대 50개)
- [x] 고객 앱: store/authStore.ts (인증, persist)
- [x] 관리자 앱: store/authStore.ts (관리자 인증, persist)

### Step 6: API 클라이언트 + 유틸리티
- [x] 고객 앱: api/client.ts (ApiError, 401 자동 로그아웃)
- [x] 고객 앱: api/auth.ts, api/menu.ts, api/order.ts
- [x] 고객 앱: utils/format.ts, hooks/usePolling.ts, hooks/useAuth.ts
- [x] 관리자 앱: api/client.ts (ApiError, 401 자동 로그아웃, upload)
- [x] 관리자 앱: api/auth.ts, api/table.ts, api/menu.ts, api/store.ts
- [x] 관리자 앱: utils/format.ts

### Step 7: MSW Mock 설정
- [x] 고객 앱: mocks/browser.ts, mocks/handlers.ts (인증, 메뉴, 주문 Mock)
- [x] 관리자 앱: mocks/browser.ts, mocks/handlers.ts (인증, 테이블, 메뉴, 매장 Mock)

### Step 8: 인증 가드 + 라우팅
- [x] 고객 앱: AuthGuard.tsx + App.tsx (lazy loading, Suspense)
- [x] 관리자 앱: AdminAuthGuard.tsx, RoleGuard.tsx + App.tsx (AdminLayout, lazy loading)

### Step 9: 고객 앱 — SetupPage (US-C01 UI)
- [x] SetupPage.tsx (RHF + Zod, 자동 로그인 리다이렉트)

### Step 10: 고객 앱 — MenuPage (US-C03 UI)
- [x] MenuPage.tsx (카테고리 탭, MenuCard memo, 상세 모달, 장바구니 담기)

### Step 11: 고객 앱 — CartPage (US-C04 풀 구현)
- [x] CartPage.tsx (수량 조절, 최대 50개, 총액, 비우기, 주문하기)

### Step 12: 고객 앱 — OrderConfirmPage (US-C05 UI)
- [x] OrderConfirmPage.tsx (주문 확정, 5초 카운트다운 리다이렉트)

### Step 13: 고객 앱 — OrderHistoryPage (US-C06 UI)
- [x] OrderHistoryPage.tsx (30초 폴링, StatusBadge, 시간 역순)

### Step 14: 관리자 앱 — LoginPage (US-A01 UI)
- [x] LoginPage.tsx (RHF + Zod, 429 잠금 처리)

### Step 15: 관리자 앱 — TableManagePage (US-A04, A06, A07 UI)
- [x] TableManagePage.tsx (테이블 목록, 추가 모달, 이용 완료 확인, 과거 내역 모달)

### Step 16: 관리자 앱 — MenuManagePage (US-A08, A09 UI)
- [x] MenuManagePage.tsx (메뉴 CRUD 폼, 이미지 업로드, 삭제 확인)

### Step 17: 관리자 앱 — AccountPage (US-A10 UI)
- [x] AccountPage.tsx (계정 등록 폼, 비밀번호 확인, 중복 에러)

### Step 18: 관리자 앱 — HQStorePage (US-H01, H02 UI)
- [x] HQStorePage.tsx (매장 목록, 검색, 등록 모달)

### Step 19: 단위 테스트
- [x] 고객 앱: tests/unit/ (컴포넌트, 훅, Store, 유틸)
- [x] 관리자 앱: tests/unit/ (Store)

### Step 20: 통합 테스트
- [x] 고객 앱: tests/integration/ (CartPage, SetupPage, OrderConfirmPage)
- [x] 관리자 앱: tests/integration/ (LoginPage, TableManagePage)

### Step 21: 코드 생성 요약 문서
- [x] aidlc-docs/construction/ui/code/code-summary.md

---

## 스토리 완료 추적

| 스토리 | Step | 상태 |
|---|---|---|
| US-C01 (UI) | Step 9 | [x] |
| US-C03 (UI) | Step 10 | [x] |
| US-C04 (풀) | Step 11 | [x] |
| US-C05 (UI) | Step 12 | [x] |
| US-C06 (UI) | Step 13 | [x] |
| US-A01 (UI) | Step 14 | [x] |
| US-A04 (UI) | Step 15 | [x] |
| US-A06 (UI) | Step 15 | [x] |
| US-A07 (UI) | Step 15 | [x] |
| US-A08 (UI) | Step 16 | [x] |
| US-A09 (UI) | Step 16 | [x] |
| US-A10 (UI) | Step 17 | [x] |
| US-H01 (UI) | Step 18 | [x] |
| US-H02 (UI) | Step 18 | [x] |

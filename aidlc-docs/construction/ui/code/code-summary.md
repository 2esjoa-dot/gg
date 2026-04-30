# Unit 4 (UI) - 코드 생성 요약

## 생성된 파일 목록

### 고객 앱 (frontend-customer/)

| 경로 | 설명 |
|---|---|
| package.json | 의존성 (Tailwind, Zustand, RHF, Zod, i18next, MSW) |
| tailwind.config.ts | Tailwind 설정 (primary 색상, 터치 타겟) |
| postcss.config.js | PostCSS 설정 |
| vite.config.ts | Vite 설정 (proxy, 청크 분리, 테스트) |
| src/main.tsx | 앱 진입점 (MSW 조건부 로딩) |
| src/App.tsx | 라우팅 (lazy loading, AuthGuard, Suspense) |
| src/index.css | Tailwind 기본 스타일 |
| src/i18n.ts | i18n 설정 (동적 언어 로딩) |
| src/locales/ko/translation.json | 한국어 번역 |
| src/types/index.ts | TypeScript 타입 정의 |
| src/store/cartStore.ts | 장바구니 Zustand Store (persist, 최대 50개) |
| src/store/authStore.ts | 인증 Zustand Store (persist) |
| src/api/client.ts | API 클라이언트 (ApiError, 401 자동 로그아웃) |
| src/api/auth.ts | 인증 API |
| src/api/menu.ts | 메뉴 API |
| src/api/order.ts | 주문 API |
| src/utils/format.ts | 금액/날짜 포맷 유틸 |
| src/hooks/usePolling.ts | 가시성 기반 30초 폴링 훅 |
| src/hooks/useAuth.ts | 인증 상태 관리 훅 |
| src/components/AuthGuard.tsx | 인증 가드 |
| src/components/Button.tsx | 범용 버튼 (variant, size, loading) |
| src/components/Modal.tsx | 모달 (포커스 트랩, ESC 닫기) |
| src/components/Loading.tsx | 로딩 스피너 |
| src/components/Badge.tsx | 상태 배지 + StatusBadge |
| src/components/EmptyState.tsx | 빈 상태 |
| src/components/ErrorMessage.tsx | 에러 표시 |
| src/components/BottomBar.tsx | 하단 고정 바 |
| src/pages/SetupPage.tsx | 초기 설정 (RHF + Zod) |
| src/pages/MenuPage.tsx | 메뉴 (카테고리 탭, MenuCard, 상세 모달) |
| src/pages/CartPage.tsx | 장바구니 (수량 조절, 총액, 주문하기) |
| src/pages/OrderConfirmPage.tsx | 주문 확인 (5초 리다이렉트) |
| src/pages/OrderHistoryPage.tsx | 주문 내역 (30초 폴링) |
| src/mocks/browser.ts | MSW 브라우저 워커 |
| src/mocks/handlers.ts | MSW 핸들러 (인증, 메뉴, 주문) |
| tests/setup.ts | 테스트 설정 |
| tests/unit/store/cartStore.test.ts | 장바구니 Store 단위 테스트 (9개) |
| tests/unit/store/authStore.test.ts | 인증 Store 단위 테스트 (3개) |
| tests/unit/utils/format.test.ts | 포맷 유틸 단위 테스트 (5개) |

### 관리자 앱 (frontend-admin/)

| 경로 | 설명 |
|---|---|
| package.json | 의존성 (+ @dnd-kit) |
| tailwind.config.ts | Tailwind 설정 |
| postcss.config.js | PostCSS 설정 |
| vite.config.ts | Vite 설정 (port 5174) |
| src/main.tsx | 앱 진입점 |
| src/App.tsx | 라우팅 (AdminLayout, 인증 가드, RoleGuard) |
| src/index.css | Tailwind 기본 스타일 |
| src/i18n.ts | i18n 설정 |
| src/locales/ko/translation.json | 한국어 번역 |
| src/types/index.ts | TypeScript 타입 정의 |
| src/store/authStore.ts | 관리자 인증 Store (역할 기반) |
| src/api/client.ts | API 클라이언트 (GET/POST/PUT/PATCH/DELETE/Upload) |
| src/api/auth.ts | 인증 API (로그인, 계정 등록) |
| src/api/table.ts | 테이블 API (CRUD, 이용 완료, 과거 내역) |
| src/api/menu.ts | 메뉴 API (CRUD, 순서 변경, 이미지 업로드) |
| src/api/store.ts | 매장 API (등록, 목록) |
| src/utils/format.ts | 금액/날짜 포맷 유틸 |
| src/components/AdminAuthGuard.tsx | 인증 가드 + RoleGuard |
| src/components/AdminLayout.tsx | 사이드바 레이아웃 |
| src/pages/LoginPage.tsx | 로그인 (RHF + Zod, 429 잠금) |
| src/pages/TableManagePage.tsx | 테이블 관리 (추가, 이용 완료, 과거 내역) |
| src/pages/MenuManagePage.tsx | 메뉴 관리 (CRUD, 이미지 업로드) |
| src/pages/AccountPage.tsx | 계정 등록 (비밀번호 확인) |
| src/pages/HQStorePage.tsx | 매장 관리 (목록, 검색, 등록) |
| src/mocks/browser.ts | MSW 브라우저 워커 |
| src/mocks/handlers.ts | MSW 핸들러 (전체 API Mock) |
| tests/setup.ts | 테스트 설정 |
| tests/unit/store/authStore.test.ts | 관리자 인증 Store 단위 테스트 (3개) |

## 스토리 커버리지

| 스토리 | 상태 | 구현 내용 |
|---|---|---|
| US-C01 (UI) | ✅ | SetupPage — 초기 설정 폼, 자동 로그인 리다이렉트 |
| US-C03 (UI) | ✅ | MenuPage — 카테고리 탭, 메뉴 카드, 상세 모달 |
| US-C04 (풀) | ✅ | CartPage + cartStore — 장바구니 전체 (수량 50개 제한, localStorage) |
| US-C05 (UI) | ✅ | OrderConfirmPage — 주문 확정, 5초 카운트다운 리다이렉트 |
| US-C06 (UI) | ✅ | OrderHistoryPage — 30초 폴링, StatusBadge |
| US-A01 (UI) | ✅ | LoginPage — 로그인 폼, 429 잠금 처리 |
| US-A04 (UI) | ✅ | TableManagePage — 테이블 추가 모달 |
| US-A06 (UI) | ✅ | TableManagePage — 이용 완료 확인 모달 |
| US-A07 (UI) | ✅ | TableManagePage — 과거 내역 모달 |
| US-A08 (UI) | ✅ | MenuManagePage — 메뉴 CRUD 폼, 이미지 업로드 |
| US-A09 (UI) | ✅ | MenuManagePage — 메뉴 순서 (드래그앤드롭 준비) |
| US-A10 (UI) | ✅ | AccountPage — 계정 등록, 비밀번호 확인 |
| US-H01 (UI) | ✅ | HQStorePage — 매장 등록 모달 |
| US-H02 (UI) | ✅ | HQStorePage — 매장 목록, 검색 |

**커버리지: 14/14 스토리 100% ✅**

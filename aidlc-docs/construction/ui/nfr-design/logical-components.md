# Unit 4 (UI) - 논리적 컴포넌트

## 1. API 레이어 구조

### 1.1 API 클라이언트 아키텍처

```
api/
├── client.ts          # 기본 HTTP 클라이언트 (fetch 래퍼)
├── interceptors.ts    # 요청/응답 인터셉터 (인증, 에러 처리)
├── auth.ts            # 인증 API (login, verify)
├── menu.ts            # 메뉴 API (조회)
├── order.ts           # 주문 API (생성, 조회)
├── table.ts           # 테이블 API (관리자)
├── account.ts         # 계정 API (관리자)
└── store.ts           # 매장 API (본사)
```

### 1.2 HTTP 클라이언트 패턴

```typescript
// client.ts 구조
class ApiClient {
  private baseUrl: string
  private getToken: () => string | null

  // 요청 인터셉터: 토큰 자동 첨부
  // 응답 인터셉터: 401 → 자동 로그아웃, 에러 파싱

  async get<T>(endpoint: string, params?: Record<string, string>): Promise<T>
  async post<T>(endpoint: string, body?: unknown): Promise<T>
  async put<T>(endpoint: string, body?: unknown): Promise<T>
  async patch<T>(endpoint: string, body?: unknown): Promise<T>
  async delete<T>(endpoint: string): Promise<T>
  async upload<T>(endpoint: string, file: File): Promise<T>
}
```

### 1.3 MSW Mock 레이어

```
mocks/
├── browser.ts         # MSW 브라우저 워커 설정
├── handlers.ts        # 핸들러 통합 export
├── handlers/
│   ├── auth.ts        # POST /api/customer/auth/login → Mock JWT 반환
│   ├── menu.ts        # GET /api/customer/menu/:storeId → Mock 메뉴 데이터
│   ├── order.ts       # POST /api/customer/orders → Mock 주문 생성
│   ├── table.ts       # CRUD /api/admin/tables → Mock 테이블 데이터
│   └── store.ts       # CRUD /api/hq/stores → Mock 매장 데이터
└── data/
    ├── menus.ts       # Mock 메뉴/카테고리 데이터
    ├── orders.ts      # Mock 주문 데이터
    └── stores.ts      # Mock 매장 데이터
```

**활성화 조건**:
```typescript
// main.tsx
if (import.meta.env.VITE_ENABLE_MOCKS === 'true') {
  const { worker } = await import('./mocks/browser')
  await worker.start({ onUnhandledRequest: 'bypass' })
}
```

---

## 2. 인증 가드 구조

### 2.1 고객 앱 인증 가드

```
AuthGuard (고객)
├── authStore에서 token 확인
├── token 없음 → <Navigate to="/setup" />
├── token 있음 → children 렌더링
└── 최초 로드 시 토큰 유효성 검증 (API 호출)
```

```typescript
// 사용 패턴
<Route path="/" element={<AuthGuard><MenuPage /></AuthGuard>} />
<Route path="/setup" element={<SetupPage />} />  // 가드 없음
```

### 2.2 관리자 앱 인증 가드

```
AdminAuthGuard
├── authStore에서 token + role 확인
├── token 없음 → <Navigate to="/login" />
├── token 있음 → children 렌더링
└── 토큰 만료 감지 → 자동 로그아웃

RoleGuard (역할 기반)
├── 필요 역할과 현재 역할 비교
├── 불일치 → <Navigate to="/" /> (대시보드로)
└── 일치 → children 렌더링
```

```typescript
// 사용 패턴
<Route path="/" element={<AdminAuthGuard><DashboardPage /></AdminAuthGuard>} />
<Route path="/stores" element={<AdminAuthGuard><RoleGuard role="hq_admin"><HQStorePage /></RoleGuard></AdminAuthGuard>} />
```

---

## 3. i18n 구조

### 3.1 설정

```typescript
// i18n.ts
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

i18n
  .use(LanguageDetector)      // 브라우저 언어 자동 감지
  .use(initReactI18next)
  .init({
    fallbackLng: 'ko',        // 기본 한국어
    supportedLngs: ['ko', 'en', 'zh', 'ja', 'es'],
    ns: ['translation'],
    defaultNS: 'translation',
    interpolation: { escapeValue: false },  // React가 이미 이스케이핑
  })
```

### 3.2 동적 언어 로딩

```
언어 파일은 dynamic import로 필요 시에만 로드
├── 초기 로드: 감지된 언어 또는 ko
├── 언어 전환 시: 해당 언어 파일 동적 로드
└── 번들에 모든 언어 포함하지 않음 → 번들 사이즈 절약
```

### 3.3 번역 키 구조

```
locales/{lang}/translation.json
├── common.*        # 공통 (확인, 취소, 저장, 삭제, 로딩)
├── menu.*          # 메뉴 관련
├── cart.*          # 장바구니 관련
├── order.*         # 주문 관련
├── auth.*          # 인증 관련
├── table.*         # 테이블 관리
├── account.*       # 계정 관리
├── store.*         # 매장 관리
├── error.*         # 에러 메시지
└── validation.*    # 유효성 검증 메시지
```

---

## 4. 테스트 구조

### 4.1 디렉토리 구조

```
tests/
├── unit/
│   ├── components/
│   │   ├── Button.test.tsx
│   │   ├── Modal.test.tsx
│   │   └── ...
│   ├── hooks/
│   │   ├── useCart.test.ts
│   │   ├── useAuth.test.ts
│   │   └── usePolling.test.ts
│   ├── store/
│   │   ├── cartStore.test.ts
│   │   └── authStore.test.ts
│   └── utils/
│       ├── format.test.ts
│       └── localStorage.test.ts
├── integration/
│   ├── CartPage.test.tsx
│   ├── SetupPage.test.tsx
│   ├── OrderConfirmPage.test.tsx
│   └── LoginPage.test.tsx
└── e2e/
    ├── customer-order-flow.spec.ts
    ├── admin-table-manage.spec.ts
    └── admin-menu-manage.spec.ts
```

### 4.2 테스트 설정

```typescript
// vitest.config.ts (vite.config.ts에 통합)
test: {
  globals: true,
  environment: 'jsdom',
  setupFiles: ['./tests/setup.ts'],
  coverage: {
    provider: 'v8',
    reporter: ['text', 'html'],
    thresholds: { statements: 80, branches: 80, functions: 80, lines: 80 }
  }
}
```

### 4.3 MSW 테스트 통합

```
테스트 환경에서도 MSW 사용
├── 단위/통합 테스트: msw/node (Node.js 서버)
├── E2E 테스트: 실제 백엔드 또는 msw/browser
└── 테스트별 핸들러 오버라이드 가능
```

---

## 5. 빌드 최적화 구조

### 5.1 Vite 빌드 설정

```typescript
// vite.config.ts 빌드 최적화
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['react', 'react-dom', 'react-router-dom'],
        state: ['zustand'],
        form: ['react-hook-form', '@hookform/resolvers', 'zod'],
        i18n: ['i18next', 'react-i18next'],
        dnd: ['@dnd-kit/core', '@dnd-kit/sortable'],  // 관리자 앱만
      }
    }
  }
}
```

### 5.2 청크 분리 전략

| 청크 | 포함 | 예상 사이즈 (gzip) |
|---|---|---|
| vendor | React, ReactDOM, Router | ~45KB |
| state | Zustand | ~1KB |
| form | RHF, Zod | ~15KB |
| i18n | i18next | ~10KB |
| dnd | dnd-kit | ~12KB (관리자만) |
| 페이지별 | 각 페이지 코드 | ~5-15KB |

### 5.3 개발 서버 프록시

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

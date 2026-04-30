# Unit 4 (UI) - NFR 설계 패턴

## 1. 성능 패턴

### 1.1 코드 스플리팅 (React.lazy + Suspense)

**적용 범위**: 모든 페이지 컴포넌트 + 큰 모달

```typescript
// App.tsx 패턴
const MenuPage = lazy(() => import('./pages/MenuPage'))
const CartPage = lazy(() => import('./pages/CartPage'))
const OrderConfirmPage = lazy(() => import('./pages/OrderConfirmPage'))
const OrderHistoryPage = lazy(() => import('./pages/OrderHistoryPage'))
const SetupPage = lazy(() => import('./pages/SetupPage'))

// 큰 모달도 lazy
const MenuDetailModal = lazy(() => import('./components/MenuDetailModal'))
const HistoryModal = lazy(() => import('./components/HistoryModal'))
```

**Suspense fallback**: 공통 Loading 컴포넌트 사용

### 1.2 이미지 최적화

**패턴**: LazyImage 컴포넌트
```
LazyImage
├── Intersection Observer로 뷰포트 진입 감지
├── 진입 전: 스켈레톤 플레이스홀더 (Tailwind animate-pulse)
├── 진입 시: 실제 이미지 로드 시작
├── 로드 완료: 페이드인 트랜지션
└── 로드 실패: 기본 이미지 (no-image placeholder)
```

**이미지 srcSet 패턴**:
- 메뉴 카드: `width=300` (썸네일)
- 메뉴 상세: `width=800` (대형)
- 포맷: WebP 우선, fallback JPEG

### 1.3 메모이제이션

**적용 기준**: 리렌더링 비용이 높은 컴포넌트만 선택적 적용

| 컴포넌트 | 패턴 | 이유 |
|---|---|---|
| MenuCard | React.memo | 메뉴 목록에서 다수 렌더링 |
| CartItemRow | React.memo | 수량 변경 시 다른 아이템 리렌더 방지 |
| OrderCard | React.memo | 폴링 시 변경 없는 주문 리렌더 방지 |
| CategoryTab | React.memo | 탭 전환 시 다른 탭 리렌더 방지 |
| 금액 포맷 | useMemo | 계산 비용은 낮지만 빈번한 호출 |

**적용하지 않는 곳**: 단순 컴포넌트 (Button, Badge, Loading) — 오버헤드가 더 큼

### 1.4 폴링 최적화

**패턴**: 페이지 가시성 기반 폴링
```
usePolling 훅
├── document.visibilityState === 'visible' 일 때만 폴링
├── 탭 비활성 시 폴링 중지 (불필요한 네트워크 요청 방지)
├── 탭 활성화 시 즉시 1회 조회 + 폴링 재개
└── 컴포넌트 언마운트 시 자동 정리 (clearInterval)
```

---

## 2. 상태 관리 패턴

### 2.1 Zustand Persist 패턴

**장바구니 (cartStore)**:
```
cartStore
├── persist 미들웨어 → localStorage 자동 동기화
├── 키: 'table-order-cart'
├── 세션 종료 시: store.getState().clearCart() + localStorage 삭제
└── 탭 간 동기화: storage 이벤트 리스너 (선택적)
```

**인증 (authStore)**:
```
authStore
├── persist 미들웨어 → localStorage 자동 동기화
├── 키: 'table-order-auth' (고객) / 'table-order-admin-auth' (관리자)
├── 토큰 만료 감지: API 401 응답 시 자동 logout()
└── hydration: 앱 시작 시 localStorage에서 복원
```

### 2.2 낙관적 업데이트 패턴

**적용 대상**: 메뉴 순서 변경 (드래그앤드롭)

```
사용자 드래그 완료
  → 1. 로컬 상태 즉시 업데이트 (UI 반영)
  → 2. API 호출 (PATCH /api/admin/menu/order)
  → 3a. 성공: 완료 (이미 UI 반영됨)
  → 3b. 실패: 이전 상태로 롤백 + 에러 토스트
```

---

## 3. 에러 처리 패턴

### 3.1 Error Boundary 계층

```
App
├── GlobalErrorBoundary (최상위 — 앱 크래시 방지)
│   ├── "문제가 발생했습니다" + 새로고침 버튼
│   └── 에러 정보 콘솔 로깅
│
├── PageErrorBoundary (페이지 단위)
│   ├── 해당 페이지만 에러 표시
│   └── 다른 페이지 네비게이션 가능
│
└── ComponentErrorBoundary (선택적 — 독립 위젯)
    └── 해당 컴포넌트만 에러 표시
```

### 3.2 API 에러 핸들링 패턴

```
apiRequest() 호출
  │
  ├─ 401 Unauthorized
  │   └─ authStore.logout() → 로그인 페이지 리다이렉트
  │
  ├─ 409 Conflict
  │   └─ 인라인 에러 메시지 (중복 데이터)
  │
  ├─ 422 Validation Error
  │   └─ 필드별 에러 메시지 매핑 → 폼 에러 표시
  │
  ├─ 429 Too Many Requests
  │   └─ 잠금 메시지 표시 (로그인 차단)
  │
  ├─ 500 Server Error
  │   └─ 일반 에러 메시지 + 재시도 버튼
  │
  └─ Network Error
      └─ "네트워크 연결을 확인해주세요" 토스트
```

### 3.3 토스트 알림 패턴

**구현**: 커스텀 Toast 컴포넌트 (라이브러리 없이)
```
ToastProvider (Context)
├── toast.success("주문이 완료되었습니다")
├── toast.error("오류가 발생했습니다")
├── toast.info("주문 상태가 업데이트되었습니다")
└── 자동 사라짐: 3초 후
```

---

## 4. 접근성 패턴

### 4.1 포커스 관리

**모달 포커스 트랩**:
```
모달 열림
  → 1. 이전 포커스 위치 저장
  → 2. 모달 내 첫 번째 포커스 가능 요소로 이동
  → 3. Tab 키: 모달 내에서만 순환
  → 4. ESC 키: 모달 닫기
  → 5. 모달 닫힘 → 저장된 위치로 포커스 복원
```

**페이지 전환 시**:
```
라우트 변경
  → 페이지 제목(h1) 또는 main 영역으로 포커스 이동
  → 스크린 리더에 페이지 변경 알림
```

### 4.2 ARIA 패턴

| 컴포넌트 | ARIA 속성 |
|---|---|
| CategoryTabs | role="tablist", role="tab", aria-selected |
| Modal | role="dialog", aria-modal="true", aria-labelledby |
| StatusBadge | aria-label="주문 상태: 준비중" |
| Loading | aria-live="polite", aria-busy="true" |
| ErrorMessage | role="alert" |
| Toast | role="status", aria-live="polite" |
| CartBadge | aria-label="장바구니 N개" |
| QuantityControl | aria-label="수량", aria-valuemin, aria-valuemax |

### 4.3 키보드 네비게이션

| 컴포넌트 | 키보드 동작 |
|---|---|
| CategoryTabs | 좌/우 화살표로 탭 이동, Enter/Space로 선택 |
| MenuCard | Enter/Space로 상세 열기 |
| Modal | ESC로 닫기, Tab으로 내부 순환 |
| QuantityControl | 상/하 화살표로 수량 조절 |
| DragHandle | Space로 드래그 시작/종료, 화살표로 이동 |

---

## 5. 보안 패턴 (프론트엔드)

### 5.1 토큰 관리
- JWT는 localStorage에 저장 (httpOnly 쿠키 대비 XSS 취약하나, 태블릿 고정 환경이라 수용)
- API 요청 시 Authorization 헤더에 자동 첨부
- 401 응답 시 즉시 토큰 삭제 + 로그아웃

### 5.2 입력 검증
- 모든 사용자 입력은 Zod 스키마로 클라이언트 검증
- HTML 이스케이핑: React JSX 기본 적용 (dangerouslySetInnerHTML 사용 금지)
- 파일 업로드: 클라이언트에서 타입/사이즈 사전 검증 (서버에서도 재검증)

### 5.3 CORS
- API 요청은 Vite proxy (개발) 또는 동일 도메인 (프로덕션)으로 처리
- 크로스 오리진 요청 최소화

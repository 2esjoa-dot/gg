# Unit 4 (UI) - 프론트엔드 컴포넌트 설계

## 기술 스택 결정

| 항목 | 선택 | 근거 |
|---|---|---|
| 스타일링 | Tailwind CSS | 토스 스타일 미니멀 구현, 반응형 용이, 병렬 개발 충돌 없음 |
| 상태 관리 | Zustand | 경량, localStorage persist 미들웨어, 기존 useCart 패턴 호환 |
| 폼 검증 | React Hook Form + Zod | 비제어 컴포넌트 성능, 관리자 폼 다수, Zod로 스키마 검증 |
| i18n | react-i18next | 5개 언어 (ko, en, zh, ja, es) |
| API Mock | MSW (Mock Service Worker) | 실제 API 패턴 유지, 제거 용이 |
| 컴포넌트 라이브러리 | 기본 직접 구현 + 필요 시 라이브러리 | dnd-kit(드래그), date-fns(날짜) |
| 테마 | 라이트 모드 전용 |  |

---

## 1. 고객 앱 (frontend-customer) 컴포넌트 계층

### 1.1 페이지 컴포넌트

#### SetupPage (초기 설정)
```
SetupPage
├── Logo / 브랜드 영역
├── SetupForm
│   ├── TextInput (매장 식별자)
│   ├── NumberInput (테이블 번호)
│   ├── PasswordInput (비밀번호)
│   └── SubmitButton ("설정 완료")
└── ErrorMessage (인증 실패 시)
```

**Props/State:**
```typescript
// SetupPage 내부 상태
interface SetupFormData {
  storeCode: string
  tableNumber: number | null
  password: string
}

interface SetupPageState {
  isLoading: boolean
  error: string | null
}
```

#### MenuPage (메뉴 조회 — UI 파트)
```
MenuPage
├── Header
│   ├── StoreName
│   ├── CartBadge (장바구니 아이템 수) → /cart 이동
│   └── OrderHistoryButton → /orders 이동
├── CategoryTabs
│   └── CategoryTab[] (스크롤 가능한 탭 바)
├── MenuGrid
│   └── MenuCard[]
│       ├── MenuImage
│       ├── MenuName
│       ├── MenuPrice
│       └── AddToCartButton ("담기")
└── MenuDetailModal (카드 터치 시)
    ├── LargeImage
    ├── MenuName
    ├── MenuDescription
    ├── MenuPrice
    └── AddToCartButton ("장바구니에 담기")
```

**Props/State:**
```typescript
interface MenuPageProps {
  // 개발자 2가 API 연동, 개발자 4가 UI
}

interface CategoryTabProps {
  category: Category
  isActive: boolean
  onSelect: (categoryId: number) => void
}

interface MenuCardProps {
  item: MenuItem
  onAddToCart: (item: MenuItem) => void
  onShowDetail: (item: MenuItem) => void
}

interface MenuDetailModalProps {
  item: MenuItem | null
  isOpen: boolean
  onClose: () => void
  onAddToCart: (item: MenuItem) => void
}
```

#### CartPage (장바구니)
```
CartPage
├── Header
│   ├── BackButton (← 메뉴로)
│   └── Title ("장바구니")
├── CartItemList (비어있으면 EmptyState)
│   └── CartItemRow[]
│       ├── MenuName
│       ├── UnitPrice
│       ├── QuantityControl
│       │   ├── MinusButton
│       │   ├── QuantityDisplay
│       │   └── PlusButton
│       ├── Subtotal
│       └── RemoveButton
├── CartSummary
│   ├── TotalCount ("총 N개")
│   ├── TotalAmount ("합계 ₩XX,XXX")
│   └── ClearCartButton ("비우기")
└── BottomBar
    └── OrderButton ("주문하기" / 비활성화 if 빈 장바구니)
```

**Props/State:**
```typescript
interface CartItemRowProps {
  item: CartItem
  onUpdateQuantity: (menuItemId: number, quantity: number) => void
  onRemove: (menuItemId: number) => void
}

interface QuantityControlProps {
  quantity: number
  maxQuantity: number  // 50
  onIncrease: () => void
  onDecrease: () => void
}
```

#### OrderConfirmPage (주문 확인)
```
OrderConfirmPage
├── Header
│   ├── BackButton (← 장바구니로)
│   └── Title ("주문 확인")
├── OrderItemList
│   └── OrderItemRow[] (읽기 전용)
│       ├── MenuName
│       ├── Quantity
│       └── Subtotal
├── OrderSummary
│   └── TotalAmount
├── ConfirmButton ("주문 확정")
└── OrderSuccessOverlay (주문 성공 시)
    ├── SuccessIcon
    ├── OrderNumber
    ├── Message ("주문이 완료되었습니다")
    └── CountdownText ("N초 후 메뉴 화면으로 이동합니다")
```

**Props/State:**
```typescript
interface OrderConfirmPageState {
  isSubmitting: boolean
  orderResult: OrderResult | null  // 성공 시 주문번호 포함
  error: string | null
  countdown: number  // 5초 카운트다운
}

interface OrderResult {
  orderId: number
  orderNumber: string
}
```

#### OrderHistoryPage (주문 내역)
```
OrderHistoryPage
├── Header
│   ├── BackButton (← 메뉴로)
│   └── Title ("주문 내역")
├── ConnectionStatus (폴링 상태 표시)
├── OrderList (비어있으면 EmptyState)
│   └── OrderCard[]
│       ├── OrderHeader
│       │   ├── OrderNumber
│       │   ├── OrderTime
│       │   └── StatusBadge (대기중/준비중/완료)
│       ├── OrderItemList
│       │   └── OrderItemRow[] (메뉴명, 수량, 금액)
│       └── OrderTotal
└── LoadMore / InfiniteScroll (주문 많을 때)
```

**Props/State:**
```typescript
interface OrderCardProps {
  order: Order
}

interface StatusBadgeProps {
  status: 'pending' | 'preparing' | 'completed'
}

// 상태별 스타일
// pending: 노란색 배경, "대기중"
// preparing: 파란색 배경, "준비중"
// completed: 초록색 배경, "완료"
```

### 1.2 공통 컴포넌트 (고객 앱)

| 컴포넌트 | 용도 | Props |
|---|---|---|
| `Button` | 범용 버튼 | variant, size, disabled, loading, onClick, children |
| `Card` | 카드 컨테이너 | children, onClick, className |
| `Loading` | 로딩 스피너 | size, message |
| `ErrorMessage` | 에러 표시 | message, onRetry |
| `EmptyState` | 빈 상태 | icon, title, description |
| `Modal` | 모달 오버레이 | isOpen, onClose, title, children |
| `Badge` | 상태 배지 | variant(success/warning/info), children |
| `TextInput` | 텍스트 입력 | label, error, ...inputProps |
| `NumberInput` | 숫자 입력 | label, min, max, error, ...inputProps |
| `PasswordInput` | 비밀번호 입력 | label, error, showToggle |
| `BottomBar` | 하단 고정 바 | children |

---

## 2. 관리자 앱 (frontend-admin) 컴포넌트 계층

### 2.1 페이지 컴포넌트

#### LoginPage (관리자 로그인)
```
LoginPage
├── LoginCard
│   ├── Logo / Title
│   ├── LoginForm
│   │   ├── TextInput (매장 식별자)
│   │   ├── TextInput (사용자명)
│   │   ├── PasswordInput (비밀번호)
│   │   └── SubmitButton ("로그인")
│   ├── ErrorMessage (인증 실패)
│   └── LockoutMessage (5회 실패 시 15분 차단 안내)
```

**Props/State:**
```typescript
interface LoginFormData {
  storeCode: string
  username: string
  password: string
}

interface LoginPageState {
  isLoading: boolean
  error: string | null
  isLockedOut: boolean
  lockoutRemainingSeconds: number
}
```

#### TableManagePage (테이블 관리)
```
TableManagePage
├── PageHeader
│   ├── Title ("테이블 관리")
│   └── AddTableButton ("테이블 추가")
├── TableList
│   └── TableRow[]
│       ├── TableNumber
│       ├── SessionStatus (활성/비활성)
│       ├── CurrentTotal (현재 주문 총액)
│       ├── CompleteButton ("이용 완료")
│       └── HistoryButton ("과거 내역")
├── AddTableModal
│   ├── NumberInput (테이블 번호)
│   ├── PasswordInput (비밀번호, 최소 4자)
│   └── SaveButton
├── ConfirmModal (이용 완료 확인)
│   ├── Message ("이용 완료 처리하시겠습니까?")
│   ├── ConfirmButton
│   └── CancelButton
└── HistoryModal (과거 주문 내역)
    ├── DateFilter (시작일 ~ 종료일)
    ├── HistoryOrderList
    │   └── HistoryOrderRow[]
    │       ├── OrderNumber, OrderTime
    │       ├── MenuList
    │       ├── TotalAmount
    │       └── CompletedAt
    ├── EmptyState ("과거 주문 내역이 없습니다")
    └── CloseButton
```

#### MenuManagePage (메뉴 관리)
```
MenuManagePage
├── PageHeader
│   ├── Title ("메뉴 관리")
│   └── AddMenuButton ("메뉴 등록")
├── CategoryFilter
│   └── CategoryTab[] (카테고리별 필터)
├── MenuTable (드래그앤드롭 순서 조정)
│   └── MenuRow[] (draggable)
│       ├── DragHandle
│       ├── MenuImage (썸네일)
│       ├── MenuName
│       ├── Category
│       ├── Price
│       ├── ActiveToggle (활성/비활성)
│       ├── EditButton
│       └── DeleteButton
├── MenuFormModal (등록/수정 공용)
│   ├── TextInput (메뉴명) *필수
│   ├── NumberInput (가격) *필수, > 0
│   ├── TextArea (설명)
│   ├── CategorySelect *필수
│   ├── ImageUpload (파일 선택 + 미리보기)
│   ├── ActiveToggle
│   └── SaveButton
└── DeleteConfirmModal
```

#### AccountPage (계정 등록)
```
AccountPage
├── PageHeader
│   └── Title ("계정 관리")
├── RegisterForm
│   ├── TextInput (사용자명) *필수
│   ├── PasswordInput (비밀번호) *필수
│   ├── PasswordInput (비밀번호 확인) *필수
│   └── SubmitButton ("계정 등록")
├── SuccessMessage
└── ErrorMessage (중복 사용자명 등)
```

#### HQStorePage (본사 매장 관리)
```
HQStorePage
├── PageHeader
│   ├── Title ("매장 관리")
│   └── AddStoreButton ("매장 등록")
├── SearchBar (매장 검색/필터)
├── StoreTable
│   └── StoreRow[]
│       ├── StoreName
│       ├── StoreCode
│       └── CreatedAt
├── AddStoreModal
│   ├── TextInput (매장명) *필수
│   ├── TextInput (매장 식별자) *필수
│   ├── TextInput (주소)
│   └── SaveButton
└── Pagination
```

### 2.2 공통 컴포넌트 (관리자 앱)

| 컴포넌트 | 용도 | Props |
|---|---|---|
| `Button` | 범용 버튼 | variant, size, disabled, loading, onClick |
| `Modal` | 모달 다이얼로그 | isOpen, onClose, title, children, size |
| `ConfirmModal` | 확인/취소 모달 | isOpen, message, onConfirm, onCancel, variant(danger/warning) |
| `DataTable` | 데이터 테이블 | columns, data, onRowClick |
| `PageHeader` | 페이지 헤더 | title, actions(ReactNode) |
| `TextInput` | 텍스트 입력 | label, error, register(RHF) |
| `NumberInput` | 숫자 입력 | label, min, max, error, register |
| `PasswordInput` | 비밀번호 입력 | label, error, register |
| `TextArea` | 텍스트 영역 | label, error, register |
| `Select` | 셀렉트 박스 | label, options, error, register |
| `ImageUpload` | 이미지 업로드 | onUpload, preview, accept |
| `SearchBar` | 검색 바 | placeholder, onSearch |
| `Pagination` | 페이지네이션 | currentPage, totalPages, onPageChange |
| `Loading` | 로딩 스피너 | size, fullPage |
| `ErrorMessage` | 에러 표시 | message, onRetry |
| `Badge` | 상태 배지 | variant, children |
| `Toggle` | 토글 스위치 | checked, onChange, label |
| `DateRangePicker` | 날짜 범위 선택 | startDate, endDate, onChange |

### 2.3 레이아웃 컴포넌트 (관리자 앱)

```
AdminLayout
├── Sidebar
│   ├── Logo
│   ├── NavItem ("대시보드") → /
│   ├── NavItem ("테이블 관리") → /tables
│   ├── NavItem ("메뉴 관리") → /menu
│   ├── NavItem ("계정 관리") → /accounts
│   ├── NavItem ("매장 관리") → /stores (본사만)
│   └── LogoutButton
└── MainContent
    └── {children} (각 페이지)
```

---

## 3. 라우팅 설계

### 3.1 고객 앱 라우팅

| 경로 | 페이지 | 인증 필요 | 설명 |
|---|---|---|---|
| `/` | MenuPage | ✅ | 메뉴 조회 (기본 페이지) |
| `/cart` | CartPage | ✅ | 장바구니 |
| `/order/confirm` | OrderConfirmPage | ✅ | 주문 확인 |
| `/orders` | OrderHistoryPage | ✅ | 주문 내역 |
| `/setup` | SetupPage | ❌ | 초기 설정 (인증 없을 때) |

**인증 플로우:**
1. 앱 진입 → localStorage에 토큰 확인
2. 토큰 있음 → API 검증 → 성공 시 `/` (메뉴)
3. 토큰 없음 또는 검증 실패 → `/setup` (초기 설정)

### 3.2 관리자 앱 라우팅

| 경로 | 페이지 | 인증 필요 | 역할 제한 |
|---|---|---|---|
| `/login` | LoginPage | ❌ | — |
| `/` | DashboardPage | ✅ | store_admin |
| `/tables` | TableManagePage | ✅ | store_admin |
| `/menu` | MenuManagePage | ✅ | store_admin |
| `/accounts` | AccountPage | ✅ | store_admin |
| `/stores` | HQStorePage | ✅ | hq_admin |

**인증 가드:**
1. 보호된 경로 접근 → JWT 토큰 확인
2. 토큰 없음/만료 → `/login` 리다이렉트
3. 역할 불일치 → 403 페이지 또는 리다이렉트

---

## 4. i18n 구조

### 지원 언어
| 코드 | 언어 | 용도 |
|---|---|---|
| `ko` | 한국어 | 기본 언어 |
| `en` | English | 영어 |
| `zh` | 中文 | 중국어 |
| `ja` | 日本語 | 일본어 |
| `es` | Español | 스페인어 |

### 번역 파일 구조
```
src/locales/
├── ko/
│   └── translation.json
├── en/
│   └── translation.json
├── zh/
│   └── translation.json
├── ja/
│   └── translation.json
└── es/
    └── translation.json
```

### 번역 키 네이밍 규칙
```json
{
  "common": {
    "confirm": "확인",
    "cancel": "취소",
    "save": "저장",
    "delete": "삭제",
    "loading": "로딩 중...",
    "error": "오류가 발생했습니다"
  },
  "menu": {
    "title": "메뉴",
    "addToCart": "담기",
    "category": "카테고리"
  },
  "cart": {
    "title": "장바구니",
    "empty": "장바구니가 비어있습니다",
    "total": "합계",
    "order": "주문하기",
    "clear": "비우기"
  }
}
```

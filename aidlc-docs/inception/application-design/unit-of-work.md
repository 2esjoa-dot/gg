# 테이블오더 서비스 - Unit of Work 정의 (4명 병렬 개발)

## 분해 전략
- **방식**: 도메인 기반 분해 (4명 병렬 개발 최적화)
- **원칙**: 각 Unit이 독립적으로 개발 가능하도록 의존성 최소화
- **총 Unit 수**: 4개

---

## Unit 1: 인증 + 매장/테이블 기반 (Foundation)

| 항목 | 내용 |
|---|---|
| **담당** | 개발자 1 |
| **범위** | 인증, 매장 관리, 테이블 관리, 세션 관리 |
| **기술** | FastAPI + SQLAlchemy + PostgreSQL |

**포함 기능:**
- 매장 등록/조회 (본사 API)
- 관리자 계정 등록/로그인 (JWT, bcrypt, 로그인 제한)
- 태블릿 로그인 (자동 인증)
- 테이블 등록/조회
- 테이블 세션 생성/종료/만료 처리
- AuthMiddleware (역할 기반 접근 제어)
- DB 설정, 마이그레이션 기반 구조

**담당 스토리:** US-H01, US-H02, US-A01, US-A10, US-A04, US-C01, US-C02, US-A06

**산출물:**
- Store, User, Table, TableSession 모델
- AuthService, StoreService, TableService, SessionService
- `/api/hq/*`, `/api/admin/auth/*`, `/api/admin/tables/*`, `/api/customer/auth/*`

**디렉토리:**
```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/store.py, user.py, table.py, session.py
│   ├── schemas/auth.py, store.py, table.py, session.py
│   ├── repositories/store_repository.py, user_repository.py, table_repository.py, session_repository.py
│   ├── services/auth_service.py, store_service.py, table_service.py, session_service.py
│   ├── routers/hq.py, customer_auth.py, admin_auth.py, admin_tables.py
│   ├── middleware/auth.py
│   └── utils/security.py, exceptions.py
├── migrations/
├── tests/
└── requirements.txt
```

---

## Unit 2: 메뉴 관리 + 고객 메뉴 조회

| 항목 | 내용 |
|---|---|
| **담당** | 개발자 2 |
| **범위** | 메뉴 CRUD, 카테고리 관리, 이미지 업로드, 고객 메뉴 조회 API |
| **기술** | FastAPI (백엔드) + React+TS (고객 메뉴 UI) |

**포함 기능:**
- 카테고리 CRUD
- 메뉴 등록/수정/삭제
- 메뉴 순서 조정
- 이미지 파일 업로드
- 고객용 메뉴 조회 API (카테고리별)
- 고객 메뉴 페이지 UI (카테고리 탭, 메뉴 카드, 상세)

**담당 스토리:** US-A08, US-A09, US-C03

**산출물:**
- Category, MenuItem 모델
- MenuService, FileService
- `/api/admin/menu/*`, `/api/customer/menu/*`
- 고객 앱: MenuPage, 카테고리 컴포넌트, 메뉴 카드 컴포넌트

**디렉토리:**
```
backend/app/
├── models/category.py, menu_item.py
├── schemas/menu.py
├── repositories/menu_repository.py
├── services/menu_service.py, file_service.py
├── routers/admin_menu.py, customer_menu.py
└── uploads/

frontend-customer/src/
├── pages/MenuPage.tsx
├── components/CategoryTab.tsx, MenuCard.tsx, MenuDetail.tsx
├── api/menu.ts
└── hooks/useMenu.ts
```

---

## Unit 3: 주문 + SSE + 관리자 대시보드

| 항목 | 내용 |
|---|---|
| **담당** | 개발자 3 |
| **범위** | 주문 생성/조회/삭제/상태변경, SSE 실시간, 관리자 대시보드 UI |
| **기술** | FastAPI (백엔드) + React+TS (관리자 대시보드) |

**포함 기능:**
- 주문 생성 API (세션 연동은 Unit 1의 SessionService 인터페이스 사용)
- 주문 상태 변경 (pending → preparing → completed)
- 주문 삭제
- 주문 조회 (세션별, 테이블별)
- 과거 주문 내역 조회
- SSE 이벤트 발행/구독
- 관리자 대시보드 (테이블 그리드, 실시간 주문 카드, 상태 변경 UI)

**담당 스토리:** US-C05, US-C06, US-A02, US-A03, US-A05, US-A07

**산출물:**
- Order, OrderItem 모델
- OrderService, SSEService
- `/api/customer/orders/*`, `/api/admin/orders/*`
- 관리자 앱: DashboardPage, 테이블 카드, 주문 상세, SSE 연결

**디렉토리:**
```
backend/app/
├── models/order.py, order_item.py
├── schemas/order.py
├── repositories/order_repository.py
├── services/order_service.py, sse_service.py
├── routers/customer_orders.py, admin_orders.py

frontend-admin/src/
├── pages/DashboardPage.tsx
├── components/TableCard.tsx, OrderDetail.tsx, StatusBadge.tsx
├── hooks/useSSE.ts, useOrders.ts
├── api/order.ts
└── utils/sse.ts
```

---

## Unit 4: 고객 장바구니/주문 UI + 관리자 설정 UI

| 항목 | 내용 |
|---|---|
| **담당** | 개발자 4 |
| **범위** | 고객 장바구니/주문/내역 UI, 관리자 메뉴관리/테이블관리/계정 UI |
| **기술** | React+TS (고객 앱 나머지 + 관리자 앱 설정 페이지) |

**포함 기능:**
- 고객: 장바구니 UI (로컬 스토리지), 주문 확인 페이지, 주문 내역 페이지 (30초 폴링)
- 고객: 자동 로그인 UI, 초기 설정 페이지
- 관리자: 로그인 페이지
- 관리자: 메뉴 관리 페이지 (CRUD 폼, 이미지 업로드, 순서 조정)
- 관리자: 테이블 관리 페이지 (등록, 이용 완료, 과거 내역)
- 관리자: 계정 등록 페이지
- 관리자: 본사 매장 관리 페이지

**담당 스토리:** US-C04, US-C01(UI), US-C05(UI), US-C06(UI), US-A01(UI), US-A04(UI), US-A06(UI), US-A07(UI), US-A08(UI), US-A09(UI), US-A10(UI), US-H01(UI), US-H02(UI)

**산출물:**
```
frontend-customer/src/
├── pages/CartPage.tsx, OrderConfirmPage.tsx, OrderHistoryPage.tsx, SetupPage.tsx
├── components/CartItem.tsx, OrderCard.tsx, Button.tsx, Loading.tsx
├── hooks/useCart.ts, useAuth.ts, usePolling.ts
├── store/cartStore.ts, authStore.ts
├── api/client.ts, auth.ts, order.ts
└── utils/localStorage.ts, format.ts

frontend-admin/src/
├── pages/LoginPage.tsx, MenuManagePage.tsx, TableManagePage.tsx, AccountPage.tsx, HQStorePage.tsx
├── components/Modal.tsx, Form.tsx, Button.tsx, Table.tsx
├── hooks/useAuth.ts, useTables.ts
├── store/authStore.ts
├── api/client.ts, auth.ts, table.ts, menu.ts, account.ts, store.ts
└── utils/format.ts
```

---

## 병렬 개발 전략

```
Week 1-2: 4명 동시 개발 시작
+--------+  +--------+  +--------+  +--------+
| Unit 1 |  | Unit 2 |  | Unit 3 |  | Unit 4 |
| 인증   |  | 메뉴   |  | 주문   |  | UI     |
| 기반   |  | 백+FE  |  | 백+FE  |  | FE     |
+--------+  +--------+  +--------+  +--------+

Week 3: 통합
- Unit 4 UI → Unit 1/2/3 API 연동
- Unit 3 주문 → Unit 1 세션 연동
- 전체 E2E 테스트
```

### 독립 개발을 위한 약속

| 항목 | 약속 |
|---|---|
| API 계약 | OpenAPI 스펙을 먼저 정의하고 각자 개발 |
| 인터페이스 | Unit 1의 SessionService 인터페이스를 먼저 공유 |
| Mock | Unit 4는 API Mock으로 UI 개발 가능 |
| DB | Unit 1이 마이그레이션 기반 구조 먼저 세팅, 각 Unit이 자기 모델 추가 |
| 브랜치 | unit/1-foundation, unit/2-menu, unit/3-order, unit/4-ui |

---

## 의존성 매트릭스

| Unit | Unit 1 | Unit 2 | Unit 3 | Unit 4 |
|---|---|---|---|---|
| **Unit 1** | — | 없음 | 없음 | 없음 |
| **Unit 2** | DB 구조 | — | 없음 | 없음 |
| **Unit 3** | SessionService 인터페이스 | 없음 | — | 없음 |
| **Unit 4** | API 스펙 | API 스펙 | API 스펙 | — |

**핵심**: Unit 1이 DB 기반 + API 스펙을 먼저 공유하면, 나머지 3명은 독립 개발 가능.

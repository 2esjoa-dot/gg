# 테이블오더 서비스 - Unit of Work 정의

## 분해 전략
- **방식**: 계층별 분해 (Layer-based decomposition)
- **근거**: 백엔드 API 완성 → 프론트엔드 개발 순서가 의존성 방향과 일치
- **총 Unit 수**: 3개

---

## Unit 1: Backend API

| 항목 | 내용 |
|---|---|
| **이름** | table-order-backend |
| **기술** | FastAPI + SQLAlchemy + PostgreSQL |
| **배포 단위** | 단일 FastAPI 앱 (AWS EC2) |
| **범위** | 전체 백엔드 로직 (인증, 매장, 테이블, 세션, 메뉴, 주문, SSE, 파일) |

**포함 컴포넌트:**
- Domain Models (8개): Store, Table, TableSession, Category, MenuItem, Order, OrderItem, User
- Repository Layer (7개): Store, Table, Session, Menu, Order, User, OrderHistory
- Service Layer (8개): Auth, Store, Table, Session, Menu, Order, SSE, File
- Router Layer (3개): customer, admin, hq
- Infrastructure: AuthMiddleware, DB Config, CORS, ExceptionHandler, FileStorage
- Database Migrations (Alembic)

**디렉토리 구조:**
```
backend/
├── app/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── config.py               # 설정 (환경변수)
│   ├── database.py             # SQLAlchemy 엔진/세션
│   ├── models/                 # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── store.py
│   │   ├── table.py
│   │   ├── session.py
│   │   ├── category.py
│   │   ├── menu_item.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── user.py
│   ├── schemas/                # Pydantic DTO
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── store.py
│   │   ├── table.py
│   │   ├── menu.py
│   │   ├── order.py
│   │   └── session.py
│   ├── repositories/           # 데이터 접근 계층
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── store_repository.py
│   │   ├── table_repository.py
│   │   ├── session_repository.py
│   │   ├── menu_repository.py
│   │   ├── order_repository.py
│   │   └── user_repository.py
│   ├── services/               # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── store_service.py
│   │   ├── table_service.py
│   │   ├── session_service.py
│   │   ├── menu_service.py
│   │   ├── order_service.py
│   │   ├── sse_service.py
│   │   └── file_service.py
│   ├── routers/                # API 엔드포인트
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── admin.py
│   │   └── hq.py
│   ├── middleware/             # 미들웨어
│   │   ├── __init__.py
│   │   └── auth.py
│   └── utils/                  # 유틸리티
│       ├── __init__.py
│       ├── security.py         # bcrypt, JWT
│       └── exceptions.py       # 커스텀 예외
├── migrations/                 # Alembic 마이그레이션
│   └── versions/
├── tests/                      # 테스트
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── uploads/                    # 이미지 업로드 디렉토리
├── alembic.ini
├── requirements.txt
└── .env.example
```

---

## Unit 2: Customer Frontend

| 항목 | 내용 |
|---|---|
| **이름** | table-order-customer |
| **기술** | React + TypeScript + Vite |
| **배포 단위** | 정적 빌드 (AWS S3 + CloudFront 또는 EC2 Nginx) |
| **범위** | 고객용 태블릿 웹앱 (메뉴 조회, 장바구니, 주문) |

**포함 모듈:**
- AuthModule: 자동 로그인, 초기 설정
- MenuModule: 카테고리별 메뉴, 메뉴 상세
- CartModule: 장바구니 관리, 로컬 스토리지
- OrderModule: 주문 생성, 주문 내역, 폴링

**디렉토리 구조:**
```
frontend-customer/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── api/                    # API 클라이언트
│   │   ├── client.ts
│   │   ├── auth.ts
│   │   ├── menu.ts
│   │   └── order.ts
│   ├── components/             # 공통 UI 컴포넌트
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Loading.tsx
│   │   └── ErrorMessage.tsx
│   ├── pages/                  # 페이지 컴포넌트
│   │   ├── MenuPage.tsx
│   │   ├── CartPage.tsx
│   │   ├── OrderConfirmPage.tsx
│   │   ├── OrderHistoryPage.tsx
│   │   └── SetupPage.tsx
│   ├── hooks/                  # 커스텀 훅
│   │   ├── useCart.ts
│   │   ├── useAuth.ts
│   │   ├── usePolling.ts
│   │   └── useMenu.ts
│   ├── store/                  # 상태 관리
│   │   ├── cartStore.ts
│   │   └── authStore.ts
│   ├── types/                  # TypeScript 타입
│   │   └── index.ts
│   └── utils/                  # 유틸리티
│       ├── localStorage.ts
│       └── format.ts
├── public/
├── tests/
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## Unit 3: Admin Frontend

| 항목 | 내용 |
|---|---|
| **이름** | table-order-admin |
| **기술** | React + TypeScript + Vite |
| **배포 단위** | 정적 빌드 (AWS S3 + CloudFront 또는 EC2 Nginx) |
| **범위** | 관리자/본사 웹앱 (주문 모니터링, 테이블/메뉴/계정/매장 관리) |

**포함 모듈:**
- AuthModule: 관리자 로그인, JWT 세션
- DashboardModule: 실시간 주문 모니터링 (SSE), 테이블 그리드
- TableModule: 테이블 설정, 이용 완료, 과거 내역
- MenuManageModule: 메뉴 CRUD, 순서 조정
- AccountModule: 관리자 계정 등록
- HQModule: 매장 등록/조회

**디렉토리 구조:**
```
frontend-admin/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── api/                    # API 클라이언트
│   │   ├── client.ts
│   │   ├── auth.ts
│   │   ├── order.ts
│   │   ├── table.ts
│   │   ├── menu.ts
│   │   ├── account.ts
│   │   └── store.ts
│   ├── components/             # 공통 UI 컴포넌트
│   │   ├── Button.tsx
│   │   ├── Modal.tsx
│   │   ├── Table.tsx
│   │   ├── Card.tsx
│   │   └── Loading.tsx
│   ├── pages/                  # 페이지 컴포넌트
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── TableManagePage.tsx
│   │   ├── MenuManagePage.tsx
│   │   ├── AccountPage.tsx
│   │   └── HQStorePage.tsx
│   ├── hooks/                  # 커스텀 훅
│   │   ├── useSSE.ts
│   │   ├── useAuth.ts
│   │   ├── useOrders.ts
│   │   └── useTables.ts
│   ├── store/                  # 상태 관리
│   │   ├── authStore.ts
│   │   └── orderStore.ts
│   ├── types/                  # TypeScript 타입
│   │   └── index.ts
│   └── utils/                  # 유틸리티
│       ├── format.ts
│       └── sse.ts
├── public/
├── tests/
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## 개발 순서

```
Unit 1 (Backend) → Unit 2 (Customer) → Unit 3 (Admin)
                         ↑                    ↑
                    API 의존              API + SSE 의존
```

1. **Unit 1 먼저**: 모든 API 엔드포인트 + DB 스키마 완성
2. **Unit 2 다음**: 고객용 앱 (상대적으로 단순, 폴링만 사용)
3. **Unit 3 마지막**: 관리자 앱 (SSE 연동, 복잡한 대시보드)

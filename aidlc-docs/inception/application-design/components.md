# 테이블오더 서비스 - 컴포넌트 정의

## 시스템 구성도

```
+--------------------------------------------------+
|                   Client Layer                    |
|  +---------------------+ +---------------------+ |
|  | Customer Web App    | | Admin Web App       | |
|  | (React+TS, Tablet)  | | (React+TS, PC)      | |
|  +---------------------+ +---------------------+ |
+--------------------------------------------------+
                      |  REST API / SSE
+--------------------------------------------------+
|                Backend API (FastAPI)              |
|  +----------+ +----------+ +----------+         |
|  | Customer | | Admin    | | HQ       |         |
|  | Router   | | Router   | | Router   |         |
|  +----------+ +----------+ +----------+         |
|  +------------------------------------------+   |
|  |           Service Layer                   |   |
|  +------------------------------------------+   |
|  +------------------------------------------+   |
|  |         Repository Layer (SQLAlchemy)     |   |
|  +------------------------------------------+   |
+--------------------------------------------------+
                      |
+--------------------------------------------------+
|              Data Layer (PostgreSQL)              |
+--------------------------------------------------+
```

---

## 1. 프론트엔드 컴포넌트

### 1.1 Customer Web App (고객용)
| 항목 | 내용 |
|---|---|
| **기술** | React + TypeScript |
| **대상** | 매장 내 고정 태블릿 |
| **책임** | 메뉴 조회, 장바구니 관리, 주문 생성, 주문 내역 조회 |
| **특징** | 터치 최적화, 자동 로그인, 로컬 스토리지 장바구니, 30초 폴링 |

**주요 페이지/모듈:**
- `AuthModule` — 자동 로그인, 초기 설정
- `MenuModule` — 카테고리별 메뉴 조회, 메뉴 상세
- `CartModule` — 장바구니 관리, 로컬 스토리지 동기화
- `OrderModule` — 주문 생성, 주문 확인, 주문 내역

### 1.2 Admin Web App (관리자용)
| 항목 | 내용 |
|---|---|
| **기술** | React + TypeScript |
| **대상** | 매장 관리자 PC/태블릿, 본사 관리자 PC |
| **책임** | 로그인, 주문 모니터링, 테이블 관리, 메뉴 관리, 계정 관리, 매장 관리 |
| **특징** | SSE 실시간 업데이트, 그리드 대시보드, 역할 기반 UI 분기 |

**주요 페이지/모듈:**
- `AuthModule` — 관리자 로그인, JWT 세션
- `DashboardModule` — 실시간 주문 모니터링 (SSE), 테이블 그리드
- `TableModule` — 테이블 설정, 이용 완료, 과거 내역
- `MenuManageModule` — 메뉴 CRUD, 순서 조정
- `AccountModule` — 관리자 계정 등록
- `HQModule` — 매장 등록/조회 (본사 관리자 전용)

---

## 2. 백엔드 컴포넌트

### 2.1 API Layer (Routers)

| Router | 경로 접두사 | 책임 |
|---|---|---|
| `customer_router` | `/api/customer/` | 고객 인증, 메뉴 조회, 주문 생성/조회 |
| `admin_router` | `/api/admin/` | 관리자 인증, 주문 모니터링, 테이블/메뉴/계정 관리 |
| `hq_router` | `/api/hq/` | 본사 인증, 매장 등록/조회 |

### 2.2 Service Layer

| Service | 책임 |
|---|---|
| `AuthService` | 인증/인가 처리 (JWT 발급, 검증, 역할 확인) |
| `StoreService` | 매장 등록, 조회, 관리 |
| `TableService` | 테이블 등록, 세션 관리, 이용 완료 처리 |
| `MenuService` | 메뉴 CRUD, 카테고리 관리, 순서 조정 |
| `OrderService` | 주문 생성, 상태 변경, 조회, 삭제 |
| `SessionService` | 테이블 세션 라이프사이클 (생성, 유효성, 종료) |
| `SSEService` | Server-Sent Events 연결 관리, 이벤트 브로드캐스트 |
| `FileService` | 이미지 파일 업로드/조회 |

### 2.3 Repository Layer

| Repository | 책임 |
|---|---|
| `StoreRepository` | 매장 데이터 CRUD |
| `TableRepository` | 테이블 데이터 CRUD |
| `MenuRepository` | 메뉴/카테고리 데이터 CRUD |
| `OrderRepository` | 주문/주문항목 데이터 CRUD |
| `SessionRepository` | 세션 데이터 CRUD |
| `UserRepository` | 관리자 계정 데이터 CRUD |
| `OrderHistoryRepository` | 과거 주문 이력 조회 |

### 2.4 Domain Models (SQLAlchemy)

| Model | 설명 |
|---|---|
| `Store` | 매장 정보 |
| `Table` | 테이블 정보 (매장 소속) |
| `TableSession` | 테이블 세션 (시작/종료 시각, 상태) |
| `Category` | 메뉴 카테고리 |
| `MenuItem` | 메뉴 항목 |
| `Order` | 주문 (세션 소속) |
| `OrderItem` | 주문 항목 (메뉴-수량) |
| `User` | 관리자 계정 (매장 소속, 역할) |

### 2.5 Infrastructure/Cross-cutting

| 컴포넌트 | 책임 |
|---|---|
| `AuthMiddleware` | JWT 검증, 역할 기반 접근 제어 |
| `DatabaseConfig` | SQLAlchemy async 엔진, 세션 팩토리 |
| `CORSConfig` | CORS 설정 |
| `ExceptionHandler` | 전역 예외 처리, 에러 응답 표준화 |
| `FileStorage` | 로컬 파일 시스템 이미지 저장/조회 |

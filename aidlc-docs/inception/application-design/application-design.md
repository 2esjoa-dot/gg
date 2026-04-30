# 테이블오더 서비스 - Application Design 통합 문서

## 아키텍처 결정 사항

| 결정 항목 | 선택 | 근거 |
|---|---|---|
| 백엔드 구조 | 단일 FastAPI + 역할 기반 미들웨어 | MVP 배포 단순화, 라우터로 도메인 분리 |
| 프론트엔드 구조 | 별도 프로젝트 (고객/관리자) | UX 패러다임 상이, 독립 배포, 번들 분리 |
| 데이터 접근 | SQLAlchemy ORM (async) | 성숙한 생태계, 관계 매핑, Alembic 마이그레이션 |

---

## 시스템 아키텍처

```
+-------------------+     +-------------------+
| Customer Web App  |     | Admin Web App     |
| (React+TS)        |     | (React+TS)        |
| - Tablet 전용     |     | - PC/Tablet       |
| - 터치 최적화     |     | - SSE 실시간      |
+-------------------+     +-------------------+
         |                         |
         | REST + Polling(30s)     | REST + SSE
         |                         |
+--------------------------------------------------+
|            FastAPI Backend (단일 앱)              |
|                                                  |
|  [AuthMiddleware] - JWT 검증, 역할 기반 접근제어 |
|                                                  |
|  /api/customer/*  /api/admin/*  /api/hq/*        |
|                                                  |
|  +--------------------------------------------+  |
|  |          Service Layer                     |  |
|  | Auth | Store | Table | Session |           |  |
|  | Menu | Order | SSE   | File    |           |  |
|  +--------------------------------------------+  |
|                                                  |
|  +--------------------------------------------+  |
|  |        Repository Layer (SQLAlchemy)       |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
                       |
              +------------------+
              |   PostgreSQL     |
              |   (AWS RDS)     |
              +------------------+
```

---

## 컴포넌트 요약

- **프론트엔드**: 2개 독립 React+TS 앱 (고객용 4모듈, 관리자용 6모듈)
- **백엔드 Router**: 3개 (customer, admin, hq)
- **Service**: 8개 (Auth, Store, Table, Session, Menu, Order, SSE, File)
- **Repository**: 7개 (Store, Table, Session, Menu, Order, User, OrderHistory)
- **Domain Model**: 8개 (Store, Table, TableSession, Category, MenuItem, Order, OrderItem, User)
- **Infrastructure**: 5개 (AuthMiddleware, DB Config, CORS, ExceptionHandler, FileStorage)

---

## 상세 문서 참조

- 컴포넌트 정의: [components.md](./components.md)
- 메서드 시그니처: [component-methods.md](./component-methods.md)
- 서비스 설계: [services.md](./services.md)
- 의존성 관계: [component-dependency.md](./component-dependency.md)

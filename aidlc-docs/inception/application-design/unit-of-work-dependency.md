# 테이블오더 서비스 - Unit of Work 의존성

## 의존성 매트릭스

| Unit | Backend API | Customer Frontend | Admin Frontend |
|---|---|---|---|
| **Backend API** | — | 없음 | 없음 |
| **Customer Frontend** | REST API 의존 | — | 없음 |
| **Admin Frontend** | REST API + SSE 의존 | 없음 | — |

---

## 의존성 방향

```
+-------------------+
| Unit 1: Backend   |  ← 의존 없음 (독립 개발 가능)
+-------------------+
       ^       ^
       |       |
  REST |       | REST + SSE
       |       |
+----------+ +----------+
| Unit 2:  | | Unit 3:  |
| Customer | | Admin    |
+----------+ +----------+
```

---

## 개발 순서 및 근거

| 순서 | Unit | 근거 |
|---|---|---|
| 1 | Backend API | 프론트엔드가 호출할 API가 먼저 존재해야 함 |
| 2 | Customer Frontend | 관리자 앱보다 단순 (폴링만, SSE 없음) |
| 3 | Admin Frontend | SSE 연동 + 복잡한 대시보드, 백엔드 완성 후 개발 |

---

## 통합 포인트

| 통합 포인트 | Unit 1 ↔ Unit 2 | Unit 1 ↔ Unit 3 |
|---|---|---|
| 인증 | JWT 토큰 발급/검증 | JWT 토큰 발급/검증 |
| 메뉴 조회 | GET /api/customer/menu | GET /api/admin/menu |
| 주문 생성 | POST /api/customer/orders | — |
| 주문 조회 | GET /api/customer/orders/session | GET /api/admin/orders/table |
| 실시간 | — (폴링) | SSE /api/admin/orders/stream |
| 테이블 관리 | — | POST/GET /api/admin/tables |
| 메뉴 관리 | — | CRUD /api/admin/menu |
| 매장 관리 | — | CRUD /api/hq/stores |

---

## 통합 테스트 전략

| 테스트 단계 | 범위 | 시점 |
|---|---|---|
| Unit 1 단독 | API 엔드포인트 + DB | Unit 1 완료 후 |
| Unit 1 + Unit 2 | 고객 주문 플로우 E2E | Unit 2 완료 후 |
| Unit 1 + Unit 3 | 관리자 모니터링 E2E | Unit 3 완료 후 |
| 전체 통합 | 고객 주문 → 관리자 수신 → 상태 변경 → 고객 확인 | 모든 Unit 완료 후 |

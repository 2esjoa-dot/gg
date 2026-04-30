# 테이블오더 서비스 - 컴포넌트 의존성

## 1. 의존성 매트릭스

### Service → Repository 의존성

| Service | StoreRepo | TableRepo | SessionRepo | MenuRepo | OrderRepo | UserRepo |
|---|---|---|---|---|---|---|
| AuthService | ✓ | | | | | ✓ |
| StoreService | ✓ | | | | | |
| TableService | | ✓ | | | | |
| SessionService | | | ✓ | | ✓ | |
| MenuService | | | | ✓ | | |
| OrderService | | | | | ✓ | |
| SSEService | | | | | | |
| FileService | | | | | | |

### Service → Service 의존성

| Service | AuthSvc | StoreSvc | TableSvc | SessionSvc | MenuSvc | OrderSvc | SSESvc | FileSvc |
|---|---|---|---|---|---|---|---|---|
| AuthService | | | | | | | | |
| StoreService | | | | | | | | |
| TableService | | | | ✓ | | ✓ | | |
| SessionService | | | | | | | | |
| MenuService | | | | | | | | ✓ |
| OrderService | | | | ✓ | | | ✓ | |
| SSEService | | | | | | | | |
| FileService | | | | | | | | |

---

## 2. 계층 의존성 규칙

```
Router → Service → Repository → Database
  |         |
  |         +→ Service (동일 레벨 호출 허용)
  |
  +→ Middleware (인증/인가)
```

**규칙:**
- Router는 Service만 호출 (Repository 직접 접근 금지)
- Service는 Repository와 다른 Service 호출 가능
- Repository는 다른 Repository 호출 금지 (Service에서 조합)
- 순환 의존성 금지

---

## 3. 데이터 흐름

### 고객 주문 플로우
```
[Customer App] --POST /orders--> [CustomerRouter]
                                      |
                                      v
                                [OrderService]
                                   /     \
                                  v       v
                          [SessionService] [SSEService]
                               |               |
                               v               v
                        [SessionRepo]    [Admin App SSE]
                               |
                               v
                         [OrderRepo]
```

### 관리자 실시간 모니터링
```
[Admin App] --GET /orders/stream--> [AdminRouter]
                                         |
                                         v
                                    [SSEService]
                                         |
                                    (subscribe)
                                         |
                    [OrderService] --publish--> [SSEService] --event--> [Admin App]
```

### 고객 주문 상태 폴링
```
[Customer App] --GET /orders/session/{id}--> [CustomerRouter]
                                                  |
                                                  v
                                            [OrderService]
                                                  |
                                                  v
                                            [OrderRepo]
                                                  |
                                                  v
                                            [Response: orders with status]
```

---

## 4. 통신 패턴

| 통신 | 방식 | 방향 | 설명 |
|---|---|---|---|
| 고객 → 서버 | REST (HTTP) | 요청-응답 | 메뉴 조회, 주문 생성 |
| 고객 ← 서버 | REST Polling | 30초 간격 | 주문 상태 업데이트 |
| 관리자 → 서버 | REST (HTTP) | 요청-응답 | 상태 변경, 메뉴 관리 |
| 관리자 ← 서버 | SSE | 서버→클라이언트 | 실시간 주문 알림 |
| 본사 → 서버 | REST (HTTP) | 요청-응답 | 매장 관리 |

---

## 5. 프론트엔드 → 백엔드 의존성

| Frontend Module | Backend Endpoint | 통신 방식 |
|---|---|---|
| Customer.AuthModule | POST /api/customer/auth/login | REST |
| Customer.MenuModule | GET /api/customer/menu/{store_id} | REST |
| Customer.CartModule | (로컬 전용) | — |
| Customer.OrderModule | POST /api/customer/orders | REST |
| Customer.OrderModule | GET /api/customer/orders/session/{id} | REST (30s polling) |
| Admin.AuthModule | POST /api/admin/auth/login | REST |
| Admin.DashboardModule | GET /api/admin/orders/stream | SSE |
| Admin.DashboardModule | PATCH /api/admin/orders/{id}/status | REST |
| Admin.TableModule | POST /api/admin/tables/{id}/complete | REST |
| Admin.TableModule | GET /api/admin/tables/{id}/history | REST |
| Admin.MenuManageModule | POST/PUT/DELETE /api/admin/menu/* | REST |
| Admin.AccountModule | POST /api/admin/auth/register | REST |
| Admin.HQModule | POST/GET /api/hq/stores | REST |

# 테이블오더 서비스 - 컴포넌트 메서드 정의

## 1. Service Layer Methods

### AuthService
| Method | Input | Output | 설명 |
|---|---|---|---|
| `login_admin(store_code, username, password)` | str, str, str | TokenResponse | 관리자 로그인, JWT 발급 |
| `login_tablet(store_code, table_number, password)` | str, int, str | TokenResponse | 태블릿 자동 로그인 |
| `verify_token(token)` | str | TokenPayload | JWT 검증, 페이로드 반환 |
| `check_login_attempts(store_code, username)` | str, str | bool | 로그인 시도 횟수 확인 (5회 초과 시 차단) |
| `register_admin(store_code, username, password)` | str, str, str | User | 관리자 계정 등록 |

### StoreService
| Method | Input | Output | 설명 |
|---|---|---|---|
| `create_store(name, code, address)` | str, str, str | Store | 매장 등록 |
| `get_store(store_code)` | str | Store | 매장 조회 |
| `list_stores()` | — | list[Store] | 전체 매장 목록 |

### TableService
| Method | Input | Output | 설명 |
|---|---|---|---|
| `create_table(store_id, table_number, password)` | int, int, str | Table | 테이블 등록 |
| `get_tables(store_id)` | int | list[Table] | 매장 테이블 목록 |
| `get_table_status(store_id, table_id)` | int, int | TableStatus | 테이블 현재 상태 (세션, 주문액) |

### SessionService
| Method | Input | Output | 설명 |
|---|---|---|---|
| `get_or_create_session(store_id, table_id)` | int, int | TableSession | 활성 세션 반환 또는 새 세션 생성 |
| `end_session(session_id)` | int | TableSession | 세션 종료 (이용 완료) |
| `get_active_session(store_id, table_id)` | int, int | TableSession or None | 현재 활성 세션 조회 |
| `is_session_valid(session_id)` | int | bool | 세션 유효성 확인 (16시간) |

### MenuService
| Method | Input | Output | 설명 |
|---|---|---|---|
| `create_menu_item(store_id, data)` | int, MenuCreateDTO | MenuItem | 메뉴 등록 |
| `update_menu_item(item_id, data)` | int, MenuUpdateDTO | MenuItem | 메뉴 수정 |
| `delete_menu_item(item_id)` | int | None | 메뉴 삭제 |
| `get_menu_by_category(store_id)` | int | dict[Category, list[MenuItem]] | 카테고리별 메뉴 조회 |
| `update_menu_order(store_id, order_data)` | int, list[OrderUpdate] | None | 메뉴 순서 변경 |
| `upload_image(file)` | UploadFile | str | 이미지 업로드, URL 반환 |

### OrderService
| Method | Input | Output | 설명 |
|---|---|---|---|
| `create_order(store_id, table_id, session_id, items)` | int, int, int, list[OrderItemDTO] | Order | 주문 생성 |
| `get_orders_by_session(session_id)` | int | list[Order] | 세션별 주문 조회 |
| `get_orders_by_table(store_id, table_id)` | int, int | list[Order] | 테이블 현재 주문 조회 |
| `update_order_status(order_id, status)` | int, OrderStatus | Order | 주문 상태 변경 |
| `delete_order(order_id)` | int | None | 주문 삭제 |
| `get_order_history(store_id, table_id, date_from, date_to)` | int, int, date, date | list[Order] | 과거 주문 내역 조회 |
| `get_table_total(store_id, table_id)` | int, int | Decimal | 테이블 총 주문액 계산 |

### SSEService
| Method | Input | Output | 설명 |
|---|---|---|---|
| `subscribe(store_id)` | int | AsyncGenerator[Event] | SSE 구독 (매장별) |
| `publish_order_event(store_id, event)` | int, OrderEvent | None | 주문 이벤트 발행 |
| `publish_status_event(store_id, event)` | int, StatusEvent | None | 상태 변경 이벤트 발행 |

### FileService
| Method | Input | Output | 설명 |
|---|---|---|---|
| `save_file(file, directory)` | UploadFile, str | str | 파일 저장, 경로 반환 |
| `get_file_url(file_path)` | str | str | 파일 접근 URL 생성 |
| `delete_file(file_path)` | str | None | 파일 삭제 |

---

## 2. Repository Layer Methods

각 Repository는 기본 CRUD 패턴을 따릅니다:
- `create(data) → Model`
- `get_by_id(id) → Model | None`
- `get_all(filters) → list[Model]`
- `update(id, data) → Model`
- `delete(id) → None`

추가 특화 메서드:

| Repository | Method | 설명 |
|---|---|---|
| `OrderRepository` | `get_by_session(session_id)` | 세션별 주문 조회 |
| `OrderRepository` | `get_by_table_active(store_id, table_id)` | 테이블 활성 주문 |
| `OrderRepository` | `get_history(store_id, table_id, date_range)` | 과거 이력 조회 |
| `SessionRepository` | `get_active(store_id, table_id)` | 활성 세션 조회 |
| `SessionRepository` | `close_session(session_id)` | 세션 종료 처리 |
| `MenuRepository` | `get_by_store_categorized(store_id)` | 카테고리별 메뉴 |
| `MenuRepository` | `update_display_order(items)` | 순서 일괄 업데이트 |
| `UserRepository` | `get_by_credentials(store_code, username)` | 로그인 조회 |

---

## 3. API Endpoints (Router Level)

### Customer Router (`/api/customer/`)
| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/auth/login` | 태블릿 로그인 |
| GET | `/menu/{store_id}` | 메뉴 조회 |
| POST | `/orders` | 주문 생성 |
| GET | `/orders/session/{session_id}` | 세션 주문 조회 |

### Admin Router (`/api/admin/`)
| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/auth/login` | 관리자 로그인 |
| POST | `/auth/register` | 관리자 계정 등록 |
| GET | `/orders/stream` | SSE 주문 스트림 |
| GET | `/orders/table/{table_id}` | 테이블 주문 조회 |
| PATCH | `/orders/{order_id}/status` | 주문 상태 변경 |
| DELETE | `/orders/{order_id}` | 주문 삭제 |
| POST | `/tables` | 테이블 등록 |
| GET | `/tables` | 테이블 목록 |
| POST | `/tables/{table_id}/complete` | 이용 완료 |
| GET | `/tables/{table_id}/history` | 과거 내역 |
| GET | `/menu` | 메뉴 목록 |
| POST | `/menu` | 메뉴 등록 |
| PUT | `/menu/{item_id}` | 메뉴 수정 |
| DELETE | `/menu/{item_id}` | 메뉴 삭제 |
| PATCH | `/menu/order` | 메뉴 순서 변경 |
| POST | `/menu/upload-image` | 이미지 업로드 |

### HQ Router (`/api/hq/`)
| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/auth/login` | 본사 로그인 |
| POST | `/stores` | 매장 등록 |
| GET | `/stores` | 매장 목록 |
| GET | `/stores/{store_id}` | 매장 상세 |

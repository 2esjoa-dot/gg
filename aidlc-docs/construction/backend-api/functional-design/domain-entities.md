# Domain Entities - Backend API

## ER 다이어그램

```
+----------+       +----------+       +----------------+
|  Store   |1----N |  Table   |1----N | TableSession   |
+----------+       +----------+       +----------------+
|1                                    |1
|N                                    |N
+----------+       +----------+       +----------+
|   User   |       | Category |1----N | Order    |
+----------+       +----------+       +----------+
                                      |1
                   +----------+       |N
                   | MenuItem |       +------------+
                   +----------+       | OrderItem  |
                        1             +------------+
                        |                   N|
                        +-------------------+
```

---

## 엔티티 정의

### Store (매장)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 매장 고유 ID |
| name | String(100) | NOT NULL | 매장명 |
| code | String(50) | UNIQUE, NOT NULL | 매장 식별자 (로그인용) |
| address | String(200) | NULL | 매장 주소 |
| is_active | Boolean | DEFAULT true | 활성 상태 |
| created_at | DateTime | NOT NULL | 등록일시 |
| updated_at | DateTime | NOT NULL | 수정일시 |

---

### User (관리자 계정)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 계정 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| username | String(50) | NOT NULL | 사용자명 |
| password_hash | String(255) | NOT NULL | bcrypt 해시 |
| role | Enum | NOT NULL | 역할 (store_admin, hq_admin) |
| is_active | Boolean | DEFAULT true | 활성 상태 |
| login_attempts | Integer | DEFAULT 0 | 연속 로그인 실패 횟수 |
| locked_until | DateTime | NULL | 잠금 해제 시각 |
| created_at | DateTime | NOT NULL | 등록일시 |

**UNIQUE 제약**: (store_id, username)

---

### Table (테이블)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 테이블 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| table_number | Integer | NOT NULL | 테이블 번호 |
| password_hash | String(255) | NOT NULL | 태블릿 비밀번호 해시 |
| is_active | Boolean | DEFAULT true | 활성 상태 |
| created_at | DateTime | NOT NULL | 등록일시 |

**UNIQUE 제약**: (store_id, table_number)

---

### TableSession (테이블 세션)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 세션 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| table_id | Integer | FK(Table), NOT NULL | 소속 테이블 |
| status | Enum | NOT NULL | 상태 (active, completed) |
| started_at | DateTime | NOT NULL | 세션 시작 시각 |
| completed_at | DateTime | NULL | 세션 종료 시각 |
| expires_at | DateTime | NOT NULL | 만료 시각 (시작+16시간) |

**INDEX**: (store_id, table_id, status) — 활성 세션 빠른 조회

---

### Category (메뉴 카테고리)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 카테고리 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| name | String(50) | NOT NULL | 카테고리명 |
| display_order | Integer | DEFAULT 0 | 표시 순서 |
| created_at | DateTime | NOT NULL | 등록일시 |

**UNIQUE 제약**: (store_id, name)

---

### MenuItem (메뉴 항목)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 메뉴 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| category_id | Integer | FK(Category), NOT NULL | 소속 카테고리 |
| name | String(100) | NOT NULL | 메뉴명 |
| price | Decimal(10,0) | NOT NULL, CHECK(>0) | 가격 (원) |
| description | Text | NULL | 메뉴 설명 |
| image_url | String(500) | NULL | 이미지 경로 |
| display_order | Integer | DEFAULT 0 | 표시 순서 |
| is_active | Boolean | DEFAULT true | 노출 여부 |
| created_at | DateTime | NOT NULL | 등록일시 |
| updated_at | DateTime | NOT NULL | 수정일시 |

---

### Order (주문)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 주문 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| table_id | Integer | FK(Table), NOT NULL | 소속 테이블 |
| session_id | Integer | FK(TableSession), NOT NULL | 소속 세션 |
| order_number | String(20) | UNIQUE, NOT NULL | 주문 번호 (표시용) |
| status | Enum | NOT NULL, DEFAULT 'pending' | 상태 (pending/preparing/completed) |
| total_amount | Decimal(10,0) | NOT NULL | 총 주문 금액 |
| created_at | DateTime | NOT NULL | 주문 시각 |
| updated_at | DateTime | NOT NULL | 수정 시각 |

**INDEX**: (session_id, created_at) — 세션별 주문 시간순 조회
**INDEX**: (store_id, table_id, status) — 테이블별 활성 주문 조회

---

### OrderItem (주문 항목)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 항목 고유 ID |
| order_id | Integer | FK(Order), NOT NULL | 소속 주문 |
| menu_item_id | Integer | FK(MenuItem), NOT NULL | 메뉴 참조 |
| menu_name | String(100) | NOT NULL | 주문 시점 메뉴명 (스냅샷) |
| quantity | Integer | NOT NULL, CHECK(>0) | 수량 |
| unit_price | Decimal(10,0) | NOT NULL | 주문 시점 단가 (스냅샷) |
| subtotal | Decimal(10,0) | NOT NULL | 소계 (수량 x 단가) |

---

## 엔티티 관계 요약

| 관계 | 카디널리티 | 설명 |
|---|---|---|
| Store → User | 1:N | 매장에 여러 관리자 |
| Store → Table | 1:N | 매장에 여러 테이블 |
| Store → Category | 1:N | 매장에 여러 카테고리 |
| Store → MenuItem | 1:N | 매장에 여러 메뉴 |
| Category → MenuItem | 1:N | 카테고리에 여러 메뉴 |
| Table → TableSession | 1:N | 테이블에 여러 세션 (시간순) |
| TableSession → Order | 1:N | 세션에 여러 주문 |
| Order → OrderItem | 1:N | 주문에 여러 항목 |
| MenuItem → OrderItem | 1:N | 메뉴가 여러 주문항목에 참조 |

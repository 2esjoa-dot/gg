# Domain Entities - Unit 2: Menu

> 본 문서는 `aidlc-docs/construction/backend-api/functional-design/domain-entities.md`의 메뉴 관련 엔티티를 Unit 2 범위로 추출한 것입니다.

## Unit 2 담당 엔티티

### Category (메뉴 카테고리)
| 필드 | 타입 | 제약조건 | 설명 |
|---|---|---|---|
| id | Integer | PK, Auto | 카테고리 고유 ID |
| store_id | Integer | FK(Store), NOT NULL | 소속 매장 |
| name | String(50) | NOT NULL | 카테고리명 |
| display_order | Integer | DEFAULT 0 | 표시 순서 |
| created_at | DateTime | NOT NULL | 등록일시 |

**UNIQUE 제약**: (store_id, name)

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

## 관계
- Store → Category (1:N)
- Store → MenuItem (1:N)
- Category → MenuItem (1:N)
- MenuItem → OrderItem (1:N) — Unit 3 연동 포인트

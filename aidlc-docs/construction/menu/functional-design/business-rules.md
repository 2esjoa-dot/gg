# Business Rules - Unit 2: Menu

## 1. 유효성 검증 규칙

### Category
| 필드 | 규칙 |
|---|---|
| name | 필수, 1~50자, 매장 내 UNIQUE |
| display_order | 선택, 기본값 0 |

### MenuItem
| 필드 | 규칙 |
|---|---|
| name | 필수, 1~100자 |
| price | 필수, 양의 정수 (원 단위, 소수점 없음) |
| description | 선택, 최대 1000자 |
| category_id | 필수, 해당 매장의 카테고리여야 함 |
| image_url | 선택, 유효한 파일 경로 |

## 2. 메뉴 삭제 규칙
- **Soft Delete**: MenuItem.is_active = false
- 기존 OrderItem의 menu_item_id 참조 유지 (스냅샷 데이터로 표시)
- 고객 메뉴 조회 시 is_active=true만 표시

## 3. 이미지 업로드 정책
| 항목 | 값 |
|---|---|
| 허용 형식 | JPEG, PNG, WebP |
| 최대 파일 크기 | 5MB |
| 저장 경로 | uploads/{store_id}/{filename} |
| 파일명 | UUID + 원본 확장자 |

## 4. 멀티테넌시 격리
- 모든 메뉴 데이터 접근은 store_id로 필터링
- JWT의 store_id와 리소스의 store_id 일치 필수

## 5. 접근 제어
| API | 허용 역할 |
|---|---|
| GET /api/customer/menu/* | tablet |
| GET/POST/PUT/DELETE /api/admin/menu/* | store_admin |

# Business Rules - Backend API

## 1. 유효성 검증 규칙

### 매장 (Store)
| 필드 | 규칙 |
|---|---|
| name | 필수, 1~100자 |
| code | 필수, 1~50자, 영문+숫자+하이픈만, UNIQUE |
| address | 선택, 최대 200자 |

### 관리자 계정 (User)
| 필드 | 규칙 |
|---|---|
| username | 필수, 3~50자, 영문+숫자+언더스코어 |
| password | 필수, 최소 4자 |
| role | 필수, enum(store_admin, hq_admin) |

### 테이블 (Table)
| 필드 | 규칙 |
|---|---|
| table_number | 필수, 양의 정수, 매장 내 UNIQUE |
| password | 필수, 최소 4자 |

### 메뉴 (MenuItem)
| 필드 | 규칙 |
|---|---|
| name | 필수, 1~100자 |
| price | 필수, 양의 정수 (원 단위, 소수점 없음) |
| description | 선택, 최대 1000자 |
| category_id | 필수, 해당 매장의 카테고리여야 함 |
| image_url | 선택, 유효한 파일 경로 |

### 주문 (Order)
| 필드 | 규칙 |
|---|---|
| items | 필수, 1개 이상 |
| items[].menu_item_id | 필수, 해당 매장의 활성 메뉴여야 함 |
| items[].quantity | 필수, 1 이상의 정수 |

---

## 2. 상태 전이 규칙

### 주문 상태 (OrderStatus)
```
pending → preparing → completed
```

| 현재 상태 | 허용 전이 | 금지 전이 |
|---|---|---|
| pending | preparing | completed, pending |
| preparing | completed | pending, preparing |
| completed | (없음) | 모든 변경 금지 |

### 세션 상태 (SessionStatus)
```
active → completed
```

| 현재 상태 | 허용 전이 | 트리거 |
|---|---|---|
| active | completed | 관리자 이용 완료 또는 16시간 만료 |
| completed | (없음) | 변경 불가 |

---

## 3. 접근 제어 규칙

### 역할별 API 접근

| API 그룹 | tablet | store_admin | hq_admin |
|---|---|---|---|
| /api/customer/* | ✅ | ❌ | ❌ |
| /api/admin/* | ❌ | ✅ | ❌ |
| /api/hq/* | ❌ | ❌ | ✅ |

### 멀티테넌시 격리 규칙
- **모든 데이터 접근은 store_id로 필터링**
- JWT의 store_id와 요청 대상 리소스의 store_id 일치 필수
- 불일치 시: 403 Forbidden
- 본사 관리자(hq_admin)는 모든 매장 접근 가능

### 인증 규칙
| 규칙 | 값 |
|---|---|
| 토큰 유효 기간 | 16시간 (57,600초) |
| 로그인 실패 허용 횟수 | 5회 |
| 계정 잠금 시간 | 15분 |
| 비밀번호 해싱 | bcrypt (cost factor: 12) |
| 토큰 알고리즘 | HS256 |

---

## 4. 데이터 무결성 규칙

### 주문 생성 시
- OrderItem의 menu_name, unit_price는 생성 시점의 MenuItem 값 스냅샷
- 이후 메뉴 가격 변경이 기존 주문에 영향 없음
- total_amount = SUM(각 OrderItem의 subtotal)

### 이용 완료 시
- 세션의 모든 주문은 그대로 유지 (삭제 아님)
- 세션 status만 completed로 변경
- 고객 앱에서 해당 세션 주문이 더 이상 표시되지 않음 (활성 세션 기준 조회)

### 메뉴 삭제 시
- 기존 OrderItem의 menu_item_id 참조는 유지 (스냅샷 데이터로 표시 가능)
- MenuItem.is_active = false로 soft delete 처리
- 고객 메뉴 조회 시 is_active=true만 표시

### 주문 삭제 시
- Order + OrderItem CASCADE 삭제 (hard delete)
- 해당 테이블의 총 주문액 재계산 필요

---

## 5. 비즈니스 정책 규칙

### 주문 번호 정책
- 형식: ORD-{YYYYMMDD}-{4자리 순번}
- 매장별 + 일별 독립 순번
- 하루 최대 9,999건

### 세션 정책
- 최대 유효 기간: 16시간
- 테이블당 동시 활성 세션: 최대 1개
- 만료된 세션은 다음 주문 시 자동 종료 + 새 세션 생성

### 이미지 업로드 정책
- 허용 형식: JPEG, PNG, WebP
- 최대 파일 크기: 5MB
- 저장 경로: uploads/{store_id}/{filename}
- 파일명: UUID + 원본 확장자

### 폴링 정책 (고객)
- 권장 간격: 30초
- 서버 측 rate limit 없음 (MVP)

### SSE 정책 (관리자)
- 매장별 독립 채널
- 연결 유지: keep-alive 15초 간격
- 재연결: 클라이언트 측 자동 재연결 (EventSource 기본 동작)

---

## 6. 에러 코드 정의

| 코드 | HTTP | 설명 |
|---|---|---|
| AUTH_INVALID | 401 | 인증 정보 불일치 |
| AUTH_LOCKED | 401 | 계정 잠금 상태 |
| AUTH_EXPIRED | 401 | 토큰 만료 |
| FORBIDDEN | 403 | 권한 없음 / 매장 불일치 |
| NOT_FOUND | 404 | 리소스 미발견 |
| DUPLICATE | 409 | 중복 데이터 (매장코드, 테이블번호, 사용자명) |
| VALIDATION | 422 | 유효성 검증 실패 |
| INVALID_STATUS | 400 | 허용되지 않는 상태 전이 |
| NO_ACTIVE_SESSION | 400 | 활성 세션 없음 (이용 완료 시) |
| SERVER_ERROR | 500 | 서버 내부 오류 |

# Business Logic Model - Backend API

## 1. 주문 생성 플로우

```
입력: store_id, table_id, items[{menu_item_id, quantity}]

1. 테이블 존재 확인 (store_id + table_id)
   → 없으면: 404 에러
2. 활성 세션 조회 (store_id + table_id + status=active)
   → 있으면: 기존 세션 사용
   → 없으면: 새 세션 생성 (expires_at = now + 16h)
3. 세션 유효성 확인 (expires_at > now)
   → 만료됨: 기존 세션 종료 + 새 세션 생성
4. 메뉴 항목 검증
   → 각 menu_item_id가 해당 store에 존재하는지
   → 각 메뉴가 is_active=true인지
   → quantity > 0인지
5. 주문 번호 생성 (형식: ORD-{YYYYMMDD}-{순번4자리})
6. 총 금액 계산 (각 항목의 price * quantity 합산)
7. Order 생성 (status=pending)
8. OrderItem 생성 (menu_name, unit_price 스냅샷 저장)
9. SSE 이벤트 발행 (store_id 채널로 new_order 이벤트)
10. 응답: Order (order_number, total_amount, created_at)
```

---

## 2. 세션 라이프사이클

### 세션 생성 (자동)
```
트리거: 첫 주문 생성 시 활성 세션 없음
1. TableSession 생성
   - status = active
   - started_at = now
   - expires_at = now + 16시간
2. 세션 ID를 주문에 연결
```

### 세션 종료 (이용 완료)
```
트리거: 관리자가 "이용 완료" 실행
입력: store_id, table_id

1. 활성 세션 조회
   → 없으면: 400 에러 ("활성 세션이 없습니다")
2. 세션 상태 변경: active → completed
3. completed_at = now
4. SSE 이벤트 발행 (table_completed 이벤트)
5. 응답: 성공
```

### 세션 만료 처리
```
트리거: 주문 생성 시 세션 유효성 확인
1. expires_at < now 이면 만료
2. 만료된 세션: status → completed, completed_at = expires_at
3. 새 세션 자동 생성
```

---

## 3. 인증/인가 로직

### 관리자 로그인
```
입력: store_code, username, password

1. 매장 조회 (store_code)
   → 없으면: 401 "인증 정보가 올바르지 않습니다"
2. 사용자 조회 (store_id + username)
   → 없으면: 401 (동일 메시지, 정보 노출 방지)
3. 잠금 확인 (locked_until > now)
   → 잠김: 401 "계정이 잠겨있습니다. {남은시간}분 후 재시도"
4. 비밀번호 검증 (bcrypt.verify)
   → 실패:
     - login_attempts += 1
     - login_attempts >= 5: locked_until = now + 15분
     - 401 "인증 정보가 올바르지 않습니다"
   → 성공:
     - login_attempts = 0
     - locked_until = NULL
5. JWT 토큰 발급
   - payload: {user_id, store_id, role, exp: now+16h}
   - 응답: {access_token, token_type: "bearer", expires_in: 57600}
```

### 태블릿 로그인
```
입력: store_code, table_number, password

1. 매장 조회 (store_code)
   → 없으면: 401
2. 테이블 조회 (store_id + table_number)
   → 없으면: 401
3. 비밀번호 검증 (bcrypt.verify)
   → 실패: 401
   → 성공: JWT 발급
     - payload: {table_id, store_id, role: "tablet", exp: now+16h}
```

### 역할 기반 접근 제어
```
미들웨어 처리:
1. Authorization 헤더에서 Bearer 토큰 추출
2. JWT 검증 (서명 + 만료)
3. 역할 확인:
   - /api/customer/* → role: "tablet"
   - /api/admin/* → role: "store_admin"
   - /api/hq/* → role: "hq_admin"
4. store_id 일치 확인 (멀티테넌시 격리)
```

---

## 4. 주문 상태 변경

```
입력: order_id, new_status
허용 전이: pending → preparing → completed

1. 주문 조회 (order_id)
   → 없으면: 404
2. 현재 상태 확인
   - pending → preparing: 허용
   - preparing → completed: 허용
   - completed → *: 거부 (400 "완료된 주문은 변경할 수 없습니다")
   - pending → completed: 거부 (400 "순서대로 변경해야 합니다")
3. 상태 업데이트
4. SSE 이벤트 발행 (order_status_changed)
5. 응답: 업데이트된 Order
```

---

## 5. 주문 삭제

```
입력: order_id

1. 주문 조회 (order_id)
   → 없으면: 404
2. 주문 삭제 (CASCADE: OrderItem도 삭제)
3. SSE 이벤트 발행 (order_deleted)
4. 응답: 성공
```

---

## 6. SSE 이벤트 관리

### 구독
```
입력: store_id (JWT에서 추출)

1. 매장별 구독자 목록에 연결 추가
2. AsyncGenerator로 이벤트 스트림 반환
3. 연결 끊김 시 구독자 목록에서 제거
```

### 이벤트 발행
```
이벤트 타입:
- new_order: {order_id, table_id, table_number, items, total_amount, created_at}
- order_status_changed: {order_id, table_id, old_status, new_status}
- order_deleted: {order_id, table_id}
- table_completed: {table_id, table_number}

발행 로직:
1. 해당 store_id의 모든 구독자에게 이벤트 전송
2. 전송 실패한 구독자는 목록에서 제거 (연결 끊김)
```

---

## 7. 메뉴 관리 로직

### 메뉴 등록
```
입력: store_id, name, price, description, category_id, image_url

1. 카테고리 존재 확인 (store_id + category_id)
   → 없으면: 404
2. 유효성 검증
   - name: 필수, 1~100자
   - price: 필수, > 0
   - category_id: 필수
3. display_order = 해당 카테고리 내 최대값 + 1
4. MenuItem 생성
5. 응답: MenuItem
```

### 메뉴 순서 변경
```
입력: items[{menu_item_id, display_order}]

1. 모든 menu_item_id가 해당 store에 속하는지 확인
2. 일괄 display_order 업데이트
3. 응답: 성공
```

---

## 8. 주문 번호 생성 규칙

```
형식: ORD-{YYYYMMDD}-{순번}
예시: ORD-20260430-0001

순번 규칙:
- 매장별 + 일별 순번
- 하루 시작 시 0001부터
- 4자리 (최대 9999건/일/매장)
```

---

## 9. 과거 주문 내역 조회

```
입력: store_id, table_id, date_from (optional), date_to (optional)

1. 해당 테이블의 completed 세션 조회
2. 각 세션의 주문 조회
3. 날짜 필터 적용 (completed_at 기준)
4. 시간 역순 정렬
5. 응답: [{session_id, completed_at, orders: [{order_number, items, total}]}]
```

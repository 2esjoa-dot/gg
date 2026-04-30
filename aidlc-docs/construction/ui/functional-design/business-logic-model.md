# Unit 4 (UI) - 비즈니스 로직 모델

## 1. 고객 앱 비즈니스 로직

### 1.1 자동 로그인 플로우 (US-C01)

```
앱 시작
  │
  ├─ localStorage에 token + storeId + tableId 존재?
  │   ├─ YES → API 토큰 검증 (GET /api/customer/auth/verify 또는 메뉴 조회 시도)
  │   │   ├─ 성공 → 메뉴 페이지 (/) 이동
  │   │   └─ 실패 → localStorage 클리어 → 초기 설정 (/setup) 이동
  │   └─ NO → 초기 설정 (/setup) 이동
  │
초기 설정 페이지
  │
  ├─ 사용자 입력: 매장 식별자, 테이블 번호, 비밀번호
  ├─ POST /api/customer/auth/login
  │   ├─ 성공 → token, storeId, tableId를 localStorage 저장 → 메뉴 페이지 이동
  │   └─ 실패 → 에러 메시지 표시 ("인증 정보가 올바르지 않습니다")
  │
브라우저 새로고침
  └─ localStorage에서 인증 정보 복원 → 자동 로그인 재시도
```

**localStorage 키:**
| 키 | 값 | 설명 |
|---|---|---|
| `token` | JWT 문자열 | 인증 토큰 |
| `store_id` | number | 매장 ID |
| `table_id` | number | 테이블 ID |
| `store_code` | string | 매장 식별자 |
| `table_number` | number | 테이블 번호 |

### 1.2 장바구니 로직 (US-C04)

**상태 구조 (Zustand Store):**
```typescript
interface CartStore {
  items: CartItem[]
  
  // Actions
  addItem: (menuItem: MenuItem) => void
  removeItem: (menuItemId: number) => void
  updateQuantity: (menuItemId: number, quantity: number) => void
  clearCart: () => void
  
  // Computed
  totalAmount: () => number
  totalCount: () => number
  isEmpty: () => boolean
}
```

**장바구니 동작 상세:**

| 동작 | 로직 | 결과 |
|---|---|---|
| 메뉴 담기 | 동일 메뉴 존재 → 수량+1, 없으면 수량 1로 추가 | 장바구니 업데이트 + localStorage 동기화 |
| 수량 증가 | 현재 수량 < 50 → 수량+1 | 수량 50이면 증가 버튼 비활성화 |
| 수량 감소 | 수량 > 1 → 수량-1, 수량 == 1 → 아이템 삭제 | 자동 삭제 |
| 아이템 삭제 | 장바구니에서 제거 | 총액 재계산 |
| 비우기 | 전체 아이템 삭제 | 빈 장바구니 |
| 새로고침 | localStorage에서 복원 | 장바구니 유지 |
| 세션 종료 | localStorage 장바구니 키 삭제 | 빈 장바구니 |

**총액 계산:**
```
totalAmount = Σ (item.menuItem.price × item.quantity)
```
- 소수점 없음 (원화 정수)
- 천 단위 콤마 포맷: `₩12,500`

### 1.3 주문 생성 플로우 (US-C05)

```
장바구니 페이지
  │
  ├─ "주문하기" 버튼 터치 (장바구니 비어있으면 비활성화)
  │
주문 확인 페이지
  │
  ├─ 주문 내역 최종 확인 (읽기 전용)
  ├─ "주문 확정" 버튼 터치
  │   ├─ isSubmitting = true (버튼 비활성화 + 로딩)
  │   ├─ POST /api/customer/orders
  │   │   Body: { store_id, table_id, session_id, items: [{menu_item_id, quantity}] }
  │   │
  │   ├─ 성공:
  │   │   ├─ 장바구니 비우기 (clearCart)
  │   │   ├─ OrderSuccessOverlay 표시
  │   │   ├─ 5초 카운트다운 시작 (5, 4, 3, 2, 1)
  │   │   └─ 카운트다운 완료 → 메뉴 페이지 (/) 자동 이동
  │   │
  │   └─ 실패:
  │       ├─ 에러 메시지 표시
  │       ├─ 장바구니 유지 (비우지 않음)
  │       └─ isSubmitting = false (재시도 가능)
```

**세션 처리:**
- 주문 생성 시 session_id가 필요
- 활성 세션이 없으면 백엔드에서 자동 생성 (Unit 1 SessionService)
- 프론트엔드는 session_id를 localStorage에 캐시하되, 백엔드 응답 우선

### 1.4 주문 내역 폴링 (US-C06)

```
주문 내역 페이지 진입
  │
  ├─ 즉시 조회: GET /api/customer/orders/session/{session_id}
  ├─ 30초 간격 폴링 시작
  │   ├─ setInterval(30000)
  │   ├─ 페이지 이탈 시 clearInterval
  │   └─ 에러 시 폴링 유지 (다음 주기에 재시도)
  │
  ├─ 응답 데이터 → 시간 역순 정렬
  ├─ 상태 변경 감지 → UI 즉시 반영
  └─ 페이지네이션: 초기 20건, 스크롤 시 추가 로드
```

**폴링 훅 (usePolling):**
```typescript
interface UsePollingOptions {
  interval: number       // 30000 (30초)
  enabled: boolean       // 페이지 활성 시만
  onError?: (error: Error) => void
}

function usePolling<T>(
  fetcher: () => Promise<T>,
  options: UsePollingOptions
): { data: T | null; isLoading: boolean; error: Error | null }
```

---

## 2. 관리자 앱 비즈니스 로직

### 2.1 관리자 로그인 플로우 (US-A01 UI)

```
로그인 페이지
  │
  ├─ 입력: 매장 식별자, 사용자명, 비밀번호
  ├─ POST /api/admin/auth/login
  │   ├─ 성공:
  │   │   ├─ JWT 토큰 → localStorage('admin_token') 저장
  │   │   ├─ 사용자 정보 (role, store_id) → Zustand authStore 저장
  │   │   └─ 대시보드 (/) 이동
  │   │
  │   ├─ 실패 (401):
  │   │   └─ "인증 정보가 올바르지 않습니다" 에러 표시
  │   │
  │   └─ 실패 (429 - 잠금):
  │       └─ "로그인이 차단되었습니다. N분 후 다시 시도해주세요" 표시
  │
토큰 만료 (16시간)
  └─ API 401 응답 감지 → localStorage 클리어 → /login 리다이렉트
```

**인증 상태 (Zustand Store):**
```typescript
interface AuthStore {
  token: string | null
  role: 'store_admin' | 'hq_admin' | null
  storeId: number | null
  username: string | null
  
  login: (token: string, payload: TokenPayload) => void
  logout: () => void
  isAuthenticated: () => boolean
  isHQAdmin: () => boolean
}
```

### 2.2 테이블 관리 로직 (US-A04, A06, A07 UI)

**테이블 추가:**
```
"테이블 추가" 클릭
  → AddTableModal 열기
  → 입력: 테이블 번호, 비밀번호 (최소 4자)
  → POST /api/admin/tables
  → 성공: 모달 닫기 + 테이블 목록 새로고침
  → 실패 (409): "이미 존재하는 테이블 번호입니다"
```

**이용 완료:**
```
"이용 완료" 클릭
  → ConfirmModal 열기 ("이용 완료 처리하시겠습니까?")
  → "확인" 클릭 → POST /api/admin/tables/{table_id}/complete
  → 성공: 테이블 상태 리셋 (주문 0, 세션 종료)
  → "취소" 클릭 → 모달 닫기
```

**과거 내역:**
```
"과거 내역" 클릭
  → HistoryModal 열기
  → GET /api/admin/tables/{table_id}/history?from=YYYY-MM-DD&to=YYYY-MM-DD
  → 날짜 필터 변경 시 재조회
  → "닫기" 클릭 → 모달 닫기
```

### 2.3 메뉴 관리 로직 (US-A08, A09 UI)

**메뉴 등록:**
```
"메뉴 등록" 클릭
  → MenuFormModal 열기 (빈 폼)
  → 입력: 메뉴명*, 가격*, 설명, 카테고리*, 이미지
  → 유효성 검증:
    - 메뉴명: 필수, 1~100자
    - 가격: 필수, 정수, > 0
    - 카테고리: 필수
    - 이미지: 선택, 5MB 이하, jpg/png/webp
  → 이미지 있으면: POST /api/admin/menu/upload-image → image_url 획득
  → POST /api/admin/menu (body에 image_url 포함)
  → 성공: 모달 닫기 + 메뉴 목록 새로고침
```

**메뉴 수정:**
```
"수정" 클릭
  → MenuFormModal 열기 (기존 데이터 채움)
  → 수정 후 저장 → PUT /api/admin/menu/{item_id}
  → 성공: 모달 닫기 + 목록 새로고침
```

**메뉴 삭제:**
```
"삭제" 클릭
  → DeleteConfirmModal 열기
  → "확인" → DELETE /api/admin/menu/{item_id}
  → 성공: 목록 새로고침
```

**메뉴 순서 조정 (드래그앤드롭):**
```
드래그 시작 → 드래그 중 (시각적 피드백) → 드롭
  → 로컬 순서 즉시 반영 (낙관적 업데이트)
  → PATCH /api/admin/menu/order (body: [{item_id, display_order}])
  → 실패 시 원래 순서로 롤백
```

### 2.4 계정 등록 로직 (US-A10 UI)

```
계정 등록 폼
  → 입력: 사용자명*, 비밀번호*, 비밀번호 확인*
  → 유효성 검증:
    - 사용자명: 필수, 3~50자, 영문+숫자
    - 비밀번호: 필수, 최소 4자
    - 비밀번호 확인: 비밀번호와 일치
  → POST /api/admin/auth/register
  → 성공: "계정이 등록되었습니다" 메시지 + 폼 초기화
  → 실패 (409): "이미 존재하는 사용자명입니다"
```

### 2.5 본사 매장 관리 로직 (US-H01, H02 UI)

**매장 등록:**
```
"매장 등록" 클릭
  → AddStoreModal 열기
  → 입력: 매장명*, 매장 식별자*, 주소
  → POST /api/hq/stores
  → 성공: 모달 닫기 + 목록 새로고침
  → 실패 (409): "이미 존재하는 매장 식별자입니다"
```

**매장 목록:**
```
페이지 진입
  → GET /api/hq/stores
  → 테이블 형태로 표시 (매장명, 식별자, 등록일)
  → 검색: 매장명 또는 식별자로 필터링 (클라이언트 사이드)
  → 페이지네이션: 20건 단위
```

---

## 3. API 연동 포인트 정리

### 고객 앱 API

| 기능 | Method | Endpoint | 담당 |
|---|---|---|---|
| 태블릿 로그인 | POST | /api/customer/auth/login | Unit 4 (UI) ↔ Unit 1 (API) |
| 메뉴 조회 | GET | /api/customer/menu/{store_id} | Unit 2 (API 연동) + Unit 4 (UI) |
| 주문 생성 | POST | /api/customer/orders | Unit 4 (UI) ↔ Unit 3 (API) |
| 주문 내역 조회 | GET | /api/customer/orders/session/{session_id} | Unit 4 (UI) ↔ Unit 3 (API) |

### 관리자 앱 API

| 기능 | Method | Endpoint | 담당 |
|---|---|---|---|
| 관리자 로그인 | POST | /api/admin/auth/login | Unit 4 (UI) ↔ Unit 1 (API) |
| 관리자 계정 등록 | POST | /api/admin/auth/register | Unit 4 (UI) ↔ Unit 1 (API) |
| 테이블 목록 | GET | /api/admin/tables | Unit 4 (UI) ↔ Unit 1 (API) |
| 테이블 등록 | POST | /api/admin/tables | Unit 4 (UI) ↔ Unit 1 (API) |
| 이용 완료 | POST | /api/admin/tables/{id}/complete | Unit 4 (UI) ↔ Unit 1 (API) |
| 과거 내역 | GET | /api/admin/tables/{id}/history | Unit 4 (UI) ↔ Unit 3 (API) |
| 메뉴 목록 | GET | /api/admin/menu | Unit 4 (UI) ↔ Unit 2 (API) |
| 메뉴 등록 | POST | /api/admin/menu | Unit 4 (UI) ↔ Unit 2 (API) |
| 메뉴 수정 | PUT | /api/admin/menu/{id} | Unit 4 (UI) ↔ Unit 2 (API) |
| 메뉴 삭제 | DELETE | /api/admin/menu/{id} | Unit 4 (UI) ↔ Unit 2 (API) |
| 메뉴 순서 변경 | PATCH | /api/admin/menu/order | Unit 4 (UI) ↔ Unit 2 (API) |
| 이미지 업로드 | POST | /api/admin/menu/upload-image | Unit 4 (UI) ↔ Unit 2 (API) |
| 매장 등록 | POST | /api/hq/stores | Unit 4 (UI) ↔ Unit 1 (API) |
| 매장 목록 | GET | /api/hq/stores | Unit 4 (UI) ↔ Unit 1 (API) |

---

## 4. Mock 전략 (MSW)

### MSW 핸들러 구조
```
src/mocks/
├── handlers/
│   ├── auth.ts        # 로그인/인증 Mock
│   ├── menu.ts        # 메뉴 조회/CRUD Mock
│   ├── order.ts       # 주문 생성/조회 Mock
│   ├── table.ts       # 테이블 관리 Mock
│   └── store.ts       # 매장 관리 Mock
├── data/
│   ├── menus.json     # Mock 메뉴 데이터
│   ├── orders.json    # Mock 주문 데이터
│   └── stores.json    # Mock 매장 데이터
├── browser.ts         # MSW 브라우저 워커 설정
└── handlers.ts        # 핸들러 통합
```

### Mock 활성화 조건
- `import.meta.env.VITE_ENABLE_MOCKS === 'true'` 일 때만 MSW 활성화
- 프로덕션 빌드에서는 자동 제외
- 백엔드 완성 후 환경변수만 변경하면 실제 API로 전환

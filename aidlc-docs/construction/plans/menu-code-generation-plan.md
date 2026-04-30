# Code Generation Plan - Unit 2: Menu

## Unit Context
- **Unit**: Unit 2 - Menu (메뉴 관리 + 고객 메뉴 조회)
- **담당 스토리**: US-A08 (메뉴 CRUD), US-A09 (메뉴 순서 변경), US-C03 (고객 메뉴 조회)
- **기술**: FastAPI (백엔드) + React+TS (고객 메뉴 UI)
- **의존성**: Unit 1의 DB 구조, AuthMiddleware, Store 모델

## 코드 위치
- **백엔드**: `backend/app/` (기존 구조 활용)
- **프론트엔드**: `frontend-customer/src/` (기존 구조 활용)
- **문서**: `aidlc-docs/construction/menu/code/`

---

## 실행 계획

### Step 1: Repository Layer — CategoryRepository
- [x] `backend/app/repositories/category_repository.py` 생성
- 메서드: get_by_store, get_by_id, create, update, delete, has_menu_items, get_max_display_order
- 스토리: US-A08

### Step 2: Repository Layer — MenuRepository
- [x] `backend/app/repositories/menu_repository.py` 생성
- 메서드: get_by_store, get_by_category, get_by_id, create, update, soft_delete, update_display_orders, get_max_display_order
- 스토리: US-A08, US-A09, US-C03

### Step 3: Service Layer — FileService
- [x] `backend/app/services/file_service.py` 생성
- Protocol 정의 + LocalFileService 구현체
- 메서드: validate_image, save_file, delete_file
- 스토리: US-A08

### Step 4: Service Layer — MenuService
- [x] `backend/app/services/menu_service.py` 생성
- 메서드: create_category, get_categories, update_category, delete_category, create_menu_item, update_menu_item, delete_menu_item, get_menu_by_store, update_menu_order
- 스토리: US-A08, US-A09, US-C03

### Step 5: Router Layer — admin_menu.py 구현
- [x] `backend/app/routers/admin_menu.py` 수정 (기존 TODO 구현)
- 엔드포인트: GET/POST/PUT/DELETE categories, GET/POST/PUT/DELETE menu items, PUT menu order, POST image upload
- 스토리: US-A08, US-A09

### Step 6: Router Layer — customer_menu.py 구현
- [x] `backend/app/routers/customer_menu.py` 수정 (기존 TODO 구현)
- 엔드포인트: GET categories, GET menu (active only)
- 스토리: US-C03

### Step 7: Static Files 설정
- [x] `backend/app/main.py` 수정 — StaticFiles 마운트 (uploads 디렉토리)
- 스토리: US-A08

### Step 8: Unit Test — Repository Layer
- [x] `backend/tests/test_menu_repository.py` 생성
- CategoryRepository, MenuRepository 테스트
- 스토리: US-A08, US-A09, US-C03

### Step 9: Unit Test — Service Layer
- [x] `backend/tests/test_menu_service.py` 생성
- MenuService, FileService 테스트
- 스토리: US-A08, US-A09, US-C03

### Step 10: Unit Test — Router Layer
- [x] `backend/tests/test_menu_router.py` 생성
- admin_menu, customer_menu 엔드포인트 테스트
- 스토리: US-A08, US-A09, US-C03

### Step 11: Frontend — API Client
- [x] `frontend-customer/src/api/menu.ts` 생성
- 함수: fetchCategories, fetchMenu
- 스토리: US-C03

### Step 12: Frontend — MenuPage 구현
- [x] `frontend-customer/src/pages/MenuPage.tsx` 수정
- 카테고리 탭 + 메뉴 그리드 + 로딩/에러 상태
- 스토리: US-C03

### Step 13: Frontend — 컴포넌트 생성
- [x] `frontend-customer/src/components/CategoryTab.tsx` 생성
- [x] `frontend-customer/src/components/MenuCard.tsx` 생성
- [x] `frontend-customer/src/components/MenuDetail.tsx` 생성
- 스토리: US-C03

### Step 14: Frontend Unit Test
- [x] `frontend-customer/src/__tests__/MenuPage.test.tsx` 생성
- MenuPage, CategoryTab, MenuCard 컴포넌트 테스트
- 스토리: US-C03

### Step 15: Documentation
- [x] `aidlc-docs/construction/menu/code/code-summary.md` 생성
- 생성/수정된 파일 목록, API 엔드포인트 요약

---

## 스토리 커버리지

| Story | Steps | Status |
|---|---|---|
| US-A08 (메뉴 CRUD + 이미지) | 1, 2, 3, 4, 5, 7, 8, 9, 10 | ✅ |
| US-A09 (메뉴 순서 변경) | 2, 4, 5, 8, 9, 10 | ✅ |
| US-C03 (고객 메뉴 조회) | 2, 4, 6, 8, 9, 10, 11, 12, 13, 14 | ✅ |

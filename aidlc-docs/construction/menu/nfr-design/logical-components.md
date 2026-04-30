# Logical Components - Unit 2: Menu

## 컴포넌트 구성도

```
+--------------------------------------------------+
|                   Router Layer                    |
|  admin_menu.py         customer_menu.py           |
+--------------------------------------------------+
                    |                |
+--------------------------------------------------+
|                  Service Layer                    |
|  MenuService              FileService (Protocol)  |
|                           LocalFileService (impl)  |
+--------------------------------------------------+
                    |
+--------------------------------------------------+
|                Repository Layer                   |
|  MenuRepository           CategoryRepository      |
+--------------------------------------------------+
                    |
+--------------------------------------------------+
|                  Database Layer                   |
|  Category Model           MenuItem Model          |
+--------------------------------------------------+
```

## 백엔드 컴포넌트

### 1. CategoryRepository
- **위치**: `backend/app/repositories/category_repository.py`
- **책임**: Category 테이블 CRUD
- **메서드**:
  - `get_by_store(store_id) → list[Category]`
  - `get_by_id(store_id, category_id) → Category | None`
  - `create(category) → Category`
  - `update(store_id, category_id, data) → Category`
  - `delete(store_id, category_id) → bool`
  - `has_menu_items(store_id, category_id) → bool`

### 2. MenuRepository
- **위치**: `backend/app/repositories/menu_repository.py`
- **책임**: MenuItem 테이블 CRUD + 조회
- **메서드**:
  - `get_by_store(store_id, include_inactive=False) → list[MenuItem]`
  - `get_by_category(store_id, category_id, active_only=True) → list[MenuItem]`
  - `get_by_id(store_id, menu_item_id) → MenuItem | None`
  - `create(menu_item) → MenuItem`
  - `update(store_id, menu_item_id, data) → MenuItem`
  - `soft_delete(store_id, menu_item_id) → bool`
  - `update_display_orders(items: list[{id, display_order}]) → bool`
  - `get_max_display_order(store_id, category_id) → int`

### 3. MenuService
- **위치**: `backend/app/services/menu_service.py`
- **책임**: 메뉴 비즈니스 로직 오케스트레이션
- **의존성**: MenuRepository, CategoryRepository, FileService
- **메서드**:
  - `create_category(store_id, data) → Category`
  - `get_categories(store_id) → list[Category]`
  - `update_category(store_id, category_id, data) → Category`
  - `delete_category(store_id, category_id) → None`
  - `create_menu_item(store_id, data, image?) → MenuItem`
  - `update_menu_item(store_id, item_id, data, image?) → MenuItem`
  - `delete_menu_item(store_id, item_id) → None`
  - `get_menu_by_store(store_id, active_only) → list[CategoryWithItems]`
  - `update_menu_order(store_id, items) → None`

### 4. FileService (Protocol)
- **위치**: `backend/app/services/file_service.py`
- **책임**: 파일 저장/삭제 추상화
- **메서드**:
  - `save_file(store_id, file) → str (url)`
  - `delete_file(file_path) → bool`
  - `validate_image(file) → None (raises on error)`

### 5. LocalFileService
- **위치**: `backend/app/services/file_service.py` (같은 파일)
- **책임**: 로컬 파일시스템 저장 구현체
- **저장 경로**: `uploads/{store_id}/{uuid}.{ext}`

## 프론트엔드 컴포넌트

### 1. MenuPage
- **위치**: `frontend-customer/src/pages/MenuPage.tsx`
- **책임**: 카테고리 탭 + 메뉴 그리드 표시
- **상태**: loading, error, categories, selectedCategory
- **API 호출**: GET /api/customer/menu

### 2. CategoryTab
- **위치**: `frontend-customer/src/components/CategoryTab.tsx`
- **책임**: 카테고리 탭 네비게이션
- **Props**: categories, selectedId, onSelect

### 3. MenuCard
- **위치**: `frontend-customer/src/components/MenuCard.tsx`
- **책임**: 개별 메뉴 아이템 카드 표시
- **Props**: menuItem, onAddToCart

### 4. MenuDetail (모달)
- **위치**: `frontend-customer/src/components/MenuDetail.tsx`
- **책임**: 메뉴 상세 정보 모달
- **Props**: menuItem, isOpen, onClose, onAddToCart

### 5. API Client
- **위치**: `frontend-customer/src/api/menu.ts`
- **책임**: 메뉴 관련 API 호출 함수
- **함수**: `fetchCategories(storeId)`, `fetchMenuByCategory(storeId, categoryId)`

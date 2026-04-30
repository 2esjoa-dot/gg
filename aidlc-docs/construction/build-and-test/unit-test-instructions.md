# Unit Test Execution - Unit 2: Menu

## 백엔드 단위 테스트

### 사전 준비
```bash
cd backend
pip install -r requirements.txt
pip install -r tests/requirements-test.txt
```

### 전체 테스트 실행
```bash
pytest tests/ -v
```

### Unit 2 관련 테스트만 실행
```bash
# Repository 계층 테스트
pytest tests/test_menu_repository.py -v

# Service 계층 테스트
pytest tests/test_menu_service.py -v

# Router 계층 테스트
pytest tests/test_menu_router.py -v
```

### 테스트 커버리지 확인
```bash
pip install pytest-cov
pytest tests/test_menu_repository.py tests/test_menu_service.py tests/test_menu_router.py --cov=app/repositories/category_repository --cov=app/repositories/menu_repository --cov=app/services/menu_service --cov=app/services/file_service --cov=app/routers/admin_menu --cov=app/routers/customer_menu -v
```

### 예상 결과

| 테스트 파일 | 테스트 수 | 예상 결과 |
|---|---|---|
| test_menu_repository.py | 18 | 전체 통과 |
| test_menu_service.py | 14 | 전체 통과 |
| test_menu_router.py | 9 | 전체 통과 |
| **합계** | **41** | **전체 통과** |

### 테스트 범위

| 계층 | 테스트 항목 |
|---|---|
| Repository | 카테고리 CRUD, 메뉴 CRUD, soft delete, 순서 변경, 멀티테넌시 격리 |
| Service | 카테고리 중복 검증, 메뉴 생성/수정/삭제, 카테고리 삭제 제한, 순서 변경 |
| Router | 인증/인가, 카테고리 API, 메뉴 API, 고객 메뉴 조회 |

## 프론트엔드 단위 테스트

### 사전 준비
```bash
cd frontend-customer
npm install
npm install --save-dev vitest jsdom
```

### vitest 설정 (vite.config.ts에 추가)
```typescript
/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
  },
})
```

### 테스트 실행
```bash
npx vitest run
```

### 예상 결과

| 테스트 파일 | 테스트 수 | 예상 결과 |
|---|---|---|
| MenuPage.test.tsx | 6 | 전체 통과 |

### 테스트 범위
- CategoryTab: onSelect 콜백 호출 검증
- MenuCard: 가격 포맷팅, placeholder 이미지 처리
- MenuPage: 카테고리 자동 선택, 카테고리별 필터링, 빈 상태 처리

# Code Summary - Unit 2: Menu

## 생성된 파일

### 백엔드 — Repository Layer
| 파일 | 상태 | 설명 |
|---|---|---|
| `backend/app/repositories/category_repository.py` | 신규 | 카테고리 CRUD, 중복 확인, 메뉴 존재 확인 |
| `backend/app/repositories/menu_repository.py` | 신규 | 메뉴 CRUD, soft delete, 순서 변경, 카테고리별 조회 |

### 백엔드 — Service Layer
| 파일 | 상태 | 설명 |
|---|---|---|
| `backend/app/services/menu_service.py` | 신규 | 메뉴 비즈니스 로직 (카테고리/메뉴 CRUD, 순서 변경) |
| `backend/app/services/file_service.py` | 신규 | 파일 업로드 (Protocol + LocalFileService) |

### 백엔드 — Router Layer
| 파일 | 상태 | 설명 |
|---|---|---|
| `backend/app/routers/admin_menu.py` | 수정 | 관리자 메뉴 API 구현 (카테고리/메뉴 CRUD, 순서, 이미지) |
| `backend/app/routers/customer_menu.py` | 수정 | 고객 메뉴 조회 API 구현 (카테고리별 활성 메뉴) |

### 백엔드 — Infrastructure
| 파일 | 상태 | 설명 |
|---|---|---|
| `backend/app/main.py` | 수정 | StaticFiles 마운트 (uploads 디렉토리) |

### 백엔드 — Unit Tests
| 파일 | 상태 | 설명 |
|---|---|---|
| `backend/tests/test_menu_repository.py` | 신규 | Repository 계층 테스트 (18개 테스트) |
| `backend/tests/test_menu_service.py` | 신규 | Service 계층 테스트 (14개 테스트) |
| `backend/tests/test_menu_router.py` | 신규 | Router 계층 테스트 (9개 테스트) |

### 프론트엔드 — Components
| 파일 | 상태 | 설명 |
|---|---|---|
| `frontend-customer/src/pages/MenuPage.tsx` | 수정 | 메뉴 페이지 (카테고리 탭 + 메뉴 그리드 + 상세 모달) |
| `frontend-customer/src/components/CategoryTab.tsx` | 신규 | 카테고리 탭 네비게이션 |
| `frontend-customer/src/components/MenuCard.tsx` | 신규 | 메뉴 카드 컴포넌트 |
| `frontend-customer/src/components/MenuDetail.tsx` | 신규 | 메뉴 상세 모달 |
| `frontend-customer/src/api/menu.ts` | 신규 | 메뉴 API 클라이언트 |

### 프론트엔드 — Unit Tests
| 파일 | 상태 | 설명 |
|---|---|---|
| `frontend-customer/src/__tests__/MenuPage.test.tsx` | 신규 | 컴포넌트 로직 테스트 |

---

## API 엔드포인트 요약

### 관리자 API (`/api/admin/menu`)
| Method | Path | 설명 |
|---|---|---|
| GET | /categories | 카테고리 목록 |
| POST | /categories | 카테고리 생성 |
| PUT | /categories/{id} | 카테고리 수정 |
| DELETE | /categories/{id} | 카테고리 삭제 |
| GET | /items | 메뉴 목록 (비활성 포함) |
| POST | /items | 메뉴 생성 (이미지 포함) |
| PUT | /items/{id} | 메뉴 수정 (이미지 포함) |
| DELETE | /items/{id} | 메뉴 삭제 (soft delete) |
| PUT | /items/order | 메뉴 순서 변경 |
| POST | /upload-image | 이미지 업로드 |

### 고객 API (`/api/customer/menu`)
| Method | Path | 설명 |
|---|---|---|
| GET | /categories | 카테고리 목록 |
| GET | / | 전체 메뉴 (카테고리별, 활성만) |

---

## 스토리 커버리지
- ✅ US-A08: 메뉴 CRUD + 이미지 업로드
- ✅ US-A09: 메뉴 순서 변경
- ✅ US-C03: 고객 메뉴 조회 + 메뉴 페이지 UI

# NFR Design Patterns - Unit 2: Menu

## 1. Repository Pattern (데이터 접근 추상화)

### 적용 대상
- MenuRepository, CategoryRepository (신규 생성)

### 패턴
```
Router → Service → Repository → DB
```

- Repository는 SQLAlchemy 세션을 주입받아 DB 접근
- Service는 비즈니스 로직만 담당, DB 접근은 Repository에 위임
- Router는 HTTP 요청/응답 변환만 담당

### 구현 방식
- 기존 프로젝트의 Repository 패턴 따름 (store_repository.py 참조)
- async/await 기반 비동기 DB 접근
- `get_db()` 의존성 주입으로 세션 관리

---

## 2. Strategy Pattern (파일 저장 추상화)

### 적용 대상
- FileService (신규 생성)

### 패턴
```
FileService (인터페이스)
  ├── LocalFileService (MVP 구현체)
  └── S3FileService (향후 구현체)
```

### 구현 방식
- `FileService` 프로토콜(Protocol) 정의: `save_file()`, `delete_file()`, `get_file_url()`
- MVP에서는 `LocalFileService` 구현체 사용
- config.py에서 저장 방식 설정 (`FILE_STORAGE_TYPE = "local"`)
- 추후 S3 마이그레이션 시 `S3FileService` 구현체만 추가

### 파일 저장 규칙
- 파일명: `{uuid4}.{원본확장자}`
- 경로: `uploads/{store_id}/{filename}`
- Content-Type 화이트리스트: `image/jpeg`, `image/png`, `image/webp`
- 최대 크기: 5MB (5 * 1024 * 1024 bytes)

---

## 3. Guard Pattern (입력 검증 + 멀티테넌시 격리)

### 적용 대상
- 모든 메뉴 관련 Service 메서드

### 패턴
```
1. Pydantic 스키마 검증 (Router 레벨, 자동)
2. store_id 격리 검증 (Service 레벨)
3. 비즈니스 규칙 검증 (Service 레벨)
4. DB 제약조건 검증 (Repository 레벨, 자동)
```

### 멀티테넌시 격리
- JWT에서 추출한 `store_id`를 모든 쿼리에 필터로 적용
- Service 메서드의 첫 번째 파라미터로 `store_id` 전달
- Repository의 모든 조회/수정/삭제 쿼리에 `WHERE store_id = :store_id` 포함
- 다른 매장 데이터 접근 시도 시 404 반환 (존재 여부 노출 방지)

---

## 4. Error Handling Pattern (일관된 에러 응답)

### 적용 대상
- 모든 메뉴 관련 Router, Service

### 패턴
- 기존 프로젝트의 `utils/exceptions.py` 활용
- 커스텀 예외 → HTTPException 변환
- 일관된 에러 응답 형식: `{"detail": "에러 메시지"}`

### 메뉴 관련 에러 코드
| 상황 | HTTP | 메시지 |
|---|---|---|
| 카테고리 미발견 | 404 | "카테고리를 찾을 수 없습니다" |
| 메뉴 미발견 | 404 | "메뉴를 찾을 수 없습니다" |
| 카테고리명 중복 | 409 | "이미 존재하는 카테고리명입니다" |
| 카테고리 삭제 불가 (메뉴 존재) | 400 | "메뉴가 존재하는 카테고리는 삭제할 수 없습니다" |
| 파일 형식 오류 | 400 | "허용되지 않는 파일 형식입니다 (JPEG, PNG, WebP만 가능)" |
| 파일 크기 초과 | 400 | "파일 크기가 5MB를 초과합니다" |
| 유효성 검증 실패 | 422 | Pydantic 자동 처리 |

---

## 5. Frontend Error Handling Pattern

### 적용 대상
- 고객 메뉴 페이지 (MenuPage)

### 패턴
- API 호출 실패 시 에러 상태 표시
- 이미지 로드 실패 시 기본 이미지(placeholder) 표시
- 로딩 상태 표시 (스피너/스켈레톤)
- 네트워크 오류 시 재시도 버튼 제공

### 구현 방식
```
useState로 3가지 상태 관리:
- loading: boolean (로딩 중)
- error: string | null (에러 메시지)
- data: Category[] | null (메뉴 데이터)
```

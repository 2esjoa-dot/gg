# Business Logic Model - Unit 2: Menu

## 1. 메뉴 등록
```
입력: store_id, name, price, description, category_id, image (optional)

1. 카테고리 존재 확인 (store_id + category_id)
   → 없으면: 404
2. 유효성 검증
   - name: 필수, 1~100자
   - price: 필수, > 0
   - category_id: 필수
3. 이미지 처리 (있으면)
   - 파일 형식 검증 (JPEG/PNG/WebP)
   - 파일 크기 검증 (≤ 5MB)
   - UUID 파일명 생성
   - uploads/{store_id}/ 에 저장
4. display_order = 해당 카테고리 내 최대값 + 1
5. MenuItem 생성
6. 응답: MenuItem
```

## 2. 메뉴 수정
```
입력: menu_item_id, name, price, description, category_id, image (optional)

1. 메뉴 존재 확인 (store_id + menu_item_id)
   → 없으면: 404
2. 카테고리 변경 시 카테고리 존재 확인
3. 유효성 검증
4. 이미지 변경 시 새 이미지 저장 (기존 이미지 유지, 덮어쓰기 아님)
5. MenuItem 업데이트
6. 응답: 업데이트된 MenuItem
```

## 3. 메뉴 삭제 (Soft Delete)
```
입력: menu_item_id

1. 메뉴 존재 확인 (store_id + menu_item_id)
   → 없으면: 404
2. is_active = false 설정
3. 응답: 성공
```

## 4. 메뉴 순서 변경
```
입력: items[{menu_item_id, display_order}]

1. 모든 menu_item_id가 해당 store에 속하는지 확인
2. 일괄 display_order 업데이트
3. 응답: 성공
```

## 5. 카테고리 CRUD
```
등록: store_id + name → UNIQUE 확인 → 생성
조회: store_id 기준 전체 조회 (display_order 순)
수정: category_id + name → UNIQUE 확인 → 업데이트
삭제: 해당 카테고리에 메뉴가 있으면 삭제 불가 (400)
```

## 6. 고객 메뉴 조회
```
입력: store_id

1. 해당 매장의 카테고리 조회 (display_order 순)
2. 각 카테고리별 활성 메뉴 조회 (is_active=true, display_order 순)
3. 응답: [{category, items: [MenuItem]}]
```

## 7. 이미지 업로드
```
입력: store_id, file

1. 파일 형식 검증 (Content-Type: image/jpeg, image/png, image/webp)
2. 파일 크기 검증 (≤ 5MB)
3. UUID 파일명 생성 (uuid4 + 원본 확장자)
4. 저장 경로: uploads/{store_id}/{uuid_filename}
5. 디렉토리 없으면 생성
6. 파일 저장
7. 응답: {image_url: "/uploads/{store_id}/{uuid_filename}"}
```

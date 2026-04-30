# Table Order Backend API

## 실행 방법

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env 파일 생성
cp .env.example .env

# DB 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

## API 문서
서버 실행 후: http://localhost:8000/docs

## 테스트
```bash
pip install -r tests/requirements-test.txt
pytest tests/ -v
```

## 프로젝트 구조
```
backend/
├── app/
│   ├── main.py          # FastAPI 앱
│   ├── config.py        # 환경 설정
│   ├── database.py      # DB 연결
│   ├── models/          # SQLAlchemy 모델
│   ├── schemas/         # Pydantic DTO
│   ├── repositories/    # 데이터 접근
│   ├── services/        # 비즈니스 로직
│   ├── routers/         # API 엔드포인트
│   ├── middleware/      # 인증 미들웨어
│   └── utils/           # 유틸리티
├── migrations/          # Alembic
└── tests/
```

## Unit 분담

| Unit | 담당 | 범위 |
|---|---|---|
| Unit 1 (완료) | 개발자 1 | 인증, 매장, 테이블, 세션 |
| Unit 2 | 개발자 2 | 메뉴 CRUD + 고객 메뉴 UI |
| Unit 3 | 개발자 3 | 주문/SSE + 관리자 대시보드 |
| Unit 4 | 개발자 4 | 장바구니 + 나머지 UI |

## 개발자 2 가이드 (메뉴)
- `app/models/` 에 `category.py`, `menu_item.py` 추가
- `app/models/__init__.py` 에 import 추가
- `app/routers/admin_menu.py`, `app/routers/customer_menu.py` 생성
- `app/main.py` 에 router 등록

## 개발자 3 가이드 (주문)
- `app/models/` 에 `order.py`, `order_item.py` 추가
- `app/services/sse_service.py` 생성
- `app/routers/admin_orders.py`, `app/routers/customer_orders.py` 생성
- `app/main.py` 에 router 등록

## 개발자 4 가이드 (UI)
- `frontend-customer/`, `frontend-admin/` 디렉토리에서 작업
- API Mock: http://localhost:8000/docs 참고
- 인증 헤더: `Authorization: Bearer {token}`

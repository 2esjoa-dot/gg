# Build Instructions - 테이블오더 서비스 Backend API

## Prerequisites
- **Python**: 3.11+
- **PostgreSQL**: 15+
- **pip**: 최신 버전
- **libmagic**: python-magic 의존성 (macOS: `brew install libmagic`, Linux: `apt install libmagic1`)

## Build Steps

### 1. 가상환경 생성 및 활성화
```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# Windows: venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 실제 값 설정
# 특히 DATABASE_URL, SECRET_KEY 변경 필수
```

### 4. 데이터베이스 생성
```bash
# PostgreSQL에서 개발/테스트 DB 생성
createdb table_order_dev
createdb table_order_test
```

### 5. 마이그레이션 실행
```bash
alembic upgrade head
```

### 6. 디렉토리 생성
```bash
mkdir -p uploads logs
```

### 7. 서버 실행 (개발)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. 빌드 검증
- Swagger UI 접속: http://localhost:8000/docs
- ReDoc 접속: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Docker 빌드 (선택)
```bash
docker build -t table-order-api .
docker run -p 8000:8000 --env-file .env table-order-api
```

## Troubleshooting

### libmagic 관련 에러
- **macOS**: `brew install libmagic`
- **Ubuntu/Debian**: `sudo apt-get install libmagic1`

### asyncpg 연결 실패
- PostgreSQL 서비스 실행 확인: `pg_isready`
- DATABASE_URL 형식 확인: `postgresql+asyncpg://user:pass@host:5432/dbname`

### Alembic 마이그레이션 실패
- DB 연결 확인 후 재시도
- `alembic downgrade base` 후 `alembic upgrade head`

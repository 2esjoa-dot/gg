# Build Instructions - Unit 2: Menu

## Prerequisites
- **Python**: 3.11+
- **Node.js**: 18+
- **PostgreSQL**: 15+ (테스트 시 SQLite 사용 가능)
- **pip**: Python 패키지 관리자

## 백엔드 빌드

### 1. 가상환경 생성 및 활성화
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
pip install -r tests/requirements-test.txt
```

### 3. 환경변수 설정
```bash
# .env.example을 복사하여 .env 생성
cp .env.example .env

# .env 파일 편집 (DB 연결 정보 등)
```

### 4. 데이터베이스 마이그레이션
```bash
alembic upgrade head
```

### 5. 서버 실행 (개발 모드)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프론트엔드 빌드

### 1. 의존성 설치
```bash
cd frontend-customer
npm install
```

### 2. 개발 서버 실행
```bash
npm run dev
```

### 3. 프로덕션 빌드
```bash
npm run build
```

## 빌드 검증
- 백엔드: `http://localhost:8000/health` → `{"status": "ok"}`
- 프론트엔드: `http://localhost:5173` → 메뉴 페이지 표시
- API 문서: `http://localhost:8000/docs` → Swagger UI 표시

## Troubleshooting

### aiosqlite 미설치 (테스트 시)
```bash
pip install aiosqlite
```

### python-multipart 미설치 (파일 업로드 시)
```bash
pip install python-multipart
```
이미 requirements.txt에 포함되어 있으나, 누락 시 수동 설치.

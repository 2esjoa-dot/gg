# Deployment Architecture - Unit 1: Backend API

## 1. 배포 프로세스

### 개발 환경 (로컬)
```
1. 저장소 클론
2. Python 가상환경 생성 (python -m venv venv)
3. 의존성 설치 (pip install -r requirements.txt)
4. .env 파일 설정 (.env.example 복사)
5. DB 마이그레이션 (alembic upgrade head)
6. 서버 실행 (uvicorn app.main:app --reload)
```

### 운영 환경 (EC2)
```
1. EC2 인스턴스 접속 (SSH)
2. 소스 코드 배포 (git pull 또는 rsync)
3. 의존성 설치 (pip install -r requirements.txt)
4. .env 파일 설정 (운영 환경 값)
5. DB 마이그레이션 (alembic upgrade head)
6. Uvicorn 재시작 (systemd service)
7. Nginx 설정 확인 (nginx -t && systemctl reload nginx)
```

---

## 2. 프로세스 관리 (systemd)

### FastAPI 서비스 파일
```ini
# /etc/systemd/system/table-order-api.service
[Unit]
Description=Table Order API
After=network.target

[Service]
Type=exec
User=app
Group=app
WorkingDirectory=/home/app/backend
Environment=PATH=/home/app/backend/venv/bin
ExecStart=/home/app/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 서비스 관리 명령
```bash
sudo systemctl start table-order-api
sudo systemctl stop table-order-api
sudo systemctl restart table-order-api
sudo systemctl status table-order-api
sudo journalctl -u table-order-api -f  # 로그 확인
```

---

## 3. Nginx 설정

### 메인 설정
```nginx
# /etc/nginx/conf.d/table-order.conf
upstream api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;

    # HTTPS 리다이렉트 (SSL 인증서 설정 후)
    # return 301 https://$server_name$request_uri;

    client_max_body_size 5M;

    # API 프록시
    location /api/ {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SSE 엔드포인트 (버퍼링 비활성화)
    location /api/admin/sse {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;
        proxy_cache off;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
        proxy_read_timeout 86400s;
    }

    # Swagger/ReDoc
    location /docs {
        proxy_pass http://api;
    }
    location /redoc {
        proxy_pass http://api;
    }
    location /openapi.json {
        proxy_pass http://api;
    }

    # 정적 파일 (이미지 업로드)
    location /uploads/ {
        alias /home/app/backend/uploads/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # Health Check
    location /health {
        proxy_pass http://api;
    }
}
```

---

## 4. 디렉토리 구조 (운영 서버)

```
/home/app/
└── backend/
    ├── app/                    # 애플리케이션 코드
    ├── migrations/             # Alembic 마이그레이션
    ├── tests/                  # 테스트
    ├── uploads/                # 이미지 업로드
    │   └── {store_id}/         # 매장별 디렉토리
    ├── logs/                   # 애플리케이션 로그
    │   └── app.log             # 일별 로테이션
    ├── venv/                   # Python 가상환경
    ├── .env                    # 환경 설정
    ├── alembic.ini             # Alembic 설정
    └── requirements.txt        # 의존성
```

---

## 5. 환경 변수 (.env)

### 개발 환경 (.env.development)
```env
# App
APP_NAME=table-order-api
DEBUG=true
API_PREFIX=/api

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/table_order_dev
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# JWT
SECRET_KEY=dev-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_HOURS=16

# CORS
ALLOWED_ORIGINS=["*"]

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880

# Logging
LOG_LEVEL=DEBUG
LOG_DIR=logs
LOG_MAX_DAYS=7
```

### 운영 환경 (.env.production)
```env
# App
APP_NAME=table-order-api
DEBUG=false
API_PREFIX=/api

# Database
DATABASE_URL=postgresql+asyncpg://appuser:STRONG_PASSWORD@rds-endpoint:5432/table_order
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30

# JWT
SECRET_KEY=RANDOM_64_CHAR_SECRET_KEY

# CORS
ALLOWED_ORIGINS=["https://customer.example.com","https://admin.example.com"]

# File Upload
UPLOAD_DIR=/home/app/backend/uploads
MAX_FILE_SIZE=5242880

# Logging
LOG_LEVEL=INFO
LOG_DIR=/home/app/backend/logs
LOG_MAX_DAYS=30
```

---

## 6. Health Check

### 엔드포인트
```
GET /health

응답 (200):
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}

응답 (503):
{
  "status": "unhealthy",
  "version": "1.0.0",
  "database": "disconnected"
}
```

---

## 7. 배포 체크리스트

### 최초 배포
- [ ] EC2 인스턴스 생성 (t3.medium, Amazon Linux 2023)
- [ ] 보안 그룹 설정 (sg-api: 80, 443, 22)
- [ ] RDS 인스턴스 생성 (db.t3.medium, PostgreSQL 15)
- [ ] 보안 그룹 설정 (sg-db: 5432 from sg-api)
- [ ] Python 3.11+ 설치
- [ ] Nginx 설치 및 설정
- [ ] 소스 코드 배포
- [ ] .env 파일 설정
- [ ] DB 마이그레이션 실행
- [ ] systemd 서비스 등록 및 시작
- [ ] uploads/ 디렉토리 생성 (권한 설정)
- [ ] logs/ 디렉토리 생성 (권한 설정)
- [ ] Health Check 확인

### 업데이트 배포
- [ ] 소스 코드 업데이트 (git pull)
- [ ] 의존성 업데이트 (pip install -r requirements.txt)
- [ ] DB 마이그레이션 (alembic upgrade head)
- [ ] 서비스 재시작 (systemctl restart table-order-api)
- [ ] Health Check 확인

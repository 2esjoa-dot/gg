# Infrastructure Design - 테이블오더 서비스

## 1. AWS 배포 아키텍처

```
                    [Internet]
                        |
                   [Route 53]
                        |
                  [ALB / Nginx]
                   /    |    \
                  /     |     \
    [EC2: Backend]  [S3: Customer]  [S3: Admin]
         |               Static         Static
         |
    [RDS PostgreSQL]
```

---

## 2. 인프라 구성 요소

### 2.1 컴퓨팅

| 구성 요소 | 서비스 | 스펙 | 용도 |
|---|---|---|---|
| Backend API | EC2 | t3.medium (2vCPU, 4GB) | FastAPI 서버 |
| Reverse Proxy | Nginx (EC2 내) | — | HTTPS, 정적 파일, 프록시 |

**MVP 단일 인스턴스 구성:**
```
EC2 (t3.medium)
├── Nginx (port 80/443)
│   ├── /api/* → uvicorn :8000
│   ├── / → frontend-customer 빌드 파일
│   └── /admin/* → frontend-admin 빌드 파일
└── uvicorn (port 8000)
    └── FastAPI app (workers: 4)
```

### 2.2 데이터베이스

| 구성 요소 | 서비스 | 스펙 | 설정 |
|---|---|---|---|
| Primary DB | RDS PostgreSQL 15 | db.t3.medium | Multi-AZ: No (MVP) |

**RDS 설정:**
- 스토리지: 20GB gp3 (자동 확장 활성)
- 백업: 자동 7일 보존
- 유지보수 윈도우: 월요일 03:00-04:00 KST
- 파라미터: max_connections=200

### 2.3 스토리지

| 용도 | 서비스 | 설정 |
|---|---|---|
| 메뉴 이미지 | EC2 로컬 (uploads/) | MVP. 향후 S3 이전 |
| 프론트엔드 빌드 | EC2 로컬 (Nginx 서빙) | MVP. 향후 S3+CloudFront |

### 2.4 네트워크

```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   └── EC2 (Backend + Nginx)
├── Private Subnet (10.0.2.0/24)
│   └── RDS PostgreSQL
└── Internet Gateway
```

**Security Groups:**
| SG | Inbound | Source |
|---|---|---|
| sg-web | 80, 443 | 0.0.0.0/0 |
| sg-app | 8000 | sg-web |
| sg-db | 5432 | sg-app |

---

## 3. 배포 프로세스

### 3.1 초기 배포
```bash
# 1. EC2 세팅
sudo apt update && sudo apt install -y python3.11 python3.11-venv nginx certbot

# 2. 백엔드 배포
git clone https://github.com/2esjoa-dot/gg.git /app
cd /app/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 실제 값으로 수정

# 3. DB 마이그레이션
alembic upgrade head

# 4. 프론트엔드 빌드
cd /app/frontend-customer && npm install && npm run build
cd /app/frontend-admin && npm install && npm run build

# 5. Nginx 설정
# 6. systemd 서비스 등록
# 7. SSL 인증서 (certbot)
```

### 3.2 업데이트 배포
```bash
cd /app
git pull origin main
cd backend && pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart tableorder

cd /app/frontend-customer && npm install && npm run build
cd /app/frontend-admin && npm install && npm run build
sudo systemctl reload nginx
```

---

## 4. 환경 설정

### 4.1 환경변수 (.env)
```
DATABASE_URL=postgresql+asyncpg://tableorder:PASSWORD@rds-endpoint:5432/tableorder
JWT_SECRET_KEY=production-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=16
MAX_LOGIN_ATTEMPTS=5
LOCK_DURATION_MINUTES=15
UPLOAD_DIR=/app/backend/uploads
MAX_FILE_SIZE_MB=5
```

### 4.2 Nginx 설정
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Customer App
    location / {
        root /app/frontend-customer/dist;
        try_files $uri $uri/ /index.html;
    }

    # Admin App
    location /admin {
        alias /app/frontend-admin/dist;
        try_files $uri $uri/ /admin/index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;  # SSE 지원
    }

    # 이미지 파일
    location /uploads {
        alias /app/backend/uploads;
        expires 7d;
    }
}
```

### 4.3 systemd 서비스
```ini
[Unit]
Description=Table Order API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/app/backend
Environment="PATH=/app/backend/venv/bin"
ExecStart=/app/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 5. 비용 예측 (월간)

| 서비스 | 스펙 | 예상 비용 |
|---|---|---|
| EC2 t3.medium | On-Demand | ~$30 |
| RDS db.t3.medium | Single-AZ | ~$50 |
| EBS (EC2) | 30GB gp3 | ~$3 |
| RDS Storage | 20GB gp3 | ~$3 |
| Data Transfer | ~50GB/월 | ~$5 |
| **합계** | | **~$91/월** |

---

## 6. 향후 확장 경로

| 현재 (MVP) | 확장 시 |
|---|---|
| EC2 단일 인스턴스 | ALB + Auto Scaling Group |
| RDS Single-AZ | RDS Multi-AZ + Read Replica |
| 이미지 로컬 저장 | S3 + CloudFront CDN |
| 프론트 Nginx 서빙 | S3 + CloudFront |
| SSE 인메모리 | Redis Pub/Sub |
| 수동 배포 | CodeDeploy / GitHub Actions |

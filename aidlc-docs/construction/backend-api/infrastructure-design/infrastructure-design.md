# Infrastructure Design - Unit 1: Backend API

## 1. 논리 → 인프라 매핑

| 논리 컴포넌트 | AWS 서비스 | 설명 |
|---|---|---|
| FastAPI Application | EC2 (t3.medium) | Uvicorn ASGI 서버 |
| PostgreSQL | RDS (db.t3.medium) | Managed PostgreSQL 15 |
| File Storage (MVP) | EC2 EBS (로컬 디스크) | uploads/ 디렉토리 |
| File Storage (향후) | S3 | 객체 스토리지 전환 |
| 로그 파일 | EC2 EBS | logs/ 디렉토리 |
| 로그 모니터링 (향후) | CloudWatch Logs | 중앙 로그 수집 |

---

## 2. Compute Infrastructure

### EC2 인스턴스
| 항목 | 개발 환경 | 운영 환경 |
|---|---|---|
| 인스턴스 타입 | t3.small | t3.medium |
| vCPU | 2 | 2 |
| 메모리 | 2 GB | 4 GB |
| OS | Amazon Linux 2023 | Amazon Linux 2023 |
| Python | 3.11+ | 3.11+ |
| 스토리지 | EBS gp3 20GB | EBS gp3 50GB |

### Uvicorn 설정
| 항목 | 개발 환경 | 운영 환경 |
|---|---|---|
| Workers | 1 | 4 (CPU 코어 x 2) |
| Host | 0.0.0.0 | 0.0.0.0 |
| Port | 8000 | 8000 |
| Reload | Yes | No |
| Access Log | Yes | Yes (JSON) |

---

## 3. Database Infrastructure

### RDS PostgreSQL
| 항목 | 개발 환경 | 운영 환경 |
|---|---|---|
| 인스턴스 | db.t3.micro | db.t3.medium |
| 엔진 | PostgreSQL 15 | PostgreSQL 15 |
| 스토리지 | gp3 20GB | gp3 50GB (자동 확장) |
| Multi-AZ | No | No (MVP, 향후 Yes) |
| 백업 | 자동 7일 | 자동 14일 |
| 암호화 | No | Yes (AES-256) |

### 연결 설정
```
DATABASE_URL = postgresql+asyncpg://{user}:{password}@{host}:5432/{dbname}

개발: host = localhost 또는 RDS 엔드포인트
운영: host = RDS 엔드포인트 (VPC 내부)
```

---

## 4. Network Infrastructure

### VPC 구성 (운영)
```
VPC (10.0.0.0/16)
  ├─ Public Subnet (10.0.1.0/24)
  │   └─ EC2 (FastAPI) — Elastic IP
  ├─ Private Subnet (10.0.2.0/24)
  │   └─ RDS (PostgreSQL)
  └─ Internet Gateway
```

### Security Groups
| 보안 그룹 | 인바운드 | 아웃바운드 |
|---|---|---|
| **sg-api** (EC2) | 80/443 (0.0.0.0/0), 22 (관리 IP) | 전체 허용 |
| **sg-db** (RDS) | 5432 (sg-api만) | 전체 허용 |

### 포트 매핑
| 서비스 | 포트 | 프로토콜 |
|---|---|---|
| FastAPI (Uvicorn) | 8000 | HTTP |
| Nginx (리버스 프록시) | 80, 443 | HTTP/HTTPS |
| PostgreSQL | 5432 | TCP |
| SSE | 8000 (동일) | HTTP (text/event-stream) |

---

## 5. Reverse Proxy (Nginx)

### 역할
- HTTPS 종료 (SSL/TLS)
- 정적 파일 서빙 (uploads/)
- 리버스 프록시 (→ Uvicorn :8000)
- SSE 연결 지원 (proxy_buffering off)

### 주요 설정
```
# SSE 지원
location /api/admin/sse {
    proxy_pass http://127.0.0.1:8000;
    proxy_buffering off;
    proxy_cache off;
    proxy_set_header Connection '';
    proxy_http_version 1.1;
    chunked_transfer_encoding off;
}

# 파일 업로드 크기 제한
client_max_body_size 5M;

# 정적 파일
location /uploads/ {
    alias /app/uploads/;
    expires 7d;
}
```

---

## 6. 환경별 구성 요약

### 개발 환경
```
개발자 로컬 머신
  ├─ FastAPI (uvicorn --reload)
  ├─ PostgreSQL (Docker 또는 로컬 설치)
  └─ uploads/ (로컬 디렉토리)
```

### 운영 환경
```
AWS
  ├─ EC2 (t3.medium)
  │   ├─ Nginx (리버스 프록시, HTTPS)
  │   ├─ Uvicorn (4 workers)
  │   ├─ uploads/ (EBS)
  │   └─ logs/ (EBS)
  ├─ RDS (db.t3.medium, PostgreSQL 15)
  └─ Route 53 (도메인, 선택)
```

---

## 7. 비용 추정 (월간, 서울 리전)

| 서비스 | 사양 | 예상 비용 (USD) |
|---|---|---|
| EC2 t3.medium | On-Demand | ~$38 |
| EBS gp3 50GB | 스토리지 | ~$4 |
| RDS db.t3.medium | Single-AZ | ~$52 |
| RDS 스토리지 50GB | gp3 | ~$6 |
| 데이터 전송 | ~50GB/월 | ~$5 |
| **합계** | | **~$105/월** |

*Reserved Instance 적용 시 약 40% 절감 가능*

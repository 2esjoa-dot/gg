# NFR Requirements - Unit 1: Backend API

## 1. 성능 요구사항

### PERF-01: API 응답 시간
| 항목 | 목표 |
|---|---|
| 일반 API (CRUD, 인증) | 500ms 이내 |
| 복잡한 쿼리 (주문 내역, 과거 이력) | 1초 이내 |
| SSE 이벤트 전달 (신규 주문) | 2초 이내 |

### PERF-02: 동시 접속 처리
| 항목 | 목표 |
|---|---|
| 동시 접속자 | 500명 이상 |
| DB Connection Pool | pool_size=20, max_overflow=30 |
| 비동기 처리 | FastAPI async/await 전면 활용 |

### PERF-03: 데이터베이스 최적화
| 항목 | 전략 |
|---|---|
| 인덱스 | 주요 조회 패턴별 복합 인덱스 적용 |
| 쿼리 최적화 | N+1 방지 (joinedload/selectinload) |
| Connection Pool | SQLAlchemy AsyncSession + pool 설정 |

---

## 2. 확장성 요구사항

### SCALE-01: SSE 연결 관리
| 항목 | 전략 |
|---|---|
| MVP | In-memory 구독자 관리 (asyncio.Queue 기반) |
| 확장 | Redis Pub/Sub 전환 가능한 인터페이스 설계 |
| 패턴 | EventPublisher 추상 클래스 → InMemoryPublisher / RedisPublisher |

### SCALE-02: 수평 확장 준비
| 항목 | 전략 |
|---|---|
| 상태 관리 | 서버 상태 최소화 (SSE 외 stateless) |
| 세션 | JWT 기반 (서버 측 세션 저장 없음) |
| 파일 저장 | 로컬 → S3 전환 가능한 인터페이스 |

---

## 3. 가용성 요구사항

### AVAIL-01: 서비스 가용성
| 항목 | 목표 |
|---|---|
| 가용성 | 매장 운영 시간 중 99.5% |
| 다운타임 허용 | 월 ~3.6시간 |
| 배포 전략 | 단일 서버 (MVP), 향후 Blue-Green 배포 |

### AVAIL-02: 장애 복구
| 항목 | 전략 |
|---|---|
| DB 백업 | AWS RDS 자동 백업 (일 1회) |
| 에러 처리 | 글로벌 예외 핸들러 + 구조화된 에러 응답 |
| SSE 재연결 | 클라이언트 EventSource 자동 재연결 |

---

## 4. 신뢰성 요구사항

### REL-01: 에러 처리 및 로깅
| 항목 | 전략 |
|---|---|
| 로깅 형식 | 구조화된 JSON 로깅 |
| 로그 저장 | 파일 로테이션 (일별, 최대 30일 보관) |
| 로그 레벨 | DEBUG(개발), INFO(운영) |
| 요청 추적 | Request ID 기반 추적 (미들웨어) |

### REL-02: Rate Limiting
| 항목 | 전략 |
|---|---|
| 적용 범위 | 인증 API만 (로그인 엔드포인트) |
| 제한 | 로그인 5회 실패 시 15분 잠금 (애플리케이션 레벨) |
| 전체 API | MVP에서는 미적용, 향후 필요 시 추가 |

### REL-03: 데이터 무결성
| 항목 | 전략 |
|---|---|
| 트랜잭션 | Service 레이어에서 트랜잭션 경계 관리 |
| 주문 번호 | PostgreSQL SEQUENCE 활용 (동시성 안전) |
| 스냅샷 | 주문 시점 메뉴명/가격 OrderItem에 복사 |

---

## 5. 보안 요구사항

### SEC-01: 인증/인가
| 항목 | 전략 |
|---|---|
| 비밀번호 | bcrypt (cost factor: 12) |
| 토큰 | JWT HS256, 16시간 유효 |
| 역할 | tablet, store_admin, hq_admin |
| 멀티테넌시 | store_id 기반 데이터 격리 |

### SEC-02: 파일 업로드 보안
| 항목 | 전략 |
|---|---|
| 파일명 | UUID 생성 + 원본 확장자 |
| 확장자 | 화이트리스트 (JPEG, PNG, WebP) |
| MIME 타입 | 서버 측 검증 (python-magic 또는 filetype) |
| 파일 크기 | 서버 측 재검증 (최대 5MB) |
| 저장 경로 | uploads/{store_id}/{uuid}.{ext} |

### SEC-03: CORS
| 항목 | 전략 |
|---|---|
| 개발 환경 | 전체 허용 (*) |
| 운영 환경 | 특정 도메인만 허용 (환경변수 ALLOWED_ORIGINS) |
| 메서드 | GET, POST, PUT, PATCH, DELETE |
| 헤더 | Authorization, Content-Type |

---

## 6. 유지보수성 요구사항

### MAINT-01: 코드 구조
| 항목 | 전략 |
|---|---|
| 아키텍처 | 계층형 (Router → Service → Repository → Model) |
| 의존성 주입 | FastAPI Depends 활용 |
| 설정 관리 | Pydantic Settings (타입 검증, .env 파일) |

### MAINT-02: 테스트
| 항목 | 전략 |
|---|---|
| 프레임워크 | pytest + pytest-asyncio |
| HTTP 클라이언트 | httpx AsyncClient |
| 커버리지 | pytest-cov (목표: 80% 이상) |
| 테스트 데이터 | factory_boy (모델별 팩토리) |
| 테스트 DB | 테스트용 PostgreSQL (또는 SQLite in-memory) |

### MAINT-03: 데이터베이스 마이그레이션
| 항목 | 전략 |
|---|---|
| 도구 | Alembic (SQLAlchemy 공식) |
| 자동 생성 | autogenerate 활용 |
| 버전 관리 | migrations/versions/ 디렉토리 |

### MAINT-04: API 문서화
| 항목 | 전략 |
|---|---|
| Swagger UI | /docs (자동 생성) |
| ReDoc | /redoc (자동 생성) |
| 커스텀 설명 | 각 엔드포인트에 docstring + response_model 명시 |
| 태그 분류 | customer, admin, hq 그룹별 |

---

## 7. NFR 요약 매트릭스

| 카테고리 | 핵심 지표 | 목표 |
|---|---|---|
| 성능 | API 응답 시간 | 500ms / 1s |
| 성능 | 동시 접속 | 500명+ |
| 성능 | SSE 전달 | 2초 이내 |
| 확장성 | SSE 관리 | In-memory → Redis 전환 가능 |
| 가용성 | 서비스 가용성 | 99.5% |
| 신뢰성 | 로깅 | JSON 구조화 + 파일 로테이션 |
| 보안 | 파일 업로드 | 3중 검증 (확장자+MIME+크기) |
| 유지보수 | 테스트 커버리지 | 80%+ |
| 유지보수 | DB 마이그레이션 | Alembic |

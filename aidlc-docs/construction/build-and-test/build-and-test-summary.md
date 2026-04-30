# Build and Test Summary - 테이블오더 서비스 Backend API

## Build Status
| 항목 | 내용 |
|---|---|
| **Build Tool** | pip + uvicorn |
| **Python** | 3.11+ |
| **Framework** | FastAPI 0.115.0 |
| **Database** | PostgreSQL 15 + SQLAlchemy 2.0 |
| **Migration** | Alembic 1.13 |

## Test Execution Summary

### Unit Tests
| 항목 | 값 |
|---|---|
| **총 테스트** | ~53개 |
| **유틸리티 테스트** | 21개 (security, exceptions, order_number) |
| **Service 테스트** | 21개 (auth, store, table, session) |
| **Repository 테스트** | 11개 (store, user, table, session) |
| **커버리지 목표** | 80%+ |

### Integration Tests
| 항목 | 값 |
|---|---|
| **총 테스트** | 15개 |
| **Health** | 1개 |
| **HQ API** | 4개 (매장 CRUD + 인증) |
| **Admin Auth** | 3개 (로그인/실패/등록) |
| **Admin Tables** | 3개 (등록/목록/이용완료) |
| **Customer Auth** | 2개 (로그인/실패) |
| **Customer Session** | 2개 (조회/없음) |

### Performance Tests
| 항목 | 목표 |
|---|---|
| **도구** | Locust |
| **동시 사용자** | 500명 |
| **응답 시간 (Median)** | < 500ms |
| **응답 시간 (P95)** | < 1000ms |
| **에러율** | < 1% |
| **상태** | 지침 생성 완료 (실행은 환경 구성 후) |

## Quick Start Commands

```bash
# 1. 환경 설정
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 2. DB 생성
createdb table_order_dev
createdb table_order_test

# 3. 마이그레이션
alembic upgrade head

# 4. 단위 테스트
pytest tests/unit/ -v --cov=app

# 5. 통합 테스트
pytest tests/integration/ -v

# 6. 전체 테스트
pytest -v --cov=app --cov-report=term-missing

# 7. 서버 실행
uvicorn app.main:app --reload
```

## Generated Files
| 파일 | 설명 |
|---|---|
| build-instructions.md | 빌드 환경 설정 및 실행 가이드 |
| unit-test-instructions.md | 단위 테스트 실행 지침 |
| integration-test-instructions.md | 통합 테스트 시나리오 및 실행 |
| performance-test-instructions.md | Locust 기반 성능 테스트 |
| build-and-test-summary.md | 이 문서 (전체 요약) |

## Story Coverage
| 스토리 | 단위 테스트 | 통합 테스트 |
|---|---|---|
| US-H01 (매장 등록) | ✅ | ✅ |
| US-H02 (매장 조회) | ✅ | ✅ |
| US-A01 (관리자 로그인) | ✅ | ✅ |
| US-A10 (계정 등록) | ✅ | ✅ |
| US-A04 (테이블 등록) | ✅ | ✅ |
| US-C01 (태블릿 로그인) | ✅ | ✅ |
| US-C02 (세션 관리) | ✅ | ✅ |
| US-A06 (이용 완료) | ✅ | ✅ |

## Next Steps
- Unit 2 (메뉴 관리) Construction 진행
- Unit 3 (주문 + SSE) Construction 진행
- Unit 4 (UI) Construction 진행
- 전체 Unit 완료 후 통합 E2E 테스트

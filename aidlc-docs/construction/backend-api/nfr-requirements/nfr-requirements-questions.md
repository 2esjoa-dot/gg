# NFR Requirements 질문 - Unit 1: Backend API

아래 질문에 답변해 주세요. 각 질문의 [Answer]: 태그 뒤에 선택지 문자를 입력해 주세요.

---

## Question 1
API 응답 시간 목표를 어떻게 설정하시겠습니까?

A) 일반 API 200ms 이내, 복잡한 쿼리(주문 내역 등) 500ms 이내
B) 일반 API 500ms 이내, 복잡한 쿼리 1초 이내 (요구사항 기준)
C) 일반 API 100ms 이내, 복잡한 쿼리 300ms 이내 (고성능)
D) Other (please describe after [Answer]: tag below)

[Answer]: B 

---

## Question 2
동시 접속자 500명 기준에서 데이터베이스 Connection Pool 전략은?

A) 기본 설정 (pool_size=5, max_overflow=10) — 소규모 시작 후 튜닝
B) 중간 설정 (pool_size=20, max_overflow=30) — 500명 동시 접속 대비
C) 대규모 설정 (pool_size=50, max_overflow=100) + PgBouncer 도입
D) Other (please describe after [Answer]: tag below)

[Answer]: B 

---

## Question 3
SSE 연결 관리 전략은? (관리자 대시보드 실시간 주문 수신)

A) In-memory 구독자 관리 (단일 서버, MVP 적합)
B) Redis Pub/Sub 기반 (다중 서버 확장 가능)
C) In-memory로 시작하되, Redis 전환 가능한 인터페이스 설계
D) Other (please describe after [Answer]: tag below)

[Answer]: C 

---

## Question 4
에러 처리 및 로깅 전략은?

A) 기본 Python logging + 콘솔 출력 (MVP)
B) 구조화된 JSON 로깅 + 파일 로테이션 (운영 대비)
C) 구조화된 JSON 로깅 + CloudWatch 연동 (AWS 통합)
D) Other (please describe after [Answer]: tag below)

[Answer]: B 

---

## Question 5
API Rate Limiting 적용 범위는?

A) 적용하지 않음 (MVP, 내부 네트워크 사용)
B) 인증 API만 적용 (로그인 시도 제한은 이미 구현)
C) 전체 API에 기본 Rate Limit 적용 (IP당 분당 60회 등)
D) Other (please describe after [Answer]: tag below)

[Answer]: B 

---

## Question 6
데이터베이스 마이그레이션 도구 선택은?

A) Alembic (SQLAlchemy 공식 마이그레이션 도구)
B) 수동 SQL 스크립트 관리
C) Other (please describe after [Answer]: tag below)

[Answer]: A 

---

## Question 7
테스트 프레임워크 및 전략은?

A) pytest + httpx (AsyncClient) — 단위 + 통합 테스트
B) pytest + httpx + pytest-cov (커버리지 포함)
C) pytest + httpx + pytest-cov + factory_boy (테스트 데이터 팩토리)
D) Other (please describe after [Answer]: tag below)

[Answer]: C 

---

## Question 8
이미지 업로드 파일 저장 시 파일명 충돌 방지 및 보안 전략은?

A) UUID 파일명 + 확장자 화이트리스트 (JPEG, PNG, WebP)
B) UUID 파일명 + 확장자 화이트리스트 + MIME 타입 검증
C) UUID 파일명 + 확장자 화이트리스트 + MIME 타입 검증 + 파일 크기 서버 측 재검증
D) Other (please describe after [Answer]: tag below)

[Answer]: C 

---

## Question 9
CORS (Cross-Origin Resource Sharing) 설정 전략은?

A) 개발 환경: 전체 허용 (*), 운영 환경: 특정 도메인만 허용
B) 모든 환경에서 특정 도메인만 허용 (환경변수로 관리)
C) 개발 환경: 전체 허용, 운영 환경: 설정 없음 (같은 도메인 배포)
D) Other (please describe after [Answer]: tag below)

[Answer]: A 

---

## Question 10
환경 설정 관리 방식은?

A) .env 파일 + python-dotenv (단순)
B) .env 파일 + Pydantic Settings (타입 검증 포함)
C) AWS Systems Manager Parameter Store 연동
D) Other (please describe after [Answer]: tag below)

[Answer]: B 

---

## Question 11
주문 번호 생성 시 동시성 처리 전략은? (매장별 일별 순번)

A) 데이터베이스 시퀀스 활용 (PostgreSQL SEQUENCE)
B) 애플리케이션 레벨 락 (asyncio.Lock)
C) SELECT MAX + 1 방식 (단순, 동시성 이슈 가능)
D) Redis INCR 활용 (원자적 증가)
E) Other (please describe after [Answer]: tag below)

[Answer]: A 

---

## Question 12
API 문서화 방식은?

A) FastAPI 자동 생성 Swagger UI만 사용
B) FastAPI Swagger + ReDoc + 커스텀 설명 추가
C) FastAPI Swagger + 별도 API 문서 (Markdown)
D) Other (please describe after [Answer]: tag below)

[Answer]: B 

---

# Application Design Plan - 테이블오더 서비스

## 개요
요구사항과 유저 스토리를 기반으로 시스템의 컴포넌트 구조, 서비스 레이어, 의존성을 설계합니다.

---

## 설계 질문

아래 질문에 답변해 주세요. 각 `[Answer]:` 태그 뒤에 선택한 옵션 문자를 입력해 주세요.

### Question 1
백엔드 API 구조를 어떻게 구성하시겠습니까?

A) 단일 FastAPI 앱 — 모든 API를 하나의 앱에서 라우터로 분리
B) 도메인별 분리 앱 — 고객 API / 관리자 API / 본사 API를 별도 FastAPI 앱으로 분리
C) 단일 앱 + 역할 기반 미들웨어 — 하나의 앱에서 인증 미들웨어로 접근 제어
X) Other (please describe after [Answer]: tag below)

[Answer]: C

---

### Question 2
프론트엔드 프로젝트 구조를 어떻게 구성하시겠습니까?

A) 모노레포 — 고객용/관리자용을 하나의 React 프로젝트에서 라우팅으로 분리
B) 별도 프로젝트 — 고객용 앱과 관리자용 앱을 완전히 분리된 프로젝트로 구성
C) 모노레포 + 공유 라이브러리 — 별도 앱이지만 공통 컴포넌트/유틸을 공유 패키지로 관리
X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 3
데이터 접근 계층(ORM/DB 접근)을 어떻게 구성하시겠습니까?

A) SQLAlchemy ORM — 모델 정의 + ORM 쿼리
B) SQLAlchemy Core — SQL 표현식 빌더 (ORM 없이)
C) Raw SQL + asyncpg — 직접 SQL 작성
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## 설계 실행 계획

### Step 1: 컴포넌트 식별
- [x] 백엔드 컴포넌트 정의 (도메인별 모듈)
- [x] 프론트엔드 컴포넌트 정의 (페이지/기능별)
- [x] 공통/인프라 컴포넌트 정의

### Step 2: 컴포넌트 메서드 정의
- [x] 각 백엔드 컴포넌트의 주요 메서드 시그니처
- [x] 서비스 레이어 메서드 정의
- [x] 입출력 타입 정의

### Step 3: 서비스 레이어 설계
- [x] 서비스 정의 및 책임 분배
- [x] 서비스 간 오케스트레이션 패턴
- [x] 트랜잭션 경계 정의

### Step 4: 의존성 및 통신 패턴
- [x] 컴포넌트 간 의존성 매트릭스
- [x] 데이터 흐름 다이어그램
- [x] API 통신 패턴 (REST, SSE)

### Step 5: 검증 및 완료
- [x] 설계 일관성 검증
- [x] 유저 스토리 커버리지 확인
- [x] 최종 문서 생성

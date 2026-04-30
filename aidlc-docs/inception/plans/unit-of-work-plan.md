# Unit of Work Plan - 테이블오더 서비스

## 개요
시스템을 개발 가능한 작업 단위(Unit of Work)로 분해합니다.

---

## 분해 질문

### Question 1
개발 순서 및 단위 분해 전략을 어떻게 하시겠습니까?

A) 계층별 분해 — 백엔드 먼저 완성 → 프론트엔드 순차 개발
B) 기능별 분해 — 주문 플로우 전체(백+프론트)를 하나의 단위로, 관리 기능을 다른 단위로
C) 배포 단위별 분해 — 백엔드 API(1개 단위) + 고객 앱(1개 단위) + 관리자 앱(1개 단위)
D) AI 판단에 맡김
X) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## AI 분석 결과

프로젝트 특성을 고려한 분해 전략: **계층별 분해 (A)** 선택

**근거:**
- 백엔드 API가 완성되어야 프론트엔드 개발이 가능 (의존성 방향이 명확)
- 단일 FastAPI 앱이므로 백엔드를 더 쪼갤 이유 없음
- 프론트엔드 2개는 독립 프로젝트이므로 병렬 개발 가능하지만, 순차 진행이 품질 관리에 유리
- Construction Phase에서 per-unit loop를 돌 때 백엔드 → 고객앱 → 관리자앱 순서가 자연스러움

**Unit 분해:**
1. **Unit 1: Backend API** — FastAPI 서버 전체 (모델, 서비스, 라우터, 인프라)
2. **Unit 2: Customer Frontend** — 고객용 React 앱
3. **Unit 3: Admin Frontend** — 관리자용 React 앱 (본사 기능 포함)

---

## 실행 계획

### Step 1: Unit 정의
- [x] Unit 1 (Backend API) 범위 및 책임 정의
- [x] Unit 2 (Customer Frontend) 범위 및 책임 정의
- [x] Unit 3 (Admin Frontend) 범위 및 책임 정의

### Step 2: Unit 의존성 매트릭스
- [x] Unit 간 의존성 정의
- [x] 개발 순서 결정
- [x] 통합 포인트 식별

### Step 3: Story-Unit 매핑
- [x] 각 유저 스토리를 Unit에 할당
- [x] 크로스 유닛 스토리 식별
- [x] 커버리지 검증

### Step 4: 코드 구조 정의 (Greenfield)
- [x] 각 Unit의 디렉토리 구조 정의
- [x] 공통 규약 정의

### Step 5: 검증
- [x] 모든 스토리 할당 확인
- [x] 의존성 순환 없음 확인
- [x] 최종 문서 생성

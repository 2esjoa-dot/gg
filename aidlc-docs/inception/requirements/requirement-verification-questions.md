# 테이블오더 서비스 - 요구사항 명확화 질문

제공해주신 요구사항 문서를 분석한 결과, 아래 항목들에 대한 추가 확인이 필요합니다.
각 질문의 `[Answer]:` 태그 뒤에 선택한 옵션 문자를 입력해 주세요.

---

## Question 1
백엔드 기술 스택으로 어떤 것을 사용하시겠습니까?

A) Node.js + Express (JavaScript/TypeScript)
B) Spring Boot (Java/Kotlin)
C) Django/FastAPI (Python)
D) NestJS (TypeScript)
X) Other (please describe after [Answer]: tag below)

[Answer]:  C

---

## Question 2
프론트엔드 기술 스택으로 어떤 것을 사용하시겠습니까?

A) React + TypeScript
B) Vue.js + TypeScript
C) Next.js (React 기반 풀스택 프레임워크)
D) Nuxt.js (Vue 기반 풀스택 프레임워크)
X) Other (please describe after [Answer]: tag below)

[Answer]: A or x 

---

## Question 3
데이터베이스로 어떤 것을 사용하시겠습니까?

A) PostgreSQL (관계형 데이터베이스)
B) MySQL/MariaDB (관계형 데이터베이스)
C) MongoDB (NoSQL 문서형 데이터베이스)
D) SQLite (경량 관계형 데이터베이스, 개발/소규모 운영용)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4
배포 환경은 어떻게 계획하고 계십니까?

A) AWS (EC2, RDS, S3 등)
B) Docker + Docker Compose (로컬/온프레미스)
C) Kubernetes (클라우드 또는 온프레미스)
D) 배포 환경은 나중에 결정 (개발 환경만 우선 구성)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 5
매장(Store) 관리 구조는 어떻게 되나요? (멀티테넌시 관련)

A) 단일 매장만 지원 (하나의 매장에서만 사용)
B) 다중 매장 지원 (하나의 시스템에서 여러 매장 관리, 각 매장은 독립적 데이터)
C) 다중 매장 + 본사 관리 (매장별 관리 + 본사에서 전체 관리)
X) Other (please describe after [Answer]: tag below)

[Answer]: c

---

## Question 6
메뉴 이미지 관리는 어떻게 하시겠습니까?

A) 외부 이미지 URL 직접 입력 (별도 이미지 서버 없음)
B) 서버에 이미지 파일 업로드 (로컬 파일 시스템 저장)
C) 클라우드 스토리지 업로드 (S3, GCS 등)
D) 이미지 기능은 MVP에서 제외 (텍스트만 표시)
X) Other (please describe after [Answer]: tag below)

[Answer]: b

---

## Question 7
동시 접속 사용자 규모는 어느 정도로 예상하십니까?

A) 소규모 (1개 매장, 동시 10~20명 이하)
B) 중규모 (1~5개 매장, 동시 50~100명)
C) 대규모 (10개 이상 매장, 동시 500명 이상)
D) 규모는 나중에 결정 (우선 소규모로 시작)
X) Other (please describe after [Answer]: tag below)

[Answer]: c

---

## Question 8
관리자 계정 관리는 어떻게 하시겠습니까?

A) 시스템 초기 설정 시 관리자 계정 1개 생성 (고정)
B) 매장별 관리자 계정 등록 기능 포함 (관리자가 직접 등록)
C) 슈퍼 관리자가 매장별 관리자 계정을 생성/관리
X) Other (please describe after [Answer]: tag below)

[Answer]: b

---

## Question 9
고객용 인터페이스의 접근 방식은 어떻게 되나요?

A) 태블릿 전용 (매장 내 고정 태블릿에서만 사용)
B) QR 코드 스캔 후 모바일 브라우저에서 접근 + 태블릿
C) 태블릿 전용 (요구사항 문서 기준, 모바일 접근은 향후 확장)
X) Other (please describe after [Answer]: tag below)

[Answer]: c

---

## Question 10
주문 상태 실시간 업데이트(고객 화면)에 대해 어떻게 하시겠습니까? 요구사항에 "선택사항"으로 표기되어 있습니다.

A) MVP에 포함 (SSE 또는 폴링으로 고객 화면에서도 실시간 상태 업데이트)
B) MVP에서 제외 (고객은 수동 새로고침으로 상태 확인)
C) 간단한 폴링 방식으로 구현 (30초 간격 자동 새로고침)
X) Other (please describe after [Answer]: tag below)

[Answer]: c

---

## Question 11
메뉴 관리 기능은 MVP에 포함하시겠습니까? 요구사항 문서의 MVP 범위에 메뉴 관리가 명시적으로 포함되어 있지 않습니다.

A) MVP에 포함 (관리자가 메뉴 CRUD 가능)
B) MVP에서 제외 (초기 데이터는 DB 시딩으로 처리)
C) 기본적인 메뉴 등록/수정만 포함 (삭제, 순서 조정은 제외)
X) Other (please describe after [Answer]: tag below)

[Answer]: a

---

## Question 12: Security Extensions
이 프로젝트에 보안 확장 규칙(SECURITY rules)을 적용하시겠습니까?

A) Yes — 모든 SECURITY 규칙을 blocking constraint로 적용 (프로덕션 수준 애플리케이션에 권장)
B) No — 모든 SECURITY 규칙 건너뛰기 (PoC, 프로토타입, 실험적 프로젝트에 적합)
X) Other (please describe after [Answer]: tag below)

[Answer]: b

---

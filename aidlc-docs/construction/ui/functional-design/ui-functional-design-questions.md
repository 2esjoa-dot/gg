# Unit 4 (UI) Functional Design - 질문

아래 질문에 답변해주세요. 각 질문의 [Answer]: 뒤에 선택지 알파벳을 입력하면 됩니다.
선택지가 맞지 않으면 마지막 옵션(Other)을 선택하고 설명을 추가해주세요.

---

## UI 디자인 톤 & 스타일

### Question 1
고객 앱(태블릿)의 전체적인 UI 톤은 어떤 방향인가요?

A) 미니멀/클린 — 여백 많고 깔끔한 스타일 (예: 토스, 배민)
B) 비주얼 중심 — 큰 이미지, 화려한 색상 (예: 요기요, 쿠팡이츠)
C) 키오스크 스타일 — 큰 버튼, 단순 레이아웃, 고대비 (예: 맥도날드 키오스크)
D) Other (please describe after [Answer]: tag below)

[Answer]: A. 토스 스타일로 해줘.

### Question 2
관리자 앱의 UI 톤은 어떤 방향인가요?

A) 대시보드 중심 — 데이터 밀도 높은 관리 화면 (예: Grafana, Admin LTE)
B) 심플 관리 — 깔끔한 폼/테이블 위주 (예: Notion, Linear)
C) 고객 앱과 동일한 톤 유지
D) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 3
CSS/스타일링 방식은 어떤 것을 선호하나요?

A) Tailwind CSS — 유틸리티 클래스 기반
B) CSS Modules — 컴포넌트별 스코프 CSS
C) styled-components — CSS-in-JS
D) 순수 CSS / SCSS
E) Other (please describe after [Answer]: tag below)

[Answer]: E. 어떤 스타일링 방식이 최적일지 니가 판단하고 진행해.

---

## 컴포넌트 라이브러리

### Question 4
UI 컴포넌트 라이브러리를 사용할 건가요?

A) 사용 안 함 — 모든 컴포넌트 직접 구현
B) 경량 라이브러리 — Headless UI, Radix UI 등 (스타일 없이 동작만)
C) 풀 라이브러리 — MUI, Ant Design, Chakra UI 등
D) Other (please describe after [Answer]: tag below)

[Answer]: D. 필요한 곳에서만 라이브러리 사용. 

---

## 상태 관리

### Question 5
전역 상태 관리 라이브러리를 사용할 건가요? (현재 useCart는 useState + localStorage로 구현됨)

A) 라이브러리 없음 — React 내장 (useState, useContext, useReducer)만 사용
B) Zustand — 경량 상태 관리
C) Redux Toolkit — 대규모 상태 관리
D) Jotai / Recoil — 원자적 상태 관리
E) Other (please describe after [Answer]: tag below)

[Answer]: E. 어떤 스타일링 방식이 최적일지 니가 판단하고 진행해.

---

## 장바구니 비즈니스 규칙

### Question 6
장바구니에 메뉴 아이템 최대 수량 제한이 필요한가요?

A) 제한 없음
B) 아이템당 최대 수량 제한 (예: 99개)
C) 장바구니 전체 아이템 수 제한 (예: 총 50개)
D) 아이템당 + 전체 모두 제한
E) Other (please describe after [Answer]: tag below)

[Answer]: B. 최대 50개 

### Question 7
장바구니 데이터의 유효 기간이 있나요? (세션 종료 시 장바구니 처리)

A) 세션과 무관 — 브라우저 로컬 스토리지에 계속 유지
B) 주문 성공 시에만 비움
C) 세션 종료(이용 완료) 시 자동 비움
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## 폼 유효성 검증

### Question 8
폼 유효성 검증 라이브러리를 사용할 건가요?

A) 라이브러리 없음 — 직접 구현
B) React Hook Form
C) Formik
D) Other (please describe after [Answer]: tag below)

[Answer]: D. 모르겠어. 니가 판단하고 해.

---

## 반응형 / 접근성

### Question 9
고객 앱은 태블릿 전용인데, 특정 해상도를 기준으로 설계할까요?

A) iPad 기준 (1024x768 / 1180x820)
B) 10인치 안드로이드 태블릿 기준 (1280x800)
C) 반응형 — 다양한 태블릿 크기 대응
D) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 10
다국어(i18n) 지원이 필요한가요?

A) 한국어만
B) 한국어 + 영어
C) 다국어 지원 (i18n 프레임워크 적용)
D) Other (please describe after [Answer]: tag below)

[Answer]: C. 한국어, 영어, 중국어, 일본어, 스페인어

---

## API Mock 전략

### Question 11
백엔드 완성 전 개발 시 Mock 전략은 어떻게 할까요?

A) MSW (Mock Service Worker) — 브라우저 레벨 API 모킹
B) JSON 파일 기반 — 정적 Mock 데이터
C) Vite proxy + 로컬 JSON Server
D) Mock 없이 — 백엔드 완성 후 연동
E) Other (please describe after [Answer]: tag below)

[Answer]: 모르겠어. 니가 판단해서 최적인걸로 선택해.

---

## 테마 / 다크모드

### Question 12
다크모드 지원이 필요한가요?

A) 라이트 모드만
B) 다크모드 지원 (시스템 설정 따름)
C) 사용자 토글 (라이트/다크 전환)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

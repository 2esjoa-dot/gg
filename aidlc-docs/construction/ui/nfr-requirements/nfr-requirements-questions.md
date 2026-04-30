# Unit 4 (UI) NFR Requirements - 질문

각 질문의 [Answer]: 뒤에 선택지 알파벳을 입력해주세요.

---

## 성능

### Question 1
페이지 초기 로딩 시간 목표는?

A) 1초 이내 (매우 빠름)
B) 2초 이내 (빠름)
C) 3초 이내 (보통)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 2
이미지 최적화 전략은?

A) lazy loading만 적용
B) lazy loading + WebP 변환 + 썸네일 리사이즈
C) CDN 사용 (CloudFront 등)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## 테스트

### Question 3
프론트엔드 테스트 범위는 어느 수준까지?

A) 단위 테스트만 (컴포넌트, 훅, 유틸)
B) 단위 + 통합 테스트 (페이지 레벨 렌더링)
C) 단위 + 통합 + E2E 테스트 (Playwright/Cypress)
D) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 4
테스트 프레임워크 선호도는?

A) Vitest + React Testing Library
B) Jest + React Testing Library
C) 니가 판단해
D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## 코드 품질

### Question 5
린터/포매터 설정은?

A) ESLint + Prettier (표준)
B) Biome (ESLint + Prettier 통합 대체)
C) ESLint만
D) Other (please describe after [Answer]: tag below)

[Answer]: D. 니가 판단해.

---

## 접근성

### Question 6
접근성 준수 수준은?

A) WCAG 2.1 AA (표준 — 대부분의 서비스 권장)
B) WCAG 2.1 A (최소)
C) 접근성 별도 고려 안 함
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## 번들 최적화

### Question 7
코드 스플리팅 전략은?

A) 페이지 단위 lazy loading (React.lazy + Suspense)
B) 페이지 + 모달 등 큰 컴포넌트도 lazy loading
C) 별도 최적화 안 함
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## 에러 모니터링

### Question 8
프론트엔드 에러 모니터링 도구를 사용할 건가요?

A) 사용 안 함 (콘솔 로그만)
B) Sentry
C) 나중에 추가 (MVP에서는 제외)
D) Other (please describe after [Answer]: tag below)

[Answer]: C

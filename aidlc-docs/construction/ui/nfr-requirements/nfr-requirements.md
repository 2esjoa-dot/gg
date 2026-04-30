# Unit 4 (UI) - 비기능 요구사항 (NFR)

## 1. 성능 요구사항

| ID | 요구사항 | 목표 | 측정 방법 |
|---|---|---|---|
| NFR-P01 | 페이지 초기 로딩 시간 | 2초 이내 | Lighthouse Performance Score |
| NFR-P02 | 페이지 전환 시간 | 300ms 이내 | React Router 전환 |
| NFR-P03 | 장바구니 조작 반응 시간 | 즉시 (16ms 이내) | 로컬 상태 업데이트 |
| NFR-P04 | 폴링 응답 처리 | 백그라운드, UI 블로킹 없음 | 30초 간격 비동기 |
| NFR-P05 | 이미지 로딩 | lazy loading + WebP + 썸네일 | Intersection Observer |
| NFR-P06 | 번들 사이즈 (초기) | 200KB 이하 (gzip) | Vite 빌드 분석 |

### 이미지 최적화 전략
- **lazy loading**: Intersection Observer 기반, 뷰포트 진입 시 로드
- **WebP 변환**: 서버(Unit 2)에서 업로드 시 WebP 변환, 프론트는 WebP 우선 요청
- **썸네일**: 메뉴 카드용 소형(300px), 상세용 대형(800px) 두 가지 사이즈
- **placeholder**: 이미지 로드 전 스켈레톤 UI 표시

## 2. 접근성 요구사항

| ID | 요구사항 | 기준 |
|---|---|---|
| NFR-A01 | WCAG 2.1 AA 준수 | 전체 페이지 |
| NFR-A02 | 최소 터치 타겟 44x44px | 모든 인터랙티브 요소 |
| NFR-A03 | 색상 대비 4.5:1 이상 | 텍스트 콘텐츠 |
| NFR-A04 | 키보드 네비게이션 | 모든 기능 접근 가능 |
| NFR-A05 | aria-label / aria-describedby | 아이콘 버튼, 상태 배지 |
| NFR-A06 | 포커스 관리 | 모달 열림/닫힘 시 포커스 트랩 |
| NFR-A07 | 스크린 리더 호환 | 시맨틱 HTML + ARIA |

> 참고: WCAG 완전 준수 검증은 보조 기술을 사용한 수동 테스트와 전문가 접근성 리뷰가 필요합니다.

## 3. 테스트 요구사항

| 레벨 | 범위 | 도구 | 커버리지 목표 |
|---|---|---|---|
| 단위 테스트 | 컴포넌트, 훅, 유틸, Store | Vitest + React Testing Library | 80% 이상 |
| 통합 테스트 | 페이지 레벨 렌더링, 라우팅 | Vitest + React Testing Library | 주요 플로우 |
| E2E 테스트 | 사용자 시나리오 전체 | Playwright | 핵심 시나리오 |

### 단위 테스트 대상
- **컴포넌트**: Button, Modal, Card, Badge, Input 등 공통 컴포넌트
- **훅**: useCart, useAuth, usePolling
- **Store**: cartStore, authStore (Zustand)
- **유틸**: format (금액, 날짜), localStorage 헬퍼

### 통합 테스트 대상
- CartPage: 장바구니 추가/삭제/수량변경 → 총액 계산
- SetupPage: 폼 입력 → 로그인 API 호출 → 리다이렉트
- OrderConfirmPage: 주문 확정 → 성공 오버레이 → 5초 리다이렉트

### E2E 테스트 시나리오
- 고객: 메뉴 조회 → 장바구니 담기 → 주문 확정 → 주문 내역 확인
- 관리자: 로그인 → 테이블 추가 → 메뉴 등록 → 이용 완료

## 4. 번들 최적화 요구사항

| ID | 요구사항 | 전략 |
|---|---|---|
| NFR-B01 | 페이지 단위 코드 스플리팅 | React.lazy + Suspense |
| NFR-B02 | 모달 등 큰 컴포넌트 lazy loading | 동적 import |
| NFR-B03 | 트리 쉐이킹 | Vite 기본 지원 (ESM) |
| NFR-B04 | 의존성 청크 분리 | vendor 청크 별도 분리 |
| NFR-B05 | i18n 언어 파일 동적 로드 | 선택 언어만 로드 |

## 5. 코드 품질 요구사항

| ID | 요구사항 | 도구 |
|---|---|---|
| NFR-Q01 | 린팅 | ESLint (react, typescript, a11y 플러그인) |
| NFR-Q02 | 포매팅 | Prettier |
| NFR-Q03 | 타입 안전성 | TypeScript strict 모드 |
| NFR-Q04 | import 정렬 | eslint-plugin-import |

## 6. 에러 모니터링

| ID | 요구사항 | 상태 |
|---|---|---|
| NFR-M01 | 에러 모니터링 도구 | MVP 이후 추가 예정 |
| NFR-M02 | 콘솔 에러 로깅 | MVP에서 기본 적용 |
| NFR-M03 | Error Boundary | React Error Boundary 적용 |

## 7. 반응형 요구사항

| ID | 요구사항 | 기준 |
|---|---|---|
| NFR-R01 | 고객 앱 | 768px ~ 1280px 태블릿 최적화 |
| NFR-R02 | 관리자 앱 | 1024px ~ 1920px PC/대형 태블릿 최적화 |
| NFR-R03 | 최소 지원 해상도 | 640px (소형 태블릿) |

# Build and Test 요약 - Unit 4 (UI)

## 빌드 상태
- **빌드 도구**: Vite 5.4 + TypeScript 5.5
- **빌드 상태**: 문서 생성 완료 (실행은 개발자가 수행)
- **빌드 산출물**: `dist/` (고객 앱), `dist/` (관리자 앱)

## 테스트 실행 요약

### 단위 테스트
- **총 테스트**: 20개
- **고객 앱**: 17개 (cartStore 9, authStore 3, format 5)
- **관리자 앱**: 3개 (authStore 3)
- **프레임워크**: Vitest + React Testing Library
- **커버리지 목표**: 80%

### 통합 테스트
- **시나리오**: 4개 (CartPage, SetupPage, OrderConfirmPage, LoginPage)
- **방식**: MSW Mock 기반 페이지 레벨 테스트

### E2E 테스트
- **시나리오**: 4개 (고객 주문 플로우, 장바구니 관리, 관리자 테이블, 메뉴 관리)
- **프레임워크**: Playwright
- **실행 모드**: Mock 모드 + 실제 백엔드 연동

### 성능 테스트
- **해당 없음**: 프론트엔드 UI 유닛 — Lighthouse 기반 성능 측정으로 대체
- **목표**: 초기 로딩 2초 이내, 번들 200KB 이하 (gzip)

## 생성된 문서

| 파일 | 설명 |
|---|---|
| build-instructions.md | 빌드 가이드 (의존성 설치, 빌드, 개발 서버) |
| unit-test-instructions.md | 단위 테스트 실행 가이드 |
| integration-test-instructions.md | 통합 테스트 시나리오 및 실행 가이드 |
| e2e-test-instructions.md | E2E 테스트 시나리오 및 Playwright 실행 가이드 |
| build-and-test-summary.md | 이 문서 |

## 실행 순서 (권장)

```
1. npm install (고객 앱 + 관리자 앱)
2. npm run test (단위 테스트 — 각 앱)
3. npm run build (빌드 검증 — 각 앱)
4. VITE_ENABLE_MOCKS=true npm run dev (Mock 모드 수동 검증)
5. npx playwright test (E2E — 통합 후)
```

## 전체 상태
- **빌드**: 문서 준비 완료 ✅
- **단위 테스트**: 20개 작성 완료 ✅
- **통합 테스트**: 시나리오 정의 완료 ✅
- **E2E 테스트**: 시나리오 정의 완료 ✅
- **Operations 준비**: Unit 4 완료, 다른 Unit 통합 대기

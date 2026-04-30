# Unit 4 (UI) - 기술 스택 결정

## 핵심 기술 스택

| 카테고리 | 기술 | 버전 | 근거 |
|---|---|---|---|
| 프레임워크 | React | ^18.3.0 | 기존 프로젝트 설정 유지 |
| 언어 | TypeScript | ^5.5.0 | strict 모드, 타입 안전성 |
| 빌드 도구 | Vite | ^5.4.0 | 기존 프로젝트 설정 유지 |
| 라우팅 | react-router-dom | ^6.26.0 | 기존 프로젝트 설정 유지 |

## 추가 의존성

### 스타일링
| 패키지 | 버전 | 용도 |
|---|---|---|
| tailwindcss | ^3.4.0 | 유틸리티 CSS |
| @tailwindcss/forms | ^0.5.0 | 폼 요소 기본 스타일 리셋 |
| postcss | ^8.4.0 | Tailwind 빌드 |
| autoprefixer | ^10.4.0 | 브라우저 호환 |

### 상태 관리
| 패키지 | 버전 | 용도 |
|---|---|---|
| zustand | ^4.5.0 | 전역 상태 관리 (cart, auth) |

### 폼 검증
| 패키지 | 버전 | 용도 |
|---|---|---|
| react-hook-form | ^7.53.0 | 폼 상태 관리 |
| @hookform/resolvers | ^3.9.0 | Zod 연동 |
| zod | ^3.23.0 | 스키마 유효성 검증 |

### i18n
| 패키지 | 버전 | 용도 |
|---|---|---|
| react-i18next | ^15.0.0 | React i18n 통합 |
| i18next | ^23.15.0 | i18n 코어 |
| i18next-browser-languagedetector | ^8.0.0 | 브라우저 언어 감지 |

### UI 보조
| 패키지 | 버전 | 용도 |
|---|---|---|
| @dnd-kit/core | ^6.1.0 | 드래그앤드롭 (메뉴 순서) |
| @dnd-kit/sortable | ^8.0.0 | 정렬 가능 리스트 |
| date-fns | ^4.1.0 | 날짜 포맷/필터 |

### API Mock
| 패키지 | 버전 | 용도 | devDependency |
|---|---|---|---|
| msw | ^2.4.0 | API 모킹 | ✅ |

## 테스트 도구

| 패키지 | 버전 | 용도 |
|---|---|---|
| vitest | ^2.1.0 | 테스트 러너 |
| @testing-library/react | ^16.0.0 | 컴포넌트 테스트 |
| @testing-library/jest-dom | ^6.5.0 | DOM 매처 |
| @testing-library/user-event | ^14.5.0 | 사용자 이벤트 시뮬레이션 |
| @vitest/coverage-v8 | ^2.1.0 | 커버리지 |
| @playwright/test | ^1.47.0 | E2E 테스트 |
| jsdom | ^25.0.0 | DOM 환경 |

## 코드 품질 도구

| 패키지 | 버전 | 용도 |
|---|---|---|
| eslint | ^9.10.0 | 린팅 |
| prettier | ^3.3.0 | 포매팅 |
| eslint-plugin-react | ^7.36.0 | React 규칙 |
| eslint-plugin-react-hooks | ^4.6.0 | Hooks 규칙 |
| eslint-plugin-jsx-a11y | ^6.10.0 | 접근성 규칙 |
| eslint-plugin-import | ^2.30.0 | import 정렬 |
| typescript-eslint | ^8.6.0 | TS 린팅 |

## 기술 결정 근거

### Tailwind CSS 선택 이유
- 토스 스타일 미니멀 UI에 유틸리티 클래스가 빠르게 대응
- 병렬 개발 시 CSS 클래스 충돌 없음 (스코프 문제 없음)
- 반응형 브레이크포인트 내장 (`sm:`, `md:`, `lg:`, `xl:`)
- Vite와 빌드 통합 간단
- 사용하지 않는 CSS 자동 제거 (PurgeCSS 내장)

### Zustand 선택 이유
- 기존 useCart 훅의 useState + localStorage 패턴과 유사한 API
- 보일러플레이트 최소 (Redux 대비 80% 이상 코드 감소)
- `persist` 미들웨어로 localStorage 동기화 내장
- 번들 사이즈 ~1KB (gzip)
- React 외부에서도 상태 접근 가능 (MSW 핸들러 등)

### Vitest 선택 이유
- Vite 프로젝트와 설정 공유 (vite.config.ts 재사용)
- Jest 호환 API (마이그레이션 용이)
- ESM 네이티브 지원
- HMR 기반 빠른 테스트 재실행

### React Hook Form + Zod 선택 이유
- 비제어 컴포넌트 기반으로 리렌더링 최소화
- 관리자 앱에 폼이 6개 이상 (로그인, 테이블 추가, 메뉴 CRUD, 계정 등록, 매장 등록)
- Zod 스키마를 타입과 유효성 검증에 동시 사용 (DRY)
- TypeScript 타입 추론 자동

### ESLint + Prettier 선택 이유
- 가장 넓은 생태계, 팀 표준 설정 공유 용이
- jsx-a11y 플러그인으로 접근성 린팅 자동화
- 대부분의 React 프로젝트 표준

## 프로젝트 구조 (최종)

### 고객 앱
```
frontend-customer/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── i18n.ts                 # i18n 설정
│   ├── api/                    # API 클라이언트
│   ├── components/             # 공통 UI 컴포넌트
│   ├── pages/                  # 페이지 컴포넌트
│   ├── hooks/                  # 커스텀 훅
│   ├── store/                  # Zustand 스토어
│   ├── types/                  # TypeScript 타입
│   ├── utils/                  # 유틸리티
│   ├── locales/                # 번역 파일 (ko, en, zh, ja, es)
│   └── mocks/                  # MSW 핸들러 + Mock 데이터
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.ts
├── postcss.config.js
├── eslint.config.js
├── .prettierrc
└── playwright.config.ts
```

### 관리자 앱
```
frontend-admin/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── i18n.ts
│   ├── api/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── store/
│   ├── types/
│   ├── utils/
│   ├── locales/
│   └── mocks/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.ts
├── postcss.config.js
├── eslint.config.js
├── .prettierrc
└── playwright.config.ts
```

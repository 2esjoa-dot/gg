# Build Instructions - Unit 4 (UI)

## 사전 요구사항
- **Node.js**: v18.x 이상
- **npm**: v9.x 이상
- **디스크 공간**: 500MB 이상 (node_modules)

## 빌드 순서

### 1. 고객 앱 의존성 설치
```bash
cd frontend-customer
npm install
```

### 2. 관리자 앱 의존성 설치
```bash
cd frontend-admin
npm install
```

### 3. 고객 앱 빌드
```bash
cd frontend-customer
npm run build
```
- **예상 출력**: `dist/` 디렉토리에 정적 파일 생성
- **예상 번들 사이즈**: 초기 로드 200KB 이하 (gzip)

### 4. 관리자 앱 빌드
```bash
cd frontend-admin
npm run build
```
- **예상 출력**: `dist/` 디렉토리에 정적 파일 생성

## 개발 서버 실행

### 고객 앱 (Mock 모드)
```bash
cd frontend-customer
VITE_ENABLE_MOCKS=true npm run dev
```
- URL: http://localhost:5173

### 관리자 앱 (Mock 모드)
```bash
cd frontend-admin
VITE_ENABLE_MOCKS=true npm run dev
```
- URL: http://localhost:5174

### 백엔드 연동 모드
```bash
cd frontend-customer
npm run dev
```
- 백엔드가 http://localhost:8000 에서 실행 중이어야 함
- Vite proxy가 `/api` 요청을 백엔드로 전달

## 트러블슈팅

### 의존성 설치 실패
- `rm -rf node_modules package-lock.json && npm install`

### TypeScript 컴파일 에러
- `npx tsc --noEmit` 으로 타입 에러 확인
- `tsconfig.json`의 `strict: true` 설정 확인

### Tailwind 스타일 미적용
- `tailwind.config.ts`의 `content` 경로 확인
- `src/index.css`에 `@tailwind` 디렉티브 확인

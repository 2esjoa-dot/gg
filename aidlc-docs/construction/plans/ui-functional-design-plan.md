# Functional Design Plan - Unit 4: UI

## 개요
고객 앱(frontend-customer)과 관리자 앱(frontend-admin)의 UI 컴포넌트, 상태 관리, 사용자 인터랙션 플로우를 상세 설계합니다.

## 범위
- **고객 앱**: SetupPage, CartPage, OrderConfirmPage, OrderHistoryPage, MenuPage(UI 파트)
- **관리자 앱**: LoginPage, TableManagePage, MenuManagePage, AccountPage, HQStorePage
- **공통**: 상태 관리, API 클라이언트, 공통 컴포넌트, 타입 정의

## 실행 계획

### Step 1: 프론트엔드 컴포넌트 설계
- [x] 고객 앱 컴포넌트 계층 구조 정의
- [x] 관리자 앱 컴포넌트 계층 구조 정의
- [x] 공통 UI 컴포넌트 정의 (Button, Card, Modal, Loading, ErrorMessage 등)
- [x] 각 컴포넌트의 Props/State 인터페이스 정의

### Step 2: 사용자 인터랙션 플로우
- [x] 고객 앱 화면 전환 플로우 (라우팅)
- [x] 관리자 앱 화면 전환 플로우 (라우팅 + 인증 가드)
- [x] 폼 유효성 검증 규칙
- [x] 에러 처리 및 사용자 피드백 패턴

### Step 3: 상태 관리 설계
- [x] 고객 앱 상태 관리 (장바구니, 인증, 세션)
- [x] 관리자 앱 상태 관리 (인증, 주문 데이터)
- [x] 로컬 스토리지 동기화 전략
- [x] API 연동 포인트 및 Mock 전략

### Step 4: 비즈니스 규칙 (프론트엔드)
- [x] 장바구니 비즈니스 로직 (수량 제한, 총액 계산)
- [x] 폴링 로직 (30초 간격 주문 상태 조회)
- [x] 자동 로그인 / 토큰 만료 처리
- [x] 5초 리다이렉트 로직 (주문 성공 후)

### Step 5: 질문 수집 및 분석
- [x] 사용자 답변 수집
- [x] 모호성 검증
- [x] 필요 시 명확화 질문

### Step 6: 아티팩트 생성
- [x] frontend-components.md (컴포넌트 계층, Props, State)
- [x] business-logic-model.md (프론트엔드 비즈니스 로직)
- [x] business-rules.md (프론트엔드 유효성/상태 규칙)

# 테이블오더 서비스 - 서비스 레이어 설계

## 서비스 아키텍처 개요

```
Router Layer (API Endpoints)
       |
       v
Service Layer (Business Logic + Orchestration)
       |
       v
Repository Layer (Data Access)
       |
       v
Database (PostgreSQL)
```

---

## 1. 서비스 정의 및 책임

### AuthService
- **책임**: 인증/인가 전체 관리
- **핵심 로직**:
  - JWT 토큰 발급 (16시간 만료)
  - 비밀번호 bcrypt 해싱/검증
  - 로그인 시도 제한 (5회 실패 → 15분 차단)
  - 역할 기반 접근 제어 (tablet, store_admin, hq_admin)
- **의존**: UserRepository, StoreRepository

### StoreService
- **책임**: 매장 라이프사이클 관리
- **핵심 로직**:
  - 매장 등록 시 고유 식별자 검증
  - 매장 정보 조회
- **의존**: StoreRepository

### TableService
- **책임**: 테이블 등록 및 상태 관리
- **핵심 로직**:
  - 테이블 번호 중복 검증 (매장 내)
  - 테이블 비밀번호 해싱
  - 테이블 현재 상태 집계 (활성 세션, 총 주문액)
- **의존**: TableRepository, SessionService, OrderService

### SessionService
- **책임**: 테이블 세션 라이프사이클
- **핵심 로직**:
  - 첫 주문 시 세션 자동 생성
  - 16시간 유효성 관리
  - 이용 완료 시 세션 종료 + 주문 이력 이동
- **의존**: SessionRepository, OrderRepository

### MenuService
- **책임**: 메뉴 데이터 관리
- **핵심 로직**:
  - 메뉴 CRUD + 유효성 검증
  - 카테고리별 그룹화
  - 노출 순서 관리
  - 이미지 파일 연동
- **의존**: MenuRepository, FileService

### OrderService
- **책임**: 주문 처리 전체 관리
- **핵심 로직**:
  - 주문 생성 시 세션 확인/생성 연동
  - 주문 상태 전이 (대기중 → 준비중 → 완료)
  - 주문 삭제 시 총액 재계산
  - SSE 이벤트 발행 트리거
- **의존**: OrderRepository, SessionService, SSEService

### SSEService
- **책임**: 실시간 이벤트 관리
- **핵심 로직**:
  - 매장별 SSE 연결 관리 (구독/해제)
  - 주문 이벤트 브로드캐스트
  - 연결 끊김 감지 및 정리
- **의존**: 없음 (인메모리 이벤트 큐)

### FileService
- **책임**: 파일 저장/조회
- **핵심 로직**:
  - 이미지 파일 로컬 저장
  - 파일 경로 → URL 변환
- **의존**: 없음 (파일 시스템)

---

## 2. 서비스 오케스트레이션 패턴

### 주문 생성 플로우
```
CustomerRouter.create_order()
  → OrderService.create_order()
    → SessionService.get_or_create_session()  // 세션 확인/생성
    → OrderRepository.create()                // 주문 저장
    → SSEService.publish_order_event()        // 관리자에게 실시간 알림
    → return Order
```

### 이용 완료 플로우
```
AdminRouter.complete_table()
  → SessionService.end_session()
    → SessionRepository.close_session()       // 세션 종료
    → OrderRepository.archive_orders()        // 주문 이력 이동
    → SSEService.publish_status_event()       // 대시보드 업데이트
    → return success
```

### 주문 상태 변경 플로우
```
AdminRouter.update_order_status()
  → OrderService.update_order_status()
    → OrderRepository.update()                // 상태 변경
    → SSEService.publish_status_event()       // 대시보드 업데이트
    → return Order
```

---

## 3. 트랜잭션 경계

| 오퍼레이션 | 트랜잭션 범위 | 설명 |
|---|---|---|
| 주문 생성 | 세션 생성 + 주문 + 주문항목 | 하나라도 실패 시 전체 롤백 |
| 이용 완료 | 세션 종료 + 주문 아카이브 | 원자적 처리 |
| 주문 삭제 | 주문 삭제 + 주문항목 삭제 | cascade |
| 메뉴 삭제 | 메뉴 삭제 (주문 참조 유지) | soft delete 고려 |
| 매장 등록 | 매장 생성 | 단일 엔티티 |

---

## 4. 에러 처리 전략

| 에러 유형 | HTTP Status | 처리 방식 |
|---|---|---|
| 인증 실패 | 401 | 에러 메시지 반환, 시도 횟수 증가 |
| 권한 없음 | 403 | 역할 불일치 에러 |
| 리소스 없음 | 404 | 엔티티 미발견 |
| 유효성 검증 실패 | 422 | 필드별 에러 상세 |
| 중복 데이터 | 409 | 충돌 에러 (매장코드, 테이블번호, 사용자명) |
| 서버 에러 | 500 | 로깅 + 일반 에러 메시지 |

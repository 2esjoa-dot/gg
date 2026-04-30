# 테이블오더 서비스 - Unit of Work 의존성 (4명 병렬)

## 의존성 매트릭스

| Unit | Unit 1 (Foundation) | Unit 2 (Menu) | Unit 3 (Order) | Unit 4 (UI) |
|---|---|---|---|---|
| **Unit 1** | — | 없음 | 없음 | 없음 |
| **Unit 2** | DB 구조 공유 | — | 없음 | 없음 |
| **Unit 3** | SessionService 인터페이스 | 없음 | — | 없음 |
| **Unit 4** | API 스펙 (Mock) | API 스펙 (Mock) | API 스펙 (Mock) | — |

---

## 병렬 개발 가능 조건

1. **Unit 1이 Day 1에 공유할 것:**
   - DB 마이그레이션 기반 구조 (alembic 설정)
   - SessionService 인터페이스 (메서드 시그니처)
   - OpenAPI 스펙 초안 (전체 엔드포인트 목록)
   - 공통 모듈 (config, database, exceptions, security utils)

2. **나머지 Unit은 독립 개발:**
   - Unit 2: 메뉴 모델/API를 독립적으로 개발
   - Unit 3: 주문 모델/API를 독립적으로 개발 (세션은 인터페이스 Mock)
   - Unit 4: API Mock 서버로 UI 개발

---

## 통합 순서

```
Phase 1 (병렬): 각 Unit 독립 개발 + 단위 테스트
Phase 2 (통합): Unit 1 + Unit 2 + Unit 3 백엔드 머지
Phase 3 (연동): Unit 4 UI → 실제 API 연동
Phase 4 (E2E): 전체 플로우 테스트
```

---

## 브랜치 전략

| Unit | 브랜치명 | 머지 대상 |
|---|---|---|
| Unit 1 | `unit/1-foundation` | `develop` |
| Unit 2 | `unit/2-menu` | `develop` |
| Unit 3 | `unit/3-order` | `develop` |
| Unit 4 | `unit/4-ui` | `develop` |

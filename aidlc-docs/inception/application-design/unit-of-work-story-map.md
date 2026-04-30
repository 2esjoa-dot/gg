# 테이블오더 서비스 - Story-Unit 매핑 (4명 병렬)

## 매핑 요약

| Unit | 담당 | 스토리 |
|---|---|---|
| Unit 1: Foundation | 개발자 1 | US-H01, US-H02, US-A01, US-A10, US-A04, US-C01, US-C02, US-A06 |
| Unit 2: Menu | 개발자 2 | US-A08, US-A09, US-C03 |
| Unit 3: Order | 개발자 3 | US-C05, US-C06, US-A02, US-A03, US-A05, US-A07 |
| Unit 4: UI | 개발자 4 | US-C04 + 전체 스토리의 프론트엔드 UI |

---

## Unit 1: Foundation — 상세 매핑

| Story | 구현 내용 |
|---|---|
| US-H01 | 매장 등록 API |
| US-H02 | 매장 목록 조회 API |
| US-A01 | 관리자 로그인 API (JWT, bcrypt, 잠금) |
| US-A10 | 관리자 계정 등록 API |
| US-A04 | 테이블 등록 API |
| US-C01 | 태블릿 로그인 API |
| US-C02 | 세션 생성/조회/만료 로직 |
| US-A06 | 이용 완료 API (세션 종료) |

---

## Unit 2: Menu — 상세 매핑

| Story | 구현 내용 |
|---|---|
| US-A08 | 메뉴 CRUD API + 이미지 업로드 |
| US-A09 | 메뉴 순서 변경 API |
| US-C03 | 고객 메뉴 조회 API + 메뉴 페이지 UI |

---

## Unit 3: Order — 상세 매핑

| Story | 구현 내용 |
|---|---|
| US-C05 | 주문 생성 API |
| US-C06 | 세션별 주문 조회 API |
| US-A02 | SSE 스트림 + 관리자 대시보드 UI |
| US-A03 | 주문 상태 변경 API |
| US-A05 | 주문 삭제 API |
| US-A07 | 과거 주문 내역 조회 API |

---

## Unit 4: UI — 상세 매핑

| Story | 구현 내용 |
|---|---|
| US-C04 | 장바구니 UI (로컬 스토리지, 수량 조절, 총액) |
| US-C01 (UI) | 자동 로그인 UI, 초기 설정 페이지 |
| US-C05 (UI) | 주문 확인 페이지, 5초 리다이렉트 |
| US-C06 (UI) | 주문 내역 페이지, 30초 폴링 |
| US-A01 (UI) | 관리자 로그인 페이지 |
| US-A04 (UI) | 테이블 관리 페이지 |
| US-A06 (UI) | 이용 완료 UI, 확인 모달 |
| US-A07 (UI) | 과거 내역 모달, 날짜 필터 |
| US-A08 (UI) | 메뉴 관리 페이지 (CRUD 폼) |
| US-A09 (UI) | 메뉴 순서 드래그앤드롭 |
| US-A10 (UI) | 계정 등록 폼 |
| US-H01 (UI) | 매장 등록 페이지 |
| US-H02 (UI) | 매장 목록 페이지 |

---

## 커버리지 검증

- 전체 스토리: 18개
- 백엔드 커버: 18/18 (Unit 1 + 2 + 3) ✅
- 프론트엔드 커버: 18/18 (Unit 2 일부 + Unit 3 일부 + Unit 4) ✅
- 미할당: 0개 ✅

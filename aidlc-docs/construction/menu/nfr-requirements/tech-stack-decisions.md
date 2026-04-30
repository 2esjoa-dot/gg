# Tech Stack Decisions - Unit 2: Menu

## 백엔드

| 항목 | 선택 | 근거 |
|---|---|---|
| 프레임워크 | FastAPI | 프로젝트 전체 기술 스택 |
| ORM | SQLAlchemy (async) | 프로젝트 전체 기술 스택 |
| DB | PostgreSQL | 프로젝트 전체 기술 스택 |
| 파일 저장 | 로컬 파일시스템 | MVP 단순화, FileService 인터페이스로 추후 S3 교체 가능 |
| 이미지 처리 | 없음 (원본 저장) | MVP, CSS 리사이징으로 충분 |
| 캐싱 | 없음 | 데이터 규모가 작아 불필요 |
| 파일 서빙 | FastAPI StaticFiles | 별도 Nginx 없이 직접 서빙 (MVP) |
| 테스트 | pytest + pytest-asyncio | 비동기 테스트 지원 |

## 프론트엔드 (고객 메뉴 페이지)

| 항목 | 선택 | 근거 |
|---|---|---|
| 프레임워크 | React + TypeScript | 프로젝트 전체 기술 스택 |
| 빌드 도구 | Vite | 프로젝트 전체 기술 스택 |
| 상태 관리 | React 기본 (useState/useEffect) | 단순 조회 화면, 외부 의존성 최소화 |
| HTTP 클라이언트 | fetch API 또는 기존 api/client.ts | 프로젝트 기존 패턴 활용 |
| 스타일링 | CSS Modules 또는 인라인 | 프로젝트 기존 패턴 따름 |

## 의존성 요약

### 백엔드 (추가 필요 없음)
- 기존 requirements.txt의 FastAPI, SQLAlchemy, python-multipart로 충분
- python-multipart: 파일 업로드 처리 (이미 포함)

### 프론트엔드 (추가 필요 없음)
- 기존 package.json의 React, TypeScript, Vite로 충분
- 외부 상태 관리 라이브러리 불필요

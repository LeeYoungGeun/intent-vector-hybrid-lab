# 바이브코딩 프롬프트 (API 테스트 템플릿 구현용)

아래 프롬프트는 “이 리포지토리 뼈대(md/spec/templates)”를 기반으로, 실제 실행 가능한 코드(CLI + 리포트 생성)를 바이브코딩으로 만들기 위한 **단일 마스터 프롬프트**입니다.

---

## 시스템(역할/원칙)
당신은 검색/추천/LLM 파이프라인을 만드는 시니어 엔지니어다. 목표는 “의도 기반 벡터/하이브리드 검색”의 5단계(임베딩/벡터리트리벌/하이브리드/리랭킹/필터링)를 동일한 테스트셋과 지표로 비교하는 **API 테스트 전용 템플릿**을 구현하는 것이다.

제약:
- 리포지토리 루트에 `.venv` 하나만 사용(하위 폴더 venv 금지)
- API 키는 `.env` 또는 환경변수로만 주입(코드/로그/리포에 노출 금지)
- 모든 실행은 루트에서 가능한 단일 CLI로 제공
- 결과는 JSONL(1쿼리=1라인) + 요약 Markdown 리포트로 저장

---

## 입력(이미 존재하는 파일)
- `docs/*.md`: 요구사항/설계/지표/런북
- `specs/*.md`: 인터페이스/로그 스키마
- `templates/*.yaml|tsv`: 예시 설정/테스트케이스

---

## 구현 요구사항(반드시)

### 1) 프로젝트 스택
- Python 3.11+
- HTTP 클라이언트: httpx
- 설정: pyyaml + pydantic
- 결과 저장: jsonlines
- 리포트: markdown 생성(단순 텍스트로 충분)

### 2) 폴더/모듈 구조(권장)
- `src/`
  - `core/` (파이프라인/타입/로깅)
  - `adapters/` (openai, cohere, voyage, pinecone, qdrant, elastic 등)
  - `eval/` (지표 계산)
  - `cli.py` (엔트리)
- `runs/` (실행 결과 저장)
- `reports/` (요약 리포트)

### 3) CLI 기능
- `python -m src.cli run --pipeline <id> --vendor-set <id> --testcases <path>`
- 출력:
  - `runs/<run_id>/detail.jsonl`
  - `reports/<run_id>/summary.md`

### 4) 단계별 처리
- embedding 단계: intent_text를 벡터로
- retrieval 단계: VectorDB top_k 후보
- bm25 단계: BM25 top_k 후보
- fusion 단계: RRF 또는 가중합(둘 중 하나는 구현, 나머지는 옵션)
- rerank 단계: 상위 N개 재정렬
- filter 단계:
  - min_score 컷
  - metadata 규칙(카테고리 불일치 제거)
  - dropped에 이유(reasons) 기록

### 5) 평가
- 최소: Precision@K, Recall@K, MRR
- 가능하면: nDCG@K

### 6) 개발 편의
- `Makefile` 제공: setup/run/report
- `.env.example` 제공

---

## 단계별 작업 지시(바이브코딩용)
1) 위 구조로 파일을 생성하고, 각 모듈은 **작게** 시작한다.
2) 먼저 “Mock Adapter”(외부 API 없이 더미 데이터)로 end-to-end를 통과시킨다.
3) 그 다음 OpenAI Embedding, Qdrant(또는 Pinecone), Elasticsearch(또는 OpenSearch), Cohere Rerank 어댑터를 순차로 붙인다.
4) 각 어댑터는 실패 시 오류를 명확히 표준화된 예외로 반환한다.
5) 최종적으로 docs/spec/templates의 규격과 출력 스키마가 일치하는지 점검한다.

---

## 출력 요구
- 실제로 실행 가능한 코드 전체
- 최소 예제 실행법을 README에 추가
- 샘플 실행 결과(더미) 1회 생성할 수 있게 제공


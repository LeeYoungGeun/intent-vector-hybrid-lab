# 로컬 실행/환경 셋업(권장 스택)

> 이 문서는 코드가 생성된 이후(바이브코딩 결과물) 기준으로 바로 실행 가능한 형태를 목표로 합니다.

## 권장 스택
- Python 3.11+
- 패키지: `httpx`, `pydantic`, `pyyaml`, `rich`, `pandas`(선택), `numpy`(선택)
- 실행 방식: CLI 우선(추가로 FastAPI 서버 옵션)

## 환경 변수(예시)
- `OPENAI_API_KEY`
- `COHERE_API_KEY`
- `GOOGLE_API_KEY` / Vertex AI 관련 변수
- `PINECONE_API_KEY`
- `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_API_KEY`
- `ELASTIC_URL`, `ELASTIC_API_KEY`

`.env`는 커밋하지 말고, `templates/.env.example`를 복사해 사용합니다.

## 실행 시나리오(코드 생성 후)
- 테스트셋 준비: `data/testcases.tsv` (본 템플릿에서는 스펙만 제공)
- 파이프라인 실행: `python -m app.cli run --pipeline pipelines/default.yaml --testset data/testcases.tsv`
- 리포트 생성: `python -m app.cli report --run-id <id>`

## 최소 성공 기준
- (1)~(5) 단계별 결과가 동일한 JSON 스키마로 저장
- 단일 벤더(예: OpenAI + Qdrant + Cohere rerank)로 end-to-end 1회 실행 가능
- 리트리벌 지표(Recall@K, Precision@K)와 랭킹 지표(nDCG/MRR) 산출


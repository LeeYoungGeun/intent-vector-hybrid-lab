# 작업 백로그(권장 순서)

## Phase 0 — 스캐폴딩
- [ ] Python 프로젝트 초기화(.venv, requirements/pyproject)
- [ ] src/cli.py 생성 및 기본 커맨드 파싱
- [ ] runs/, reports/ 출력 디렉토리 생성

## Phase 1 — Mock로 E2E 통과
- [ ] MockEmbeddingProvider
- [ ] MockVectorRetriever
- [ ] MockBM25Retriever
- [ ] Fusion(RRF) 1개 구현
- [ ] MockReranker
- [ ] FilterEngine(min_score + category rule)
- [ ] detail.jsonl 스키마로 저장
- [ ] summary.md 리포트 생성

## Phase 2 — 실제 어댑터 연결(최소)
- [ ] OpenAI Embedding 어댑터
- [ ] Qdrant 또는 Pinecone VectorRetriever
- [ ] Elasticsearch 또는 OpenSearch BM25
- [ ] Cohere Rerank

## Phase 3 — 튜닝/확장
- [ ] 하이브리드 가중합(alpha) 옵션
- [ ] 캐시(임베딩/리트리벌) 옵션
- [ ] 비용 추정(벤더별 usage 기반)
- [ ] 에러 분석 리포트(오탐 유형 분류)

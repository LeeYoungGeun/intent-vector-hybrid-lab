# 바이브코딩 작업 분해(TASK_BREAKDOWN)

## Phase 0: 스캐폴딩
- `app/` 패키지 생성
- `app/cli.py`에 `run`, `report`, `smoke` 서브커맨드

## Phase 1: 데이터/스키마
- `TestCase`, `Candidate`, `StageResult` Pydantic 모델
- TSV 로더, catalog 로더

## Phase 2: 어댑터 인터페이스
- `EmbeddingAdapter`, `VectorStoreAdapter`, `HybridSearchAdapter`, `RerankAdapter`
- 샘플 더미 어댑터(외부 API 없이도 로컬 동작)

## Phase 3: 파이프라인 실행기
- 단계별 실행/타이머/로그
- 실패 시 graceful degrade(예: rerank 실패하면 fused 결과를 그대로 사용)

## Phase 4: 평가
- Recall@K, Precision@K, MRR, nDCG 구현
- 실패 케이스 추출(오탐 상위)

## Phase 5: 벤더 어댑터 1개씩 추가
- OpenAI Embedding
- Qdrant 또는 Pinecone retrieval
- Cohere rerank


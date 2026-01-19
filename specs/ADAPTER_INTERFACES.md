# 어댑터 인터페이스 스펙(ADAPTER_INTERFACES)

## 설계 원칙
- 벤더별 구현은 달라도 **입출력 스키마는 동일**
- 장애/타임아웃/레이트리밋은 표준 에러 타입으로 래핑

## 인터페이스(개념)
### EmbeddingAdapter
- `embed(text: str) -> vector: List[float]`

### VectorStoreAdapter
- `query(vector: List[float], top_k: int, filter: dict | None) -> List[Candidate]`
- `upsert(docs: List[Doc])` (옵션)

### HybridSearchAdapter
- `search(text: str, vector: List[float] | None, top_k: int, filter: dict | None) -> List[Candidate]`

### RerankAdapter
- `rerank(query: str, candidates: List[Candidate], top_n: int) -> List[Candidate]`

### FilterAdapter (또는 Pipeline 내 RuleEngine)
- `apply(candidates: List[Candidate], ruleset: dict) -> (final: List[Candidate], rejected: List[Rejected])`

## Candidate 최소 스키마
- `doc_id: str`
- `text: str` (또는 title/description)
- `payload: dict` (category, price, tags, …)
- `scores: {dense?, sparse?, fused?, rerank?}`


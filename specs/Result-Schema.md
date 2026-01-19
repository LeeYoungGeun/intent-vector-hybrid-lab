# Result Schema (로그/결과 JSON 규격)

## 목적
- 단계별 결과를 **JSONL 한 줄 1쿼리**로 남겨 재현성/분석성을 확보합니다.

## 필수 필드(권장)
- run_id: string
- pipeline_id: string
- vendor_set_id: string
- query:
  - id
  - raw_text
  - intent_text
- stages:
  - embedding: {model, latency_ms, usage, vector_dim}
  - vector_retrieval: {engine, top_k, latency_ms, candidates: [...]}
  - bm25: {engine, top_k, latency_ms, candidates: [...]}
  - fusion: {method, params, latency_ms, candidates: [...]}
  - rerank: {model, latency_ms, candidates: [...]}
  - filter: {ruleset_id, min_score, dropped: [...], final: [...]}
- eval:
  - expected_doc_ids: [...]
  - metrics: {precision_at_k, recall_at_k, mrr, ndcg_at_k, ...}


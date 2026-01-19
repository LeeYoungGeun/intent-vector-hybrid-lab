# 파이프라인 스펙(PIPELINE_SPEC)

## 목적
(1)~(5) 단계를 “교체 가능한 모듈”로 표준화하여 벤더/모델 비교를 빠르게 수행합니다.

## 단계 정의
### Stage 1: Embedding
- 입력: `intent_text` (의도 정제 후 문장)
- 출력: `query_vector: float[]`
- 로그: 모델명, 토큰(가능하면), latency_ms

### Stage 2: Vector Retrieval
- 입력: `query_vector`, `top_k`, `filters(optional)`
- 출력: `candidates[]` (doc_id, score_dense, payload)
- 로그: index명, latency_ms, result_count

### Stage 3: Hybrid Fusion
- 입력: `query_text`, `query_vector`, `top_k_sparse`, `top_k_dense`
- 처리: BM25 결과와 Dense 결과를 fusion (예: RRF or weighted sum)
- 출력: `candidates[]` (doc_id, score_dense, score_sparse, score_fused, payload)

### Stage 4: Re-ranking
- 입력: `query_text`, `candidates[] (top_n)`
- 출력: `reranked[]` (doc_id, score_rerank, payload)
- 로그: rerank model, latency_ms

### Stage 5: Score/Rule Filtering
- 입력: `reranked[]` 또는 `candidates[]`, `ruleset`, `thresholds`
- 처리: min_score, metadata constraints, banned terms, category allowlist 등
- 출력: `final[]`
- 로그: 필터 사유(왜 제외됐는지), 최종 남은 수

## 공통 출력 포맷(요약)
- 각 stage 결과는 `runs/<run_id>/outputs.jsonl`에 1 test-case당 1라인 저장
- 최소 필드: `testcase_id`, `stage`, `items[]`, `latency_ms`, `vendor`, `model_or_engine`, `params` 


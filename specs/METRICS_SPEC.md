# 지표 스펙(METRICS_SPEC)

## Retrieval (Stage 2/3)
- Recall@K
- Precision@K
- HitRate@K (정답 하나라도 포함 여부)

## Ranking (Stage 4/5)
- MRR
- nDCG@K

## Quality/Business (옵션)
- Ambiguity rate (꼬리질문 필요 판정 비율)
- Wrong-category rate (카테고리 오탐 비율)

## Performance
- stage별 latency_ms (p50/p95)
- 호출 횟수, (가능하면) 비용/토큰


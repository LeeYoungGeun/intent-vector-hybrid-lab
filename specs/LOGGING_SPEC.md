# 로깅/추적 스펙(LOGGING_SPEC)

## 저장 위치
- `runs/<run_id>/inputs.jsonl` : testcase 입력(원문+의도문+정답)
- `runs/<run_id>/outputs.jsonl` : stage별 산출
- `runs/<run_id>/trace.jsonl` : 요청/응답 메타(헤더 제외), 오류, 재시도

## 필수 로그 필드(권장)
- `run_id`, `testcase_id`, `stage`
- `vendor`, `model_or_engine`
- `latency_ms`, `retry_count`, `error_code(optional)`
- `params` (top_k, alpha, rrf_k, min_score 등)
- `score_breakdown` (dense/sparse/fused/rerank)
- `rejected_reasons` (필터링 단계)

## 개인정보/보안
- 원문에 개인정보 가능성이 있으면 마스킹 옵션 제공
- API 키/토큰/헤더는 절대 로그 금지


# 04. 평가 지표와 리포트

## 리트리벌 품질(검색)
- Precision@K: 상위 K개 중 정답 비율
- Recall@K: 정답이 상위 K개에 포함되는 비율
- MRR: 최초 정답의 역순위 평균
- nDCG@K: 랭킹 품질(가중 정답 가능)

## 리랭킹 효과 측정
- Rerank 전/후의 nDCG@K, MRR 비교
- 오탐(불일치 카테고리) 감소율

## 필터링 효과 측정
- min_score/규칙 적용 전후:
  - Precision 상승 vs Recall 하락(트레이드오프) 곡선
  - “안전하게 컷”이 필요한 케이스에서 fail-safe 성공률

## 운영 지표
- Latency(단계별/전체)
- 비용(토큰/호출 수/벤더 요금 추정)
- 캐시 적중률(추가 구현 시)

## 리포트 산출물(권장)
- `reports/summary.md`: 파이프라인별 요약
- `reports/detail.jsonl`: 쿼리별 단계 로그


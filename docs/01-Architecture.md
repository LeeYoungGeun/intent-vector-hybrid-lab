# 01. 아키텍처(개념 설계)

## 전체 흐름
입력(사용자 발화/의도) → 임베딩 → 벡터 리트리벌 → (선택)BM25 리트리벌 → 하이브리드 퓨전 → 리랭킹 → 점수/규칙 필터링 → 최종 Top-K

이 템플릿은 위 흐름을 **단일 파이프라인**으로 실행하되, 각 단계를 독립적으로 교체 가능하도록 설계합니다.

## 컴포넌트 대분류
1) EmbeddingProvider
- 입력 텍스트(의도)를 벡터로 변환
- 출력: vector(float[]), usage(토큰/비용), latency

2) VectorRetriever
- query vector로 ANN 검색
- 출력: candidates[{doc_id, score_dense, metadata, fields...}]

3) LexicalRetriever (BM25)
- query text로 BM25 검색
- 출력: candidates[{doc_id, score_bm25, ...}]

4) FusionEngine (Hybrid)
- dense + bm25 후보군을 통합
- 출력: fused_candidates[{doc_id, score_fused, features...}]

5) Reranker
- (query, doc_text) 쌍을 입력으로 재정렬
- 출력: reranked[{doc_id, score_rerank, ...}]

6) FilterEngine
- 임계값/메타데이터/금칙 규칙 적용
- 출력: final[{doc_id, final_score, reasons[]}]

## 설계 원칙
- **표준 I/O**: 모든 단계는 공통 스키마로 입출력
- **벤더 독립성**: API 변경 시 어댑터만 수정
- **관측성**: 단계별 latency, 비용, 후보군 크기, 점수 분포를 로그로 남김
- **재현성**: 실행 설정은 YAML로 고정(파이프라인/벤더/모델/가중치)

## 파이프라인 모드
- MODE-A: Dense only (임베딩 + 벡터 검색)
- MODE-B: Hybrid (BM25 + Dense + Fusion)
- MODE-C: Hybrid + Rerank
- MODE-D: Hybrid + Rerank + Filter (권장 기본)


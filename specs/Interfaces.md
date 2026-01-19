# Interfaces (표준 인터페이스 초안)

이 문서는 바이브코딩으로 실제 코드를 만들 때 **어댑터가 반드시 지켜야 하는 계약**을 정의합니다.

## 공통 타입(개념)
- Query
  - id: string
  - raw_text: string
  - intent_text: string  (이미 “의도 추출”된 결과를 입력으로 사용)

- Candidate
  - doc_id: string
  - score_dense?: float
  - score_bm25?: float
  - score_fused?: float
  - score_rerank?: float
  - metadata?: object
  - text?: string (리랭킹용 본문/요약)

## 1) EmbeddingProvider
- input: intent_text
- output: vector(float[]), usage, latency_ms

## 2) VectorRetriever
- input: vector, top_k, filters?
- output: candidates[]

## 3) LexicalRetriever(BM25)
- input: intent_text, top_k, filters?
- output: candidates[]

## 4) FusionEngine
- input: dense_candidates[], bm25_candidates[], params(alpha, rrf_k...)
- output: fused_candidates[]

## 5) Reranker
- input: intent_text, candidates[] (with text fields), top_k
- output: reranked_candidates[]

## 6) FilterEngine
- input: candidates[], ruleset, min_score
- output: final_candidates[], dropped_candidates(with reasons)


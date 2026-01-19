# 02. 벤더/서비스 매트릭스(예시)

아래는 “어댑터로 붙일 수 있는 후보”의 예시입니다. 실제로는 대표님이 쓰는 스택과 예산/지연시간 요구에 맞춰 선택합니다.

## 1) 임베딩(EmbeddingProvider)
- OpenAI: text-embedding-3-* 계열
- Google Vertex AI: Gemini embedding 계열
- Cohere: embed 계열
- Amazon Bedrock: Titan embed 계열

## 2) 벡터 리트리벌(VectorRetriever)
- Pinecone / Weaviate / Qdrant / Milvus
- Elastic / OpenSearch vector
- Azure AI Search vector
- Vertex AI Vector Search

## 3) BM25(LexicalRetriever)
- Elasticsearch / OpenSearch / Azure AI Search
- (로컬 개발용) Whoosh/Lucene 기반 구현(테스트 목적)

## 4) 리랭킹(Reranker)
- Cohere Rerank
- Voyage Rerank
- Jina Reranker

## 5) 필터링(FilterEngine)
- 대부분의 벡터DB/검색엔진이 제공:
  - metadata/payload filter
  - min_score
  - pre-filter/post-filter


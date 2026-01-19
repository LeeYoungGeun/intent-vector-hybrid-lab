# 벤더/엔진 매트릭스(예시)

> 실제 연결은 각 벤더의 API 키/엔드포인트를 준비한 뒤, 어댑터 설정으로 전환합니다.

## (1) Embedding
- OpenAI: `text-embedding-3-small`, `text-embedding-3-large`
- Google Vertex AI: `gemini-embedding-001`
- Cohere: `embed-v4.0`

## (2) Vector Retrieval (ANN/VectorDB)
- Pinecone
- Qdrant
- Weaviate
- (클라우드) Azure AI Search / OpenSearch / Elasticsearch

## (3) Hybrid Fusion (BM25 + Vector)
- Elasticsearch (RRF 등)
- OpenSearch (hybrid + RRF)
- Azure AI Search (Hybrid + RRF)
- Weaviate(Pure hybrid), Pinecone(sparse+dense)

## (4) Re-ranking
- Cohere Rerank (v4)
- Voyage Rerank
- Jina Reranker

## (5) Score/Rule Filtering
- VectorDB metadata filter (Pinecone/Qdrant/Weaviate)
- Search engine `min_score`/bool filter(Elastic/OpenSearch)
- Strict post-filter(Azure AI Search) 같은 엔진 고유 필터


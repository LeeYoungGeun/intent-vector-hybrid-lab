# 05. 실행/운영 런북(템플릿)

## 로컬 실행 기본 원칙
- 모든 실행은 **리포지토리 루트**에서 수행
- API 키는 `.env` 또는 CI 시크릿으로 주입(커밋 금지)

## 권장 실행 커맨드(예시)
- `make setup` : 의존성 설치
- `make lint` : 정적 분석
- `make run PIPELINE=hybrid_rerank_filter VENDOR_SET=baseline`
- `make report RUN_ID=...`

> 위 커맨드는 “바이브코딩” 단계에서 실제로 구현합니다.

## 시크릿/환경변수
- OpenAI: `OPENAI_API_KEY`
- Google: `GOOGLE_API_KEY` 또는 Vertex 인증 방식
- Cohere: `COHERE_API_KEY`
- Pinecone: `PINECONE_API_KEY`, `PINECONE_INDEX`
- Elastic/OpenSearch: `ELASTIC_URL`, `ELASTIC_API_KEY`

## 안전 수칙
- 로그에 원문 사용자 개인정보를 남기지 말 것(테스트셋도 익명화)
- 샘플 데이터는 공개 가능한 내용만


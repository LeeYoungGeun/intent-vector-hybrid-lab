[목표]
intent-vector-hybrid-lab 프로젝트에 "Google Gemini(Developer API) 임베딩" 어댑터를 추가하고,
OpenAI 임베딩 vs Google 임베딩을 동일 테스트셋으로 비교 실행할 수 있게 만든다.
또한 COHERE_API_KEY가 없어도 rerank 파이프라인을 돌릴 수 있게 "mock rerank" vendor-set도 추가한다.

[전제]
- 프로젝트는 pyproject.toml 기반 패키지이며 CLI는 `ivhl`.
- `.env`는 프로젝트 루트에 존재하며, ivhl 실행 시 pipeline.py에서 load_dotenv()로 로드된다.
- 사용자는 OPENAI_API_KEY, GOOGLE_API_KEY(또는 GEMINI_API_KEY)를 보유.
- Cohere는 당장 사용하지 않을 수 있으므로, cohere 키 없이도 rerank 파이프라인을 실행 가능해야 함.
- 프로젝트 루트폴더는 intent-vector-hybrid-lab

[해야 할 변경 작업 목록]

1) 의존성 추가
- pyproject.toml [project].dependencies에 아래 추가:
  - openai>=2.0.0
  - google-genai>=1.0.0
  - (선택) cohere>=5.0.0  # 기존 baseline vendor-set을 살리고 싶으면 유지
- requirements.txt에도 동일 라인 추가(편의용). 단, pyproject.toml이 소스 오브 트루스.

2) Google 임베딩 어댑터 구현
- 파일: src/ivhl/adapters/embedding.py
- 현재 MockEmbeddingAdapter / OpenAIEmbeddingAdapter 외에 GoogleEmbeddingAdapter 추가
- google-genai SDK 사용:
  - from google import genai
  - from google.genai import types
- API 키 로딩 로직:
  - api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
  - client = genai.Client(api_key=api_key)  (api_key가 None이면 예외를 명확히 발생)
- 기본 모델:
  - model 기본값 = "gemini-embedding-001"
- task_type 지원(설정 가능):
  - 문서 임베딩: "RETRIEVAL_DOCUMENT"
  - 쿼리 임베딩: "RETRIEVAL_QUERY"
- 구현 방식(배치 지원):
  - embed_documents(texts: List[str]) -> List[List[float]]
    - client.models.embed_content(model=..., contents=texts, config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", output_dimensionality=<optional>))
  - embed_query(text: str) -> List[float]
    - contents=text, task_type="RETRIEVAL_QUERY"
- 반환 파싱은 형태 변화에 강건하게:
  - result.embeddings가 list이고, 각 원소가 `.values`를 가지면 values를 사용
  - 그렇지 않으면 list(...)로 강제 변환 시도
- 기존 Protocol(EmbeddingAdapter)은 깨지지 않게 유지:
  - embed_texts(texts)도 제공(내부적으로 embed_documents를 호출)하여 기존 코드 호환
- build_embedding_adapter(cfg)에서 provider == "google" 분기 추가:
  - cfg에서 model, output_dimensionality, api_key_env(옵션) 등을 받을 수 있게

3) 파이프라인에서 query/doc task 분리 사용(권장)
- 파일: src/ivhl/core/pipeline.py
- 문서 임베딩 생성 시:
  - if hasattr(embedding, "embed_documents"): embedding.embed_documents(doc_texts) else embedding.embed_texts(doc_texts)
- 쿼리 임베딩 생성 시:
  - if hasattr(embedding, "embed_query"): embedding.embed_query(c.intent_text) else embedding.embed_texts([c.intent_text])[0]

4) 코사인 유사도 정확화(중요)
- 파일: src/ivhl/adapters/retrieval.py
- 현재 _cosine이 "정규화된 벡터" 전제(dot product)인데, 외부 임베딩은 정규화 보장 X
- _cosine을 진짜 cosine으로 변경:
  - dot / (||a||*||b||), 0 division 방지
- 이렇게 하면 OpenAI/Google 임베딩에서도 점수가 정상화됨

5) vendor-set 추가(설정 파일만으로도 Cohere 없이 rerank 가능하게)
- 파일: templates/vendors.example.yaml
- vendor_sets에 아래 2개를 추가:
  - openai_only:
      embedding: {provider: openai, model: text-embedding-3-small}
      vector_db: {provider: qdrant}  # 현재 로컬 brute-force라 의미는 없지만 형식 유지
      bm25: {provider: elastic}
      fusion: {provider: rrf, k: 60}
      rerank: {provider: mock}   # COHERE 없이도 rerank 파이프라인 실행 가능
      filter: {provider: rules, min_score: 0.0}
  - google_only:
      embedding: {provider: google, model: gemini-embedding-001, output_dimensionality: 768}  # output_dimensionality는 옵션(없으면 기본 차원)
      vector_db: {provider: qdrant}
      bm25: {provider: elastic}
      fusion: {provider: rrf, k: 60}
      rerank: {provider: mock}
      filter: {provider: rules, min_score: 0.0}
- 기존 baseline/frontier는 그대로 둔다(호환 유지)

6) .env 템플릿 보강
- 파일: templates/.env.example
- 아래 키 안내 추가:
  - OPENAI_API_KEY=...
  - GOOGLE_API_KEY=...   (또는 GEMINI_API_KEY=... 둘 중 하나면 되도록 코드가 처리)
  - (선택) COHERE_API_KEY=...

7) 문서 갱신
- README.md 또는 docs/04_RUNBOOK.md에 아래 커맨드 추가:
  - OpenAI vs Google 임베딩 비교 실행 예시
  - COHERE 없이 rerank 파이프라인 실행 예시(openai_only/google_only)

[완료 기준(로컬에서 실제로 통과해야 함)]
A. 설치
- pip install -e .
- (또는 pip install -U openai google-genai)

B. 실행
- ivhl list 시 vendor sets에 openai_only, google_only가 보인다
- 아래가 모두 성공한다:
  1) ivhl run --pipeline-id hybrid --vendor-set openai_only --catalog data\catalog.example.tsv --testcases templates\testcases.example.tsv --out-dir runs
  2) ivhl run --pipeline-id hybrid --vendor-set google_only --catalog ... 동일
  3) ivhl run --pipeline-id hybrid_rerank_filter --vendor-set openai_only --catalog ... 동일  (rerank=mock 이므로 COHERE 없이 성공)

[주의]
- 키 값은 출력/로그에 절대 노출하지 말 것.
- Google 임베딩 호출 실패 시(키 누락 등) 에러 메시지는 "GOOGLE_API_KEY 또는 GEMINI_API_KEY 필요"로 명확히 안내.

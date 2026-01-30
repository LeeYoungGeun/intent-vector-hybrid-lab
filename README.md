# Intent Vector/Hybrid Lab (ivhl)

의도 기반 벡터/하이브리드 검색 파이프라인을 **동일한 테스트셋/지표**로 비교하기 위한 템플릿입니다.

현재 버전(v0.1.0)은 **로컬 mock 구현**으로 e2e 실행이 가능하며, 이후 OpenAI/Qdrant/Elastic/Cohere 등 실제 벤더 어댑터를 단계적으로 추가하는 구조입니다.

## Quickstart (로컬 mock)

```bash
cd intent-vector-hybrid-lab
python -m pip install -r requirements.txt
python -m pip install -e .

# 파이프라인/벤더셋 목록
ivhl list

# 샘플 카탈로그 + 샘플 테스트케이스 실행
ivhl run \
  --pipeline-id hybrid_rerank_filter \
  --vendor-set local_mock \
  --catalog data/catalog.example.tsv \
  --testcases templates/testcases.example.tsv \
  --out-dir runs
```

결과는 `runs/<run_id>/` 아래에 생성됩니다.
- `detail.jsonl`: 케이스별 단계별 결과 로그
- `summary.json`: 지표 요약
- `report.md`: 사람이 보기 쉬운 리포트

## 범위
- (1) 임베딩
- (2) 벡터 리트리벌
- (3) BM25 + 하이브리드 퓨전
- (4) 리랭킹
- (5) 점수/규칙 기반 필터링

## 주의
- 이 레포는 **API 키를 요구하지 않는 로컬 mock**을 기본 제공하며, 실제 벤더 연동은 어댑터 구현이 필요합니다.

## OpenAI vs Google 임베딩 비교

### 1) 환경변수 설정

프로젝트 루트에 `.env` 파일을 만들고 다음 중 필요한 키를 넣습니다.

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY` 또는 `GEMINI_API_KEY`

(`templates/.env.example` 참고)

### 2) vendor-set 확인

```bash
ivhl list
```

`openai_only`, `google_only`가 보이면 정상입니다.

### 3) OpenAI 임베딩으로 실행

```bash
ivhl run --pipeline-id hybrid --vendor-set openai_only --catalog data/catalog.example.tsv --testcases templates/testcases.example.tsv --out-dir runs
```

### 4) Google 임베딩으로 실행

```bash
ivhl run --pipeline-id hybrid --vendor-set google_only --catalog data/catalog.example.tsv --testcases templates/testcases.example.tsv --out-dir runs
```

### 5) Cohere 없이 rerank 파이프라인 실행(mock rerank)

```bash
ivhl run --pipeline-id hybrid_rerank_filter --vendor-set openai_only --catalog data/catalog.example.tsv --testcases templates/testcases.example.tsv --out-dir runs
```

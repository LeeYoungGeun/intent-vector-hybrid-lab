# 프로젝트 트리(현재 템플릿)

아래는 현재 템플릿에 포함된 파일 목록입니다.

```
./README.md
./docs/00-Project-Goal.md
./docs/00_GOALS.md
./docs/01-Architecture.md
./docs/01_SETUP.md
./docs/02-Vendor-Matrix.md
./docs/02_PROJECT_TREE.md
./docs/03-Testcases-Design.md
./docs/03_VENDOR_MATRIX.md
./docs/04-Metrics-Eval.md
./docs/04_RUNBOOK.md
./docs/05-Runbook.md
./prompts/CODING_RULES.md
./prompts/TASK_BREAKDOWN.md
./prompts/Task-Backlog.md
./prompts/VIBE_CODING_PROMPT.md
./specs/ADAPTER_INTERFACES.md
./specs/INDEX.md
./specs/Interfaces.md
./specs/LOGGING_SPEC.md
./specs/METRICS_SPEC.md
./specs/PIPELINE_SPEC.md
./specs/Result-Schema.md
./specs/TESTSET_SPEC.md
./templates/.env.example
./templates/pipeline.example.yaml
./templates/pipelines.example.yaml
./templates/testcases.example.tsv
./templates/vendors.example.yaml
```

---

## (추가) 실행 코드 구조 (0.1.0)
- `src/ivhl/` : CLI 및 실행 코드
- `data/catalog.example.tsv` : 로컬 실행용 샘플 카탈로그
- `runs/` : 실행 결과 출력 폴더

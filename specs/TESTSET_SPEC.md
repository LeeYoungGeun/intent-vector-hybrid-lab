# 테스트셋 스펙(TESTSET_SPEC)

## 파일 포맷
- `data/testcases.tsv`
- UTF-8, tab-separated

## 컬럼(권장)
- `testcase_id`
- `raw_query` : 사용자 원문
- `intent_text` : 의도 정제 문장(없으면 런타임에 생성 가능)
- `expected_doc_ids` : 정답 doc_id 리스트(콤마)
- `expected_category` : 정답 카테고리(옵션)
- `notes` : 애매성/오타/동의어 등 태그

## 커버리지 가이드
- 정확 상품명(정확 키워드)
- 동의어/축약
- 목적/설명형(“샤워실에 까는 미끄럼 방지”)
- 잡음/짧은 발화(“안녕하세요”, “매트요”)
- 다의어/카테고리 충돌(“매트”: 욕실/요가/캠핑)


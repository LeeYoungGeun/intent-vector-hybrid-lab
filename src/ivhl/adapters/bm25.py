# src/ivhl/adapters/bm25.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from ivhl.core.types import Document, ScoredDoc


def _simple_tokenize(text: str) -> List[str]:
    # 매우 단순 토크나이저(공백 기반). 필요 시 여기를 Mecab/Khannanum 등으로 교체
    return [t for t in (text or "").strip().split() if t]


@dataclass
class LocalBM25:
    docs: List[Document]

    def __post_init__(self) -> None:
        self._doc_texts: List[str] = [(d.title + " " + d.text).strip() for d in self.docs]
        self._doc_tokens: List[List[str]] = [_simple_tokenize(t) for t in self._doc_texts]

        # 아주 단순 BM25 구현(외부 라이브러리 의존 제거 목적)
        # 기존에 rank_bm25 등을 쓰고 있다면: "항상 top_k개 반환"만 보장하도록 query 쪽을 수정하면 됩니다.
        self._df: Dict[str, int] = {}
        for toks in self._doc_tokens:
            for tok in set(toks):
                self._df[tok] = self._df.get(tok, 0) + 1

        self._N = max(len(self.docs), 1)
        self._avgdl = sum(len(t) for t in self._doc_tokens) / self._N

        # BM25 params
        self._k1 = 1.5
        self._b = 0.75

    def _idf(self, term: str) -> float:
        # Robertson/Sparck Jones IDF with +0.5 smoothing
        df = self._df.get(term, 0)
        return max(0.0, ((self._N - df + 0.5) / (df + 0.5)))  # log는 생략(상대 비교면 충분)
        # log를 쓰려면: import math; return math.log(1 + (N-df+0.5)/(df+0.5))

    def query(self, query_text: str, *, top_k: int = 50) -> List[ScoredDoc]:
        q_tokens = _simple_tokenize(query_text)
        if not q_tokens:
            # ✅ 빈 쿼리면 점수 0으로라도 top_k 반환(비교 실험용)
            return [
                ScoredDoc(doc_id=self.docs[i].doc_id, score=0.0, extra={"rank": i + 1})
                for i in range(min(top_k, len(self.docs)))
            ]

        scores: List[float] = [0.0 for _ in self.docs]
        for i, doc_toks in enumerate(self._doc_tokens):
            dl = len(doc_toks) or 1
            tf: Dict[str, int] = {}
            for t in doc_toks:
                tf[t] = tf.get(t, 0) + 1

            s = 0.0
            for term in q_tokens:
                f = tf.get(term, 0)
                if f <= 0:
                    continue
                idf = self._idf(term)
                denom = f + self._k1 * (1 - self._b + self._b * (dl / self._avgdl))
                s += idf * (f * (self._k1 + 1)) / max(denom, 1e-9)
            scores[i] = s

        # ✅ 항상 top_k개를 반환(0점 포함)
        idx_sorted = sorted(range(len(self.docs)), key=lambda i: scores[i], reverse=True)
        idx_sorted = idx_sorted[: min(top_k, len(idx_sorted))]

        out: List[ScoredDoc] = []
        for rank, i in enumerate(idx_sorted, start=1):
            out.append(
                ScoredDoc(
                    doc_id=self.docs[i].doc_id,
                    score=float(scores[i]),
                    extra={"rank": rank},
                )
            )
        return out

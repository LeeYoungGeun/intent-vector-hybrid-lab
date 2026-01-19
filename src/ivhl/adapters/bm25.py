from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Protocol

from ivhl.core.tokenize import tokenize
from ivhl.core.types import Document, ScoredDoc


class BM25Retriever(Protocol):
    def query(self, query_text: str, *, top_k: int) -> List[ScoredDoc]:
        ...


@dataclass
class LocalBM25:
    docs: List[Document]
    k1: float = 1.5
    b: float = 0.75

    def __post_init__(self) -> None:
        self._tokens: Dict[str, List[str]] = {}
        self._doc_len: Dict[str, int] = {}
        self._df: Dict[str, int] = {}
        self._N = len(self.docs)
        total_len = 0
        for d in self.docs:
            toks = tokenize((d.title or "") + " " + (d.text or ""))
            self._tokens[d.doc_id] = toks
            L = len(toks)
            self._doc_len[d.doc_id] = L
            total_len += L
            seen = set()
            for t in toks:
                if t in seen:
                    continue
                self._df[t] = self._df.get(t, 0) + 1
                seen.add(t)
        self._avgdl = (total_len / self._N) if self._N > 0 else 0.0

    def _idf(self, term: str) -> float:
        df = self._df.get(term, 0)
        # BM25+ style idf smoothing
        return math.log(1 + (self._N - df + 0.5) / (df + 0.5))

    def query(self, query_text: str, *, top_k: int) -> List[ScoredDoc]:
        q = tokenize(query_text)
        if not q:
            return []
        scored: List[ScoredDoc] = []
        for d in self.docs:
            toks = self._tokens.get(d.doc_id) or []
            if not toks:
                continue
            # term frequency
            tf: Dict[str, int] = {}
            for t in toks:
                tf[t] = tf.get(t, 0) + 1
            L = self._doc_len.get(d.doc_id, 0)
            denom_base = self.k1 * (1 - self.b + self.b * (L / (self._avgdl or 1.0)))
            score = 0.0
            for term in q:
                f = tf.get(term, 0)
                if f <= 0:
                    continue
                idf = self._idf(term)
                score += idf * (f * (self.k1 + 1)) / (f + denom_base)
            if score > 0:
                scored.append(ScoredDoc(doc_id=d.doc_id, score=score, source="bm25"))
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]

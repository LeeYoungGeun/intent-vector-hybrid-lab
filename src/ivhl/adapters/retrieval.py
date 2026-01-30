from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Protocol

from ivhl.core.types import Document, ScoredDoc


class VectorRetriever(Protocol):
    def query(self, qvec: List[float], *, top_k: int) -> List[ScoredDoc]:
        ...


def _cosine(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    # Robust cosine similarity (works for non-normalized vectors).
    s = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    denom = na * nb
    if denom == 0.0:
        return 0.0
    return float(s / denom)


@dataclass
class BruteForceVectorRetriever:
    docs: List[Document]
    doc_vecs: Dict[str, List[float]]

    def query(self, qvec: List[float], *, top_k: int) -> List[ScoredDoc]:
        scored: List[ScoredDoc] = []
        for d in self.docs:
            v = self.doc_vecs.get(d.doc_id)
            if v is None:
                continue
            score = _cosine(qvec, v)
            scored.append(ScoredDoc(doc_id=d.doc_id, score=score, source="dense"))
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]

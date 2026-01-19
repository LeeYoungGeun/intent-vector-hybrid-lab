from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Protocol

from ivhl.core.types import Document, ScoredDoc


class VectorRetriever(Protocol):
    def query(self, qvec: List[float], *, top_k: int) -> List[ScoredDoc]:
        ...


def _cosine(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors.
    
    Handles non-normalized vectors properly by dividing by magnitudes.
    """
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(dot / (norm_a * norm_b))


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

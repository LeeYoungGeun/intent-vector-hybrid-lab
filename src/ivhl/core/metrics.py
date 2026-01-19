from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence


def _dcg(rels: Sequence[int]) -> float:
    s = 0.0
    for i, rel in enumerate(rels, start=1):
        # log2(i+1)
        denom = math.log2(i + 1)
        s += (2**rel - 1) / denom
    return s


def precision_at_k(pred: Sequence[str], gold: Sequence[str], k: int) -> float:
    if k <= 0:
        return 0.0
    p = pred[:k]
    if not p:
        return 0.0
    g = set(gold)
    hits = sum(1 for x in p if x in g)
    return hits / len(p)


def recall_at_k(pred: Sequence[str], gold: Sequence[str], k: int) -> float:
    if k <= 0:
        return 0.0
    g = set(gold)
    if not g:
        return 0.0
    p = pred[:k]
    hits = sum(1 for x in p if x in g)
    return hits / len(g)


def mrr(pred: Sequence[str], gold: Sequence[str]) -> float:
    g = set(gold)
    if not g:
        return 0.0
    for i, x in enumerate(pred, start=1):
        if x in g:
            return 1.0 / i
    return 0.0


def ndcg_at_k(pred: Sequence[str], gold: Sequence[str], k: int) -> float:
    if k <= 0:
        return 0.0
    g = set(gold)
    if not g:
        return 0.0
    rels = [1 if x in g else 0 for x in pred[:k]]
    dcg = _dcg(rels)
    ideal_rels = sorted(rels, reverse=True)
    idcg = _dcg(ideal_rels)
    return dcg / idcg if idcg > 0 else 0.0


@dataclass
class MetricsSummary:
    n_eval: int
    p_at_10: float
    r_at_10: float
    mrr: float
    ndcg_at_10: float

    def as_dict(self) -> Dict[str, float | int]:
        return {
            "n_eval": self.n_eval,
            "precision@10": self.p_at_10,
            "recall@10": self.r_at_10,
            "mrr": self.mrr,
            "ndcg@10": self.ndcg_at_10,
        }


def aggregate(case_metrics: Iterable[Dict[str, float]]) -> MetricsSummary:
    items = list(case_metrics)
    n = len(items)
    if n == 0:
        return MetricsSummary(n_eval=0, p_at_10=0.0, r_at_10=0.0, mrr=0.0, ndcg_at_10=0.0)

    def mean(key: str) -> float:
        return sum(m.get(key, 0.0) for m in items) / n

    return MetricsSummary(
        n_eval=n,
        p_at_10=mean("precision@10"),
        r_at_10=mean("recall@10"),
        mrr=mean("mrr"),
        ndcg_at_10=mean("ndcg@10"),
    )

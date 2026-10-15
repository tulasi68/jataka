"""Transparent, deterministic aggregation of evidence from separate engines."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Evidence:
    """One engine's contribution to a topic.

    score is an internal normalized value in [-1, 1], not a probability.
    weight must be non-negative. Missing evidence should be omitted rather
    than encoded as a zero-valued negative/positive result.
    """

    engine: str
    topic: str
    score: float
    weight: float = 1.0
    rule_id: str = ""

    def __post_init__(self) -> None:
        if not self.engine.strip():
            raise ValueError("engine must not be empty")
        if not self.topic.strip():
            raise ValueError("topic must not be empty")
        if not -1.0 <= self.score <= 1.0:
            raise ValueError("score must be between -1 and 1")
        if self.weight < 0:
            raise ValueError("weight must be non-negative")


def build_consensus(evidence: Iterable[Evidence]) -> dict[str, dict[str, object]]:
    """Aggregate evidence per topic using a transparent weighted mean.

    Topics with only zero-weight evidence are reported as unavailable. Original
    engine contributions are retained so disagreements remain visible. This
    is bookkeeping, not a probability or a claim of predictive accuracy.
    """
    grouped: dict[str, list[Evidence]] = {}
    for item in evidence:
        grouped.setdefault(item.topic, []).append(item)

    result: dict[str, dict[str, object]] = {}
    for topic in sorted(grouped):
        items = grouped[topic]
        total_weight = sum(item.weight for item in items)
        score = (
            sum(item.score * item.weight for item in items) / total_weight
            if total_weight > 0
            else None
        )
        result[topic] = {
            "score": score,
            "status": "available" if score is not None else "no_positive_weight",
            "evidence": [
                {
                    "engine": item.engine,
                    "score": item.score,
                    "weight": item.weight,
                    "rule_id": item.rule_id,
                }
                for item in sorted(items, key=lambda x: (x.engine, x.rule_id, x.score))
            ],
            "interpretation": "internal normalized score; not a probability",
        }
    return result

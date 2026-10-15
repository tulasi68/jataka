import pytest

from jataka.consensus import Evidence, build_consensus


def test_weighted_mean_is_deterministic() -> None:
    result = build_consensus(
        [
            Evidence(engine="parashari", topic="career", score=1.0, weight=2.0),
            Evidence(engine="jaimini", topic="career", score=-1.0, weight=1.0),
        ]
    )
    assert result["career"]["score"] == pytest.approx(1 / 3)
    assert result["career"]["status"] == "available"
    assert len(result["career"]["evidence"]) == 2


def test_zero_weight_evidence_is_not_treated_as_a_score() -> None:
    result = build_consensus(
        [Evidence(engine="transit", topic="timing", score=1.0, weight=0.0)]
    )
    assert result["timing"]["score"] is None
    assert result["timing"]["status"] == "no_positive_weight"


def test_invalid_score_and_weight_are_rejected() -> None:
    with pytest.raises(ValueError):
        Evidence(engine="x", topic="y", score=1.2)
    with pytest.raises(ValueError):
        Evidence(engine="x", topic="y", score=0.0, weight=-1.0)


def test_empty_evidence_returns_empty_mapping() -> None:
    assert build_consensus([]) == {}

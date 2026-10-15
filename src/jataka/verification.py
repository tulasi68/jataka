"""Three-pass evidence ledger for transparent, non-probabilistic cross-checking.

The verifier never calls agreement a probability or invents a missing pass. It
records engine independence and blocks a verified status if any pass is absent,
shares the same source, or has not been validated against reference fixtures.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


REQUIRED_PASSES = ("parashari", "jaimini", "ashtakavarga_transit")


@dataclass(frozen=True)
class PassEvidence:
    pass_name: str
    source_id: str
    status: str
    findings: Mapping[str, str]
    reference_validated: bool = False


def verify_three_passes(passes: Iterable[PassEvidence]) -> dict[str, object]:
    supplied = list(passes)
    by_name: dict[str, PassEvidence] = {}
    for item in supplied:
        if item.pass_name not in REQUIRED_PASSES:
            raise ValueError(f"Unknown verification pass: {item.pass_name}")
        if item.pass_name in by_name:
            raise ValueError(f"Duplicate verification pass: {item.pass_name}")
        by_name[item.pass_name] = item
    missing = [name for name in REQUIRED_PASSES if name not in by_name]
    source_ids = {item.source_id for item in supplied if item.source_id.strip()}
    independent_sources = len(source_ids) == len(supplied) and len(supplied) == 3
    validated = all(item.reference_validated and item.status == "validated" for item in supplied)
    topics = sorted({topic for item in supplied for topic in item.findings})
    comparisons = {}
    for topic in topics:
        entries = {
            name: by_name[name].findings[topic]
            for name in REQUIRED_PASSES
            if name in by_name and topic in by_name[name].findings
        }
        counts: dict[str, int] = {}
        for value in entries.values():
            counts[value] = counts.get(value, 0) + 1
        comparisons[topic] = {
            "findings": entries,
            "agreement_count": max(counts.values(), default=0),
            "pass_count": len(entries),
            "disagreement": len(counts) > 1,
        }
    ready = not missing and independent_sources and validated and all(
        len(value["findings"]) == 3 and not value["disagreement"]
        for value in comparisons.values()
    )
    if missing:
        status = "INCOMPLETE_MISSING_PASSES"
    elif not independent_sources:
        status = "INCOMPLETE_SOURCE_INDEPENDENCE_NOT_ESTABLISHED"
    elif not validated:
        status = "UNVALIDATED_REFERENCE_CHECKS_PENDING"
    elif any(value["disagreement"] for value in comparisons.values()):
        status = "DISAGREEMENT_REQUIRES_REVIEW"
    else:
        status = "THREE_PASS_AGREEMENT_REFERENCE_VALIDATED"
    return {
        "status": status,
        "ready_to_label_verified": ready,
        "required_passes": list(REQUIRED_PASSES),
        "missing_passes": missing,
        "independent_sources_established": independent_sources,
        "all_passes_reference_validated": validated,
        "topics": comparisons,
        "interpretation": (
            "Agreement is a consistency check only, not a probability or proof of predictive accuracy. "
            "The three passes must use genuinely independent calculations and separately sourced reference cases."
        ),
    }

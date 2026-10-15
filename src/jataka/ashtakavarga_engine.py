"""Classical seven-planet Bhinna and Sarva Ashtakavarga calculations.

Rule table follows the common Parāśari benefic-house tables as transcribed in
B.V. Raman's treatment and cross-checked against published open references.
Rule variants exist; this implementation is not yet reference-validated.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
CONTRIBUTORS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna")
RECIPIENTS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")

BENEFIC_HOUSES = {
    "Sun": {
        "Sun": (1,2,4,7,8,9,10,11), "Moon": (3,6,10,11), "Mars": (1,2,4,7,8,9,10,11),
        "Mercury": (3,5,6,9,10,11,12), "Jupiter": (5,6,9,11), "Venus": (6,7,12),
        "Saturn": (1,2,4,7,8,9,10,11), "Lagna": (3,4,6,10,11,12),
    },
    "Moon": {
        "Sun": (3,6,7,8,10,11), "Moon": (1,3,6,7,10,11), "Mars": (2,3,5,6,9,10,11),
        "Mercury": (1,3,4,5,7,8,10,11), "Jupiter": (1,4,7,8,10,11,12),
        "Venus": (3,4,5,7,9,10,11), "Saturn": (3,5,6,11), "Lagna": (3,6,10,11),
    },
    "Mars": {
        "Sun": (3,5,6,10,11), "Moon": (3,6,11), "Mars": (1,2,4,7,8,10,11),
        "Mercury": (3,5,6,11), "Jupiter": (6,10,11,12), "Venus": (6,8,11,12),
        "Saturn": (1,4,7,8,9,10,11), "Lagna": (1,3,6,10,11),
    },
    "Mercury": {
        "Sun": (5,6,9,11,12), "Moon": (2,4,6,8,10,11), "Mars": (1,2,4,7,8,9,10,11),
        "Mercury": (1,3,5,6,9,10,11,12), "Jupiter": (6,8,11,12),
        "Venus": (1,2,3,4,5,8,9,11), "Saturn": (1,2,4,7,8,9,10,11),
        "Lagna": (1,2,4,6,8,10,11),
    },
    "Jupiter": {
        "Sun": (1,2,3,4,7,8,9,10,11), "Moon": (2,5,7,9,11), "Mars": (1,2,4,7,8,10,11),
        "Mercury": (1,2,4,5,6,9,10,11), "Jupiter": (1,2,3,4,7,8,10,11),
        "Venus": (2,5,6,9,10,11), "Saturn": (3,5,6,12), "Lagna": (1,2,4,5,6,7,9,10,11),
    },
    "Venus": {
        "Sun": (8,11,12), "Moon": (1,2,3,4,5,8,9,11,12), "Mars": (3,5,6,9,11,12),
        "Mercury": (3,5,6,9,11), "Jupiter": (5,8,9,10,11),
        "Venus": (1,2,3,4,5,8,9,10,11), "Saturn": (3,4,5,8,9,10,11),
        "Lagna": (1,2,3,4,5,8,9,11),
    },
    "Saturn": {
        "Sun": (1,2,4,7,8,10,11), "Moon": (3,6,11), "Mars": (3,5,6,10,11,12),
        "Mercury": (6,8,9,10,11,12), "Jupiter": (5,6,11,12), "Venus": (6,11,12),
        "Saturn": (3,5,6,11), "Lagna": (1,3,4,6,10,11),
    },
}
EXPECTED_TOTALS = {"Sun":48, "Moon":49, "Mars":39, "Mercury":54, "Jupiter":56, "Venus":52, "Saturn":39}


@dataclass(frozen=True)
class AshtakavargaSettings:
    ruleset_version: str = "parashari-bav-sav-common-table-v1"


def _validate_positions(positions: Mapping[str, int], required: tuple[str, ...]) -> None:
    missing = [name for name in required if name not in positions]
    if missing:
        raise ValueError("Missing sign positions: " + ", ".join(missing))
    for name in required:
        value = positions[name]
        if not isinstance(value, int) or not 0 <= value < 12:
            raise ValueError(f"{name} sign must be a zero-based index from 0 to 11")


def calculate_ashtakavarga(
    sign_positions: Mapping[str, int], settings: AshtakavargaSettings | None = None
) -> dict[str, object]:
    """Return seven BAV sign tables and the 337-bindu Sarvāṣṭakavarga table."""
    settings = settings or AshtakavargaSettings()
    _validate_positions(sign_positions, CONTRIBUTORS)
    bav = {}
    for recipient in RECIPIENTS:
        scores = [0] * 12
        for contributor in CONTRIBUTORS:
            base = sign_positions[contributor]
            for house in BENEFIC_HOUSES[recipient][contributor]:
                scores[(base + house - 1) % 12] += 1
        bav[recipient] = {
            "by_sign": {SIGNS[i]: scores[i] for i in range(12)},
            "by_sign_index": scores,
            "total": sum(scores),
            "expected_total": EXPECTED_TOTALS[recipient],
            "total_matches_rule_table": sum(scores) == EXPECTED_TOTALS[recipient],
        }
    sav = [sum(bav[planet]["by_sign_index"][i] for planet in RECIPIENTS) for i in range(12)]
    return {
        "status": "DERIVED_UNVALIDATED",
        "ruleset_version": settings.ruleset_version,
        "bhinna_ashtakavarga": bav,
        "sarvashtakavarga": {"by_sign": {SIGNS[i]: sav[i] for i in range(12)},
                             "by_sign_index": sav, "total": sum(sav)},
        "expected_sarvashtakavarga_total": 337,
        "all_classical_totals_match": all(item["total_matches_rule_table"] for item in bav.values()),
        "convention": "Seven BAV recipient planets; contributors are seven planets plus Lagna; Rahu/Ketu excluded",
        "warning": "Traditional tables and interpretations vary; calculated bindus are not a probability or proven forecast.",
    }


def calculate_transit_triggers(
    natal_positions: Mapping[str, int],
    transit_positions: Mapping[str, int],
    ruleset_version: str = "ashtakavarga-transit-sign-score-v1",
) -> dict[str, object]:
    """Score transit signs using natal BAV tables; no event predictions are generated."""
    natal = calculate_ashtakavarga(natal_positions)
    results = []
    for planet in RECIPIENTS:
        if planet not in transit_positions:
            continue
        transit_sign = transit_positions[planet]
        if not isinstance(transit_sign, int) or not 0 <= transit_sign < 12:
            raise ValueError(f"{planet} transit sign must be a zero-based index from 0 to 11")
        bindus = natal["bhinna_ashtakavarga"][planet]["by_sign_index"][transit_sign]
        moon_sign = natal_positions["Moon"]
        moon_house = ((transit_sign - moon_sign) % 12) + 1
        asc_sign = natal_positions["Lagna"]
        asc_house = ((transit_sign - asc_sign) % 12) + 1
        results.append({
            "planet": planet, "transit_sign": SIGNS[transit_sign],
            "natal_bav_bindus_in_transit_sign": bindus,
            "transit_house_from_moon": moon_house,
            "transit_house_from_ascendant": asc_house,
            "rule_id": ruleset_version,
            "status": "DESCRIPTIVE_UNVALIDATED",
        })
    return {
        "status": "DESCRIPTIVE_UNVALIDATED",
        "as_of": None,
        "transits": results,
        "warning": "This reports sign-based traditional indicators only; it does not predict events or validate timing.",
    }

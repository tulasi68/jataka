"""Jaimini factors with explicitly stated sign-counting conventions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from jataka.derived_engine import calculate_jaimini_chara_karakas

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
RULERS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury",
    6: "Venus", 7: "Mars", 8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}


@dataclass(frozen=True)
class JaiminiSettings:
    chara_karaka_count: int = 7
    include_rahu: bool = False
    ruleset_version: str = "jaimini-0.2.0"

    def __post_init__(self) -> None:
        if self.chara_karaka_count not in (7, 8):
            raise ValueError("chara_karaka_count must be 7 or 8")
        if self.include_rahu != (self.chara_karaka_count == 8):
            raise ValueError("Select 7 karakas without Rahu or 8 karakas with Rahu")


def calculate_arudha_padas(
    sign_positions: Mapping[str, int],
) -> dict[str, object]:
    """Calculate AL and the 12 Arudha Padas using classical seven-planet rulers.

    Positions are zero-based sidereal sign indices. If the projected pada lands
    in the source sign or its seventh sign, this implementation applies the
    commonly used exception by moving to the tenth sign from the projection.
    School-specific exceptions and Rahu/Ketu rulership are not inferred.
    """
    required = set(RULERS.values())
    missing = sorted(required - set(sign_positions))
    if missing:
        raise ValueError("Missing sign positions for lords: " + ", ".join(missing))
    for planet, sign in sign_positions.items():
        if not isinstance(sign, int) or not 0 <= sign < 12:
            raise ValueError(f"{planet} sign must be a zero-based index from 0 to 11")
    results = []
    for source_sign in range(12):
        lord = RULERS[source_sign]
        lord_sign = sign_positions[lord]
        distance = (lord_sign - source_sign) % 12 + 1
        projected = (lord_sign + distance - 1) % 12
        exception_used = projected in (source_sign, (source_sign + 6) % 12)
        if exception_used:
            projected = (projected + 9) % 12
        results.append({
            "house": source_sign + 1,
            "source_sign": SIGNS[source_sign],
            "lord": lord,
            "lord_sign": SIGNS[lord_sign],
            "counted_distance": distance,
            "arudha_sign_index": projected,
            "arudha_sign": SIGNS[projected],
            "exception_applied": exception_used,
            "rule_id": "arudha-pada-classical-rulers-tenth-exception-v1",
        })
    return {
        "status": "DERIVED_UNVALIDATED",
        "arudha_lagna": results[0],
        "padas": results,
        "convention": "Classical seven-planet sign rulers; tenth-sign exception; no node rulership",
        "warning": "Arudha counting and exceptions vary by lineage; compare against trusted reference charts.",
    }


def calculate_jaimini_factors(
    sidereal_longitudes: Mapping[str, float], settings: JaiminiSettings | None = None
) -> dict[str, object]:
    """Return Chara Kārakas and Arudha Padas from sidereal longitudes."""
    settings = settings or JaiminiSettings()
    sign_positions = {}
    for planet, value in sidereal_longitudes.items():
        longitude = float(value)
        if not 0 <= longitude < 360:
            raise ValueError(f"{planet} longitude must be in [0, 360)")
        sign_positions[planet] = int(longitude // 30)
    karakas = calculate_jaimini_chara_karakas(
        sidereal_longitudes,
        karaka_count=settings.chara_karaka_count,
        include_rahu=settings.include_rahu,
    )
    arudhas = calculate_arudha_padas(sign_positions)
    return {
        "status": "DERIVED_UNVALIDATED",
        "ruleset_version": settings.ruleset_version,
        "chara_karakas": karakas,
        "arudha_padas": arudhas,
        "warnings": [
            "Jaimini rules differ by tradition and have not been reference-validated.",
            "Arudha uses the classical seven-planet rulership scheme and a documented tenth-sign exception.",
        ],
    }

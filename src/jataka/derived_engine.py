"""Traceable derived Jyotish factors built from supplied sidereal longitudes.

These are deterministic traditional-rule calculations, not independently validated
astronomical results or evidence of predictive accuracy. Rule choices are versioned
and surfaced in each response.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from math import floor
from typing import Mapping

RULESET_VERSION = "jyotish-derived-0.1.0"

SIGNS = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)
NAKSHATRAS = (
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
)
NAKSHATRA_LORDS = (
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
) * 3
VIMSHOTTARI_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
DASHA_SEQUENCE = ("Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury")
DASHA_YEAR_DAYS = 365.25
NAKSHATRA_SPAN = 360.0 / 27.0
PADA_SPAN = NAKSHATRA_SPAN / 4.0


def _longitude(value: float, label: str) -> float:
    try:
        lon = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a finite longitude") from exc
    if not 0.0 <= lon < 360.0:
        raise ValueError(f"{label} must be in the range [0, 360)")
    return lon


def sign_index(longitude: float) -> int:
    """Return zero-based sidereal sign index for a longitude in [0, 360)."""
    return int(floor(_longitude(longitude, "longitude") / 30.0))


def describe_longitude(longitude: float) -> dict[str, object]:
    """Return sign, degree within sign, nakshatra/pada, and Navamsa sign."""
    lon = _longitude(longitude, "longitude")
    sign = int(lon // 30)
    in_sign = lon - sign * 30
    nak_index = min(26, int(lon // NAKSHATRA_SPAN))
    nak_offset = lon - nak_index * NAKSHATRA_SPAN
    pada = min(4, int(nak_offset // PADA_SPAN) + 1)

    # D9 begins from the same sign for movable signs, ninth from fixed signs,
    # and fifth from dual signs; each 3°20′ division advances one sign.
    modality_start = sign if sign % 3 == 0 else (sign + 8) % 12 if sign % 3 == 1 else (sign + 4) % 12
    navamsa_part = min(8, int(in_sign // PADA_SPAN))
    navamsa = (modality_start + navamsa_part) % 12

    return {
        "longitude": lon,
        "sign_index": sign,
        "sign": SIGNS[sign],
        "degree_in_sign": round(in_sign, 8),
        "nakshatra_index": nak_index,
        "nakshatra": NAKSHATRAS[nak_index],
        "nakshatra_lord": NAKSHATRA_LORDS[nak_index],
        "pada": pada,
        "navamsa_sign_index": navamsa,
        "navamsa_sign": SIGNS[navamsa],
        "rule_id": "sidereal-sign-nakshatra-navamsa-v1",
    }


def vimshottari_birth_sequence(
    moon_longitude: float,
    birth_time_utc: datetime,
) -> dict[str, object]:
    """Return the birth Mahadasha balance and a traceable 9-period sequence.

    The 365.25-day year is an explicit implementation convention. The start of
    the first Mahadasha is back-calculated from the elapsed portion of the Moon's
    birth Nakshatra. This sequence is not a prediction or validated timing claim.
    """
    moon = _longitude(moon_longitude, "Moon longitude")
    if birth_time_utc.tzinfo is None or birth_time_utc.utcoffset() is None:
        raise ValueError("birth_time_utc must be timezone-aware")
    birth = birth_time_utc.astimezone(timezone.utc)
    nak_index = min(26, int(moon // NAKSHATRA_SPAN))
    nak_start = nak_index * NAKSHATRA_SPAN
    fraction_elapsed = (moon - nak_start) / NAKSHATRA_SPAN
    first_lord = NAKSHATRA_LORDS[nak_index]
    first_years = VIMSHOTTARI_YEARS[first_lord]
    elapsed_days = fraction_elapsed * first_years * DASHA_YEAR_DAYS
    first_start = birth - timedelta(days=elapsed_days)

    start_idx = DASHA_SEQUENCE.index(first_lord)
    ordered = DASHA_SEQUENCE[start_idx:] + DASHA_SEQUENCE[:start_idx]
    periods = []
    cursor = first_start
    for i, lord in enumerate(ordered):
        years = VIMSHOTTARI_YEARS[lord]
        end = cursor + timedelta(days=years * DASHA_YEAR_DAYS)
        periods.append({
            "lord": lord,
            "duration_years": years,
            "start_utc": cursor.isoformat(),
            "end_utc": end.isoformat(),
            "starts_at_birth": i == 0,
            "rule_id": "vimshottari-120-year-365.25-day-year-v1",
        })
        cursor = end

    balance_years = first_years * (1.0 - fraction_elapsed)
    return {
        "birth_nakshatra": NAKSHATRAS[nak_index],
        "birth_nakshatra_lord": first_lord,
        "fraction_of_nakshatra_elapsed": round(fraction_elapsed, 10),
        "first_mahadasha_balance_years": round(balance_years, 8),
        "periods": periods,
        "conventions": {
            "cycle_years": 120,
            "year_days": DASHA_YEAR_DAYS,
            "boundary": "half-open intervals [start, end)",
            "rule_id": "vimshottari-120-year-365.25-day-year-v1",
        },
        "status": "DERIVED_UNVALIDATED",
    }


def calculate_jaimini_chara_karakas(
    sidereal_longitudes: Mapping[str, float],
    *,
    karaka_count: int = 7,
    include_rahu: bool | None = None,
) -> dict[str, object]:
    """Rank Chara Kārakas by within-sign longitude using a declared rule variant.

    Seven-karaka mode ranks Sun through Saturn. Eight-karaka mode includes Rahu,
    whose within-sign longitude is reversed (30° - within-sign degree). Ketu is
    not included. Ties are preserved and reported instead of silently broken.
    """
    if karaka_count not in (7, 8):
        raise ValueError("karaka_count must be 7 or 8")
    if include_rahu is None:
        include_rahu = karaka_count == 8
    if include_rahu != (karaka_count == 8):
        raise ValueError("include_rahu must be False for 7 karakas and True for 8")
    names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    if include_rahu:
        names.append("Rahu")
    missing = [name for name in names if name not in sidereal_longitudes]
    if missing:
        raise ValueError("Missing longitudes for: " + ", ".join(missing))

    ranked = []
    for name in names:
        lon = _longitude(sidereal_longitudes[name], f"{name} longitude")
        in_sign = lon % 30.0
        degree = 30.0 - in_sign if name == "Rahu" else in_sign
        ranked.append({"planet": name, "longitude_in_sign": round(in_sign, 8),
                       "karaka_degree": round(degree, 8)})
    ranked.sort(key=lambda item: (-item["karaka_degree"], item["planet"]))
    roles = ("Atmakaraka", "Amatyakaraka", "Bhratrikaraka", "Matrikaraka",
             "Putrakaraka", "Gnatikaraka", "Darakaraka")
    if karaka_count == 8:
        roles = ("Atmakaraka", "Amatyakaraka", "Bhratrikaraka", "Matrikaraka",
                 "Putrakaraka", "Gnatikaraka", "Darakaraka", "Pitru/Matru variant")
    for index, item in enumerate(ranked):
        item["rank"] = index + 1
        item["role"] = roles[index]
    ties = []
    for i, item in enumerate(ranked):
        for other in ranked[i + 1:]:
            if abs(item["karaka_degree"] - other["karaka_degree"]) < 1e-8:
                ties.append([item["planet"], other["planet"]])
    return {
        "karaka_count": karaka_count,
        "include_rahu": include_rahu,
        "rankings": ranked,
        "ties": ties,
        "rule_id": "jaimini-chara-karaka-within-sign-degree-v1",
        "status": "DERIVED_UNVALIDATED",
        "warning": "Chara Kāraka variants differ across traditions; confirm this rule before relying on it.",
    }


def derive_chart_factors(
    planets: Mapping[str, Mapping[str, float]],
    ascendant_longitude: float,
    birth_time_utc: datetime,
) -> dict[str, object]:
    """Derive sign/house, Nakshatra/pada, Navamsa, Vimshottari, and Jaimini factors."""
    asc = describe_longitude(ascendant_longitude)
    derived_planets: dict[str, object] = {}
    raw_longitudes: dict[str, float] = {}
    for name, item in planets.items():
        if "longitude" not in item:
            continue
        info = describe_longitude(item["longitude"])
        info["whole_sign_house"] = ((int(info["sign_index"]) - int(asc["sign_index"]) + 12) % 12) + 1
        derived_planets[name] = info
        raw_longitudes[name] = float(item["longitude"])
    if "Moon" not in raw_longitudes:
        raise ValueError("Moon longitude is required for Vimshottari derivation")
    return {
        "status": "DERIVED_UNVALIDATED",
        "ruleset_version": RULESET_VERSION,
        "ascendant": {**asc, "whole_sign_house": 1},
        "planets": derived_planets,
        "vimshottari": vimshottari_birth_sequence(raw_longitudes["Moon"], birth_time_utc),
        "jaimini_chara_karakas_7": calculate_jaimini_chara_karakas(
            raw_longitudes, karaka_count=7, include_rahu=False
        ),
        "jaimini_chara_karakas_8": calculate_jaimini_chara_karakas(
            raw_longitudes, karaka_count=8, include_rahu=True
        ),
        "warnings": [
            "Derived factors inherit any errors in the unvalidated astronomical longitudes.",
            "Traditional rule variants exist; compare these outputs with a trusted reference before use.",
        ],
    }

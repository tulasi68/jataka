"""A transparent multi-tradition outlook assembled from computed factors.

This is a time-windowed summary of traditional symbolism, not an event prediction.
It does not produce a probability, claim three independent astronomical engines,
or silently convert low bindu counts into good/bad life outcomes.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Mapping

from jataka.report_engine import PLANET_TOPICS

DASHA_ORDER = ("Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury")
DASHA_YEARS = {"Ketu":7, "Venus":20, "Sun":6, "Moon":10, "Mars":7,
               "Rahu":18, "Jupiter":16, "Saturn":19, "Mercury":17}
DAYS_PER_YEAR = 365.25
DASHA_REFLECTIONS = {
    "Ketu": "simplification, inward attention, and reassessing attachments",
    "Venus": "relationships, values, creativity, and comfort",
    "Sun": "purpose, visibility, confidence, and responsibility",
    "Moon": "habits, care, belonging, and emotional rhythms",
    "Mars": "initiative, boundaries, effort, and handling friction",
    "Rahu": "novelty, ambition, unfamiliar territory, and discernment",
    "Jupiter": "learning, guidance, meaning, and growth",
    "Saturn": "patience, duty, limits, and sustainable commitments",
    "Mercury": "learning, communication, analysis, and practical choices",
}


def _active_antardasha(maha: Mapping[str, object], now: datetime) -> dict[str, object] | None:
    lord = str(maha["lord"])
    start = datetime.fromisoformat(str(maha["start_utc"]))
    maha_end = datetime.fromisoformat(str(maha["end_utc"]))
    cycle = DASHA_ORDER[DASHA_ORDER.index(lord):] + DASHA_ORDER[:DASHA_ORDER.index(lord)]
    cursor = start
    for sublord in cycle:
        duration = timedelta(days=float(maha["duration_years"]) * DASHA_YEARS[sublord] / 120 * DAYS_PER_YEAR)
        end = cursor + duration
        if cursor <= now < end:
            return {
                "lord": sublord,
                "start_utc": cursor.isoformat(),
                "end_utc": end.isoformat(),
                "traditional_themes": DASHA_REFLECTIONS[sublord],
            }
        cursor = end
    return None


def build_multi_pass_outlook(
    derived: Mapping[str, object],
    ashtakavarga: Mapping[str, object],
    transit_analysis: Mapping[str, object],
    verification: Mapping[str, object],
    *,
    numerology: Mapping[str, object] | None = None,
    palmistry: Mapping[str, object] | None = None,
    now_utc: datetime | None = None,
) -> dict[str, object]:
    """Produce a transparent dashboard across the three traditional analysis passes."""
    now = (now_utc or datetime.now(timezone.utc)).astimezone(timezone.utc)
    vim = derived.get("vimshottari", {})
    periods = vim.get("periods", []) if isinstance(vim, Mapping) else []
    active = None
    for period in periods:
        if not isinstance(period, Mapping):
            continue
        start = datetime.fromisoformat(str(period["start_utc"]))
        end = datetime.fromisoformat(str(period["end_utc"]))
        if start <= now < end:
            active = dict(period)
            active["antardasha"] = _active_antardasha(period, now)
            active["traditional_themes"] = DASHA_REFLECTIONS.get(str(period["lord"]), "traditional planetary themes")
            break

    jaimini = derived.get("jaimini", {})
    arudha_sign = None
    atmakaraka = None
    if isinstance(jaimini, Mapping):
        arudhas = jaimini.get("arudha_padas", {})
        if isinstance(arudhas, Mapping):
            al = arudhas.get("arudha_lagna", {})
            if isinstance(al, Mapping):
                arudha_sign = al.get("arudha_sign")
        karakas = jaimini.get("chara_karakas", {})
        if isinstance(karakas, Mapping):
            rankings = karakas.get("rankings", [])
            if rankings and isinstance(rankings[0], Mapping):
                atmakaraka = rankings[0].get("planet")

    transit_rows = transit_analysis.get("transits", []) if isinstance(transit_analysis, Mapping) else []
    transit_summary = []
    for row in transit_rows:
        if not isinstance(row, Mapping):
            continue
        points = int(row.get("natal_bav_bindus_in_transit_sign", 0))
        transit_summary.append({
            "planet": row.get("planet"),
            "sign": row.get("transit_sign"),
            "bindus": points,
            "house_from_moon": row.get("transit_house_from_moon"),
            "house_from_ascendant": row.get("transit_house_from_ascendant"),
            "count_note": (
                "above four bindus in this sign" if points > 4
                else "four bindus in this sign" if points == 4
                else "below four bindus in this sign"
            ),
            "meaning": "Traditional sign-based count only; not an event forecast.",
        })

    return {
        "status": "MULTI_PASS_TRADITIONAL_OUTLOOK_UNVALIDATED",
        "generated_at_utc": now.isoformat(),
        "title": "Jataka — Multi-pass traditional outlook",
        "passes": [
            {
                "name": "Parāśari / Drik",
                "state": "computed_unvalidated",
                "current_vimshottari_mahadasha": active,
                "meaning": "The current period's traditional symbolic topics are shown as reflection prompts, not predicted events.",
            },
            {
                "name": "Jaimini",
                "state": "computed_unvalidated",
                "arudha_lagna_sign": arudha_sign,
                "atmakaraka": atmakaraka,
                "meaning": "Arūḍha and Chara Kāraka values depend on the chosen tradition and require reference validation.",
            },
            {
                "name": "Ashtakavarga / Gochara",
                "state": "computed_unvalidated",
                "sarvashtakavarga_total": (ashtakavarga.get("sarvashtakavarga", {}) or {}).get("total"),
                "transit_indicators": transit_summary,
                "meaning": "Bindu counts and transit signs are descriptive traditional indicators, not probabilities.",
            },
        ],
        "optional_traditions": {
            "numerology": {
                "included": numerology is not None,
                "status": numerology.get("status") if numerology else "not_requested",
                "warning": "Numerology is separate from the three astrology passes and is not independently validated.",
            },
            "palmistry": {
                "included": palmistry is not None,
                "status": palmistry.get("status") if palmistry else "not_requested",
                "warning": "Palmistry observations are user-recorded and folklore-based; no image was analysed.",
            },
        },
        "verification": dict(verification),
        "synthesis": (
            "The application presents three traditional analysis lenses side by side. "
            "They share the same natal astronomical positions, so this is not independent three-pass "
            "verification. No combined prediction score or probability is calculated."
        ),
        "disclaimer": (
            "Astrology, numerology and palmistry are cultural/divinatory traditions, not scientifically "
            "validated methods for reliably predicting life events. Do not use this report as the sole "
            "basis for medical, legal, financial, relationship, or other high-stakes decisions."
        ),
    }

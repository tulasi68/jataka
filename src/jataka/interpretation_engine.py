"""Evidence-led, plain-language interpretations of traditional Jyotish factors.

The interpretation layer explains why a chart-specific traditional theme was selected.
It does not alter astronomical calculations, infer missing birth data, or claim certainty.
"""
from __future__ import annotations

from typing import Mapping

from jataka.report_engine import SIGN_REFLECTIONS

SIGN_RULERS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}
PLANET_THEMES = {
    "Sun": "purpose, authority, visibility, and responsibility",
    "Moon": "everyday habits, emotional needs, care, and belonging",
    "Mercury": "analysis, communication, learning, and practical decisions",
    "Venus": "relationships, agreement, comfort, aesthetics, and values",
    "Mars": "initiative, technical action, competition, and handling friction",
    "Jupiter": "teaching, counsel, principles, and broadening understanding",
    "Saturn": "duty, structure, persistence, limits, and long-term work",
    "Rahu": "ambition, experimentation, appetite, and unfamiliar territory",
    "Ketu": "specialisation, simplification, detachment, and inward focus",
}
HOUSE_THEMES = {
    1: "the way you approach life and present yourself",
    2: "family, savings, speech, and what you value",
    3: "self-effort, communication, practice, and practical courage",
    4: "home, roots, private life, and emotional security",
    5: "creative work, learning, judgement, and self-expression",
    6: "daily work, service, routines, and solving problems",
    7: "one-to-one relationships, clients, partnerships, and agreements",
    8: "shared resources, obligations, uncertainty, and deep change",
    9: "higher learning, principles, mentors, and wider horizons",
    10: "career, public responsibilities, and contribution",
    11: "income from work, networks, communities, and long-range goals",
    12: "rest, privacy, expenses, retreat, and matters behind the scenes",
}
AREAS = [
    {"key": "Self-understanding", "houses": (1,), "primary": 1,
     "question": "What style of approach or self-presentation do you recognise in your own life?"},
    {"key": "Work and contribution", "houses": (10, 6), "primary": 10,
     "question": "Which parts of your work involve responsibility, service, problem-solving, or public contribution?"},
    {"key": "Relationships and cooperation", "houses": (7, 2), "primary": 7,
     "question": "How do partnership, clients, agreements, family values, and communication interact in your experience?"},
    {"key": "Money, values and security", "houses": (2, 11), "primary": 2,
     "question": "How do saving, speech, networks, and long-term goals fit together in your real financial life?"},
    {"key": "Home and private life", "houses": (4, 12), "primary": 4,
     "question": "What balance do you need between home responsibilities, private time, and outside demands?"},
    {"key": "Learning and judgement", "houses": (5, 9, 3), "primary": 9,
     "question": "Which forms of study, practice, mentoring, or creative thinking have actually helped you grow?"},
]


def _map(value: object) -> Mapping[str, object]:
    return value if isinstance(value, Mapping) else {}


def _planet_name_for_house(house: int, asc_index: int) -> str | None:
    sign = _sign((asc_index + house - 1) % 12)
    return SIGN_RULERS.get(sign)


def _sign(index: int) -> str:
    signs = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
    return signs[index % 12]


def _placement_sentence(name: str, planets: Mapping[str, object]) -> str | None:
    item = _map(planets.get(name))
    if not item:
        return None
    sign = str(item.get("sign", "unknown sign"))
    house = int(item.get("whole_sign_house", 0) or 0)
    if not house:
        return f"{name} is shown in {sign}, but its house is unavailable."
    ordinal = {1:"1st", 2:"2nd", 3:"3rd"}.get(house, f"{house}th")
    theme = PLANET_THEMES.get(name, "its traditional planetary themes")
    sign_theme = SIGN_REFLECTIONS.get(sign, "the sign's traditional symbolism")
    return (
        f"{name} is in {sign}, in the {ordinal} house. Traditional Jyotish associates "
        f"{name} with {theme}; {sign} with {sign_theme}; and the {ordinal} house with "
        f"{HOUSE_THEMES[house]}. These are the specific symbols used in this reading."
    )


def _ruler_reading(house: int, asc_index: int, planets: Mapping[str, object]) -> dict[str, object]:
    house_sign = _sign((asc_index + house - 1) % 12)
    ruler = SIGN_RULERS[house_sign]
    ruler_item = _map(planets.get(ruler))
    ruler_house = int(ruler_item.get("whole_sign_house", 0) or 0)
    ruler_sign = str(ruler_item.get("sign", "unknown sign"))
    if ruler_house:
        destination = HOUSE_THEMES[ruler_house]
        ruler_sentence = (
            f"The {house}th-house sign is {house_sign}, whose traditional ruler is {ruler}. "
            f"{ruler} is placed in {ruler_sign}, house {ruler_house}. In this Jyotish framework, "
            f"that connects {HOUSE_THEMES[house]} with {destination}. "
            "This house-ruler connection is the main reason for the interpretation below."
        )
        link = {
            "house": house, "house_sign": house_sign, "ruler": ruler,
            "ruler_sign": ruler_sign, "ruler_house": ruler_house,
            "topic": HOUSE_THEMES[house], "linked_topic": destination,
        }
    else:
        ruler_sentence = (
            f"The {house}th-house sign is {house_sign}, traditionally ruled by {ruler}, "
            "but the ruler's placement is unavailable, so this report does not infer a house-to-house link."
        )
        link = {"house": house, "house_sign": house_sign, "ruler": ruler, "ruler_house": None}
    return {"ruler": ruler, "house_sign": house_sign, "ruler_house": ruler_house or None,
            "evidence": ruler_sentence, "link": link}


def _area_reading(area: Mapping[str, object], asc_index: int, planets: Mapping[str, object]) -> dict[str, object]:
    primary = int(area["primary"])
    ruler = _ruler_reading(primary, asc_index, planets)
    occupants = []
    for name, value in planets.items():
        item = _map(value)
        if int(item.get("whole_sign_house", 0) or 0) in tuple(area["houses"]):
            occupants.append({
                "planet": str(name),
                "sign": str(item.get("sign", "unknown")),
                "house": int(item.get("whole_sign_house", 0) or 0),
                "theme": PLANET_THEMES.get(str(name), "traditional planetary themes"),
            })
    if ruler["ruler_house"]:
        linked = str(ruler["link"]["linked_topic"])
        explanation = (
            f"For {str(area['key']).lower()}, the chart-specific connection is between "
            f"{HOUSE_THEMES[primary]} and {linked}. The traditional ruler is {ruler['ruler']}, "
            f"placed in house {ruler['ruler_house']}. This describes how the tradition connects "
            "two topics; it does not establish that an event will occur."
        )
    else:
        explanation = (
            f"This section focuses on {HOUSE_THEMES[primary]}. The ruler placement needed for a more "
            "specific house-to-house interpretation is unavailable, so no further conclusion is drawn."
        )
    return {
        "title": str(area["key"]),
        "question": str(area["question"]),
        "specific_interpretation": explanation,
        "reasoning": ruler["evidence"],
        "ruler_link": ruler["link"],
        "occupants": occupants,
        "confidence_label": "Traditional interpretation · unvalidated",
        "scope_note": (
            "This is a specific reading of the selected house-ruler rule. It is not a claim about your actual "
            "character, success, finances, relationship status, or future; compare it with concrete life experience."
        ),
    }


def build_common_reading(
    derived: Mapping[str, object],
    multi_pass_outlook: Mapping[str, object],
    verification: Mapping[str, object],
    *,
    numerology: Mapping[str, object] | None = None,
    palmistry: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Build chart-specific explanations with an explicit evidence trail."""
    planets = _map(derived.get("planets"))
    asc = _map(derived.get("ascendant"))
    asc_index = int(asc.get("sign_index", 0) or 0)
    asc_sign = str(asc.get("sign", _sign(asc_index)))
    lagna_lord = SIGN_RULERS.get(asc_sign)
    moon = _map(planets.get("Moon"))
    sun = _map(planets.get("Sun"))

    anchors = []
    if lagna_lord and _map(planets.get(lagna_lord)):
        p = _map(planets.get(lagna_lord))
        house = int(p.get("whole_sign_house", 0) or 0)
        anchors.append({
            "title": "The chart's starting point",
            "finding": f"The ascendant is {asc_sign}; its traditional ruler is {lagna_lord}.",
            "meaning": (
                f"{lagna_lord} is in {p.get('sign', 'an unavailable sign')}, house {house}. "
                f"The {lagna_lord} symbolically relates to {PLANET_THEMES.get(lagna_lord, 'its traditional themes')}, "
                f"while house {house} relates to {HOUSE_THEMES.get(house, 'a life area')}. "
                "In this tradition, the ascendant ruler's placement is used as a central organising theme, "
                "not as a complete description of your personality."
            ),
            "evidence": {"ascendant_sign": asc_sign, "ascendant_ruler": lagna_lord,
                         "ruler_sign": p.get("sign"), "ruler_house": house},
        })
    if moon:
        mhouse = int(moon.get("whole_sign_house", 0) or 0)
        anchors.append({
            "title": "The Moon's specific place in the chart",
            "finding": f"Moon in {moon.get('sign', 'unknown')}, house {mhouse}.",
            "meaning": (
                f"The Moon is traditionally read for habits, felt security, and day-to-day responses. "
                f"Here it is in {moon.get('sign', 'an unknown sign')} "
                f"({SIGN_REFLECTIONS.get(str(moon.get('sign')), 'traditional sign symbolism')}) "
                f"and house {mhouse} ({HOUSE_THEMES.get(mhouse, 'a life area')}). "
                f"The chart-specific combination therefore connects these themes with "
                f"{HOUSE_THEMES.get(mhouse, 'that life area')}; it does not tell us how you actually feel."
            ),
            "evidence": {"planet": "Moon", "sign": moon.get("sign"), "house": mhouse,
                         "nakshatra": moon.get("nakshatra"), "pada": moon.get("pada")},
        })
    if sun:
        shouse = int(sun.get("whole_sign_house", 0) or 0)
        anchors.append({
            "title": "Purpose and responsibility",
            "finding": f"Sun in {sun.get('sign', 'unknown')}, house {shouse}.",
            "meaning": (
                f"The Sun is traditionally associated with purpose, visibility, and responsibility. "
                f"In this chart it is in {sun.get('sign', 'an unknown sign')} and house {shouse}, "
                f"linking those symbols with {HOUSE_THEMES.get(shouse, 'a life area')}. "
                "This is a symbolic emphasis, not proof of status, authority, or career outcome."
            ),
            "evidence": {"planet": "Sun", "sign": sun.get("sign"), "house": shouse},
        })

    area_readings = [_area_reading(area, asc_index, planets) for area in AREAS]
    outlook_passes = _map(multi_pass_outlook).get("passes", [])
    if not isinstance(outlook_passes, list):
        outlook_passes = []
    jaimini = next((p for p in outlook_passes if isinstance(p, Mapping) and p.get("name") == "Jaimini"), {})
    transit = next((p for p in outlook_passes if isinstance(p, Mapping) and p.get("name") == "Ashtakavarga / Gochara"), {})
    extra_lenses = []
    arudha_sign = _map(jaimini).get("arudha_lagna_sign")
    if arudha_sign:
        extra_lenses.append({
            "title": "Public image — Jaimini lens",
            "text": (
                f"The computed Arudha Lagna is {arudha_sign}. In a Jaimini tradition, it is used to discuss "
                "how a person or situation appears outwardly. Its sign theme is "
                f"{SIGN_REFLECTIONS.get(str(arudha_sign), 'not available')}. This is not evidence of how others see you."
            ),
            "evidence": {"arudha_lagna_sign": arudha_sign},
        })
    atmakaraka = _map(jaimini).get("atmakaraka")
    if atmakaraka:
        extra_lenses.append({
            "title": "Jaimini self-development lens",
            "text": (
                f"The selected seven-karaka calculation assigns Atmakaraka to {atmakaraka}. "
                f"Traditional interpretations associate this planet with {PLANET_THEMES.get(str(atmakaraka), 'its planetary themes')}. "
                "This role depends on a rule variant that has not been independently checked."
            ),
            "evidence": {"atmakaraka": atmakaraka},
        })
    sav = _map(transit).get("sarvashtakavarga_total")
    if sav is not None:
        extra_lenses.append({
            "title": "Ashtakavarga and current transits",
            "text": (
                f"The calculated Sarvashtakavarga sum is {sav}. It is a traditional tally, not a score out of 100 "
                "and not a measure of whether life is good or bad. Individual transit sign counts are shown as "
                "descriptive values in the technical details; they are not converted into event predictions."
            ),
            "evidence": {"sarvashtakavarga_total": sav},
        })

    active_period = None
    for item in outlook_passes:
        if isinstance(item, Mapping) and item.get("current_vimshottari_mahadasha"):
            active_period = _map(item.get("current_vimshottari_mahadasha"))
            break
    period = None
    if active_period:
        maha = str(active_period.get("lord", "unknown"))
        sub = _map(active_period.get("antardasha"))
        sublord = str(sub.get("lord")) if sub.get("lord") else None
        period_planets = []
        for name in (maha, sublord):
            if name and _map(planets.get(name)):
                p = _map(planets.get(name))
                house = int(p.get("whole_sign_house", 0) or 0)
                period_planets.append({
                    "planet": name, "sign": p.get("sign"), "house": house,
                    "house_theme": HOUSE_THEMES.get(house, "a life area"),
                    "planet_theme": PLANET_THEMES.get(name, "traditional planetary themes"),
                })
        period = {
            "mahadasha": maha, "antardasha": sublord,
            "themes": active_period.get("traditional_themes", ""),
            "subperiod_themes": sub.get("traditional_themes", ""),
            "natal_links": period_planets,
            "plain_language": (
                f"The selected Vimshottari convention places this date in the {maha} major period"
                + (f" and {sublord} sub-period" if sublord else "")
                + ". Rather than treating the period name alone as a prediction, this reading shows where "
                "those planets are placed in the natal chart and which life topics the tradition associates with them. "
                "The period timing and interpretation remain unvalidated."
            ),
        }

    return {
        "status": "PERSONALISED_EVIDENCE_LED_INTERPRETATION_UNVALIDATED",
        "title": "Your Jataka — what the chart specifically says",
        "opening": (
            f"The ascendant calculated from the supplied birth details is {asc_sign}. "
            "The reading below uses the actual sign, house, and house-ruler relationships in this chart. "
            "Each conclusion includes the traditional rule behind it, so you can see why it appears."
        ),
        "quick_view": [
            {"label": "Ascendant", "text": f"{asc_sign}; its traditional ruler is {lagna_lord or 'not available'}."},
            {"label": "Moon placement", "text": f"{moon.get('sign', 'unavailable')}, house {moon.get('whole_sign_house', 'unavailable')}; Nakshatra {moon.get('nakshatra', 'unavailable')}, pada {moon.get('pada', 'unavailable')}."},
            {"label": "Sun placement", "text": f"{sun.get('sign', 'unavailable')}, house {sun.get('whole_sign_house', 'unavailable')}."},
        ],
        "main_takeaways": anchors,
        "area_readings": area_readings,
        "life_areas": [],
        "additional_lenses": extra_lenses,
        "current_period": period,
        "how_methods_fit": {
            "status": _map(verification).get("status", "status unavailable"),
            "text": (
                "Parashari/Drik, Jaimini, and Ashtakavarga/transit are separate traditional lenses, but all currently "
                "derive from the same natal longitudes. Their agreement is not independent verification. "
                "Reference-chart checks and rule-variant validation remain outstanding."
            ),
        },
        "optional_reflections": {
            "numerology_included": numerology is not None,
            "numerology_note": "Numerology is shown separately and does not corroborate the horoscope." if numerology is not None else None,
            "palmistry_included": palmistry is not None,
            "palmistry_note": "Palmistry uses only observations entered by the user; it is not image analysis or independent verification." if palmistry is not None else None,
        },
        "practical_guidance": [
            "Start with the evidence line under each conclusion: it names the house, ruler, sign, or planet used.",
            "Compare a traditional theme with specific events and choices in your own life; do not force a match.",
            "Where the chart's factors point to different topics, treat that as a mixed interpretation rather than hiding the difference.",
        ],
        "limitations": [
            "Astronomical positions and derived factors remain UNVALIDATED against independently sourced reference charts.",
            "House-ruler readings are one traditional Jyotish convention; other schools can interpret factors differently.",
            "The current interpretation does not yet assess every classical condition, aspect, dignity, combustion, retrogression, or divisional-chart rule.",
            "Astrology, numerology, and palmistry are not scientifically established methods for predicting individual life events.",
            "No probability, guaranteed outcome, or good/bad fate label is produced.",
        ],
        "disclaimer": (
            "This is a chart-specific explanation of selected traditional Jyotish rules, not a scientific personality test "
            "or a guaranteed forecast. Use real-world evidence for important decisions."
        ),
    }

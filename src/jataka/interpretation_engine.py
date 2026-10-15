"""Plain-language interpretation layer for everyday readers.

This module translates computed traditional symbols into understandable reflection
prompts. It never labels a person, predicts events, assigns probabilities, or
presents an unvalidated chart as fact.
"""
from __future__ import annotations

from typing import Mapping

from jataka.report_engine import HOUSE_TOPICS, PLANET_TOPICS, SIGN_REFLECTIONS

HOUSE_PLAIN = {
    1: "your way of approaching life and presenting yourself",
    2: "money habits, family, values, and communication",
    3: "learning, initiative, everyday courage, and communication",
    4: "home, family roots, comfort, and emotional security",
    5: "creativity, enjoyment, learning, and self-expression",
    6: "daily routines, service, practical problems, and responsibilities",
    7: "close relationships, cooperation, and agreements",
    8: "shared responsibilities, uncertainty, and major changes",
    9: "beliefs, education, mentors, and broader horizons",
    10: "work, responsibility, and contribution to the wider world",
    11: "friendships, communities, networks, and shared goals",
    12: "rest, privacy, reflection, and letting go",
}

PLANET_PLAIN = {
    "Sun": "purpose, confidence, identity, and responsibility",
    "Moon": "emotional needs, habits, belonging, and a sense of security",
    "Mercury": "thinking, learning, communication, and weighing choices",
    "Venus": "affection, relationships, beauty, comfort, and personal values",
    "Mars": "initiative, energy, boundaries, and handling disagreement",
    "Jupiter": "learning, guidance, meaning, generosity, and growth",
    "Saturn": "patience, duty, limits, persistence, and long-term effort",
    "Rahu": "ambition, curiosity, novelty, and unfamiliar experiences",
    "Ketu": "simplification, inward attention, and loosening attachments",
}

AREA_HOUSES = {
    "Self-understanding": (1,),
    "Work and contribution": (10, 6),
    "Relationships and cooperation": (7, 2),
    "Money, values and security": (2, 11, 8),
    "Home and wellbeing": (4, 12, 6),
    "Learning and personal growth": (3, 5, 9),
}


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, Mapping) else {}


def _plain_placement(name: str, placement: Mapping[str, object]) -> dict[str, object]:
    sign = str(placement.get("sign", "unknown"))
    house = int(placement.get("whole_sign_house", 0) or 0)
    topic = HOUSE_PLAIN.get(house, "a life area")
    planet_theme = PLANET_PLAIN.get(name, PLANET_TOPICS.get(name, "traditional symbolism"))
    sign_theme = SIGN_REFLECTIONS.get(sign, "traditional symbolic themes")
    ordinal = {1: "1st", 2: "2nd", 3: "3rd"}.get(house, f"{house}th")
    return {
        "planet": name,
        "sign": sign,
        "house": house or None,
        "life_area": topic,
        "traditional_theme": planet_theme,
        "sign_theme": sign_theme,
        "plain_language": (
            f"In traditional Jyotish, {name} is associated with {planet_theme}. "
            f"Placed in the {ordinal} house, it is traditionally discussed in connection with {topic}. "
            "Use this as a question to reflect on your own experience, not as a statement "
            "that this trait or outcome must apply to you."
        ) if house else (
            f"In traditional Jyotish, {name} is associated with {planet_theme}; "
            f"its sign, {sign}, is symbolically associated with {sign_theme}. "
            "This is a cultural interpretation, not a measured personality finding."
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
    """Build an everyday-language reading from the existing computed factors."""
    planets = _mapping(derived.get("planets"))
    asc = _mapping(derived.get("ascendant"))
    asc_sign = str(asc.get("sign", "not available"))
    moon = _mapping(planets.get("Moon"))
    sun = _mapping(planets.get("Sun"))

    sections: list[dict[str, object]] = []
    for title, houses in AREA_HOUSES.items():
        matches = [
            _plain_placement(str(name), _mapping(item))
            for name, item in planets.items()
            if isinstance(item, Mapping)
            and int(_mapping(item).get("whole_sign_house", 0) or 0) in houses
        ]
        # Do not treat an empty house as evidence that an area is absent or deficient.
        sections.append({
            "title": title,
            "traditional_question": (
                f"Which parts of {title.lower()} are most relevant in your life right now?"
            ),
            "interpretations": matches[:4],
            "note": (
                "These are symbolic associations from the selected Jyotish conventions. "
                "They are prompts for reflection, not a verdict or forecast."
                if matches else
                "No listed planet occupies the selected houses in this calculation. "
                "That does not mean this area of life is missing, weak, or unimportant; "
                "this brief reading does not interpret house rulers or every traditional factor."
            ),
        })

    active_period = None
    for p in _mapping(multi_pass_outlook).get("passes", []) if isinstance(_mapping(multi_pass_outlook).get("passes", []), list) else []:
        if isinstance(p, Mapping) and p.get("current_vimshottari_mahadasha"):
            active_period = _mapping(p.get("current_vimshottari_mahadasha"))
            break
    period = None
    if active_period:
        sub = _mapping(active_period.get("antardasha"))
        period = {
            "mahadasha": active_period.get("lord"),
            "antardasha": sub.get("lord") if sub else None,
            "themes": active_period.get("traditional_themes", ""),
            "subperiod_themes": sub.get("traditional_themes", "") if sub else "",
            "plain_language": (
                "The traditional Vimshottari system associates the current major period "
                f"with {active_period.get('traditional_themes', 'symbolic themes')}"
                + (f", and its sub-period with {sub.get('traditional_themes')}." if sub else ".")
                + " This is a traditional timing framework, not evidence that a specific event will happen."
            ),
        }

    return {
        "status": "PLAIN_LANGUAGE_TRADITIONAL_INTERPRETATION_UNVALIDATED",
        "title": "Your Jataka — explained in everyday language",
        "opening": (
            f"The calculated ascendant is {asc_sign}. In traditional Jyotish, this sign is "
            f"associated with {SIGN_REFLECTIONS.get(asc_sign, 'symbolic themes')}. "
            "Think of this as one lens for reflection, not a fixed description of who you are."
        ),
        "quick_view": [
            {
                "label": "Starting point",
                "text": (
                    f"Ascendant: {asc_sign}. Traditional theme: "
                    f"{SIGN_REFLECTIONS.get(asc_sign, 'not available')}."
                ),
            },
            {
                "label": "Emotional life and habits",
                "text": (
                    f"Moon in {moon.get('sign', 'an unavailable sign')} is traditionally associated "
                    f"with {PLANET_PLAIN['Moon']}. This does not establish your actual feelings "
                    "or personality; compare it with your lived experience."
                ) if moon else "Moon placement unavailable.",
            },
            {
                "label": "Purpose and responsibility",
                "text": (
                    f"Sun in {sun.get('sign', 'an unavailable sign')} is traditionally associated "
                    f"with {PLANET_PLAIN['Sun']}. Treat this as a reflection prompt, not a verdict."
                ) if sun else "Sun placement unavailable.",
            },
        ],
        "life_areas": sections,
        "current_period": period,
        "how_methods_fit": {
            "status": _mapping(verification).get("status", "status unavailable"),
            "text": (
                "Jataka combines Parashari/Drik placements, Jaimini factors, and "
                "Ashtakavarga/transit indicators as three traditional analysis perspectives. "
                "They currently share the same underlying natal longitudes, so agreement between "
                "them is not independent verification. Reference-chart validation is still outstanding."
            ),
        },
        "optional_reflections": {
            "numerology_included": numerology is not None,
            "numerology_note": (
                "Name and birth-date numerology is shown separately as a cultural reflection system; "
                "it does not verify the horoscope."
            ) if numerology is not None else None,
            "palmistry_included": palmistry is not None,
            "palmistry_note": (
                "Palmistry uses only observations you recorded. It is not an automatic palm reading "
                "and does not establish lifespan, health, or future events."
            ) if palmistry is not None else None,
        },
        "practical_guidance": [
            "Use the themes to ask useful questions, not to make decisions out of fear.",
            "For work, money, relationships, and health, combine reflection with real-world evidence and qualified advice where appropriate.",
            "Keep what genuinely resonates with your experience; set aside what does not.",
        ],
        "limitations": [
            "The astronomical and derived calculations remain UNVALIDATED against independently sourced reference charts.",
            "Traditional symbolism is not scientific proof of personality or future events.",
            "An empty house does not mean that the related area of life is absent or destined to fail.",
            "No probabilities, guaranteed predictions, or good/bad fate labels are generated.",
        ],
        "disclaimer": (
            "This is an interpretation of traditional Jyotish symbolism for reflection. "
            "It is not a scientific assessment, guaranteed prediction, or substitute for professional advice."
        ),
    }

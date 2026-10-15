"""Cautious, deterministic reflective report from derived Jyotish factors.

This module does not predict outcomes. It translates calculated placements into
traditional symbolic topics and explicitly keeps interpretation separate from
the ephemeris calculation.
"""
from __future__ import annotations

from typing import Mapping

SIGN_REFLECTIONS = {
    "Aries": "initiative, directness, and beginning things",
    "Taurus": "steadiness, practical values, and continuity",
    "Gemini": "curiosity, communication, and learning",
    "Cancer": "care, belonging, and emotional security",
    "Leo": "creative expression, visibility, and generosity",
    "Virgo": "craft, discernment, and improving systems",
    "Libra": "balance, dialogue, and cooperation",
    "Scorpio": "depth, privacy, and sustained investigation",
    "Sagittarius": "meaning, exploration, and broad perspectives",
    "Capricorn": "structure, responsibility, and long-term effort",
    "Aquarius": "systems thinking, community, and experimentation",
    "Pisces": "imagination, empathy, and reflection",
}
PLANET_TOPICS = {
    "Sun": "identity, purpose, confidence, and responsibility",
    "Moon": "emotional rhythms, habits, belonging, and felt safety",
    "Mercury": "communication, analysis, learning, and trade-offs",
    "Venus": "affection, aesthetics, values, and relationship style",
    "Mars": "initiative, boundaries, energy, and handling disagreement",
    "Jupiter": "learning, meaning, guidance, and growth",
    "Saturn": "duty, patience, limits, and sustainable effort",
    "Rahu": "ambition, novelty, appetite, and unfamiliar territory",
    "Ketu": "simplification, detachment, and inward attention",
}
HOUSE_TOPICS = {
    1: "identity, body, and approach to life",
    2: "resources, family, and speech",
    3: "communication, practice, and initiative",
    4: "home, roots, and inner security",
    5: "creativity, learning, and play",
    6: "service, routines, and problem-solving",
    7: "partnerships, agreements, and cooperation",
    8: "shared resources, uncertainty, and change",
    9: "beliefs, higher learning, and wider horizons",
    10: "work, responsibility, and public contribution",
    11: "community, networks, and shared goals",
    12: "rest, retreat, and letting go",
}


def _placement(planets: Mapping[str, object], name: str) -> Mapping[str, object] | None:
    value = planets.get(name)
    return value if isinstance(value, Mapping) else None


def _location_text(name: str, placement: Mapping[str, object] | None) -> str:
    if not placement:
        return f"{name}: placement unavailable."
    return (
        f"{name} in {placement.get('sign', 'an unknown sign')}, "
        f"whole-sign house {placement.get('whole_sign_house', '?')}: "
        f"traditional themes include {PLANET_TOPICS.get(name, 'traditional significations')}. "
        f"This can be used as a reflection prompt about "
        f"{HOUSE_TOPICS.get(int(placement.get('whole_sign_house', 1)), 'life topics')}."
    )


def build_personal_report(derived: Mapping[str, object]) -> dict[str, object]:
    """Build a non-predictive personal reflection report from derived placements."""
    planets_obj = derived.get("planets", {})
    if not isinstance(planets_obj, Mapping):
        raise ValueError("derived planets must be a mapping")
    planets = planets_obj
    asc_obj = derived.get("ascendant", {})
    if not isinstance(asc_obj, Mapping):
        raise ValueError("derived ascendant must be a mapping")
    asc = asc_obj
    asc_sign = str(asc.get("sign", "unknown"))
    moon = _placement(planets, "Moon")
    sun = _placement(planets, "Sun")
    tenth = sorted(
        (name for name, item in planets.items()
         if isinstance(item, Mapping) and item.get("whole_sign_house") == 10)
    )
    seventh = sorted(
        (name for name, item in planets.items()
         if isinstance(item, Mapping) and item.get("whole_sign_house") == 7)
    )
    venus = _placement(planets, "Venus")

    overview = (
        f"The supplied ascendant falls in {asc_sign}. In traditional Jyotish symbolism, "
        f"this sign is associated with {SIGN_REFLECTIONS.get(asc_sign, 'a set of symbolic themes')}. "
        "Treat this as a cultural reflection framework, not a measured personality assessment."
    )
    sections = [
        {
            "title": "Self-understanding",
            "summary": overview,
            "placements": [
                _location_text("Ascendant", {**asc, "whole_sign_house": 1}),
                _location_text("Sun", sun),
                _location_text("Moon", moon),
            ],
            "questions": [
                "Which of these themes feels recognisable in your lived experience?",
                "Which parts do not fit, and what real-life examples explain the difference?",
            ],
        },
        {
            "title": "Work and contribution",
            "summary": (
                "The tenth whole-sign house is traditionally associated with work, "
                "responsibility, and public contribution. "
                + ("Bodies shown there: " + ", ".join(tenth) + ". " if tenth
                   else "No listed planet falls in the tenth whole-sign house. ")
                + "This is a prompt for reflection, not a career forecast."
            ),
            "placements": [
                _location_text(name, _placement(planets, name)) for name in tenth
            ] or ["The tenth-house sign and its ruler have not yet been interpreted in this report."],
            "questions": [
                "Which responsibilities give you a sense of useful contribution?",
                "What skills would you like to strengthen over the next year?",
            ],
        },
        {
            "title": "Relationships and cooperation",
            "summary": (
                "The seventh whole-sign house is traditionally associated with "
                "partnerships and agreements. "
                + ("Bodies shown there: " + ", ".join(seventh) + ". " if seventh
                   else "No listed planet falls in the seventh whole-sign house. ")
                + "Venus is included as a separate traditional relationship symbol; "
                "this does not predict relationship outcomes."
            ),
            "placements": [
                _location_text(name, _placement(planets, name)) for name in seventh
            ] + ([_location_text("Venus", venus)] if venus else []),
            "questions": [
                "Which agreements benefit from clearer communication?",
                "What helps you balance care for others with your own boundaries?",
            ],
        },
        {
            "title": "Strengths, challenges, and reflection",
            "summary": (
                "Traditional planetary themes can be used to organise reflection, "
                "but this report does not classify a person as destined for success "
                "or difficulty. Consider the examples below alongside lived experience."
            ),
            "placements": [
                _location_text(name, _placement(planets, name))
                for name in ("Mercury", "Mars", "Jupiter", "Saturn")
            ],
            "questions": [
                "Which habit has helped you handle a difficult situation?",
                "Where would a practical change, support, or new skill help most?",
            ],
        },
    ]
    return {
        "status": "INTERPRETIVE_REFLECTION_NOT_PREDICTION",
        "title": "Jataka — Personal Reflection Report",
        "basis": "Supplied birth inputs and derived placements, all unvalidated",
        "sections": sections,
        "disclaimer": (
            "Traditional symbolic interpretation only. This report is not a scientific "
            "personality assessment, guaranteed prediction, or substitute for professional advice."
        ),
    }

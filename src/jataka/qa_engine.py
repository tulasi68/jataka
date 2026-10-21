"""Deterministic, rule-based Q&A over computed chart factors.

The engine maps a free-text question to the life areas and time periods the
selected Jyotish tradition uses, then reports what the tradition says about the
relevant factors in this specific chart. It does not predict events, produce
probabilities, or answer yes/no fate questions. Every answer carries the
evidence used and an explicit non-prediction scope note.

The Vimśottarī timeline is clamped to the person's life window: past periods
start at birth (never before), and only the buckets requested (past / present /
future) are returned. The current period is always included as context.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Mapping

from jataka.forecast_engine import DASHA_REFLECTIONS
from jataka.interpretation_engine import (
    HOUSE_THEMES, PLANET_THEMES, _map, _ruler_reading, _sign,
)
from jataka.report_engine import SIGN_REFLECTIONS

TOPICS = {
    "relationships": {
        "label": "relationships, marriage and partnership",
        "houses": (7,),
        "planets": ("Venus",),
        "keywords": ("relationship", "relationships", "marriage", "married", "partner",
                     "spouse", "husband", "wife", "love", "romance", "dating",
                     "commitment", "divorce", "separation"),
    },
    "career": {
        "label": "work, career and public role",
        "houses": (10, 6),
        "planets": ("Saturn", "Sun"),
        "keywords": ("career", "job", "work", "profession", "promotion", "business",
                     "employment", "boss", "office", "vocation", "calling"),
    },
    "money": {
        "label": "money, savings and resources",
        "houses": (2, 11),
        "planets": ("Jupiter", "Venus"),
        "keywords": ("money", "wealth", "finance", "financial", "income", "salary",
                     "savings", "debt", "loan", "rich", "poor", "earnings", "assets"),
    },
    "home_family": {
        "label": "home, family and roots",
        "houses": (4,),
        "planets": ("Moon",),
        "keywords": ("home", "family", "mother", "father", "parents", "childhood",
                     "roots", "property", "real estate"),
    },
    "children": {
        "label": "children and creative legacy",
        "houses": (5,),
        "planets": ("Jupiter",),
        "keywords": ("child", "children", "pregnancy", "son", "daughter",
                     "parenting", "fertility"),
    },
    "education": {
        "label": "learning, education and skills",
        "houses": (5, 9, 3),
        "planets": ("Mercury", "Jupiter"),
        "keywords": ("education", "study", "studies", "school", "college",
                     "university", "degree", "exam", "learning", "skill",
                     "training", "course"),
    },
    "health": {
        "label": "body, health and daily routines",
        "houses": (1, 6),
        "planets": ("Sun", "Saturn"),
        "keywords": ("health", "body", "illness", "sick", "disease", "energy",
                     "vitality", "medical", "doctor", "hospital"),
    },
    "spirituality": {
        "label": "spirituality, beliefs and inner life",
        "houses": (9, 12),
        "planets": ("Ketu", "Jupiter"),
        "keywords": ("spiritual", "spirituality", "religion", "god", "faith",
                     "meditation", "moksha", "enlightenment", "belief",
                     "philosophy", "guru"),
    },
    "self": {
        "label": "self, identity and approach to life",
        "houses": (1,),
        "planets": ("Sun", "Moon"),
        "keywords": ("myself", "self", "identity", "personality", "character",
                     "who am i", "purpose", "confidence"),
    },
}

TIME_KEYWORDS = {
    "past": ("past", "before", "already", "happened", "used to", "earlier",
             "previous", "childhood", "so far", "life so far"),
    "present": ("present", "now", "currently", "today", "this year",
                "at the moment", "right now"),
    "future": ("future", "will", "later", "upcoming", "next year", "soon",
               "coming", "ahead", "next"),
}


def _ordinal(n: int) -> str:
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


def _topic_reading(topic_key: str, topic: Mapping, asc_index: int,
                   planets: Mapping[str, object]) -> dict[str, object]:
    house_rows = []
    for house in topic["houses"]:
        r = _ruler_reading(house, asc_index, planets)
        link = r.get("link", {}) or {}
        house_rows.append({
            "house": house,
            "house_sign": r["house_sign"],
            "ruler": r["ruler"],
            "ruler_sign": link.get("ruler_sign"),
            "ruler_house": r.get("ruler_house"),
            "house_theme": HOUSE_THEMES.get(house, "a life area"),
            "linked_topic": link.get("linked_topic"),
            "evidence": r["evidence"],
        })
    planet_rows = []
    for name in topic["planets"]:
        item = _map(planets.get(name))
        if not item:
            continue
        house = int(item.get("whole_sign_house", 0) or 0)
        planet_rows.append({
            "planet": name,
            "sign": item.get("sign"),
            "house": house,
            "planet_theme": PLANET_THEMES.get(name, "traditional planetary themes"),
            "house_theme": HOUSE_THEMES.get(house, "a life area"),
            "sign_theme": SIGN_REFLECTIONS.get(str(item.get("sign")), "traditional sign symbolism"),
        })
    return {"topic": topic_key, "label": topic["label"],
            "houses": house_rows, "planets": planet_rows}


def _topic_answer_text(reading: Mapping) -> str:
    parts: list[str] = []
    for h in reading["houses"]:
        if h["ruler_house"]:
            parts.append(
                f"Your {_ordinal(h['house'])} house — the house the tradition links with "
                f"{h['house_theme']} — is {h['house_sign']}, ruled by {h['ruler']}. "
                f"{h['ruler']} is placed in {h['ruler_sign']}, house {h['ruler_house']}, "
                f"which the tradition links with {h['linked_topic']}. So the tradition "
                f"connects {h['house_theme']} with {h['linked_topic']} in your chart."
            )
        else:
            parts.append(
                f"Your {_ordinal(h['house'])} house — the house the tradition links with "
                f"{h['house_theme']} — is {h['house_sign']}, ruled by {h['ruler']}, but the "
                "ruler's placement is unavailable in this response, so no house-to-house "
                "link is drawn."
            )
    for p in reading["planets"]:
        parts.append(
            f"{p['planet']} — traditionally linked with {p['planet_theme']} — is in "
            f"{p['sign']} ({p['sign_theme']}) in house {p['house']} ({p['house_theme']})."
        )
    return " ".join(parts)


def _dasha_timeline(derived: Mapping, now: datetime, birth_utc: datetime | None):
    """Split the Vimśottarī sequence into past / current / future buckets.

    Past periods are clamped to the birth instant, so a birth-balance period
    that started before birth reports as starting at birth. Periods that end
    at or before ``now`` go to ``past``; the period containing ``now`` is
    ``current``; anything starting after ``now`` is ``future``. If ``birth_utc``
    is supplied, nothing is returned that lies wholly before birth.
    """
    vim = _map(derived.get("vimshottari"))
    periods = vim.get("periods", []) if isinstance(vim, Mapping) else []
    past, current, future = [], None, []
    for period in periods:
        try:
            start = datetime.fromisoformat(str(period["start_utc"]))
            end = datetime.fromisoformat(str(period["end_utc"]))
        except (KeyError, ValueError):
            continue
        if birth_utc is not None and end <= birth_utc:
            continue
        clamped_start = max(start, birth_utc) if birth_utc is not None else start
        if clamped_start >= end:
            continue
        row = {
            **period,
            "start_utc": clamped_start.isoformat(),
            "end_utc": end.isoformat(),
            "clamped_at_birth": bool(birth_utc is not None and start < birth_utc),
        }
        if end <= now:
            past.append(row)
        elif clamped_start <= now < end:
            current = row
        else:
            future.append(row)
    return past, current, future


def _format_period(period: Mapping, label: str) -> dict[str, object]:
    lord = str(period.get("lord"))
    return {
        "label": label,
        "lord": lord,
        "start_utc": period.get("start_utc"),
        "end_utc": period.get("end_utc"),
        "years": period.get("duration_years"),
        "themes": DASHA_REFLECTIONS.get(lord, "traditional planetary themes"),
        "clamped_at_birth": bool(period.get("clamped_at_birth", False)),
    }


def _timeline_plain_language(
    focuses, past, current, future, birth_utc: datetime | None = None,
) -> str:
    parts: list[str] = []
    birth_year = birth_utc.year if birth_utc else None

    if "past" in focuses and past:
        lords = ", ".join(str(p.get("lord")) for p in past)
        window = (
            f"from your birth in {birth_year} to today"
            if birth_year else "up to today"
        )
        parts.append(
            f"In the Vimśottarī timeline {window}, you moved through "
            f"{len(past)} Mahādaśā period(s): {lords}."
        )

    if current:
        lord = str(current.get("lord"))
        themes = DASHA_REFLECTIONS.get(lord, "planetary themes")
        try:
            start_y = datetime.fromisoformat(str(current["start_utc"])).year
            end_y = datetime.fromisoformat(str(current["end_utc"])).year
            window = f"{start_y}–{end_y}"
        except (KeyError, ValueError):
            window = "now"
        parts.append(
            f"You are currently in the {lord} Mahādaśā ({window}) — the tradition "
            f"associates it with {themes}."
        )

    if "future" in focuses and future:
        lords = ", ".join(str(p.get("lord")) for p in future)
        parts.append(
            f"After the current period, the cycle continues with {len(future)} "
            f"further Mahādaśā period(s): {lords}."
        )

    if "future" in focuses and not future:
        parts.append("No further Mahādaśā periods were returned in this response.")

    parts.append(
        "Vimśottarī dates and themes are a traditional timing framework. Each period "
        "has a symbolic theme the tradition assigns to it; the dates are not a record "
        "of specific events that occurred in that window."
    )
    return " ".join(parts)


def answer_question(
    question: str,
    derived: Mapping,
    *,
    now_utc: datetime | None = None,
    birth_utc: datetime | None = None,
) -> dict[str, object]:
    """Answer a free-text question from the chart's computed factors.

    The answer is a report of what the selected tradition associates with the
    relevant houses, rulers and dasha periods in this specific chart. It is not
    a prediction, a probability, or a claim about the user's actual life events.

    When ``birth_utc`` is supplied, past dasha periods are clamped to birth and
    only the requested time buckets (past / present / future) are returned.
    """
    q = (question or "").strip().lower()
    if len(q) < 2:
        raise ValueError("Enter a question with at least two characters.")
    if len(q) > 500:
        raise ValueError("Please keep the question to 500 characters or fewer.")

    now = (now_utc or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if birth_utc is not None:
        birth_utc = birth_utc.astimezone(timezone.utc)

    planets = _map(derived.get("planets"))
    asc = _map(derived.get("ascendant"))
    asc_index = int(asc.get("sign_index", 0) or 0)
    asc_sign = str(asc.get("sign", _sign(asc_index)))

    matched_topics = [key for key, t in TOPICS.items()
                      if any(kw in q for kw in t["keywords"])]
    time_focuses = [label for label, kws in TIME_KEYWORDS.items()
                    if any(kw in q for kw in kws)]

    fallback = False
    if not matched_topics and not time_focuses:
        matched_topics = ["self"]
        fallback = True

    readings = [_topic_reading(k, TOPICS[k], asc_index, planets) for k in matched_topics]
    answer_sections = [{
        "heading": r["label"],
        "text": _topic_answer_text(r),
        "houses": r["houses"],
        "planets": r["planets"],
    } for r in readings]

    timeline = None
    if time_focuses:
        past, current, future = _dasha_timeline(derived, now, birth_utc)
        show_past = "past" in time_focuses
        show_future = "future" in time_focuses
        timeline = {
            "requested": time_focuses,
            "past": [_format_period(p, "Past") for p in past] if show_past else [],
            "current": _format_period(current, "Current") if current else None,
            "future": [_format_period(p, "Future") for p in future] if show_future else [],
            "plain_language": _timeline_plain_language(
                time_focuses,
                past if show_past else [],
                current,
                future if show_future else [],
                birth_utc,
            ),
        }

    return {
        "status": "TRADITIONAL_QA_UNVALIDATED",
        "question": question,
        "ascendant_sign": asc_sign,
        "matched_topics": matched_topics,
        "used_default_overview": fallback,
        "answer_sections": answer_sections,
        "timeline": timeline,
        "scope_note": (
            "This answer reports what the selected Jyotish tradition says about the "
            "factors in your chart. It is not a prediction of events, a probability, or "
            "a statement about your actual past, present or future. The astronomical "
            "positions and derived factors remain unvalidated."
        ),
        "disclaimer": (
            "Astrology is a cultural/divinatory tradition, not a scientifically validated "
            "method for recovering past events or predicting the future. Use this as a "
            "structured reflection, not as evidence about what has happened or will happen."
        ),
    }

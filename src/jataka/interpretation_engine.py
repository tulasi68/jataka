"""Evidence-led, plain-language interpretations of traditional Jyotish factors.

The interpretation layer explains why a chart-specific traditional theme was
selected. It does not alter astronomical calculations, infer missing birth
data, or claim certainty. Interpretive prose is confident in the register of a
traditional reading; scope notes and limitations live in the reading envelope,
not in every sentence.
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
HOUSE_PHRASE = {
    1: "your presence and the way you move through the world",
    2: "your resources, your voice, and what you value",
    3: "your daily effort, communication, and the skills you build",
    4: "your home, family, roots, and the private core that regenerates you",
    5: "your creativity, play, and what you bring into the world",
    6: "your daily work, health, and the routines that keep you steady",
    7: "your partnerships and the one-to-one agreements that shape your life",
    8: "shared resources, deep change, and the private material of transformation",
    9: "your beliefs, horizons, and what you reach toward",
    10: "your career, public role, and what you are known for",
    11: "your community, networks, and shared goals",
    12: "your inner life — solitude, retreat, and what happens behind the scenes",
}

ASCENDANT_CHARACTER = {
    "Aries": "You meet life directly — quick to act, quick to speak, allergic to waiting for permission.",
    "Taurus": "You meet life steadily. You trust what you can build, keep, and touch, and you're rarely hurried into anything you don't feel good about.",
    "Gemini": "You meet life through conversation and curiosity. You think best out loud, and you find your own view by trying it out on others.",
    "Cancer": "You meet life feeling-first. You read the emotional temperature of every room before anything else, and safety, home and memory matter to you more than they do to most.",
    "Leo": "You meet life warmly and proudly. You want to be seen for what you contribute, and you have a natural dignity that people feel when you walk in.",
    "Virgo": "You meet life with precision. You notice what's not quite right and your instinct is to fix it, and you'd rather do one thing well than ten things approximately.",
    "Libra": "You meet life seeking balance. You weigh both sides, you want things fair, and you have an aesthetic instinct that shapes your choices more than you realise.",
    "Scorpio": "You meet life with intensity. You want to know what's underneath, what's really going on, and you'd rather sit in silence with someone honest than fill a room with noise.",
    "Sagittarius": "You meet life reaching outward. You want the bigger picture, and you get restless when the view gets too small.",
    "Capricorn": "You meet life building. You take responsibility seriously, you plan in decades, and you'd rather be respected than liked.",
    "Aquarius": "You meet life standing back a bit. You want to see the pattern before you join the crowd, and you're loyal to ideas as much as to people.",
    "Pisces": "You meet life absorbing. You feel what's around you as if it were your own, and you need regular solitude to sort what's yours from what isn't.",
}
MOON_CHARACTER = {
    "Aries": "Your emotions are quick and hot — you feel first and process later, and you need people who can keep up with your pace.",
    "Taurus": "You feel safest when things are steady: predictable rhythms, physical comfort, familiar people.",
    "Gemini": "You process feeling through talk. You need someone to think out loud with, and stillness feels heavier than motion.",
    "Cancer": "Your emotional life is deep and tidal. You give care the way you would want to receive it, and you remember every feeling that has ever been spent on you.",
    "Leo": "You need to be warmly received and appreciated — not flattery, but real recognition of what you offer.",
    "Virgo": "You show care through practical attention. Making things better is your love language, and worry is a form of affection.",
    "Libra": "You feel safest when things between you and the people close to you are harmonious. Discord costs you more than it costs most people.",
    "Scorpio": "Your emotions run deep and are rarely fully spoken. You need trust before you give access, and you never forget a betrayal or a gift.",
    "Sagittarius": "You need space to breathe and a sense that there's somewhere bigger to go. Heaviness drains you; optimism restores you.",
    "Capricorn": "You process feeling slowly and often through duty. Showing up when you said you would is your form of love.",
    "Aquarius": "You feel at some distance from your own emotions. You need friendships that respect your space, and you sort feeling through thought more than through talk.",
    "Pisces": "You absorb other people's emotions and need regular solitude to sort your own from what you've picked up.",
}
SUN_CHARACTER = {
    "Aries": "Your sense of purpose pulls you toward initiation — you're here to begin things and go first.",
    "Taurus": "Your sense of purpose pulls you toward building something real and lasting — a life, a home, a body of work you can stand on.",
    "Gemini": "Your sense of purpose pulls you toward communication and inquiry — teaching, writing, sharing, connecting ideas.",
    "Cancer": "Your sense of purpose is bound up in care. You measure yourself by how well you look after the people who are yours.",
    "Leo": "Your sense of purpose pulls you toward expression — you are made to be seen doing what you love, with warmth and integrity.",
    "Virgo": "Your sense of purpose pulls you toward service and craft — making things work, doing the unglamorous work that holds everything up.",
    "Libra": "Your sense of purpose pulls you toward partnership and fairness — you shine in collaboration and in any arena where diplomacy matters.",
    "Scorpio": "Your sense of purpose pulls you toward depth — truth that isn't easy, transformation, work that requires nerve and confidentiality.",
    "Sagittarius": "Your sense of purpose pulls you toward meaning — teaching, learning, exploring, working at something that widens your view.",
    "Capricorn": "Your sense of purpose pulls you toward long-range building — you shoulder what others won't, and you measure yourself in decades.",
    "Aquarius": "Your sense of purpose pulls you toward the wider group — community work, reform, anything that serves beyond personal ambition.",
    "Pisces": "Your sense of purpose pulls you toward the inner world — creative work, spiritual service, empathy that can't be measured by output.",
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


def _sign(index: int) -> str:
    signs = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
    return signs[index % 12]


def _ordinal(n: int) -> str:
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


def _ruler_reading(house: int, asc_index: int, planets: Mapping[str, object]) -> dict[str, object]:
    house_sign = _sign((asc_index + house - 1) % 12)
    ruler = SIGN_RULERS[house_sign]
    ruler_item = _map(planets.get(ruler))
    ruler_house = int(ruler_item.get("whole_sign_house", 0) or 0)
    ruler_sign = str(ruler_item.get("sign", "unknown sign"))
    if ruler_house:
        link = {
            "house": house, "house_sign": house_sign, "ruler": ruler,
            "ruler_sign": ruler_sign, "ruler_house": ruler_house,
            "topic": HOUSE_THEMES[house], "linked_topic": HOUSE_THEMES[ruler_house],
        }
    else:
        link = {"house": house, "house_sign": house_sign, "ruler": ruler,
                "ruler_sign": None, "ruler_house": None,
                "topic": HOUSE_THEMES[house], "linked_topic": None}
    return {"ruler": ruler, "house_sign": house_sign,
            "ruler_house": ruler_house or None, "link": link}


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
        explanation = (
            f"On {str(area['key']).lower()}: your {_ordinal(primary)} house is "
            f"{ruler['house_sign']}, ruled by {ruler['ruler']}, which sits in "
            f"{ruler['link']['ruler_sign']} in the {_ordinal(ruler['ruler_house'])} house. "
            f"The tradition reads these as a single theme in your chart — "
            f"{HOUSE_THEMES[primary]}, played out through {HOUSE_THEMES[ruler['ruler_house']]}."
        )
    else:
        explanation = (
            f"This section focuses on {HOUSE_THEMES[primary]}. The ruler placement needed "
            "for a more specific house-to-house interpretation is unavailable, so no further "
            "conclusion is drawn."
        )
    return {
        "title": str(area["key"]),
        "question": str(area["question"]),
        "specific_interpretation": explanation,
        "reasoning": (
            f"{ruler['house_sign']} rises on the {_ordinal(primary)} house; its ruler "
            f"{ruler['ruler']} is in {ruler['link']['ruler_sign']}, house "
            f"{ruler['ruler_house']}."
            if ruler["ruler_house"] else
            f"{ruler['house_sign']} rises on the {_ordinal(primary)} house; its ruler "
            f"{ruler['ruler']}'s placement is unavailable."
        ),
        "ruler_link": ruler["link"],
        "occupants": occupants,
        "confidence_label": "Traditional interpretation · unvalidated",
        "scope_note": (
            "One traditional convention among several; other schools read house rulers "
            "differently. Compare with your lived experience."
        ),
    }


def _portrait(asc_sign: str, moon_sign: str, sun_sign: str,
              moon_house: int, sun_house: int) -> dict[str, object]:
    parts = [
        f"Your rising sign is {asc_sign}. {ASCENDANT_CHARACTER[asc_sign]}",
        f"Your Moon is in {moon_sign}, in the {_ordinal(moon_house)} house. "
        f"{MOON_CHARACTER[moon_sign]} The {_ordinal(moon_house)} house is where you live "
        f"this out — {HOUSE_PHRASE[moon_house]}.",
        f"Your Sun is in {sun_sign}, in the {_ordinal(sun_house)} house. "
        f"{SUN_CHARACTER[sun_sign]} The {_ordinal(sun_house)} house is where you express "
        f"it — {HOUSE_PHRASE[sun_house]}.",
        f"Read together, these are not three separate traits but one person: the way you "
        f"meet life ({asc_sign}), what you need to feel whole (Moon in {moon_sign}), and "
        f"what pulls you forward (Sun in {sun_sign}) reinforce each other.",
    ]
    return {
        "title": "Your portrait",
        "text": " ".join(parts),
        "factors": {"ascendant": asc_sign, "moon": moon_sign, "sun": sun_sign,
                    "moon_house": moon_house, "sun_house": sun_house},
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
    moon_sign = str(moon.get("sign", "unknown sign"))
    sun_sign = str(sun.get("sign", "unknown sign"))
    moon_house = int(moon.get("whole_sign_house", 0) or 0)
    sun_house = int(sun.get("whole_sign_house", 0) or 0)

    anchors = []

    if lagna_lord and _map(planets.get(lagna_lord)):
        p = _map(planets.get(lagna_lord))
        ruler_house = int(p.get("whole_sign_house", 0) or 0)
        ruler_sign = str(p.get("sign", "an unknown sign"))
        anchors.append({
            "title": "Where your chart begins — the Ascendant",
            "finding": f"With {asc_sign} rising, {ASCENDANT_CHARACTER[asc_sign].lower()}",
            "meaning": (
                f"{ASCENDANT_CHARACTER[asc_sign]} "
                f"{lagna_lord} — the ruler of {asc_sign} — sits in {ruler_sign}, in the "
                f"{_ordinal(ruler_house)} house. This gives your rising sign its specific colour: "
                f"the tradition reads your approach to life through {HOUSE_PHRASE[ruler_house]}."
            ),
            "evidence": {"ascendant_sign": asc_sign, "ascendant_ruler": lagna_lord,
                         "ruler_sign": ruler_sign, "ruler_house": ruler_house},
        })

    if moon:
        anchors.append({
            "title": "What the Moon emphasises",
            "finding": f"Your Moon is in {moon_sign}, in the {_ordinal(moon_house)} house "
                       f"({moon.get('nakshatra', 'nakshatra unavailable')}, pada "
                       f"{moon.get('pada', '?')}).",
            "meaning": (
                f"{MOON_CHARACTER[moon_sign]} "
                f"Because it sits in the {_ordinal(moon_house)} house, this plays out in "
                f"{HOUSE_PHRASE[moon_house]}. "
                f"The {moon.get('nakshatra', 'nakshatra')} adds its own texture: the tradition "
                f"reads Nakshatra placement as refining the tone of the sign — here, pada "
                f"{moon.get('pada', '?')} sharpens the theme further."
            ),
            "evidence": {"planet": "Moon", "sign": moon_sign, "house": moon_house,
                         "nakshatra": moon.get("nakshatra"), "pada": moon.get("pada")},
        })

    if sun:
        anchors.append({
            "title": "Purpose and visibility",
            "finding": f"Your Sun is in {sun_sign}, in the {_ordinal(sun_house)} house.",
            "meaning": (
                f"{SUN_CHARACTER[sun_sign]} "
                f"In the {_ordinal(sun_house)} house, this shows up in "
                f"{HOUSE_PHRASE[sun_house]}. That's the arena where the tradition says your "
                f"sense of self is built and tested."
            ),
            "evidence": {"planet": "Sun", "sign": sun_sign, "house": sun_house},
        })

    portrait = (
        _portrait(asc_sign, moon_sign, sun_sign, moon_house, sun_house)
        if moon and sun and moon_house and sun_house else None
    )

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
                f"The computed Arudha Lagna is {arudha_sign}. The tradition uses this to discuss "
                f"how a person appears outwardly, and {arudha_sign} gives a public flavour of "
                f"{SIGN_REFLECTIONS.get(str(arudha_sign), 'its sign themes')}. Treat this as a "
                "secondary lens, not a description of how others actually see you."
            ),
            "evidence": {"arudha_lagna_sign": arudha_sign},
        })
    atmakaraka = _map(jaimini).get("atmakaraka")
    if atmakaraka:
        extra_lenses.append({
            "title": "Jaimini self-development lens",
            "text": (
                f"The seven-karaka calculation assigns Atmakaraka to {atmakaraka}. The tradition "
                f"reads Atmakaraka as the planet most tied to the soul's lessons in this life — "
                f"here, lessons of {PLANET_THEMES.get(str(atmakaraka), 'its planetary themes')}. "
                "Karaka rule variants differ across traditions; this is one reading."
            ),
            "evidence": {"atmakaraka": atmakaraka},
        })
    sav = _map(transit).get("sarvashtakavarga_total")
    if sav is not None:
        extra_lenses.append({
            "title": "Ashtakavarga and current transits",
            "text": (
                f"The calculated Sarvashtakavarga sum is {sav} (the classical total for a "
                "complete chart is 337). Individual transit sign bindus are shown in the "
                "technical details; they indicate relative traditional strength of transits, "
                "not specific outcomes."
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
                f"You are in the {maha} Mahādaśā"
                + (f" / {sublord} antardaśā" if sublord else "")
                + f". The tradition reads this period as carrying themes of "
                + f"{active_period.get('traditional_themes', 'planetary symbolism')}"
                + (f", sharpened by {sub.get('traditional_themes', '')}" if sublord else "")
                + f". Where {maha} sits in your chart — house {period_planets[0]['house'] if period_planets else '?'} "
                "— is where those themes tend to surface most visibly."
            ),
        }

    return {
        "status": "PERSONALISED_EVIDENCE_LED_INTERPRETATION_UNVALIDATED",
        "title": "Your Jataka — what the chart specifically says",
        "opening": (
            f"Your rising sign is {asc_sign}. The reading below works from the actual "
            "sign, house and ruler relationships in this chart, and shows the reasoning "
            "for each conclusion."
        ),
        "portrait": portrait,
        "quick_view": [
            {"label": "Ascendant", "text": f"{asc_sign}; traditional ruler {lagna_lord or 'not available'}."},
            {"label": "Moon", "text": f"{moon_sign}, house {moon_house or '?'}; Nakshatra {moon.get('nakshatra', '?')}, pada {moon.get('pada', '?')}."},
            {"label": "Sun", "text": f"{sun_sign}, house {sun_house or '?'}."},
        ],
        "main_takeaways": anchors,
        "area_readings": area_readings,
        "life_areas": [],
        "additional_lenses": extra_lenses,
        "current_period": period,
        "how_methods_fit": {
            "status": _map(verification).get("status", "status unavailable"),
            "text": (
                "Parashari/Drik, Jaimini, and Ashtakavarga/transit are separate traditional lenses, "
                "all currently derived from the same natal longitudes. The agreement between them "
                "is a consistency check, not independent verification."
            ),
        },
        "optional_reflections": {
            "numerology_included": numerology is not None,
            "numerology_note": "Numerology is a separate cultural tradition and does not corroborate the horoscope." if numerology is not None else None,
            "palmistry_included": palmistry is not None,
            "palmistry_note": "Palmistry uses only observations entered by the user; it is not image analysis." if palmistry is not None else None,
        },
        "practical_guidance": [
            "Compare each chart claim with concrete lived experience — where it fits, notice; where it doesn't, notice that too.",
            "Where two life areas pull in different directions, treat that as a mixed reading rather than smoothing it over.",
            "Use the current-period section as a lens for the present moment, not as a forecast of events.",
        ],
        "limitations": [
            "Astronomical positions and derived factors remain unvalidated against independently sourced reference charts.",
            "House-ruler readings follow one traditional Jyotish convention; other schools can interpret the same factors differently.",
            "This reading does not yet assess every classical condition — aspects, dignities, combustion, retrogression, or divisional-chart rules.",
            "Astrology is a cultural tradition, not a scientifically established method for predicting life events.",
        ],
        "disclaimer": (
            "Traditional Jyotish interpretation, offered as a structured reflection. "
            "Not a scientific personality assessment, not a guaranteed forecast. "
            "Use it alongside real-world evidence for important decisions."
        ),
    }

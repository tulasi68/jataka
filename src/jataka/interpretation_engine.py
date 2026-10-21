"""Evidence-led, plain-language interpretations of traditional Jyotish factors.

The interpretation layer explains what a chart-specific combination produces in
lived experience, not just where things sit. Confident in the register of a
traditional reading; the scope notes live in the reading envelope, not in every
sentence.
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
    2: "your money, your voice, and what you value",
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

PLANET_IN_HOUSE = {
    ("Sun", 1): "You lead with your personality and confidence; your purpose is visible on your face, and you're recognised for who you are.",
    ("Sun", 2): "Your identity is bound to what you own and value; earning and spending are personal statements, and you take pride in your resources.",
    ("Sun", 3): "You shine through communication and daily effort — teaching, writing, coordinating, or the small repeated acts that build skill.",
    ("Sun", 4): "Your sense of self is rooted at home, in family, in property, in the private core. Your purpose is felt most strongly in domestic life.",
    ("Sun", 5): "Creative self-expression and personal passion carry your life's purpose. You are made to build something that reflects you — art, children, ideas.",
    ("Sun", 6): "You find purpose in service and problem-solving. You take pride in the difficult, unglamorous work that holds things together.",
    ("Sun", 7): "You come alive in partnership and public collaboration; your identity is shaped by the 'we' rather than the 'I'.",
    ("Sun", 8): "Purpose operates in hidden or transformative domains — crisis, deep study, shared resources, and the material of change.",
    ("Sun", 9): "You're drawn to beliefs, teaching, philosophy; you shine as the seeker or the guide, and higher learning is where you feel most yourself.",
    ("Sun", 10): "Career and identity are one. Your public role is where you build your name, and your sense of purpose is expressed through your work in the world.",
    ("Sun", 11): "You shine in community and networks — leading groups, aligning with shared ambitions, and building through collective effort.",
    ("Sun", 12): "Purpose operates behind the scenes: your energy goes toward private work, retreat, healing, or helping others without recognition. Money often flows through unseen channels — expenses you don't discuss, or earnings from behind-the-scenes work.",
    ("Moon", 1): "Your feelings show on your face; you absorb others' moods and react instinctively. People read your emotional state before you speak.",
    ("Moon", 2): "You feel safest when material security is in place. Family resources and financial stability shape your emotional life deeply.",
    ("Moon", 3): "You process feeling through talk and movement — you need to think out loud, and stillness feels heavier than motion.",
    ("Moon", 4): "Emotional roots are strong. Home, mother, family, and inner life are central to who you are, and you need a private space that feels truly yours.",
    ("Moon", 5): "Feelings flow through creativity and children. You nurture what you love, and creative work restores you.",
    ("Moon", 6): "Emotions and health are linked. You process feeling through routine and service, and unresolved stress shows up in the body.",
    ("Moon", 7): "You feel safest in partnership. Being alone for long stretches unsettles you, and connection restores you.",
    ("Moon", 8): "Your emotional life is deep and private. You feel more than you say, and trust is earned slowly.",
    ("Moon", 9): "You feel at home when you're learning, travelling, or exploring meaning. Belief and philosophy are emotional anchors.",
    ("Moon", 10): "Your feelings are channeled into career and public role. You need visible purpose to feel secure.",
    ("Moon", 11): "Community and friendship are your emotional home. The group you belong to matters as much as the family you came from.",
    ("Moon", 12): "Your feelings run deep and private. Solitude is both refuge and risk — necessary for regeneration, dangerous in excess.",
    ("Mars", 1): "You act first and think later; assertiveness is on your surface. Physical presence and directness define your approach.",
    ("Mars", 2): "You put energy into earning and building resources, and you fight for what you value.",
    ("Mars", 3): "Courage shows up in communication and daily effort. You're a doer of small things well, and you argue persuasively.",
    ("Mars", 4): "Energy goes into home and family. There is intensity about domestic matters — protection and territory matter here.",
    ("Mars", 5): "You pursue passions and creative work with drive. Competitive by nature, you play hard and create with force.",
    ("Mars", 6): "You fight for health, routines, and solving problems. Energetic in service, you thrive on fixing what's broken.",
    ("Mars", 7): "You assert yourself through partnership. Conflict and collaboration are bound together for you.",
    ("Mars", 8): "You act in crisis and shared resources. Energy goes into transformation, and you handle pressure well.",
    ("Mars", 9): "You fight for beliefs and principles; energy goes into travel, learning, and causes larger than yourself.",
    ("Mars", 10): "Your drive is public — career and ambition on display. You compete openly and lead visibly.",
    ("Mars", 11): "You push for community and shared goals. Energy goes into networks, collaborations, and group projects.",
    ("Mars", 12): "Energy works behind the scenes. Action happens in private or abroad, and anger tends to be absorbed rather than expressed.",
    ("Mercury", 1): "You think on your feet; your intellect is visible on your surface. Words, manner, and mental quickness define your presence.",
    ("Mercury", 2): "Your mind is drawn to values and resources. You're good with money-talk, and your voice carries weight.",
    ("Mercury", 3): "Curiosity and communication define you — writing, teaching, conversation, and the constant exchange of ideas.",
    ("Mercury", 4): "You think about home and family; your intellect is rooted, and your private space is where your mind does its best work.",
    ("Mercury", 5): "Creative thinking and analysis define your self-expression. Ideas, art, and children are all arenas for your mind.",
    ("Mercury", 6): "Your mind goes toward health, routines, and problem-solving. Analysis and diagnosis come naturally.",
    ("Mercury", 7): "You think through partnership; your mind is relational, and conversation with close people is where you do your best thinking.",
    ("Mercury", 8): "You think deeply about shared resources, transformation, and hidden matters. The mind dives rather than skims.",
    ("Mercury", 9): "You study big ideas; your mind runs on philosophy, travel, faith, and the wider questions.",
    ("Mercury", 10): "Your mind is career-focused. Communication is your professional tool, and you're known for how you speak or write in your field.",
    ("Mercury", 11): "You think in networks and communities. Ideas for the group come naturally, and you're a natural communicator of collective goals.",
    ("Mercury", 12): "Your mind goes inward. Deep private study, imagination, and research behind the scenes are where your intellect thrives.",
    ("Venus", 1): "You're charming and aesthetic; pleasure and beauty are part of your identity, and people respond to your warmth.",
    ("Venus", 2): "You value beautiful things and spend toward aesthetics and comfort. Your resources are shaped by what you find genuinely worth having.",
    ("Venus", 3): "You communicate warmly, and you bring grace to daily life and thought. Relationships with siblings and neighbours tend to be harmonious.",
    ("Venus", 4): "You value home and family deeply. There's warmth and beauty in your private space, and home is where you invest.",
    ("Venus", 5): "You love creative work, children, and play. You bring beauty to expression, and pleasure is not an indulgence — it's a necessity.",
    ("Venus", 6): "Your work has grace; you value good routine and health, and you bring aesthetics into daily tasks.",
    ("Venus", 7): "Partnership is central. You love deeply, value harmony, and your happiness is bound up with the quality of your intimate relationships.",
    ("Venus", 8): "You value deep intimacy. Love has a transformational, private quality, and shared resources are handled with care.",
    ("Venus", 9): "You love learning and beauty. Pleasure comes from travel, ideas, and the company of people who widen your view.",
    ("Venus", 10): "You value a career that reflects your aesthetics. Charm in public role, and your work is likely to have a visible element of beauty or harmony.",
    ("Venus", 11): "You love community and friendship. Aesthetic and social values meet, and your friendships tend to be warm and generous.",
    ("Venus", 12): "You love in private, and hidden or retreat-oriented pleasures matter more than public ones. Romance may have a secret or spiritual quality.",
    ("Jupiter", 1): "You grow through self-development. Generosity and confidence define you, and you tend to expand whatever you touch.",
    ("Jupiter", 2): "Fortune in resources. You value growth, learning, and family wealth, and there's often a history of family generosity behind you.",
    ("Jupiter", 3): "You grow through communication and effort. Optimism in daily life, and teaching, writing, and skill-building come naturally.",
    ("Jupiter", 4): "Your home is your expansion zone. Family wealth and inner growth are tied together, and you may live in more than one place.",
    ("Jupiter", 5): "Wisdom comes through creativity and children. Your pupils and your art are one — teaching is your natural creative act.",
    ("Jupiter", 6): "Growth comes through service. You heal through helping, and there's protection in routine and devotion.",
    ("Jupiter", 7): "You grow in partnership. Generosity toward others is repaid, and marriage often brings expansion.",
    ("Jupiter", 8): "Growth through shared resources and depth. Wisdom earned through transformation, and inheritance or other people's resources play a role.",
    ("Jupiter", 9): "Beliefs and philosophy are your expansion — travel, teaching, faith. You're here to learn the wider view and share it.",
    ("Jupiter", 10): "Your career expands you. Public role reflects your wisdom, and you grow through taking on visible responsibility.",
    ("Jupiter", 11): "You grow through community and networks. Friends are the source of good fortune, and shared ambitions bear fruit.",
    ("Jupiter", 12): "Wisdom through retreat and solitude. Growth happens in private realms — spiritual practice, healing, and charity.",
    ("Saturn", 1): "You take yourself seriously. Responsibility shapes your identity, and maturity comes through learning to shoulder more than feels comfortable.",
    ("Saturn", 2): "Financial discipline is central. Resources are earned slowly and kept carefully, and family money history carries weight.",
    ("Saturn", 3): "Learning and communication are serious efforts. You take daily work seriously and build skills through patient repetition.",
    ("Saturn", 4): "Home and family carry responsibility. You may support family or work on repairing your roots, and inner security is earned slowly.",
    ("Saturn", 5): "Creativity requires discipline. You take learning and play seriously, and children may come late or bring lessons in patience.",
    ("Saturn", 6): "Health and work are your mastery subjects. Patient through illness and service, you heal by working through problems methodically.",
    ("Saturn", 7): "Partnership requires work. You take commitments seriously, and this placement often brings a serious or older partner.",
    ("Saturn", 8): "Depth and shared resources demand discipline. Crisis teaches you mastery, and you can sit with what most people avoid.",
    ("Saturn", 9): "Beliefs are earned through work. You study deeply, and your philosophy is one you've built rather than inherited.",
    ("Saturn", 10): "Career is your discipline. You build slowly toward mastery in your field, and public responsibility comes with weight.",
    ("Saturn", 11): "Community work requires patience. You build networks carefully, and long-term friendships carry more weight than many contacts.",
    ("Saturn", 12): "Solitude and inner work are your discipline. Mastery comes through retreat, and hidden fears are the material you transform.",
    ("Rahu", 1): "You have an unusual identity; you stand out in ways you didn't plan for. Selfhood is a site of both ambition and uncertainty.",
    ("Rahu", 2): "You hunger for resources and value. Earning may come through unconventional channels, and there's often a pattern of big swings in money.",
    ("Rahu", 3): "Your communication and effort go in unusual directions. You may feel compelled to speak or write, and courage is both a gift and a test.",
    ("Rahu", 4): "Home and family life carry a lesson. You may live abroad or in unusual family arrangements, and belonging is something you construct.",
    ("Rahu", 5): "Creativity and children carry unusual energy. Unconventional expression, and learning happens through experimentation.",
    ("Rahu", 6): "Health and work have unusual challenges and solutions. You heal through non-standard means, and service may take unfamiliar forms.",
    ("Rahu", 7): "Relationships have unusual dynamics. You attract partners who challenge convention, and marriage can be both expansion and disruption.",
    ("Rahu", 8): "Depth and transformation are your arena. Unusual access to hidden resources, and crisis teaches you what stability cannot.",
    ("Rahu", 9): "Beliefs and travel shape you in unexpected ways. You seek beyond conventional wisdom, and gurus come in unusual forms.",
    ("Rahu", 10): "Career takes unusual shape. Ambition is strong and unconventional, and you may be known for something you never expected.",
    ("Rahu", 11): "Community and networks are strong but unpredictable. Unusual gains through groups, and friendships may arrive suddenly.",
    ("Rahu", 12): "Private life and retreat hold unusual significance. The unseen draws you, and solitude is both a site of growth and a temptation.",
    ("Ketu", 1): "You feel detached from your own identity. You don't fully identify with your surface self, and selfhood feels like something you observe.",
    ("Ketu", 2): "You're less attached to money. Resources come and go, and you don't cling — for better and for worse.",
    ("Ketu", 3): "You're detached from ordinary communication. You speak with unusual authority or not at all, and self-promotion doesn't come naturally.",
    ("Ketu", 4): "Home and family carry a lesson of detachment. You may feel separated from roots, and inner peace is found away from where you started.",
    ("Ketu", 5): "Creativity and children are handled with detachment. You don't cling to outcomes, and creative work has a spiritual or inward quality.",
    ("Ketu", 6): "Health is a lesson in detachment. You may neglect or over-focus on routines, and healing comes through letting go.",
    ("Ketu", 7): "You carry detachment in partnership. You're learning to love without clinging, and serious relationships may come late or feel incomplete.",
    ("Ketu", 8): "You have deep ease with depth and transformation. The unseen is familiar, and the material of change is your natural element.",
    ("Ketu", 9): "Beliefs come from deep within. You have instinctive wisdom that bypasses conventional study, and you may depart from inherited faith.",
    ("Ketu", 10): "Career operates with detachment. You do the work without ambition in the usual sense, and public recognition may feel hollow.",
    ("Ketu", 11): "Community is not your anchor. You seek your own way, and gains from groups feel less meaningful than the work itself.",
    ("Ketu", 12): "You're naturally at home in the unseen. Meditation, solitude, and retreat come naturally, and the private realm is where you feel most whole.",
}

AREAS = [
    {"key": "Self-understanding", "houses": (1,), "primary": 1},
    {"key": "Money, values and security", "houses": (2, 11), "primary": 2},
    {"key": "Work and contribution", "houses": (10, 6), "primary": 10},
    {"key": "Relationships and cooperation", "houses": (7,), "primary": 7},
    {"key": "Home and private life", "houses": (4, 12), "primary": 4},
    {"key": "Learning and judgement", "houses": (5, 9, 3), "primary": 9},
]


def _map(value: object) -> Mapping[str, object]:
    return value if isinstance(value, Mapping) else {}


def _sign(index: int) -> str:
    signs = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
    return signs[index % 12]


def _ordinal(n: int) -> str:
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


def _planet_in_house(planet: str, house: int) -> str:
    text = PLANET_IN_HOUSE.get((planet, house))
    if text:
        return text
    return (
        f"{planet} in the {_ordinal(house)} house channels the planet's themes of "
        f"{PLANET_THEMES.get(planet, 'its significations')} through {HOUSE_PHRASE.get(house, 'that domain')}."
    )


def _area_reading(area: Mapping[str, object], asc_index: int, planets: Mapping[str, object]) -> dict[str, object]:
    primary = int(area["primary"])
    house_sign = _sign((asc_index + primary - 1) % 12)
    ruler = SIGN_RULERS[house_sign]
    ruler_item = _map(planets.get(ruler))
    ruler_sign = str(ruler_item.get("sign", "unknown sign"))
    ruler_house = int(ruler_item.get("whole_sign_house", 0) or 0)
    sign_flavour = SIGN_REFLECTIONS.get(house_sign, "its symbolic themes")
    house_theme = HOUSE_THEMES.get(primary, "that life area")
    house_phrase = HOUSE_PHRASE.get(primary, "that life area")

    paragraphs = []
    paragraphs.append(
        f"Your {_ordinal(primary)} house — traditionally {house_theme} — is {house_sign}. "
        f"This gives {house_phrase} a flavour of {sign_flavour}."
    )
    if ruler_house:
        paragraphs.append(
            f"The ruler of your {_ordinal(primary)} house is {ruler}, and it sits in "
            f"{ruler_sign} in the {_ordinal(ruler_house)} house. The tradition reads this as: "
            f"{_planet_in_house(ruler, ruler_house)}"
        )
        paragraphs.append(
            f"Because the ruler sits in {HOUSE_PHRASE.get(ruler_house, 'another life area')}, "
            f"the tradition reads your {str(area['key']).lower()} as operating through "
            f"{HOUSE_PHRASE.get(ruler_house, 'that domain')}. That's the specific connection "
            "this chart makes for this life area."
        )
    else:
        paragraphs.append(
            f"The ruler of your {_ordinal(primary)} house is {ruler}, but its placement "
            "isn't available in this response, so no further reading is drawn."
        )

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

    return {
        "title": str(area["key"]),
        "specific_interpretation": " ".join(paragraphs),
        "reasoning": (
            f"{house_sign} rises on the {_ordinal(primary)} house; ruler {ruler} sits in "
            f"{ruler_sign} in the {_ordinal(ruler_house)} house."
            if ruler_house else
            f"{house_sign} rises on the {_ordinal(primary)} house; ruler {ruler}'s placement unavailable."
        ),
        "ruler_link": {
            "house": primary, "house_sign": house_sign, "ruler": ruler,
            "ruler_sign": ruler_sign if ruler_house else None,
            "ruler_house": ruler_house or None,
            "topic": house_theme,
            "linked_topic": HOUSE_THEMES.get(ruler_house) if ruler_house else None,
        },
        "occupants": occupants,
        "scope_note": "One traditional convention among several; other schools read house rulers differently.",
    }


def _portrait(asc_sign, moon_sign, sun_sign, moon_house, sun_house):
    parts = [
        f"Your rising sign is {asc_sign}. {ASCENDANT_CHARACTER[asc_sign]}",
        f"Your Moon is in {moon_sign}, in the {_ordinal(moon_house)} house. "
        f"{MOON_CHARACTER[moon_sign]} "
        f"That plays out in {HOUSE_PHRASE[moon_house]}.",
        f"Your Sun is in {sun_sign}, in the {_ordinal(sun_house)} house. "
        f"{SUN_CHARACTER[sun_sign]} "
        f"That plays out in {HOUSE_PHRASE[sun_house]}.",
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
            "finding": f"With {asc_sign} rising: {ASCENDANT_CHARACTER[asc_sign]}",
            "meaning": (
                f"{lagna_lord} — the ruler of {asc_sign} — sits in {ruler_sign} in the "
                f"{_ordinal(ruler_house)} house. This gives your rising sign its specific "
                f"colour: the tradition reads your approach to life through "
                f"{HOUSE_PHRASE.get(ruler_house, 'that domain')}. "
                f"{_planet_in_house(lagna_lord, ruler_house)}"
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
                f"{MOON_CHARACTER[moon_sign]} Because it sits in the {_ordinal(moon_house)} "
                f"house, this plays out in {HOUSE_PHRASE.get(moon_house, 'that domain')}. "
                f"{_planet_in_house('Moon', moon_house)}"
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
                f"In the {_ordinal(sun_house)} house: {_planet_in_house('Sun', sun_house)}"
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
                f"The computed Arudha Lagna is {arudha_sign}. The tradition reads this as the "
                f"public-facing flavour of your chart — a secondary lens on how you appear, "
                f"with {SIGN_REFLECTIONS.get(str(arudha_sign), 'its sign themes')} colouring "
                "your outward presentation."
            ),
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
                + ". Where the period planets sit in your chart is where those themes "
                "surface most visibly."
            ),
        }

    return {
        "status": "PERSONALISED_EVIDENCE_LED_INTERPRETATION_UNVALIDATED",
        "title": "Your Jataka — what the chart specifically says",
        "opening": (
            f"Your rising sign is {asc_sign}. The reading below works from the actual "
            "sign, house and ruler relationships in this chart."
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
                "Parashari/Drik, Jaimini, and Ashtakavarga/transit are separate traditional "
                "lenses, all currently derived from the same natal longitudes."
            ),
        },
        "optional_reflections": {
            "numerology_included": numerology is not None,
            "numerology_note": "Numerology is a separate cultural tradition and does not corroborate the horoscope." if numerology is not None else None,
            "palmistry_included": palmistry is not None,
            "palmistry_note": "Palmistry uses only observations entered by the user; it is not image analysis." if palmistry is not None else None,
        },
        "practical_guidance": [
            "Compare each chart claim with concrete lived experience — notice where it fits, and notice where it doesn't.",
            "Where two life areas pull in different directions, treat that as a mixed reading rather than smoothing it over.",
        ],
        "limitations": [
            "Astronomical positions and derived factors remain unvalidated against independently sourced reference charts.",
            "House-ruler readings follow one traditional Jyotish convention; other schools can interpret the same factors differently.",
            "This reading does not yet assess every classical condition — aspects, dignities, combustion, retrogression, or divisional-chart rules.",
            "Astrology is a cultural tradition, not a scientifically established method for predicting life events.",
        ],
        "disclaimer": (
            "Traditional Jyotish interpretation, offered as a structured reflection. "
            "Not a scientific personality assessment, not a guaranteed forecast."
        ),
    }

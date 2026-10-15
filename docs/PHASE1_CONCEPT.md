# Trimatasta Tech — South Indian Astro Engine
## Phase 1 concept and implementation plan

### Purpose

Create a modular engine for South Indian Vedic astrology workflows. The proposed design has three calculation passes followed by an explicit consensus matrix. The project name in this repository is Jataka.

This document records a software design, not a claim that astrological interpretations are scientifically validated.

### Product principle: conversation before charts

**Do not display a horoscope chart in the initial product.** The first experience should be an interactive, guided conversation in which the user provides information one step at a time. Every answer must be validated before it is accepted or used in a calculation.

The interface should:
- ask one clear question at a time where practical;
- explain why a detail is needed when that is not obvious;
- validate dates, times, time zones, location coordinates, and choices immediately;
- show the interpreted value back to the user for confirmation when ambiguity is possible;
- identify missing, contradictory, or uncertain information and ask the user to resolve it;
- never silently guess a birth time, time zone, location, ayanāṃśa, or tradition-specific rule;
- let the user correct an earlier answer without restarting the whole conversation;
- keep confirmed inputs distinct from inferred or unconfirmed values;
- show a concise summary of the inputs and conventions before running a chart calculation;
- report what is unknown or not implemented rather than inventing an answer.

The trust goal is not to promise that every interpretation is correct. It is to make inputs, calculation choices, uncertainty, and limitations visible so the user can catch errors early.

### Pass 1 — Parāśari / Drik

Planned responsibilities:

- Use Swiss Ephemeris through pyswisseph for reproducible astronomical positions.
- Accept birth date/time, geographic latitude/longitude, and an explicit time-zone identifier or UTC offset with provenance.
- Calculate sidereal longitudes using an explicitly selected sidereal mode.
- Derive Lagna/Ascendant, rāśi placements, house relationships, Navāṃśa (D9), and Vimśottarī daśā where conventions are specified.
- Include calculation settings and source/version metadata in results.

### Pass 2 — Jaimini factors

Planned responsibilities:

- Chara Kārakas using an explicitly selected rule, including how Rāhu is handled if included.
- Arūḍha Padas, including Arūḍha Lagna and A10, with documented exception rules.
- Keep each derived factor traceable to its input longitudes and rule.

### Pass 3 — Ashtakavarga and Gochara

Planned responsibilities:

- Distinguish Bhinna Ashtakavarga (planet-specific bindu tables) from Sarvāṣṭakavarga (aggregate scores).
- Record the rules used to calculate bindus and the mapping of signs/planets.
- Add transit triggers, including Jupiter and Saturn, only after transit conventions and reference cases are established.
- Keep natal and transit calculations independently inspectable.

### Consensus matrix

The consensus layer should accept evidence from the three passes and produce a transparent summary. Each evidence item should identify its source engine, topic, direction or category, rule identifier, and score/weight.

The matrix must be deterministic for identical inputs, preserve original evidence, make weights and aggregation rules explicit, avoid treating missing evidence as negative evidence, retain contradictions, and distinguish an internal software score from probability, certainty, or validated prediction.

The initial implementation uses a generic evidence aggregation utility. Domain-specific weights should not be set until documented and reviewed.

### Q&A / language-model layer (later phase)

A future language model may explain calculated results in culturally appropriate language. It must not calculate or silently alter astronomical values. The application should pass structured, versioned calculation output to the interpretation layer and label interpretation as such. If a response depends on an uncertain input or an unimplemented calculation, the system should say so and ask for clarification instead of presenting a confident-sounding answer.

### Chart display

Chart rendering is explicitly deferred. The first version should focus on the guided interaction, answer validation, input review, traceable calculations, and clear explanations. Do not spend implementation effort on a South Indian chart display until the user experience and calculation validation are established. If chart display is added later, confirm the exact 4×4 perimeter cell mapping and sign order against agreed reference charts first.

### Suggested delivery sequence

1. Define the guided question flow and answer-validation rules.
2. Freeze calculation conventions and data models.
3. Add birth-input validation and time-zone conversion.
4. Implement and test core ephemeris and sidereal longitude calculations.
5. Implement derived Parāśari factors and compare with reference charts.
6. Implement Jaimini factors and test edge cases.
7. Implement Bhinna and Sarvāṣṭakavarga independently.
8. Add transit calculations and reference cases.
9. Connect validated engine outputs to the guided Q&A flow and transparent consensus layer.
10. Consider chart rendering only in a later phase.

### Acceptance criteria

A calculation feature is not complete until it has documented conventions, deterministic automated tests, trusted reference cases and edge-case coverage, recorded calculation settings and software version, and documented known limitations.

A user interaction is not complete until invalid or ambiguous answers are caught, corrections are possible, and the system can show which inputs are confirmed versus unresolved.

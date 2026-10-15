# Trimatasta Tech — South Indian Astro Engine
## Phase 1 concept and implementation plan

### Purpose

Create a modular engine for South Indian Vedic astrology workflows. The proposed design has three calculation passes followed by an explicit consensus matrix. The project name in this repository is Jataka.

This document records a software design, not a claim that astrological interpretations are scientifically validated.

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

A future language model may explain calculated results in culturally appropriate language. It must not calculate or silently alter astronomical values. The application should pass structured, versioned calculation output to the interpretation layer and label interpretation as such.

### South Indian chart display (later phase)

The intended visual convention is a fixed-rāśi South Indian chart in a 4×4 perimeter arrangement, with Mesha/Aries at the top-left and signs proceeding clockwise. Before chart rendering is implemented, confirm the exact cell mapping, center-panel content, sign labels, and whether the layout matches reference charts used for validation.

### Suggested delivery sequence

1. Freeze calculation conventions and data models.
2. Add birth-input validation and time-zone conversion.
3. Implement and test core ephemeris and sidereal longitude calculations.
4. Implement derived Parāśari factors and compare with reference charts.
5. Implement Jaimini factors and test edge cases.
6. Implement Bhinna and Sarvāṣṭakavarga independently.
7. Add transit calculations and reference cases.
8. Add chart visualization and API endpoints.
9. Add consensus rules and explanation layer only after engine outputs are traceable.

### Acceptance criteria

A calculation feature is not complete until it has documented conventions, deterministic automated tests, trusted reference cases and edge-case coverage, recorded calculation settings and software version, and documented known limitations.

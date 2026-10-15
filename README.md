# Jataka — South Indian Astro Engine (Phase 1)

Jataka is a modular research and software project for implementing a South Indian Vedic astrology calculation engine using clearly documented conventions. The proposed design combines three calculation passes and a deterministic consensus layer. Any future language-model interpretation will remain separate from calculation results.

**Status: initial scaffold.** This repository does not yet provide a complete or validated astrology calculator. Calculation modules identify unfinished work rather than inventing results.

## Product principle

**The initial product will not display a horoscope chart.** It will use an interactive, guided conversation with validation at every user answer. Ambiguous or invalid information should be clarified, not silently guessed. Users should be able to review and correct inputs before calculations run.

## Phase 1 goals

1. Define a guided question flow and immediate answer-validation rules.
2. Define explicit date/time, location, zodiac, ayanāṃśa, house, and calculation conventions.
3. Build independent modules for Parāśari/Drik calculations, Jaimini-derived factors, and Ashtakavarga/transits.
4. Keep astronomical calculations deterministic and reproducible.
5. Combine supplied evidence through a transparent, testable consensus matrix.
6. Validate outputs against trusted reference charts before describing calculations as complete.

## Architecture

- src/jataka/parashari_engine.py — Parāśari/Drik calculation boundary.
- src/jataka/jaimini_engine.py — Jaimini factor boundary.
- src/jataka/ashtakavarga_engine.py — Ashtakavarga and transit boundary.
- src/jataka/consensus.py — deterministic evidence aggregation.
- src/jataka/api.py — FastAPI application.

## Development

Python 3.11 or later is recommended.

    python -m venv .venv
    # Windows: .venv/Scripts/activate
    # macOS/Linux:
    source .venv/bin/activate
    pip install -e ".[dev]"
    pytest
    uvicorn jataka.api:app --reload

The package uses a src layout. Install it with pip install -e . before running the app.

## Important conventions and limits

- Birth date/time must be interpreted in the birth location's time zone; never silently assume the machine's local zone.
- Astronomical calculation settings, including Swiss Ephemeris version, sidereal mode/ayanāṃśa, house system, and coordinates, must be recorded with outputs.
- Parāśari, Jaimini, and Ashtakavarga outputs remain separate evidence streams.
- Consensus scores are software bookkeeping, not a measure of scientific truth or predictive accuracy.
- Any AI-generated explanation must be presented as interpretation, not as a source of planetary positions or other calculated facts.
- This project is not a substitute for professional, medical, financial, or legal advice.

See docs/PHASE1_CONCEPT.md, docs/CALCULATION_CONVENTIONS.md, and docs/INTERACTION_AND_TRUST.md.

# Jataka — South Indian Astro Engine (Phase 1)

Jataka is a modular research and software project for implementing a South Indian Vedic astrology calculation engine using clearly documented conventions. The proposed design combines three calculation passes and a deterministic consensus layer. Any future language-model interpretation will remain separate from calculation results.

**Status: early implementation.** Jataka now includes explicit local-birth-time-to-UTC conversion and a first Swiss Ephemeris numerical pass for sidereal planetary longitudes and house cusps. These outputs are marked unvalidated and are not yet connected to the guided web interface. The project is not a complete or validated astrology calculator.

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

- src/jataka/birth_time.py — local civil birth time to UTC conversion with DST ambiguity checks.\n- src/jataka/parashari_engine.py — first Swiss Ephemeris pass for planetary longitudes and house cusps; explicit settings required.
- src/jataka/jaimini_engine.py — Jaimini factor boundary.
- src/jataka/ashtakavarga_engine.py — Ashtakavarga and transit boundary.
- src/jataka/consensus.py — deterministic evidence aggregation.
- src/jataka/api.py — local FastAPI application.
- functions/ — Cloudflare Pages endpoints for health and prototype status.

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

## Interactive prototype

The browser interface asks for birth details one step at a time, validates each response, allows back-navigation and correction, and provides an explicit birthplace search using Open-Meteo's geocoding API. The user selects a matching place; coordinates and a suggested IANA time zone are then displayed for confirmation. The guided interface deliberately has no chart display. It submits confirmed birth details to the FastAPI calculation endpoint and displays raw planetary longitudes only with a prominent unvalidated status. On Cloudflare Pages, `/api/calculate` proxies to the separately hosted Python service when `JATAKA_ENGINE_URL` is configured; unless both `JATAKA_ENGINE_URL` and the matching secret `JATAKA_ENGINE_TOKEN` are configured, it fails safely and performs no calculation. The proxy sends the token only from the server-side Pages function; it is not exposed to browser JavaScript. There is no account system or server-side storage of entered birth details.

## Hosted prototype

The guided interface is hosted on Cloudflare Pages:

- Website: https://jataka.pages.dev
- Health endpoint: https://jataka.pages.dev/health
- Prototype status: https://jataka.pages.dev/api/status

Cloudflare Pages deploys the static interface from `src/jataka/static` and serves the small status endpoints from `functions/`. The FastAPI app provides `POST /api/calculate` for local use and for a separately hosted Python service. It requires a confirmed date, exact local time, IANA time zone, and coordinates; ambiguous/nonexistent daylight-saving times are rejected rather than guessed. The first pass explicitly uses Lahiri and whole-sign houses (`W`) and returns unvalidated numerical data only. Hosted Pages requires a separately hosted Python/Swiss Ephemeris service plus `JATAKA_ENGINE_URL` and a matching secret `JATAKA_ENGINE_TOKEN` on Pages. See [hosted engine deployment instructions](docs/HOSTED_ENGINE_DEPLOYMENT.md) for the container and free-tier Render setup.

This is an early prototype, not a validated astrology calculator. Birthplace lookup uses Open-Meteo's public geocoding endpoint (GeoNames data); it requires an internet connection and is intended for non-commercial use under the provider's published terms. The user must confirm the selected location; city-centre coordinates may not represent the exact birth building. Input checks validate format and ranges, not astrological interpretations. Astronomical calculation conventions and reference-chart validation remain unfinished.

## Important conventions and limits

- Birth date/time must be interpreted in the birth location's time zone; never silently assume the machine's local zone.
- The initial ayanāṃśa standard is Lahiri (Chitrapaksha); any alternative mode must be explicitly selected and recorded.\n- Astronomical calculation settings, including Swiss Ephemeris version, sidereal mode/ayanāṃśa, house system, and coordinates, must be recorded with outputs.
- Parāśari, Jaimini, and Ashtakavarga outputs remain separate evidence streams.
- Consensus scores are software bookkeeping, not a measure of scientific truth or predictive accuracy.
- Any AI-generated explanation must be presented as interpretation, not as a source of planetary positions or other calculated facts.
- This project is not a substitute for professional, medical, financial, or legal advice.

See docs/PHASE1_CONCEPT.md, docs/CALCULATION_CONVENTIONS.md, and docs/INTERACTION_AND_TRUST.md.

## License

Jataka is licensed under the GNU Affero General Public License, version 3 or (at your option) any later version. See [LICENSE](LICENSE). Because the application is offered over a network, the running interface links to the corresponding public source. Swiss Ephemeris is dual-licensed; this project chooses its AGPL option. Preserve upstream notices and review the upstream [license](https://github.com/aloistr/swisseph/blob/master/LICENSE) before redistributing components.

## Calculation status

The first Swiss Ephemeris module is an engineering foundation, not a claim of astrological correctness. Its output includes the selected sidereal mode, house system, library version and explicit warnings. Independent reference-chart validation, edge-case testing, and documented convention choices are still required before calculations should be presented as validated. The interface integration does not change this status.

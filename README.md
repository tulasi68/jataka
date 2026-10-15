# Jataka — Guided South Indian Jyotish App

Jataka is a modular research and software project for implementing a South Indian Vedic astrology calculation engine using clearly documented conventions. The proposed design combines three calculation passes and a deterministic consensus layer. Any future language-model interpretation will remain separate from calculation results.

**Status: active prototype; calculation accuracy is not yet validated.** The guided interface now displays a South Indian Rāśi chart, derived sign/house/Nakshatra/pada/Navāṃśa factors, a Vimśottarī Mahādaśā sequence, explicit 7- and 8-karaka Chara Kāraka variants, and a cautious personal reflection report. A new plain-language interpretation layer presents an everyday-language reading first while keeping every technical calculation available under an expandable details section. All derived factors inherit the unvalidated source longitudes. Arūḍha Padas, Ashtakavarga, and sign-based transit scoring are now implemented, but their rule variants and outputs remain unvalidated. Genuine independent three-pass verification and reference-chart validation remain outstanding.

## Product principle

**The interface uses an interactive, guided conversation with validation at every user answer.** It confirms birth date, time, birthplace coordinates and IANA time zone before calculating. It shows the South Indian Rāśi chart, derived factors, and a reflective report only after a successful response. Ambiguous or invalid information should be clarified, not silently guessed. Users can review and correct inputs before calculations run.

## Phase 1 goals

1. Define a guided question flow and immediate answer-validation rules.
2. Define explicit date/time, location, zodiac, ayanāṃśa, house, and calculation conventions.
3. Build independent modules for Parāśari/Drik calculations, Jaimini-derived factors, and Ashtakavarga/transits.
4. Keep astronomical calculations deterministic and reproducible.
5. Combine supplied evidence through a transparent, testable consensus matrix.
6. Validate outputs against trusted reference charts before describing calculations as complete.

## Architecture

- src/jataka/birth_time.py — local civil birth time to UTC conversion with DST ambiguity checks.
- src/jataka/parashari_engine.py — first Swiss Ephemeris pass for planetary longitudes and house cusps; explicit settings required.
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

The browser interface asks for birth details one step at a time, validates each response, allows back-navigation and correction, and provides an explicit birthplace search using Open-Meteo's geocoding API. The user selects a matching place; coordinates and a suggested IANA time zone are then displayed for confirmation. The guided interface submits confirmed birth details to the FastAPI calculation endpoint. On success, it first displays a plain-language interpretation organized by self-understanding, work, relationships, money/security, home/wellbeing, learning, and the current traditional period. It then keeps all raw planetary longitudes, South Indian Rāśi chart, derived factors, Vimśottarī periods, Chara Kāraka and Arūḍha factors, Ashtakavarga and transit sign scores, verification ledger, and printable personal reflection report available in an expandable technical-details section. Optional name numerology and user-recorded palmistry reflections can be included. All astronomical and derived outputs remain prominently unvalidated. On Cloudflare Pages, `/api/calculate` proxies to the separately hosted Python service when `JATAKA_ENGINE_URL` is configured; unless both `JATAKA_ENGINE_URL` and the matching secret `JATAKA_ENGINE_TOKEN` are configured, it fails safely and performs no calculation. The proxy sends the token only from the server-side Pages function; it is not exposed to browser JavaScript. There is no account system or server-side storage of entered birth details.

## Hosted prototype

The guided interface is hosted on Cloudflare Pages:

- Website: https://jataka.pages.dev
- Health endpoint: https://jataka.pages.dev/health
- Prototype status: https://jataka.pages.dev/api/status

Cloudflare Pages deploys the static interface from `src/jataka/static` and serves the small status endpoints from `functions/`. The FastAPI app provides `POST /api/calculate` for local use and for a separately hosted Python service. It requires a confirmed date, exact local time, IANA time zone, and coordinates; ambiguous/nonexistent daylight-saving times are rejected rather than guessed. The first pass explicitly uses Lahiri and whole-sign houses (`W`). The interface presents the South Indian Rāśi chart, derived factors, and a printable reflection report; astronomical and derived results remain unvalidated. Hosted Pages requires a separately hosted Python/Swiss Ephemeris service plus `JATAKA_ENGINE_URL` and a matching secret `JATAKA_ENGINE_TOKEN` on Pages. See [hosted engine deployment instructions](docs/HOSTED_ENGINE_DEPLOYMENT.md) for the container and free-tier Render setup.

This is an early prototype, not a validated astrology calculator. Birthplace lookup uses Open-Meteo's public geocoding endpoint (GeoNames data); it requires an internet connection and is intended for non-commercial use under the provider's published terms. The user must confirm the selected location; city-centre coordinates may not represent the exact birth building. Input checks validate format and ranges, not astrological interpretations. Astronomical calculation conventions and reference-chart validation remain unfinished.

## Important conventions and limits

- Birth date/time must be interpreted in the birth location's time zone; never silently assume the machine's local zone.
- The initial ayanāṃśa standard is Lahiri (Chitrapaksha); any alternative mode must be explicitly selected and recorded.
- Astronomical calculation settings, including Swiss Ephemeris version, sidereal mode/ayanāṃśa, house system, and coordinates, must be recorded with outputs.
- Parāśari, Jaimini, and Ashtakavarga outputs remain separate evidence streams.
- Consensus scores are software bookkeeping, not a measure of scientific truth or predictive accuracy.
- Any AI-generated explanation must be presented as interpretation, not as a source of planetary positions or other calculated facts.
- This project is not a substitute for professional, medical, financial, or legal advice.

See docs/PHASE1_CONCEPT.md, docs/CALCULATION_CONVENTIONS.md, and docs/INTERACTION_AND_TRUST.md.

## License

Jataka is licensed under the GNU Affero General Public License, version 3 or (at your option) any later version. See [LICENSE](LICENSE). Because the application is offered over a network, the running interface links to the corresponding public source. Swiss Ephemeris is dual-licensed; this project chooses its AGPL option. Preserve upstream notices and review the upstream [license](https://github.com/aloistr/swisseph/blob/master/LICENSE) before redistributing components.

## Calculation status

The first Swiss Ephemeris module is an engineering foundation, not a claim of astrological correctness. Its output includes the selected sidereal mode, house system, library version and explicit warnings. Independent reference-chart validation, edge-case testing, and documented convention choices are still required before calculations should be presented as validated. The interface integration does not change this status.


## Current phase status

- **Guided input and calculation:** implemented; birth details are reviewed before submission and not stored by the app.
- **South Indian Rāśi chart:** implemented.
- **Derived factors:** implemented for sign, whole-sign house, Nakṣatra/pāda, Navāṃśa (D9), Vimśottarī Mahādaśā sequence, and two explicit Chara Kāraka variants. Automated tests are included; independent reference-chart comparison is still required.
- **Reflective explanations and personal report:** implemented as deterministic traditional-topic summaries with a browser print / save-as-PDF option. They are not predictions or scientific personality assessments.
- **Arūḍha Padas, Bhinna/Sarvāṣṭakavarga, Gochara/transit triggers:** not yet implemented. These require rule variants to be explicitly recorded and checked against trusted references before they can be safely surfaced.
- **Consensus matrix:** generic deterministic aggregation utility exists; domain-specific evidence and weights are not yet integrated into the user report.
- **Validation:** not complete. Do not remove the UNVALIDATED labels until independently sourced reference charts, tolerances, and edge cases have been checked.



## Remaining implementation and validation

- The three traditional analysis passes are implemented, but they share the same natal astronomical positions. The UI deliberately says **source independence not established**; this is not yet independent three-pass verification.
- Numerology calculates common Pythagorean and Chaldean name totals plus explicitly labelled birth-date reductions. It is optional and culturally interpretive.
- Palmistry currently accepts observations selected by the user. It does not upload or analyse palm photos; its output is folklore-based reflection, not a prediction.
- Next release gate: add independently sourced reference charts and tolerance tests for astronomical positions, validate rule variants, review API/UI behaviour, and only then consider a production label. No output is represented as a guaranteed prediction.

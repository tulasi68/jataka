# Calculation conventions — decision register

This document is the source of truth for conventions used by Jataka. Do not infer a convention silently in code. Mark unresolved items as open and add tests when a decision is made.

## Current decisions

| Area | Current status | Requirement |
|---|---|---|
| Astronomical source | Implemented: Swiss Ephemeris / pyswisseph | Record library and ephemeris versions; validate against independent fixtures |
| Zodiac | Sidereal intended | Select and document exact Swiss Ephemeris sidereal mode |
| Ayanāṃśa | Lahiri (Chitrapaksha) selected for initial product | Swiss Ephemeris sidereal mode is explicitly Lahiri; retain output metadata |
| Birth time zone | Implemented | Require IANA time-zone name and convert local civil time to UTC with DST rules; reject ambiguous/nonexistent times |
| Coordinates | Latitude/longitude required for ascendant and houses | Document coordinate source and sign convention |
| House system | Whole-sign (`W`) selected for initial product | Whole-sign placements are derived from the Ascendant sign; keep raw Swiss house cusps separately |
| Navāṃśa (D9) | Implemented, derived output unvalidated | 3°20′ divisions; movable signs start from themselves, fixed signs from the ninth sign, dual signs from the fifth sign; compare against references |
| Vimśottarī daśā | Implemented, derived output unvalidated | 27 equal nakṣatras, birth balance proportional to Moon position, 365.25-day year; variant comparisons required |
| Chara Kārakas | Implemented as explicit 7- and 8-karaka variants, unvalidated | 7-karaka excludes Rahu; 8-karaka includes Rahu with reversed within-sign degree; ties are surfaced |
| Arūḍha Padas | Implemented, unvalidated | Classical seven-planet rulers and tenth-sign exception; compare lineage variants |
| Ashtakavarga | Implemented, unvalidated | Seven BAV recipient planets; eight contributors (seven planets plus Lagna); Rahu/Ketu excluded; BAV totals and 337 SAV total are internal consistency checks |
| Transit indicators | Implemented, unvalidated | Current sidereal transit signs are scored against natal BAV tables; whole-sign houses from Moon/Ascendant shown; no event prediction or timing claim |
| South Indian chart | Proposed fixed-rāśi 4×4 perimeter | Confirm exact cell layout against reference |
| Consensus weights | Open | Use transparent documented weights; never label score as probability |

## Required metadata for a calculation result

At minimum, outputs should carry the original birth date/time string, birth coordinates, time-zone identifier and resolved UTC instant, sidereal mode/ayanāṃśa setting, house system where relevant, library and engine version, rule-set version, and warnings for missing or ambiguous inputs.

## Reference validation

Before claiming parity with an established astrology program or printed chart, create reference cases with source and version, input date/time/time zone/coordinates, convention settings, expected values and tolerances, and documented differences where conventions differ.

Do not “fix” a mismatch by changing unrelated conventions without recording the change.


## Derived-factor implementation notes

`src/jataka/derived_engine.py` currently derives rāśi sign, degree within sign, nakṣatra and pāda, Navāṃśa (D9), whole-sign house, the nine-period Vimśottarī Mahādaśā sequence, and both 7- and 8-karaka Chara Kāraka rankings. These are software implementations of named conventions and are still labelled `DERIVED_UNVALIDATED`. Their output is only as reliable as the supplied astronomical longitudes and requires independent reference fixtures before being described as validated.

The following are intentionally not presented as completed calculations yet: Arūḍha Padas, Bhinna/Sarvāṣṭakavarga, and transit trigger analysis. Those require explicit rule tables, convention choices, and trusted reference fixtures; a placeholder must not be mistaken for a result.


## Three-pass analysis and independence policy

The current three passes are (1) Parāśari/Drik astronomical positions and natal placements, (2) Jaimini Chara Kārakas and Arūḍha Padas, and (3) Bhinna/Sarvāṣṭakavarga plus sign-based transit indicators. The latter two passes reuse the same natal longitudes from Swiss Ephemeris. They are distinct traditional analytical methods, **not three independent astronomical calculations**. The verification ledger therefore reports that source independence has not been established and will not mark a chart verified.

To complete genuine three-pass verification, add independently implemented/reference-sourced calculation outputs (for example, versioned reference charts from another trusted engine), compare every planet and ascendant against documented tolerances, and record rule variants and disagreements. A consensus score is never a probability and must not conceal conflicting evidence.

## Ashtakavarga rule table

The implementation uses the common seven-recipient Bhinna Ashtakavarga table, with Sun, Moon, Mars, Mercury, Jupiter, Venus, and Saturn as recipients and those seven plus Lagna as contributors. Rahu/Ketu are excluded from this table. Expected BAV totals are 48, 49, 39, 54, 56, 52, and 39; the expected Sarvāṣṭakavarga sum is 337. These totals detect implementation mistakes but do not independently validate the table's tradition-specific interpretation. See the implementation's rule table and the reference list in `THIRD_PARTY_NOTICES.md`.

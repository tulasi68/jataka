# Calculation conventions — decision register

This document is the source of truth for conventions used by Jataka. Do not infer a convention silently in code. Mark unresolved items as open and add tests when a decision is made.

## Current decisions

| Area | Current status | Requirement |
|---|---|---|
| Astronomical source | Planned: Swiss Ephemeris / pyswisseph | Record library and ephemeris versions |
| Zodiac | Sidereal intended | Select and document exact Swiss Ephemeris sidereal mode |
| Ayanāṃśa | Lahiri (Chitrapaksha) selected for initial product | Swiss Ephemeris sidereal mode is explicitly Lahiri; retain output metadata |
| Birth time zone | Required input policy to be finalized | Prefer IANA time-zone name and convert local civil time to UTC with DST rules |
| Coordinates | Latitude/longitude required for ascendant and houses | Document coordinate source and sign convention |
| House system | Whole-sign (`W`) selected for initial product | Whole-sign placements are derived from the Ascendant sign; keep raw Swiss house cusps separately |
| Navāṃśa (D9) | Implemented, derived output unvalidated | 3°20′ divisions; movable signs start from themselves, fixed signs from the ninth sign, dual signs from the fifth sign; compare against references |
| Vimśottarī daśā | Implemented, derived output unvalidated | 27 equal nakṣatras, birth balance proportional to Moon position, 365.25-day year; variant comparisons required |
| Chara Kārakas | Implemented as explicit 7- and 8-karaka variants, unvalidated | 7-karaka excludes Rahu; 8-karaka includes Rahu with reversed within-sign degree; ties are surfaced |
| Arūḍha Padas | Open | Document standard counting and exception rules |
| Ashtakavarga | Open | Specify bindu tables and planet inclusion/exclusion |
| Transit triggers | Open | Specify transit reference, orb/counting rules, and timing convention |
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

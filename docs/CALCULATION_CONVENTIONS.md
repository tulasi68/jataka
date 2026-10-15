# Calculation conventions — decision register

This document is the source of truth for conventions used by Jataka. Do not infer a convention silently in code. Mark unresolved items as open and add tests when a decision is made.

## Current decisions

| Area | Current status | Requirement |
|---|---|---|
| Astronomical source | Planned: Swiss Ephemeris / pyswisseph | Record library and ephemeris versions |
| Zodiac | Sidereal intended | Select and document exact Swiss Ephemeris sidereal mode |
| Ayanāṃśa | Open | Choose explicitly; do not assume Lahiri without confirmation |
| Birth time zone | Required input policy to be finalized | Prefer IANA time-zone name and convert local civil time to UTC with DST rules |
| Coordinates | Latitude/longitude required for ascendant and houses | Document coordinate source and sign convention |
| House system | Open | Select and test; distinguish whole-sign houses from quadrant-house calculations |
| Navāṃśa (D9) | Planned | Document boundary handling and sign mapping |
| Vimśottarī daśā | Planned | Document nakṣatra, balance-at-birth, and year-length convention |
| Chara Kārakas | Open | Decide number of kārakas and Rāhu treatment |
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

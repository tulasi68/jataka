# Interactive flow and trust requirements

## Product decision

The initial Jataka experience is a guided, interactive conversation. **Do not show a horoscope chart in the initial version.** Prioritize clarity, validation, correction, and trust.

## Rules for every answer

1. Ask one clear question at a time where practical.
2. Validate the answer immediately against its expected type, format, range, and dependencies.
3. If invalid, explain the specific problem and ask again without discarding other confirmed answers.
4. If an answer is ambiguous, ask a clarifying question rather than selecting a likely interpretation silently.
5. For high-impact inputs (birth date, birth time, time zone, place, and calculation tradition), display the interpreted value and ask the user to confirm it before calculation.
6. Distinguish user-confirmed values, system-derived values, and unresolved values in the internal session state.
7. Let the user revisit and correct earlier answers; revalidate dependent values when an upstream answer changes.
8. Before calculation, show a compact review of the birth details and calculation conventions and require confirmation.
9. Never replace missing information with a guess. If the user does not know a value, explain the consequence and ask whether to continue with a clearly labelled limitation.
10. If a calculation is unimplemented or not validated, say so directly instead of generating a plausible-looking result.

## Validation examples

- Date: reject impossible calendar dates.
- Time: validate the clock format and distinguish unknown birth time from midnight.
- Time zone: resolve local civil time using an explicit IANA zone when available; surface daylight-saving ambiguity or nonexistent local times for clarification.
- Place: confirm the selected town/city and the coordinates used; distinguish similarly named places.
- Convention choices: present understandable descriptions and record the selected rule-set version.
- Dependencies: if birth time changes, invalidate/recompute any derived ascendant, house, or timing values that depend on it.

## Trust and explanation

- Keep raw user input, normalized input, validation result, and confirmation status separate.
- Explain what each requested detail is used for when useful.
- Show calculation settings and known limitations alongside results.
- Preserve traceability from a conclusion to its calculation engine, rule identifier, and input values.
- Do not describe consensus scores as probabilities or guarantees.
- Separate astronomical calculations from traditional astrological interpretation and any language-model-generated explanation.
- Do not imply that validation of input format proves the astrological interpretation itself is correct.

## Current scope

This document specifies intended behavior. The interactive question flow and validation framework have not yet been implemented.

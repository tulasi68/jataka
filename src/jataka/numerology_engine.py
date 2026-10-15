"""Name/date numerology using explicitly named traditional conventions.

Numerology is a cultural/divinatory practice, not a validated prediction method.
The engine computes numbers only; it does not infer a user's fate or probability.
"""
from __future__ import annotations

from datetime import date
import unicodedata
from typing import Mapping

PYTHAGOREAN = {
    **{letter: (index % 9) + 1 for index, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
}
CHALDEAN = {
    **dict.fromkeys("AIJQY", 1), **dict.fromkeys("BKR", 2),
    **dict.fromkeys("CGLS", 3), **dict.fromkeys("DMT", 4),
    **dict.fromkeys("EHNX", 5), **dict.fromkeys("UVW", 6),
    **dict.fromkeys("OZ", 7), **dict.fromkeys("FP", 8),
}


def _letters(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name)
    return "".join(ch for ch in normalized.upper() if "A" <= ch <= "Z")


def _reduce(value: int, preserve_masters: bool = True) -> int:
    if value <= 0:
        return value
    while value > 9 and not (preserve_masters and value in (11, 22, 33)):
        value = sum(int(digit) for digit in str(value))
    return value


def _sum_letters(name: str, mapping: Mapping[str, int]) -> dict[str, object]:
    letters = _letters(name)
    if not letters:
        raise ValueError("Enter a name containing at least one A-Z letter for numerology")
    values = [{"letter": letter, "value": mapping[letter]} for letter in letters]
    total = sum(item["value"] for item in values)
    return {
        "letter_values": values,
        "total": total,
        "reduced_number": _reduce(total),
    }


def calculate_numerology(full_name: str, birth_date: date) -> dict[str, object]:
    """Compute common Pythagorean and Chaldean name values and date numbers."""
    if not full_name or len(full_name.strip()) < 1 or len(full_name) > 200:
        raise ValueError("Name must contain 1 to 200 characters")
    if birth_date > date.today():
        raise ValueError("Birth date cannot be in the future")
    digits = [int(char) for char in birth_date.strftime("%Y%m%d")]
    digit_total = sum(digits)
    month_day = birth_date.month + birth_date.day
    return {
        "status": "NUMEROLOGY_COMPUTED_UNVALIDATED",
        "input": {"name_used": full_name.strip(), "birth_date": birth_date.isoformat()},
        "systems": {
            "pythagorean": _sum_letters(full_name, PYTHAGOREAN),
            "chaldean": _sum_letters(full_name, CHALDEAN),
        },
        "birth_date_numbers": {
            "digit_sum": digit_total,
            "life_path_reduced": _reduce(digit_total),
            "birth_day": birth_date.day,
            "birth_day_reduced": _reduce(birth_date.day),
            "month_day_sum_reduced": _reduce(month_day),
        },
        "conventions": {
            "pythagorean": "Latin A-Z cycle 1-9; master totals 11, 22, 33 are preserved",
            "chaldean": "Common Chaldean letter table; compound totals preserved alongside reduced number",
            "date": "Digit sum of YYYYMMDD; other numerology schools use different date-reduction conventions",
        },
        "warning": (
            "Numerology is a cultural/divinatory tradition, not a scientifically validated "
            "method for predicting events. The name and date are used only for this response."
        ),
    }

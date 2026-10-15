"""Jaimini-derived factors.

This module will implement Chara Kārakas and Arūḍha Padas after their precise
rule variants are selected in the calculation-conventions document.
"""

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class JaiminiSettings:
    chara_karaka_count: int
    include_rahu: bool
    ruleset_version: str = "0.1.0"

    def __post_init__(self) -> None:
        if self.chara_karaka_count not in (7, 8):
            raise ValueError("chara_karaka_count must be 7 or 8")


def calculate_jaimini_factors(
    sidereal_longitudes: Mapping[str, float], settings: JaiminiSettings
) -> dict[str, object]:
    """Return Jaimini factors from sidereal longitudes.

    Not implemented yet. No factors are returned until the rule variant and
    boundary/tie handling are documented and covered by tests.
    """
    del sidereal_longitudes, settings
    raise NotImplementedError(
        "Jaimini factors are not implemented; see docs/CALCULATION_CONVENTIONS.md"
    )

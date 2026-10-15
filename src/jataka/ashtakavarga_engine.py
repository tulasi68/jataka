"""Ashtakavarga and Gochara engine boundary.

Bhinna Ashtakavarga and Sarvāṣṭakavarga are distinct outputs and must not be
conflated. Transit calculations will be added after rules and reference cases
are documented.
"""

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class AshtakavargaSettings:
    ruleset_version: str = "0.1.0"


def calculate_ashtakavarga(
    sign_positions: Mapping[str, int], settings: AshtakavargaSettings
) -> dict[str, object]:
    """Calculate Bhinna and Sarvāṣṭakavarga tables.

    Not implemented yet: specify bindu rules and validate all tables against
    trusted reference cases before returning numerical results.
    """
    del sign_positions, settings
    raise NotImplementedError(
        "Ashtakavarga calculations are not implemented; see docs/CALCULATION_CONVENTIONS.md"
    )


def calculate_transit_triggers(
    natal_positions: Mapping[str, int],
    transit_positions: Mapping[str, int],
    ruleset_version: str = "0.1.0",
) -> dict[str, object]:
    """Calculate documented transit triggers (not implemented yet)."""
    del natal_positions, transit_positions, ruleset_version
    raise NotImplementedError(
        "Transit triggers are not implemented; document rules before calculating"
    )

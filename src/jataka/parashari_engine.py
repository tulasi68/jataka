"""Parāśari/Drik engine boundary.

Astronomical calculations must be deterministic and convention-explicit. This first
scaffold deliberately does not return fabricated chart values. Implement features
only alongside reference tests and a documented convention decision.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BirthData:
    """Birth inputs; birth_time_utc must already be timezone-aware and in UTC."""

    birth_time_utc: datetime
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if self.birth_time_utc.tzinfo is None or self.birth_time_utc.utcoffset() is None:
            raise ValueError("birth_time_utc must be timezone-aware")
        if not -90 <= self.latitude <= 90:
            raise ValueError("latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")


@dataclass(frozen=True)
class CalculationSettings:
    """Settings that must be explicitly selected before producing a chart."""

    sidereal_mode: str
    house_system: str
    ruleset_version: str = "0.1.0"


def calculate_chart(
    birth: BirthData, settings: CalculationSettings
) -> dict[str, object]:
    """Calculate a Parāśari chart.

    Not implemented yet: choose and document the sidereal mode and house system,
    then implement with Swiss Ephemeris and add reference-chart tests.
    """
    del birth, settings
    raise NotImplementedError(
        "Parāśari chart calculation is not implemented; see docs/CALCULATION_CONVENTIONS.md"
    )

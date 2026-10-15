"""Deterministic Parāśari/Drik calculations using Swiss Ephemeris.

This module exposes raw, traceable calculations only. Interpretations are outside
this module. Every result records the selected sidereal mode and house system.
Lahiri (Chitrapaksha) is the initial ayanāṃśa standard; callers can override it
explicitly for research comparisons.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite
from threading import RLock

import swisseph as swe


class CalculationError(ValueError):
    """The requested astronomical calculation could not be completed safely."""


_SWISS_LOCK = RLock()
_SIDEREAL_MODES = {
    "lahiri": swe.SIDM_LAHIRI,
    "raman": swe.SIDM_RAMAN,
    "krishnamurti": swe.SIDM_KRISHNAMURTI,
}
# Swiss Ephemeris house-system codes. We deliberately reject unknown codes
# before passing them into the native library.
_HOUSE_SYSTEMS = frozenset("PKORCAEVWBMTXHGU")
_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
}


@dataclass(frozen=True)
class BirthData:
    """Birth inputs; birth_time_utc must be timezone-aware."""

    birth_time_utc: datetime
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if self.birth_time_utc.tzinfo is None or self.birth_time_utc.utcoffset() is None:
            raise ValueError("birth_time_utc must be timezone-aware")
        if not isfinite(self.latitude) or not -90 <= self.latitude <= 90:
            raise ValueError("latitude must be finite and between -90 and 90")
        if not isfinite(self.longitude) or not -180 <= self.longitude <= 180:
            raise ValueError("longitude must be finite and between -180 and 180")


@dataclass(frozen=True)
class CalculationSettings:
    """Explicit astronomical choices, with Lahiri as the agreed initial standard."""

    house_system: str
    sidereal_mode: str = "lahiri"
    ruleset_version: str = "0.1.0"

    def __post_init__(self) -> None:
        if self.sidereal_mode not in _SIDEREAL_MODES:
            raise ValueError(
                "sidereal_mode must be one of: " + ", ".join(sorted(_SIDEREAL_MODES))
            )
        if self.house_system not in _HOUSE_SYSTEMS:
            raise ValueError(
                "Unsupported house_system; use a documented Swiss Ephemeris house-system code"
            )
        if not self.ruleset_version.strip():
            raise ValueError("ruleset_version must not be empty")


def _julian_day_ut(moment: datetime) -> float:
    utc = moment.astimezone(timezone.utc)
    decimal_hour = (
        utc.hour + utc.minute / 60
        + (utc.second + utc.microsecond / 1_000_000) / 3600
    )
    return swe.julday(utc.year, utc.month, utc.day, decimal_hour, swe.GREG_CAL)


def calculate_chart(birth: BirthData, settings: CalculationSettings) -> dict[str, object]:
    """Calculate sidereal planetary longitudes and house cusps.

    This is a numerical foundation, not a validated complete horoscope. Results
    must be checked against versioned reference charts before production use.
    """
    jd_ut = _julian_day_ut(birth.birth_time_utc)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    with _SWISS_LOCK:
        swe.set_sid_mode(_SIDEREAL_MODES[settings.sidereal_mode])
        planets: dict[str, dict[str, float]] = {}
        try:
            for name, planet_id in _PLANETS.items():
                values, _retflags = swe.calc_ut(jd_ut, planet_id, flags)
                planets[name] = {
                    "longitude": float(values[0] % 360),
                    "latitude": float(values[1]),
                    "distance_au": float(values[2]),
                    "longitude_speed_deg_per_day": float(values[3]),
                }
            rahu_longitude = planets["Rahu"]["longitude"]
            planets["Ketu"] = {
                "longitude": float((rahu_longitude + 180) % 360),
                "latitude": float(-planets["Rahu"]["latitude"]),
                "distance_au": float(planets["Rahu"]["distance_au"]),
                "longitude_speed_deg_per_day": float(
                    planets["Rahu"]["longitude_speed_deg_per_day"]
                ),
            }
            cusps, angles = swe.houses_ex(
                jd_ut, birth.latitude, birth.longitude,
                settings.house_system.encode("ascii"), swe.FLG_SIDEREAL
            )
        except swe.Error as exc:
            raise CalculationError(
                "Swiss Ephemeris could not calculate this chart with the selected "
                "coordinates and house system. Check the inputs and high-latitude limits."
            ) from exc

    return {
        "status": "calculated_unvalidated",
        "birth_time_utc": birth.birth_time_utc.astimezone(timezone.utc).isoformat(),
        "coordinates": {"latitude": birth.latitude, "longitude": birth.longitude},
        "julian_day_ut": jd_ut,
        "settings": {
            "sidereal_mode": settings.sidereal_mode,
            "house_system": settings.house_system,
            "ruleset_version": settings.ruleset_version,
            "ephemeris": "Swiss Ephemeris",
            "ephemeris_version": swe.version,
        },
        "planets": planets,
        "ascendant_longitude": float(angles[0] % 360),
        "midheaven_longitude": float(angles[1] % 360),
        "house_cusps": [float(value % 360) for value in cusps],
        "warnings": [
            "Numerical output has not yet been validated against agreed reference charts.",
            "House-system behavior and high-latitude edge cases require dedicated tests.",
            "Astrological interpretations are not produced by this module.",
        ],
    }

from datetime import datetime, timezone
from math import isfinite

import pytest

from jataka.birth_time import BirthTimeError, local_birth_time_to_utc
from jataka.parashari_engine import (
    BirthData,
    CalculationError,
    CalculationSettings,
    calculate_chart,
)


def test_lahiri_is_initial_ayanamsa_standard() -> None:
    settings = CalculationSettings(house_system="W")
    assert settings.sidereal_mode == "lahiri"


def test_calculation_returns_traceable_unvalidated_positions() -> None:
    birth = BirthData(
        datetime(2000, 1, 1, 12, tzinfo=timezone.utc),
        latitude=13.0827,
        longitude=80.2707,
    )
    result = calculate_chart(birth, CalculationSettings(house_system="W"))

    assert result["status"] == "calculated_unvalidated"
    assert result["settings"]["sidereal_mode"] == "lahiri"
    assert result["settings"]["ephemeris"] == "Swiss Ephemeris"
    assert result["settings"]["ephemeris_version"]
    assert len(result["house_cusps"]) == 12
    assert set(result["planets"]) == {
        "Sun", "Moon", "Mercury", "Venus", "Mars",
        "Jupiter", "Saturn", "Rahu", "Ketu",
    }
    for body in result["planets"].values():
        assert isfinite(body["longitude"])
        assert 0 <= body["longitude"] < 360
    assert (result["planets"]["Ketu"]["longitude"]
            - result["planets"]["Rahu"]["longitude"]) % 360 == pytest.approx(180)
    assert any("not yet been validated" in warning for warning in result["warnings"])


def test_other_ayanamsas_are_explicitly_selectable() -> None:
    for mode in ("raman", "krishnamurti"):
        settings = CalculationSettings(house_system="W", sidereal_mode=mode)
        assert settings.sidereal_mode == mode


def test_unknown_ayanamsa_and_house_system_are_rejected() -> None:
    with pytest.raises(ValueError, match="sidereal_mode"):
        CalculationSettings(house_system="W", sidereal_mode="made-up")
    with pytest.raises(ValueError, match="house_system"):
        CalculationSettings(house_system="?")


def test_birth_data_rejects_naive_datetime_and_nonfinite_coordinates() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        BirthData(datetime(2000, 1, 1, 12), 13, 80)
    with pytest.raises(ValueError, match="latitude"):
        BirthData(datetime(2000, 1, 1, 12, tzinfo=timezone.utc), float("nan"), 80)


def test_local_birth_time_conversion_for_india() -> None:
    utc = local_birth_time_to_utc(datetime(2000, 1, 1, 12), "Asia/Kolkata")
    assert utc == datetime(2000, 1, 1, 6, 30, tzinfo=timezone.utc)


def test_nonexistent_daylight_saving_time_is_rejected() -> None:
    with pytest.raises(BirthTimeError, match="does not exist"):
        local_birth_time_to_utc(datetime(2024, 3, 10, 2, 30), "America/New_York")


def test_ambiguous_daylight_saving_time_requires_confirmation() -> None:
    local = datetime(2024, 11, 3, 1, 30)
    with pytest.raises(BirthTimeError, match="occurs twice"):
        local_birth_time_to_utc(local, "America/New_York")
    earlier = local_birth_time_to_utc(local, "America/New_York", fold=0)
    later = local_birth_time_to_utc(local, "America/New_York", fold=1)
    assert (later - earlier).total_seconds() == 3600

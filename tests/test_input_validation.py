from datetime import datetime, timezone

import pytest

from jataka.parashari_engine import BirthData


def test_birth_data_requires_aware_utc_datetime() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        BirthData(datetime(2000, 1, 1), latitude=12.97, longitude=77.59)


def test_birth_data_rejects_invalid_coordinates() -> None:
    with pytest.raises(ValueError, match="latitude"):
        BirthData(datetime(2000, 1, 1, tzinfo=timezone.utc), latitude=91, longitude=0)


def test_birth_data_accepts_valid_coordinates() -> None:
    birth = BirthData(
        datetime(2000, 1, 1, tzinfo=timezone.utc), latitude=12.97, longitude=77.59
    )
    assert birth.latitude == pytest.approx(12.97)

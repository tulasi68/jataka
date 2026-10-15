from datetime import datetime, timezone

import pytest

from jataka.birth_time import BirthTimeError, local_birth_time_to_utc


def test_india_local_birth_time_converts_to_utc() -> None:
    result = local_birth_time_to_utc(datetime(1990, 1, 1, 12, 0), "Asia/Kolkata")
    assert result == datetime(1990, 1, 1, 6, 30, tzinfo=timezone.utc)


def test_rejects_aware_input_to_avoid_double_conversion() -> None:
    with pytest.raises(BirthTimeError, match="naive"):
        local_birth_time_to_utc(
            datetime(1990, 1, 1, 12, 0, tzinfo=timezone.utc), "Asia/Kolkata"
        )


def test_rejects_unknown_zone() -> None:
    with pytest.raises(BirthTimeError, match="Unknown IANA"):
        local_birth_time_to_utc(datetime(1990, 1, 1, 12, 0), "Mars/Olympus")


def test_rejects_nonexistent_dst_time() -> None:
    with pytest.raises(BirthTimeError, match="does not exist"):
        local_birth_time_to_utc(datetime(2024, 3, 10, 2, 30), "America/New_York")


def test_requires_choice_for_ambiguous_dst_time() -> None:
    with pytest.raises(BirthTimeError, match="occurs twice"):
        local_birth_time_to_utc(datetime(2024, 11, 3, 1, 30), "America/New_York")


def test_ambiguous_dst_time_can_be_resolved_explicitly() -> None:
    earlier = local_birth_time_to_utc(
        datetime(2024, 11, 3, 1, 30), "America/New_York", fold=0
    )
    later = local_birth_time_to_utc(
        datetime(2024, 11, 3, 1, 30), "America/New_York", fold=1
    )
    assert (later - earlier).total_seconds() == 3600

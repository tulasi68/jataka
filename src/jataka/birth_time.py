"""Conversion of local civil birth times to UTC without silent DST guesses."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class BirthTimeError(ValueError):
    """Birth time cannot be safely resolved from the supplied local time and zone."""


def local_birth_time_to_utc(
    local_time: datetime, timezone_name: str, *, fold: int | None = None
) -> datetime:
    """Convert a naive local birth time to UTC.

    Ambiguous times during a daylight-saving fall-back require fold=0 or fold=1.
    Nonexistent times during a spring-forward transition are rejected. The caller
    must collect the location's IANA zone, not a guessed numeric UTC offset.
    """
    if local_time.tzinfo is not None:
        raise BirthTimeError("local_time must be a naive local civil datetime")
    if fold not in (None, 0, 1):
        raise BirthTimeError("fold must be 0, 1, or None")
    try:
        zone = ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise BirthTimeError(f"Unknown IANA time zone: {timezone_name}") from exc

    candidates: list[datetime] = []
    for candidate_fold in (0, 1):
        local_aware = local_time.replace(tzinfo=zone, fold=candidate_fold)
        utc_candidate = local_aware.astimezone(timezone.utc)
        round_trip = utc_candidate.astimezone(zone).replace(tzinfo=None)
        if round_trip == local_time:
            candidates.append(utc_candidate)

    unique = sorted(set(candidates))
    if not unique:
        raise BirthTimeError(
            "This local time does not exist in the selected time zone due to a clock change."
        )
    if len(unique) > 1:
        if fold is None:
            raise BirthTimeError(
                "This local time occurs twice due to a clock change; confirm the earlier or later occurrence."
            )
        return local_time.replace(tzinfo=zone, fold=fold).astimezone(timezone.utc)
    return unique[0]

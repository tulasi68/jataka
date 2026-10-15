from datetime import datetime, timezone

import pytest

from jataka.derived_engine import (
    NAKSHATRA_SPAN,
    calculate_jaimini_chara_karakas,
    describe_longitude,
    derive_chart_factors,
    vimshottari_birth_sequence,
)


def test_sign_nakshatra_pada_and_navamsa_boundaries() -> None:
    assert describe_longitude(0)["sign"] == "Aries"
    assert describe_longitude(0)["nakshatra"] == "Ashwini"
    assert describe_longitude(0)["pada"] == 1
    assert describe_longitude(30)["sign"] == "Taurus"
    assert describe_longitude(13 + 20 / 60)["nakshatra"] == "Bharani"
    assert describe_longitude(30 - 1e-7)["sign"] == "Aries"
    assert describe_longitude(30 - 1e-7)["navamsa_sign"] == "Sagittarius"


def test_nakshatra_span_is_exactly_one_twenty_seventh_of_circle() -> None:
    assert NAKSHATRA_SPAN == pytest.approx(13 + 1 / 3)


def test_vimshottari_sequence_is_ordered_and_totals_120_years() -> None:
    birth = datetime(1968, 7, 6, 1, 50, tzinfo=timezone.utc)
    result = vimshottari_birth_sequence(204.22358, birth)
    assert result["status"] == "DERIVED_UNVALIDATED"
    assert len(result["periods"]) == 9
    assert sum(p["duration_years"] for p in result["periods"]) == 120
    assert result["birth_nakshatra"] == "Vishakha"
    assert result["birth_nakshatra_lord"] == "Jupiter"
    assert result["first_mahadasha_balance_years"] > 0
    assert result["conventions"]["year_days"] == 365.25


def test_chara_karaka_seven_and_eight_modes_are_explicit() -> None:
    values = {
        "Sun": 80.0, "Moon": 204.0, "Mars": 76.0, "Mercury": 61.0,
        "Jupiter": 129.0, "Venus": 84.0, "Saturn": 1.0, "Rahu": 350.0,
    }
    seven = calculate_jaimini_chara_karakas(values, karaka_count=7, include_rahu=False)
    eight = calculate_jaimini_chara_karakas(values, karaka_count=8, include_rahu=True)
    assert len(seven["rankings"]) == 7
    assert len(eight["rankings"]) == 8
    assert "Rahu" not in {p["planet"] for p in seven["rankings"]}
    assert "Rahu" in {p["planet"] for p in eight["rankings"]}
    assert eight["rankings"][0]["planet"] == "Rahu"


def test_chara_karaka_rejects_implicit_variant_conflict() -> None:
    values = {p: 1.0 for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu")}
    with pytest.raises(ValueError, match="include_rahu"):
        calculate_jaimini_chara_karakas(values, karaka_count=7, include_rahu=True)


def test_derived_chart_factors_use_whole_sign_houses() -> None:
    planets = {
        "Sun": {"longitude": 80.636233},
        "Moon": {"longitude": 204.223580},
        "Mercury": {"longitude": 61.223469},
        "Venus": {"longitude": 84.944057},
        "Mars": {"longitude": 76.513898},
        "Jupiter": {"longitude": 129.820908},
        "Saturn": {"longitude": 1.266582},
        "Rahu": {"longitude": 350.671181},
        "Ketu": {"longitude": 170.671181},
    }
    result = derive_chart_factors(
        planets, 98.929530, datetime(1968, 7, 6, 1, 50, tzinfo=timezone.utc)
    )
    assert result["ascendant"]["sign"] == "Cancer"
    assert result["planets"]["Sun"]["sign"] == "Gemini"
    assert result["planets"]["Sun"]["whole_sign_house"] == 12
    assert result["planets"]["Moon"]["sign"] == "Libra"
    assert result["planets"]["Moon"]["whole_sign_house"] == 4
    assert result["status"] == "DERIVED_UNVALIDATED"

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
    rahu = next(p for p in eight["rankings"] if p["planet"] == "Rahu")
    moon = next(p for p in eight["rankings"] if p["planet"] == "Moon")
    assert rahu["karaka_degree"] == 10.0  # Rahu uses the reversed within-sign degree
    assert moon["karaka_degree"] > rahu["karaka_degree"]


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



def test_ashtakavarga_constant_totals_and_337_sav() -> None:
    from jataka.ashtakavarga_engine import calculate_ashtakavarga

    positions = {
        "Sun": 2, "Moon": 6, "Mars": 2, "Mercury": 2,
        "Jupiter": 4, "Venus": 2, "Saturn": 0, "Lagna": 3,
    }
    result = calculate_ashtakavarga(positions)
    assert result["all_classical_totals_match"] is True
    assert result["sarvashtakavarga"]["total"] == 337
    assert {p: row["total"] for p, row in result["bhinna_ashtakavarga"].items()} == {
        "Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54,
        "Jupiter": 56, "Venus": 52, "Saturn": 39,
    }


def test_transit_scores_are_sign_based_and_non_predictive() -> None:
    from jataka.ashtakavarga_engine import calculate_transit_triggers

    natal = {
        "Sun": 2, "Moon": 6, "Mars": 2, "Mercury": 2,
        "Jupiter": 4, "Venus": 2, "Saturn": 0, "Lagna": 3,
    }
    transits = {"Sun": 4, "Moon": 8, "Mars": 1, "Mercury": 6, "Jupiter": 3, "Venus": 7, "Saturn": 11}
    result = calculate_transit_triggers(natal, transits)
    assert len(result["transits"]) == 7
    assert all("natal_bav_bindus_in_transit_sign" in row for row in result["transits"])
    assert result["status"] == "DESCRIPTIVE_UNVALIDATED"


def test_jaimini_arudha_returns_all_twelve_padas() -> None:
    from jataka.jaimini_engine import calculate_arudha_padas

    positions = {
        "Sun": 4, "Moon": 3, "Mars": 0, "Mercury": 2,
        "Jupiter": 8, "Venus": 1, "Saturn": 9,
    }
    result = calculate_arudha_padas(positions)
    assert len(result["padas"]) == 12
    assert result["arudha_lagna"]["house"] == 1
    assert all(0 <= row["arudha_sign_index"] < 12 for row in result["padas"])


def test_numerology_exposes_both_named_conventions() -> None:
    from datetime import date
    from jataka.numerology_engine import calculate_numerology

    result = calculate_numerology("Ada Lovelace", date(1815, 12, 10))
    assert set(result["systems"]) == {"pythagorean", "chaldean"}
    assert result["birth_date_numbers"]["birth_day"] == 10
    assert result["status"] == "NUMEROLOGY_COMPUTED_UNVALIDATED"


def test_palmistry_is_user_observation_not_photo_analysis() -> None:
    from jataka.palmistry_engine import build_palmistry_reflection

    result = build_palmistry_reflection({
        "heart_line": "curved", "head_line": "straight",
        "life_line": "wide_arc", "fate_line": "uncertain",
    })
    assert result["status"] == "PALMISTRY_REFLECTION_USER_RECORDED"
    assert "No image was analysed" in result["disclaimer"]
    assert len(result["observations"]) == 4


def test_three_pass_verification_never_calls_shared_source_verified() -> None:
    from jataka.verification import PassEvidence, verify_three_passes

    shared = "same-astronomical-input"
    passes = [
        PassEvidence("parashari", shared, "calculated_unvalidated", {"topic": "x"}),
        PassEvidence("jaimini", shared, "derived_unvalidated", {"topic": "x"}),
        PassEvidence("ashtakavarga_transit", shared, "derived_unvalidated", {"topic": "x"}),
    ]
    result = verify_three_passes(passes)
    assert result["status"] == "INCOMPLETE_SOURCE_INDEPENDENCE_NOT_ESTABLISHED"
    assert result["ready_to_label_verified"] is False

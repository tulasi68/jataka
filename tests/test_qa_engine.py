from datetime import datetime, timezone

import pytest

from jataka.qa_engine import answer_question


def _derived(periods=None):
    return {
        "ascendant": {"sign": "Cancer", "sign_index": 3, "whole_sign_house": 1},
        "planets": {
            "Sun":     {"sign": "Gemini", "sign_index": 2, "whole_sign_house": 12},
            "Moon":    {"sign": "Libra",  "sign_index": 6, "whole_sign_house": 4},
            "Mars":    {"sign": "Cancer", "sign_index": 3, "whole_sign_house": 1},
            "Mercury": {"sign": "Gemini", "sign_index": 2, "whole_sign_house": 12},
            "Venus":   {"sign": "Gemini", "sign_index": 2, "whole_sign_house": 12},
            "Jupiter": {"sign": "Leo",    "sign_index": 4, "whole_sign_house": 2},
            "Saturn":  {"sign": "Aries",  "sign_index": 0, "whole_sign_house": 10},
            "Rahu":    {"sign": "Pisces", "sign_index": 11, "whole_sign_house": 9},
            "Ketu":    {"sign": "Virgo",  "sign_index": 5, "whole_sign_house": 3},
        },
        "vimshottari": {"periods": periods or []},
    }


def test_relationship_question_reads_seventh_house_and_venus():
    result = answer_question("Will I get married?", _derived())
    assert result["status"] == "TRADITIONAL_QA_UNVALIDATED"
    assert "relationships" in result["matched_topics"]
    assert result["answer_sections"]
    text = result["answer_sections"][0]["text"]
    assert "7th house" in text
    assert "Venus" in text
    assert result["disclaimer"]


def test_career_question_reads_tenth_house_and_saturn():
    result = answer_question("What about my career?", _derived())
    assert "career" in result["matched_topics"]
    section = result["answer_sections"][0]
    assert any(h["house"] == 10 for h in section["houses"])
    assert any(p["planet"] == "Saturn" for p in section["planets"])


def test_present_question_includes_current_mahadasha():
    now = datetime(2026, 6, 1, tzinfo=timezone.utc)
    periods = [
        {"lord": "Venus",   "duration_years": 20,
         "start_utc": "2010-01-01T00:00:00+00:00", "end_utc": "2030-01-01T00:00:00+00:00"},
        {"lord": "Sun",     "duration_years": 6,
         "start_utc": "2030-01-01T00:00:00+00:00", "end_utc": "2036-01-01T00:00:00+00:00"},
    ]
    result = answer_question("What is happening now?", _derived(periods), now_utc=now)
    assert result["timeline"]["current"]["lord"] == "Venus"
    assert result["timeline"]["past"] == []
    assert result["timeline"]["future"] == []


def test_past_question_does_not_return_future_periods():
    now = datetime(2026, 6, 1, tzinfo=timezone.utc)
    birth = datetime(1968, 7, 6, 1, 50, tzinfo=timezone.utc)
    periods = [
        {"lord": "Jupiter", "duration_years": 16,
         "start_utc": "1963-06-11T00:00:00+00:00", "end_utc": "1979-06-11T00:00:00+00:00"},
        {"lord": "Saturn",  "duration_years": 19,
         "start_utc": "1979-06-11T00:00:00+00:00", "end_utc": "1998-06-11T00:00:00+00:00"},
        {"lord": "Venus",   "duration_years": 20,
         "start_utc": "2022-06-11T00:00:00+00:00", "end_utc": "2042-06-11T00:00:00+00:00"},
        {"lord": "Sun",     "duration_years": 6,
         "start_utc": "2042-06-11T00:00:00+00:00", "end_utc": "2048-06-11T00:00:00+00:00"},
    ]
    result = answer_question(
        "What does the chart say about my past?",
        _derived(periods),
        now_utc=now,
        birth_utc=birth,
    )
    assert result["timeline"]["past"]
    assert result["timeline"]["future"] == []
    assert result["timeline"]["current"]["lord"] == "Venus"


def test_past_question_clamps_first_period_to_birth():
    now = datetime(2026, 6, 1, tzinfo=timezone.utc)
    birth = datetime(1968, 7, 6, 1, 50, tzinfo=timezone.utc)
    periods = [
        {"lord": "Jupiter", "duration_years": 16,
         "start_utc": "1963-06-11T00:00:00+00:00", "end_utc": "1979-06-11T00:00:00+00:00"},
        {"lord": "Saturn",  "duration_years": 19,
         "start_utc": "1979-06-11T00:00

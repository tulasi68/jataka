from jataka.report_engine import build_personal_report


def test_report_is_reflective_and_has_all_requested_topics() -> None:
    derived = {
        "ascendant": {"sign": "Cancer", "whole_sign_house": 1},
        "planets": {
            "Sun": {"sign": "Gemini", "whole_sign_house": 12},
            "Moon": {"sign": "Libra", "whole_sign_house": 4},
            "Mercury": {"sign": "Gemini", "whole_sign_house": 12},
            "Venus": {"sign": "Gemini", "whole_sign_house": 12},
            "Mars": {"sign": "Gemini", "whole_sign_house": 12},
            "Jupiter": {"sign": "Leo", "whole_sign_house": 2},
            "Saturn": {"sign": "Aries", "whole_sign_house": 10},
            "Rahu": {"sign": "Pisces", "whole_sign_house": 9},
            "Ketu": {"sign": "Virgo", "whole_sign_house": 3},
        },
    }
    report = build_personal_report(derived)
    assert report["status"] == "INTERPRETIVE_REFLECTION_NOT_PREDICTION"
    titles = {section["title"] for section in report["sections"]}
    assert {"Self-understanding", "Work and contribution", "Relationships and cooperation",
            "Strengths, challenges, and reflection"} <= titles
    assert "not a scientific" in report["disclaimer"]
    work = next(s for s in report["sections"] if s["title"] == "Work and contribution")
    assert "Saturn" in work["summary"]

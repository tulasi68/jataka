from fastapi.testclient import TestClient

from jataka.api import app

client = TestClient(app)


def test_home_serves_interactive_chart_app() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Jataka" in response.text
    assert "South Indian Rāśi chart" in response.text


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_status_marks_calculations_enabled_but_unvalidated() -> None:
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["chart_display"] is True
    assert response.json()["calculations_enabled"] is True
    assert response.json()["calculation_status"] == "unvalidated"
    assert response.json()["input_storage"] is False


# Engine smoke checks are kept beside the API checks until the suite is reorganized.
from datetime import datetime, timezone
import pytest
from jataka.parashari_engine import BirthData, CalculationSettings, calculate_chart

def test_swiss_ephemeris_returns_positions():
    birth = BirthData(datetime(2000, 1, 1, 12, tzinfo=timezone.utc), 13.0827, 80.2707)
    result = calculate_chart(birth, CalculationSettings(sidereal_mode='lahiri', house_system='W'))
    assert result['status'] == 'calculated_unvalidated'
    assert len(result['house_cusps']) == 12
    assert set(result['planets']) == {'Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu'}

def test_engine_requires_explicit_sidereal_mode():
    with pytest.raises(ValueError, match='sidereal_mode'):
        CalculationSettings(sidereal_mode='', house_system='W')


def test_calculate_endpoint_returns_unvalidated_lahiri_positions():
    response = client.post("/api/calculate", json={"birth_date":"2000-01-01","birth_time":"12:00","time_zone":"Asia/Kolkata","latitude":13.0827,"longitude":80.2707})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "calculated_unvalidated"
    assert result["settings"]["sidereal_mode"] == "lahiri"
    assert result["settings"]["house_system"] == "W"
    assert result["calculation_status"].startswith("UNVALIDATED")
    assert "Sun" in result["planets"] and "birth_time_utc" in result
    assert result["derived_factors"]["status"] == "DERIVED_UNVALIDATED"
    assert result["derived_factors"]["ascendant"]["sign"] in {"Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"}
    assert len(result["derived_factors"]["vimshottari"]["periods"]) == 9
    assert result["personal_report"]["status"] == "INTERPRETIVE_REFLECTION_NOT_PREDICTION"
    assert result["ashtakavarga"]["sarvashtakavarga"]["total"] == 337
    assert len(result["transit_analysis"]["transits"]) == 7
    assert result["verification"]["status"] == "INCOMPLETE_SOURCE_INDEPENDENCE_NOT_ESTABLISHED"
    assert result["verification"]["ready_to_label_verified"] is False
    assert "arudha_padas" in result["derived_factors"]["jaimini"]

def test_calculate_endpoint_rejects_invalid_timezone():
    response = client.post("/api/calculate", json={"birth_date":"2000-01-01","birth_time":"12:00","time_zone":"Not/A_Real_Zone","latitude":13.0827,"longitude":80.2707})
    assert response.status_code == 422

def test_calculate_endpoint_rejects_invalid_clock_time():
    response = client.post("/api/calculate", json={"birth_date":"2000-01-01","birth_time":"25:99","time_zone":"Asia/Kolkata","latitude":13.0827,"longitude":80.2707})
    assert response.status_code == 422

def test_calculate_endpoint_does_not_guess_ambiguous_dst_time():
    response = client.post("/api/calculate", json={"birth_date":"2024-11-03","birth_time":"01:30","time_zone":"America/New_York","latitude":40.7128,"longitude":-74.0060})
    assert response.status_code == 422


def test_calculate_endpoint_requires_configured_engine_token(monkeypatch):
    monkeypatch.setenv("JATAKA_ENGINE_TOKEN", "test-secret")
    payload = {"birth_date":"2000-01-01","birth_time":"12:00","time_zone":"Asia/Kolkata","latitude":13.0827,"longitude":80.2707}
    denied = client.post("/api/calculate", json=payload)
    assert denied.status_code == 401
    accepted = client.post("/api/calculate", json=payload, headers={"X-Jataka-Engine-Token":"test-secret"})
    assert accepted.status_code == 200



def test_calculate_endpoint_optional_numerology_and_palmistry():
    payload = {
        "birth_date": "2000-01-01",
        "birth_time": "12:00",
        "time_zone": "Asia/Kolkata",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "full_name": "Ada Lovelace",
        "palmistry_hand": "both",
        "palmistry_observations": {
            "heart_line": "curved",
            "head_line": "straight",
            "life_line": "wide_arc",
            "fate_line": "uncertain",
        },
    }
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["numerology"]["status"] == "NUMEROLOGY_COMPUTED_UNVALIDATED"
    assert result["palmistry"]["status"] == "PALMISTRY_REFLECTION_USER_RECORDED"
    assert result["palmistry"]["hand"] == "both"

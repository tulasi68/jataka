from fastapi.testclient import TestClient

from jataka.api import app

client = TestClient(app)


def test_home_serves_interactive_no_chart_app() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Jataka" in response.text
    assert "No horoscope chart is shown" in response.text


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_status_is_clear_that_calculations_are_disabled() -> None:
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["chart_display"] is False
    assert response.json()["calculations_enabled"] is False
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

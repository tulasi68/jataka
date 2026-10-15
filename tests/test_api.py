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

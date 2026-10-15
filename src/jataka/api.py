"""FastAPI entry point for the Jataka interactive prototype."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from jataka import __version__

INDEX_FILE = Path(__file__).resolve().parent / "static" / "index.html"

app = FastAPI(
    title="Jataka — South Indian Astro Engine",
    version=__version__,
    description=(
        "Conversation-first prototype. It validates user-entered birth details "
        "but does not calculate or interpret a horoscope yet."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple deployment health check."""
    return {"status": "ok", "service": "jataka", "version": __version__}


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    """Serve the interactive, no-chart prototype."""
    return FileResponse(INDEX_FILE, media_type="text/html")


@app.get("/api/status")
def status() -> dict[str, object]:
    """Describe current capability honestly for clients and smoke tests."""
    return {
        "application": "Jataka",
        "version": __version__,
        "guided_input_prototype": True,
        "chart_display": False,
        "calculations_enabled": False,
        "input_storage": False,
        "message": (
            "Guided input validation is available in the browser. "
            "No horoscope calculation or interpretation has been performed."
        ),
    }

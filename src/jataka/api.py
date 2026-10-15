"""FastAPI entry point for the Jataka scaffold."""

from fastapi import FastAPI

from jataka import __version__

app = FastAPI(
    title="Jataka — South Indian Astro Engine",
    version=__version__,
    description=(
        "Phase 1 scaffold. Calculation endpoints are not enabled until "
        "conventions and reference-chart validation are complete."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    """Simple deployment health check."""
    return {"status": "ok", "service": "jataka", "version": __version__}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Jataka",
        "status": "scaffold",
        "message": "Chart calculations are not yet implemented or validated.",
        "documentation": "/docs",
    }

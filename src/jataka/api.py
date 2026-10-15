"""FastAPI entry point and calculation API for Jataka."""
from datetime import date, datetime, time
import os
import secrets
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from jataka import __version__
from jataka.birth_time import BirthTimeError, local_birth_time_to_utc
from jataka.parashari_engine import BirthData, CalculationSettings, CalculationError, calculate_chart
from jataka.derived_engine import derive_chart_factors
from jataka.report_engine import build_personal_report
from jataka.jaimini_engine import JaiminiSettings, calculate_jaimini_factors
from jataka.numerology_engine import calculate_numerology
from jataka.palmistry_engine import build_palmistry_reflection
from jataka.verification import PassEvidence, verify_three_passes

INDEX_FILE = Path(__file__).resolve().parent / "static" / "index.html"
app = FastAPI(
    title="Jataka — South Indian Astro Engine",
    version=__version__,
    description=(
        "Guided birth-detail review and an early, explicitly unvalidated numerical "
        "calculation endpoint. No horoscope chart or interpretation is produced."
    ),
)


class CalculationRequest(BaseModel):
    birth_date: date
    birth_time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")
    time_zone: str = Field(min_length=1, max_length=100)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    sidereal_mode: Literal["lahiri"] = "lahiri"
    house_system: Literal["W"] = "W"
    full_name: str | None = Field(default=None, max_length=200)
    palmistry_hand: Literal["dominant", "non_dominant", "both"] = "dominant"
    palmistry_observations: dict[str, str] | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "jataka", "version": __version__}


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(INDEX_FILE, media_type="text/html")


@app.get("/api/status")
def status() -> dict[str, object]:
    return {
        "application": "Jataka",
        "version": __version__,
        "guided_input_prototype": True,
        "chart_display": True,
        "calculations_enabled": True,
        "calculation_status": "unvalidated",
        "input_storage": False,
        "engine_authentication_enabled": bool(os.getenv("JATAKA_ENGINE_TOKEN")),
        "derived_factors": ["signs", "whole-sign houses", "nakshatra/pada", "Navamsa D9", "Vimshottari Mahadasha sequence", "Jaimini Chara Karakas", "Arudha Padas"],
        "verification_passes": ["Parashari/Swiss Ephemeris", "Jaimini factors", "Ashtakavarga/Gochara (not yet implemented)"],
        "optional_modules": ["Pythagorean and Chaldean numerology", "user-recorded palmistry reflection"],
        "message": (
            "Numerical and derived outputs are unvalidated and must not be treated "
            "as an independently verified horoscope."
        ),
    }


@app.post("/api/calculate")
def calculate(
    request: CalculationRequest,
    x_jataka_engine_token: str | None = Header(default=None),
) -> dict[str, object]:
    """Calculate raw positions only after receiving complete, explicit birth inputs."""
    expected_token = os.getenv("JATAKA_ENGINE_TOKEN")
    if expected_token and not secrets.compare_digest(x_jataka_engine_token or "", expected_token):
        raise HTTPException(status_code=401, detail="Invalid or missing calculation-service token.")

    try:
        ZoneInfo(request.time_zone)
        local_moment = datetime.combine(request.birth_date, time.fromisoformat(request.birth_time))
        utc_moment = local_birth_time_to_utc(local_moment, request.time_zone)
        birth = BirthData(
            birth_time_utc=utc_moment,
            latitude=request.latitude,
            longitude=request.longitude,
        )
        result = calculate_chart(
            birth,
            CalculationSettings(
                sidereal_mode=request.sidereal_mode,
                house_system=request.house_system,
            ),
        )
        result["derived_factors"] = derive_chart_factors(
            result["planets"], result["ascendant_longitude"], utc_moment
        )
        result["derived_factors"]["jaimini"] = calculate_jaimini_factors(
            {name: float(item["longitude"]) for name, item in result["planets"].items()},
            JaiminiSettings(chara_karaka_count=7, include_rahu=False),
        )
        result["personal_report"] = build_personal_report(result["derived_factors"])
        result["verification"] = verify_three_passes([
            PassEvidence(
                pass_name="parashari", source_id="swiss-ephemeris",
                status="calculated_unvalidated", findings={
                    "astronomical_positions": "computed",
                    "sign_and_house_derivation": "computed",
                }, reference_validated=False,
            )
        ])
        if request.full_name and request.full_name.strip():
            result["numerology"] = calculate_numerology(request.full_name, request.birth_date)
        if request.palmistry_observations is not None:
            result["palmistry"] = build_palmistry_reflection(
                request.palmistry_observations, request.palmistry_hand
            )
    except (ZoneInfoNotFoundError, ValueError, BirthTimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except CalculationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    result["input_confirmation"] = "client_confirmed"
    result["birth_details"] = {
        "birth_date": request.birth_date.isoformat(),
        "birth_time_local": request.birth_time,
        "time_zone": request.time_zone,
    }
    result["calculation_status"] = "UNVALIDATED — compare with independently sourced reference charts"
    result["warnings"] = list(result["warnings"]) + [
        "House system W (whole-sign) is explicitly selected for this initial pass.",
        "Derived sign, house, Nakshatra/pada, Navamsa, Vimshottari, and Chara Karaka outputs inherit the unvalidated source longitudes.",
        "Input details are processed for this request and are not persisted by this API.",
    ]
    return result

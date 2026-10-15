"""User-recorded palmistry observations and tradition-based reflection prompts.

This module intentionally does not claim to diagnose palm lines from photos or
predict life events. The user selects observations themselves; no palm image is
uploaded or retained by this endpoint.
"""
from __future__ import annotations

from typing import Mapping

LINE_OPTIONS = {
    "heart_line": {"clear": "A clear heart line", "curved": "A curved heart line",
                   "straight": "A relatively straight heart line", "uncertain": "Not sure"},
    "head_line": {"clear": "A clear head line", "straight": "A relatively straight head line",
                  "sloping": "A sloping head line", "uncertain": "Not sure"},
    "life_line": {"clear": "A clear life line", "wide_arc": "A broad arc",
                  "close_arc": "A line close to the thumb", "uncertain": "Not sure"},
    "fate_line": {"present": "A visible vertical/fate line", "faint": "A faint line",
                  "absent": "No obvious line", "uncertain": "Not sure"},
}
PROMPTS = {
    "heart_line": "In palmistry folklore, this line is associated with emotional expression and closeness. It cannot establish compatibility or predict relationships.",
    "head_line": "In palmistry folklore, this line is associated with thinking and learning style. It cannot measure intelligence or diagnose cognition.",
    "life_line": "In palmistry folklore, this line is associated with vitality or life changes. Its length or shape does not determine lifespan or health.",
    "fate_line": "In palmistry folklore, this line is associated with work and direction. Its presence or absence does not determine career outcomes.",
}


def build_palmistry_reflection(observations: Mapping[str, str], hand: str = "dominant") -> dict[str, object]:
    """Return user-entered palm observations and safe, non-predictive prompts."""
    if hand not in ("dominant", "non_dominant", "both"):
        raise ValueError("hand must be dominant, non_dominant, or both")
    accepted = {}
    for line, allowed in LINE_OPTIONS.items():
        value = observations.get(line, "uncertain")
        if value not in allowed:
            raise ValueError(f"Unsupported observation for {line}")
        accepted[line] = {
            "observation_code": value,
            "observation": allowed[value],
            "traditional_association": PROMPTS[line],
        }
    return {
        "status": "PALMISTRY_REFLECTION_USER_RECORDED",
        "hand": hand,
        "observations": accepted,
        "disclaimer": (
            "This is a description of observations selected by the user and folklore-based "
            "reflection prompts, not a palm-reading diagnosis. No image was analysed. Palmistry "
            "has no reliable scientific basis for predicting health, lifespan, relationships, "
            "or career outcomes. Do not use it for medical, financial, or other high-stakes decisions."
        ),
    }

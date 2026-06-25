"""Liquid XRF element-content validation: equipment/sample validity first, then spec check."""
from __future__ import annotations

from typing import Optional

from .schemas import ProcessLimits, QualityFlag

INVALID_SAMPLE_STATES = {"BUBBLE_DETECTED", "SEDIMENT_DETECTED", "LEAK_DETECTED", "INSUFFICIENT_SAMPLE"}


def evaluate_xrf(
    result_available: bool,
    calibration_status: str,
    sample_status: str,
    elements: dict,
    limits: ProcessLimits = ProcessLimits(),
) -> QualityFlag:
    if not result_available:
        return "WAIT"
    if calibration_status != "OK":
        return "INVALID"
    if sample_status != "OK" or sample_status in INVALID_SAMPLE_STATES:
        return "INVALID"
    for name, value in elements.items():
        limit = limits.xrf_element_limits.get(name)
        if limit is not None and value > limit:
            return "FAIL"
    return "PASS"

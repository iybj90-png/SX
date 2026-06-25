"""Final PASS/HOLD/FAIL decision and next-process transfer permission.

Kept as a deterministic rule-based state machine per the design doc:
AI/ML models may suggest probabilities, but final interlock decisions stay rule-based.
"""
from __future__ import annotations

from .schemas import QualityFlag, QualityResult


def determine_quality(ph_flag: QualityFlag, xrf_flag: QualityFlag, uvvis_flag: QualityFlag) -> QualityResult:
    flags = [ph_flag, xrf_flag, uvvis_flag]

    if all(flag == "PASS" for flag in flags):
        return QualityResult(ph_flag, xrf_flag, uvvis_flag, "PASS", "ENABLE")

    if "FAIL" in flags:
        return QualityResult(ph_flag, xrf_flag, uvvis_flag, "FAIL", "DISABLE")

    return QualityResult(ph_flag, xrf_flag, uvvis_flag, "HOLD", "DISABLE")

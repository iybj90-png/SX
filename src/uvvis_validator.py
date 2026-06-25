"""UV-Vis absorbance/color validation: equipment validity first, then absorbance spec check."""
from __future__ import annotations

from .schemas import ProcessLimits, QualityFlag


def evaluate_uvvis(
    result_available: bool,
    wavelength_nm: float,
    absorbance: float,
    baseline_status: str,
    cell_status: str,
    bubble_check: str,
    limits: ProcessLimits = ProcessLimits(),
) -> QualityFlag:
    if not result_available:
        return "WAIT"
    if wavelength_nm not in limits.uvvis_allowed_wavelengths:
        return "INVALID"
    if baseline_status != "OK":
        return "INVALID"
    if cell_status != "CLEAN":
        return "INVALID"
    if bubble_check != "OK":
        return "INVALID"
    if absorbance < limits.uvvis_absorbance_min:
        return "INVALID"
    if absorbance >= limits.uvvis_absorbance_max:
        return "INVALID"  # saturation region
    if absorbance > limits.uvvis_absorbance_max * 0.8:
        return "FAIL"
    return "PASS"

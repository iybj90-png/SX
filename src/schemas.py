"""Shared type definitions for the pH/XRF/UV-Vis control & quality pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

QualityFlag = Literal["PASS", "HOLD", "FAIL", "INVALID", "WAIT"]
QualityStatus = Literal["PASS", "HOLD", "FAIL"]
TransferStatus = Literal["ENABLE", "DISABLE"]
PIDMode = Literal["AUTO", "MANUAL", "STOP"]
PumpCmd = Literal["ON", "OFF"]


@dataclass
class PIDState:
    """Carries integral/derivative state across PID_Calculation_Cycle ticks."""

    integral: float = 0.0
    prev_error: float = 0.0
    prev_output: float = 0.0


@dataclass
class PIDGainSchedule:
    """One (error-band -> gain) entry for Gain Scheduling PID."""

    max_abs_error: float
    kp: float
    ki: float
    kd: float


@dataclass
class ProcessLimits:
    ph_sp: float = 7.0
    ph_deadband: float = 0.05
    ph_normal_low: float = 6.8
    ph_normal_high: float = 7.2
    ph_limit_low: float = 6.5
    ph_limit_high: float = 8.5
    output_min: float = 0.0
    output_max: float = 100.0
    normal_output_min: float = 10.0
    normal_output_max: float = 90.0
    max_output_rate_per_cycle: float = 4.0
    xrf_element_limits: dict = field(
        default_factory=lambda: {"Fe": 150.0, "Cu": 20.0, "Ni": 50.0, "Co": 10.0, "Mn": 30.0}
    )
    uvvis_allowed_wavelengths: tuple = (520,)
    uvvis_absorbance_max: float = 1.5
    uvvis_absorbance_min: float = 0.0


@dataclass
class ControlOutput:
    PID_Output: float
    Flow_CMD_Final: float
    Pump_CMD: PumpCmd
    Valve_CMD: str
    PID_Mode: PIDMode


@dataclass
class QualityResult:
    pH_Flag: QualityFlag
    XRF_Flag: QualityFlag
    UVVIS_Flag: QualityFlag
    Quality_Status: QualityStatus
    Transfer_To_Next_Process: TransferStatus

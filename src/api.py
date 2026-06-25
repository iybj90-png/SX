"""FastAPI judgment endpoint: one process cycle in, control+quality decision out."""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .pid_controller import run_control
from .quality_state_machine import determine_quality
from .schemas import PIDState
from .uvvis_validator import evaluate_uvvis
from .xrf_validator import evaluate_xrf

app = FastAPI(title="pH/XRF/UV-Vis Quality Judgment API")


class CycleRequest(BaseModel):
    ph_pv: float
    ph_sp: float = 7.0
    auto_mode: bool = True
    emergency_stop: bool = False
    pump_status: str = "RUN"
    chemical_tank_level: str = "NORMAL"

    xrf_result_available: bool = True
    xrf_calibration_status: str = "OK"
    xrf_sample_status: str = "OK"
    elements: dict[str, float] = {}

    uvvis_result_available: bool = True
    wavelength_nm: float = 520
    absorbance: float = 0.0
    uvvis_baseline_status: str = "OK"
    uvvis_cell_status: str = "CLEAN"
    uvvis_bubble_check: str = "OK"


class CycleResponse(BaseModel):
    PID_Output: float
    Flow_CMD_Final: float
    Pump_CMD: str
    Valve_CMD: str
    PID_Mode: str
    pH_Flag: str
    XRF_Flag: str
    UVVIS_Flag: str
    Quality_Status: str
    Transfer_To_Next_Process: str


@app.post("/quality-check", response_model=CycleResponse)
def quality_check(req: CycleRequest) -> CycleResponse:
    control = run_control(
        ph_pv=req.ph_pv,
        ph_sp=req.ph_sp,
        state=PIDState(),
        auto_mode=req.auto_mode,
        emergency_stop=req.emergency_stop,
        pump_status=req.pump_status,
        chemical_tank_level=req.chemical_tank_level,
    )

    ph_flag = "PASS" if not req.emergency_stop and control.PID_Mode == "AUTO" else "HOLD"

    xrf_flag = evaluate_xrf(
        result_available=req.xrf_result_available,
        calibration_status=req.xrf_calibration_status,
        sample_status=req.xrf_sample_status,
        elements=req.elements,
    )

    uvvis_flag = evaluate_uvvis(
        result_available=req.uvvis_result_available,
        wavelength_nm=req.wavelength_nm,
        absorbance=req.absorbance,
        baseline_status=req.uvvis_baseline_status,
        cell_status=req.uvvis_cell_status,
        bubble_check=req.uvvis_bubble_check,
    )

    quality = determine_quality(ph_flag, xrf_flag, uvvis_flag)

    return CycleResponse(
        PID_Output=control.PID_Output,
        Flow_CMD_Final=control.Flow_CMD_Final,
        Pump_CMD=control.Pump_CMD,
        Valve_CMD=control.Valve_CMD,
        PID_Mode=control.PID_Mode,
        pH_Flag=quality.pH_Flag,
        XRF_Flag=quality.XRF_Flag,
        UVVIS_Flag=quality.UVVIS_Flag,
        Quality_Status=quality.Quality_Status,
        Transfer_To_Next_Process=quality.Transfer_To_Next_Process,
    )

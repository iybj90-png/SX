"""Demo entry point: run one control+quality cycle from example process data."""
from datetime import datetime, timezone

from src.data_logger import BatchRecord, record_to_json
from src.pid_controller import run_control
from src.quality_state_machine import determine_quality
from src.schemas import PIDState
from src.uvvis_validator import evaluate_uvvis
from src.xrf_validator import evaluate_xrf


def run_one_cycle():
    state = PIDState()
    control = run_control(ph_pv=7.02, ph_sp=7.00, state=state)

    xrf_flag = evaluate_xrf(
        result_available=True,
        calibration_status="OK",
        sample_status="OK",
        elements={"Fe": 120, "Cu": 8, "Ni": 35},
    )
    uvvis_flag = evaluate_uvvis(
        result_available=True,
        wavelength_nm=520,
        absorbance=0.82,
        baseline_status="OK",
        cell_status="CLEAN",
        bubble_check="OK",
    )
    quality = determine_quality("PASS", xrf_flag, uvvis_flag)

    record = BatchRecord(
        Timestamp=datetime.now(timezone.utc).isoformat(),
        Batch_ID="B20260625-001",
        pH_PV=7.02,
        pH_SP=7.00,
        Flow_CMD_Final=control.Flow_CMD_Final,
        Flow_FB=43,
        XRF_Result=xrf_flag,
        UVVIS_Result=uvvis_flag,
        Quality_Status=quality.Quality_Status,
        Operator_ID="auto",
    )
    print(record_to_json(record))
    return control, quality


if __name__ == "__main__":
    run_one_cycle()

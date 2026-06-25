from src.pid_controller import run_control
from src.quality_state_machine import determine_quality
from src.schemas import PIDState


def test_emergency_stop():
    state = PIDState()
    result = run_control(ph_pv=7.00, ph_sp=7.00, state=state, emergency_stop=True, pump_status="RUN")
    assert result.PID_Mode == "STOP"
    assert result.Pump_CMD == "OFF"
    assert result.Flow_CMD_Final == 0

    quality = determine_quality("HOLD", "WAIT", "WAIT")
    assert quality.Transfer_To_Next_Process == "DISABLE"


def test_pump_fault_forces_stop():
    state = PIDState()
    result = run_control(ph_pv=7.00, ph_sp=7.00, state=state, pump_status="FAULT")
    assert result.PID_Mode == "STOP"
    assert result.Pump_CMD == "OFF"


def test_chemical_tank_empty_forces_manual():
    state = PIDState()
    result = run_control(ph_pv=7.00, ph_sp=7.00, state=state, chemical_tank_level="EMPTY")
    assert result.Pump_CMD == "OFF"
    assert result.Flow_CMD_Final == 0

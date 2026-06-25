from src.pid_controller import run_control
from src.schemas import PIDState


def test_normal_operation_stays_in_auto():
    state = PIDState()
    result = run_control(ph_pv=7.02, ph_sp=7.00, state=state)
    assert result.PID_Mode == "AUTO"
    assert 0.0 <= result.PID_Output <= 100.0


def test_deadband_suppresses_small_error():
    state = PIDState()
    result = run_control(ph_pv=7.02, ph_sp=7.00, state=state, feedforward=0.0)
    assert state.prev_error == 0.0


def test_output_never_exceeds_limits():
    state = PIDState()
    result = run_control(ph_pv=0.0, ph_sp=14.0, state=state)
    assert 0.0 <= result.PID_Output <= 100.0

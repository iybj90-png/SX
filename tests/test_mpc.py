from src.mpc_controller import FOPDTModel, run_mpc
from src.schemas import ProcessLimits


def test_mpc_output_within_limits():
    limits = ProcessLimits()
    flow = run_mpc(ph_pv=6.5, ph_sp=7.0, flow_history=[30.0, 30.0], limits=limits)
    assert limits.output_min <= flow <= limits.output_max


def test_mpc_increases_flow_when_ph_below_setpoint():
    flow_low_ph = run_mpc(ph_pv=6.5, ph_sp=7.0, flow_history=[30.0, 30.0], model=FOPDTModel())
    flow_at_setpoint = run_mpc(ph_pv=7.0, ph_sp=7.0, flow_history=[30.0, 30.0], model=FOPDTModel())
    assert flow_low_ph > flow_at_setpoint

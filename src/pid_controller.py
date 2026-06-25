"""pH-based PID flow control: Gain Scheduling + Deadband + Feedforward + interlocks."""
from __future__ import annotations

from .schemas import ControlOutput, PIDGainSchedule, PIDState, ProcessLimits

DEFAULT_GAIN_SCHEDULE = [
    PIDGainSchedule(max_abs_error=0.1, kp=8.0, ki=0.5, kd=0.0),
    PIDGainSchedule(max_abs_error=0.5, kp=15.0, ki=1.0, kd=0.5),
    PIDGainSchedule(max_abs_error=float("inf"), kp=25.0, ki=1.5, kd=1.0),
]


def select_gains(error: float, schedule=DEFAULT_GAIN_SCHEDULE) -> PIDGainSchedule:
    abs_error = abs(error)
    for band in schedule:
        if abs_error <= band.max_abs_error:
            return band
    return schedule[-1]


def run_control(
    ph_pv: float,
    ph_sp: float,
    state: PIDState,
    limits: ProcessLimits = ProcessLimits(),
    cycle_seconds: float = 1.0,
    feedforward: float = 0.0,
    auto_mode: bool = True,
    emergency_stop: bool = False,
    pump_status: str = "RUN",
    chemical_tank_level: str = "NORMAL",
) -> ControlOutput:
    """Compute one PID control step. Interlocks force STOP/OFF/0 regardless of error."""

    if emergency_stop or pump_status == "FAULT" or chemical_tank_level == "EMPTY" or not auto_mode:
        return ControlOutput(
            PID_Output=0.0,
            Flow_CMD_Final=0.0,
            Pump_CMD="OFF",
            Valve_CMD="CLOSE",
            PID_Mode="STOP" if (emergency_stop or pump_status == "FAULT") else "MANUAL",
        )

    error = ph_sp - ph_pv
    if abs(error) <= limits.ph_deadband:
        error = 0.0

    gains = select_gains(error)
    state.integral += error * cycle_seconds
    derivative = (error - state.prev_error) / cycle_seconds if cycle_seconds else 0.0

    raw_output = gains.kp * error + gains.ki * state.integral + gains.kd * derivative + feedforward

    clamped = max(limits.output_min, min(limits.output_max, raw_output))
    if clamped != raw_output:
        # anti-windup: undo the integral contribution that pushed us past the clamp
        state.integral -= error * cycle_seconds

    max_step = limits.max_output_rate_per_cycle
    output = max(state.prev_output - max_step, min(state.prev_output + max_step, clamped))
    output = max(limits.output_min, min(limits.output_max, output))

    state.prev_error = error
    state.prev_output = output

    pump_cmd = "ON" if output > 0 else "OFF"
    valve_cmd = "OPEN" if output > 0 else "CLOSE"

    return ControlOutput(
        PID_Output=round(output, 2),
        Flow_CMD_Final=round(output, 2),
        Pump_CMD=pump_cmd,
        Valve_CMD=valve_cmd,
        PID_Mode="AUTO",
    )

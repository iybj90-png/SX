"""Model Predictive Control for pH, per design doc section 7-2-②.

Uses a first-order-plus-dead-time (FOPDT) process model and minimizes
J = sum((pH_pred - pH_SP)^2) + lambda * sum(delta_flow^2) over a short
horizon. This is the advanced controller; pid_controller.run_control
(Gain Scheduling PID) remains the first-line controller until enough
operating data justifies switching.
"""
from __future__ import annotations

from dataclasses import dataclass

from scipy.optimize import minimize

from .schemas import ProcessLimits


@dataclass
class FOPDTModel:
    """First-order-plus-dead-time pH response to flow changes."""

    gain: float = 0.05  # pH change per % flow, per step
    time_constant_steps: int = 3
    dead_time_steps: int = 2


def _simulate(
    flow_sequence: list[float],
    ph0: float,
    model: FOPDTModel,
    flow_history: list[float],
) -> list[float]:
    history = flow_history + flow_sequence
    ph = ph0
    predictions = []
    alpha = 1.0 / model.time_constant_steps
    for i in range(len(flow_sequence)):
        idx = len(flow_history) + i - model.dead_time_steps
        delayed_flow = history[idx] if 0 <= idx < len(history) else (history[0] if history else 0.0)
        ph += alpha * (model.gain * delayed_flow - (ph - 7.0))
        predictions.append(ph)
    return predictions


def run_mpc(
    ph_pv: float,
    ph_sp: float,
    flow_history: list[float],
    model: FOPDTModel = FOPDTModel(),
    limits: ProcessLimits = ProcessLimits(),
    horizon: int = 5,
    move_penalty: float = 0.1,
) -> float:
    """Solve for the next flow command that minimizes predicted pH error + move size."""

    prev_flow = flow_history[-1] if flow_history else 0.0

    def cost(flow_sequence: list[float]) -> float:
        predictions = _simulate(list(flow_sequence), ph_pv, model, flow_history)
        tracking_error = sum((p - ph_sp) ** 2 for p in predictions)
        deltas = [flow_sequence[0] - prev_flow] + [
            flow_sequence[i] - flow_sequence[i - 1] for i in range(1, len(flow_sequence))
        ]
        move_cost = sum(d**2 for d in deltas)
        return tracking_error + move_penalty * move_cost

    x0 = [prev_flow] * horizon
    bounds = [(limits.output_min, limits.output_max)] * horizon

    result = minimize(cost, x0, bounds=bounds, method="L-BFGS-B")
    next_flow = result.x[0] if result.success else prev_flow
    return max(limits.output_min, min(limits.output_max, float(next_flow)))

"""Quality PASS-probability predictor: XGBoost over batch-level features.

Per the design doc this model is advisory only — it estimates PASS
probability and ranks influential variables, but the final PASS/HOLD/FAIL
decision stays in quality_state_machine.determine_quality.
"""
from __future__ import annotations

from typing import Sequence

try:
    from xgboost import XGBClassifier
except ImportError:  # pragma: no cover
    XGBClassifier = None

from .synthetic_data import FEATURE_NAMES


class QualityPredictor:
    def __init__(self, **xgb_params):
        self._model = None
        self._xgb_params = xgb_params or {"n_estimators": 50, "max_depth": 3, "eval_metric": "logloss"}

    def fit(self, x: Sequence[Sequence[float]], y: Sequence[int]) -> None:
        if XGBClassifier is None:
            return
        self._model = XGBClassifier(**self._xgb_params)
        self._model.fit(x, y)

    def predict_pass_probability(self, x: Sequence[Sequence[float]]) -> list[float]:
        if self._model is None:
            return [1.0] * len(x)
        return [float(p[1]) for p in self._model.predict_proba(x)]

    def feature_importance(self) -> dict[str, float]:
        if self._model is None:
            return {}
        importances = self._model.feature_importances_
        return dict(zip(FEATURE_NAMES, (float(v) for v in importances)))

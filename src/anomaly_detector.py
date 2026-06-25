"""Process anomaly detection: Isolation Forest over recent operating samples.

Optional dependency on scikit-learn; degrades to a no-op detector if unavailable
so the rule-based pipeline keeps working without it installed.
"""
from __future__ import annotations

from typing import Sequence

try:
    from sklearn.ensemble import IsolationForest
except ImportError:  # pragma: no cover
    IsolationForest = None


class ProcessAnomalyDetector:
    def __init__(self, contamination: float = 0.05, random_state: int = 0):
        self._model = None
        self._contamination = contamination
        self._random_state = random_state

    def fit(self, samples: Sequence[Sequence[float]]) -> None:
        if IsolationForest is None:
            return
        self._model = IsolationForest(contamination=self._contamination, random_state=self._random_state)
        self._model.fit(samples)

    def is_anomalous(self, sample: Sequence[float]) -> bool:
        if self._model is None:
            return False
        return bool(self._model.predict([sample])[0] == -1)

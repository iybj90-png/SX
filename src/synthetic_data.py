"""Synthetic batch data generator, used only until real operating history exists.

Mirrors the input/output schema in the design doc so downstream models
(quality_predictor, anomaly_detector) can be developed and tested before
real plant data is available.
"""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class SyntheticBatch:
    pH_PV: float
    Flow_CMD_Final: float
    Element_Fe: float
    Element_Cu: float
    Element_Ni: float
    Absorbance_Value: float
    Quality_Pass: int  # 1 = PASS, 0 = not PASS


def generate_batches(n: int, anomaly_rate: float = 0.15, seed: int = 0) -> list[SyntheticBatch]:
    rng = random.Random(seed)
    batches = []
    for _ in range(n):
        is_anomaly = rng.random() < anomaly_rate
        if is_anomaly:
            ph = rng.choice([rng.uniform(5.5, 6.4), rng.uniform(7.6, 8.5)])
            fe = rng.uniform(150, 250)
            cu = rng.uniform(20, 40)
            ni = rng.uniform(50, 80)
            absorbance = rng.uniform(1.2, 1.5)
        else:
            ph = rng.uniform(6.85, 7.15)
            fe = rng.uniform(80, 145)
            cu = rng.uniform(2, 18)
            ni = rng.uniform(15, 48)
            absorbance = rng.uniform(0.4, 1.1)

        flow = rng.uniform(20, 70)
        quality_pass = 0 if is_anomaly else 1
        batches.append(
            SyntheticBatch(
                pH_PV=round(ph, 3),
                Flow_CMD_Final=round(flow, 2),
                Element_Fe=round(fe, 1),
                Element_Cu=round(cu, 1),
                Element_Ni=round(ni, 1),
                Absorbance_Value=round(absorbance, 3),
                Quality_Pass=quality_pass,
            )
        )
    return batches


def to_feature_matrix(batches: list[SyntheticBatch]) -> tuple[list[list[float]], list[int]]:
    x = [[b.pH_PV, b.Flow_CMD_Final, b.Element_Fe, b.Element_Cu, b.Element_Ni, b.Absorbance_Value] for b in batches]
    y = [b.Quality_Pass for b in batches]
    return x, y


FEATURE_NAMES = ["pH_PV", "Flow_CMD_Final", "Element_Fe", "Element_Cu", "Element_Ni", "Absorbance_Value"]

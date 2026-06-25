"""Batch record logging: timestamp, batch id, measured values, and judgments."""
from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class BatchRecord:
    Timestamp: str
    Batch_ID: str
    pH_PV: float
    pH_SP: float
    Flow_CMD_Final: float
    Flow_FB: float
    XRF_Result: str
    UVVIS_Result: str
    Quality_Status: str
    Operator_ID: str


def append_record(record: BatchRecord, path: str) -> None:
    file_path = Path(path)
    is_new = not file_path.exists()
    row = asdict(record)
    with file_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def record_to_json(record: BatchRecord) -> str:
    return json.dumps(asdict(record), ensure_ascii=False)

"""SQLite storage for batch records (doc step 5: PostgreSQL/SQLite data persistence).

SQLite is used here as the lightweight default; swapping to PostgreSQL only
requires changing the connection string since all access goes through plain SQL.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import asdict

from .data_logger import BatchRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS batch_records (
    Timestamp TEXT NOT NULL,
    Batch_ID TEXT NOT NULL,
    pH_PV REAL,
    pH_SP REAL,
    Flow_CMD_Final REAL,
    Flow_FB REAL,
    XRF_Result TEXT,
    UVVIS_Result TEXT,
    Quality_Status TEXT,
    Operator_ID TEXT,
    PRIMARY KEY (Batch_ID, Timestamp)
)
"""


@contextmanager
def connect(db_path: str = "batch_records.db"):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_record(record: BatchRecord, db_path: str = "batch_records.db") -> None:
    row = asdict(record)
    with connect(db_path) as conn:
        conn.execute(
            f"INSERT INTO batch_records ({', '.join(row.keys())}) VALUES ({', '.join('?' * len(row))})",
            list(row.values()),
        )


def fetch_records(db_path: str = "batch_records.db", limit: int = 100) -> list[dict]:
    with connect(db_path) as conn:
        cursor = conn.execute("SELECT * FROM batch_records ORDER BY Timestamp DESC LIMIT ?", (limit,))
        columns = [c[0] for c in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

from src.data_logger import BatchRecord
from src.db import fetch_records, insert_record


def test_insert_and_fetch_record(tmp_path):
    db_path = str(tmp_path / "test_batches.db")
    record = BatchRecord(
        Timestamp="2026-06-25T00:00:00+00:00",
        Batch_ID="B-TEST-001",
        pH_PV=7.02,
        pH_SP=7.00,
        Flow_CMD_Final=45.0,
        Flow_FB=43.0,
        XRF_Result="PASS",
        UVVIS_Result="PASS",
        Quality_Status="PASS",
        Operator_ID="tester",
    )

    insert_record(record, db_path=db_path)
    rows = fetch_records(db_path=db_path)

    assert len(rows) == 1
    assert rows[0]["Batch_ID"] == "B-TEST-001"
    assert rows[0]["Quality_Status"] == "PASS"

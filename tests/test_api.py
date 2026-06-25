from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_normal_cycle_passes():
    response = client.post(
        "/quality-check",
        json={
            "ph_pv": 7.02,
            "ph_sp": 7.00,
            "elements": {"Fe": 120, "Cu": 8, "Ni": 35},
            "absorbance": 0.82,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["Quality_Status"] == "PASS"
    assert body["Transfer_To_Next_Process"] == "ENABLE"


def test_emergency_stop_disables_transfer():
    response = client.post(
        "/quality-check",
        json={"ph_pv": 7.00, "ph_sp": 7.00, "emergency_stop": True},
    )
    body = response.json()
    assert body["PID_Mode"] == "STOP"
    assert body["Transfer_To_Next_Process"] == "DISABLE"

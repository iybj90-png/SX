from src.quality_state_machine import determine_quality


def test_all_pass_yields_pass_and_transfer_enabled():
    result = determine_quality("PASS", "PASS", "PASS")
    assert result.Quality_Status == "PASS"
    assert result.Transfer_To_Next_Process == "ENABLE"


def test_ph_pass_xrf_fail_does_not_pass():
    result = determine_quality("PASS", "FAIL", "PASS")
    assert result.Quality_Status == "FAIL"
    assert result.Transfer_To_Next_Process == "DISABLE"


def test_ph_pass_uvvis_invalid_holds():
    result = determine_quality("PASS", "PASS", "INVALID")
    assert result.Quality_Status == "HOLD"
    assert result.Transfer_To_Next_Process == "DISABLE"


def test_xrf_sample_invalid_holds():
    result = determine_quality("PASS", "INVALID", "PASS")
    assert result.Quality_Status == "HOLD"
    assert result.Transfer_To_Next_Process == "DISABLE"


def test_uvvis_equipment_invalid_holds():
    result = determine_quality("PASS", "PASS", "INVALID")
    assert result.Quality_Status == "HOLD"
    assert result.Transfer_To_Next_Process == "DISABLE"

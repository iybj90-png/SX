from src.uvvis_validator import evaluate_uvvis


def test_normal_absorbance_pass():
    flag = evaluate_uvvis(True, 520, 0.82, "OK", "CLEAN", "OK")
    assert flag == "PASS"


def test_absorbance_over_threshold_fails():
    flag = evaluate_uvvis(True, 520, 1.4, "OK", "CLEAN", "OK")
    assert flag == "FAIL"


def test_contaminated_cell_is_invalid_not_pass():
    flag = evaluate_uvvis(True, 520, 0.30, "OK", "CONTAMINATED", "OK")
    assert flag == "INVALID"


def test_baseline_fail_is_invalid():
    flag = evaluate_uvvis(True, 520, 0.30, "FAIL", "CLEAN", "OK")
    assert flag == "INVALID"


def test_no_result_is_wait():
    flag = evaluate_uvvis(False, 520, 0.30, "OK", "CLEAN", "OK")
    assert flag == "WAIT"

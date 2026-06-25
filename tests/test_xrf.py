from src.xrf_validator import evaluate_xrf

NORMAL_ELEMENTS = {"Fe": 120, "Cu": 8, "Ni": 35}


def test_normal_elements_pass():
    flag = evaluate_xrf(True, "OK", "OK", NORMAL_ELEMENTS)
    assert flag == "PASS"


def test_element_over_limit_fails():
    flag = evaluate_xrf(True, "OK", "OK", {"Fe": 200, "Cu": 8, "Ni": 35})
    assert flag == "FAIL"


def test_bad_calibration_is_invalid_not_pass():
    flag = evaluate_xrf(True, "NG", "OK", NORMAL_ELEMENTS)
    assert flag == "INVALID"


def test_sample_bubble_is_invalid():
    flag = evaluate_xrf(True, "OK", "BUBBLE_DETECTED", NORMAL_ELEMENTS)
    assert flag == "INVALID"


def test_no_result_is_wait():
    flag = evaluate_xrf(False, "OK", "OK", NORMAL_ELEMENTS)
    assert flag == "WAIT"

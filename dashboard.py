"""Streamlit dashboard: manually run a process cycle and view the quality decision."""
import streamlit as st

from src.pid_controller import run_control
from src.quality_state_machine import determine_quality
from src.schemas import PIDState
from src.uvvis_validator import evaluate_uvvis
from src.xrf_validator import evaluate_xrf

st.title("pH / XRF / UV-Vis 공정제어 대시보드")

st.header("운전 상태")
col1, col2 = st.columns(2)
with col1:
    emergency_stop = st.checkbox("Emergency_Stop", value=False)
    pump_status = st.selectbox("Pump_Status", ["RUN", "STOP", "FAULT"])
with col2:
    auto_mode = st.checkbox("Auto_Mode", value=True)
    chemical_tank_level = st.selectbox("Chemical_Tank_Level", ["NORMAL", "LOW", "EMPTY"])

st.header("pH 입력")
ph_pv = st.number_input("pH_PV", min_value=0.0, max_value=14.0, value=7.02, step=0.01)
ph_sp = st.number_input("pH_SP", min_value=0.0, max_value=14.0, value=7.00, step=0.01)

st.header("XRF 입력")
xrf_result_available = st.checkbox("XRF_Result_Available", value=True)
xrf_calibration_status = st.selectbox("XRF_Calibration_Status", ["OK", "NG"])
xrf_sample_status = st.selectbox(
    "XRF_Sample_Status", ["OK", "BUBBLE_DETECTED", "SEDIMENT_DETECTED", "LEAK_DETECTED", "INSUFFICIENT_SAMPLE"]
)
fe = st.number_input("Element_Fe (mg/L)", value=120.0)
cu = st.number_input("Element_Cu (mg/L)", value=8.0)
ni = st.number_input("Element_Ni (mg/L)", value=35.0)

st.header("UV-Vis 입력")
uvvis_result_available = st.checkbox("UVVIS_Result_Available", value=True)
wavelength_nm = st.selectbox("Wavelength_nm", [520])
absorbance = st.number_input("Absorbance_Value", value=0.82, step=0.01)
uvvis_baseline_status = st.selectbox("UVVIS_Baseline_Status", ["OK", "FAIL"])
uvvis_cell_status = st.selectbox("UVVIS_Cell_Status", ["CLEAN", "CONTAMINATED"])
uvvis_bubble_check = st.selectbox("UVVIS_Bubble_Check", ["OK", "DETECTED"])

if st.button("판정 실행"):
    control = run_control(
        ph_pv=ph_pv,
        ph_sp=ph_sp,
        state=PIDState(),
        auto_mode=auto_mode,
        emergency_stop=emergency_stop,
        pump_status=pump_status,
        chemical_tank_level=chemical_tank_level,
    )
    ph_flag = "PASS" if not emergency_stop and control.PID_Mode == "AUTO" else "HOLD"

    xrf_flag = evaluate_xrf(
        result_available=xrf_result_available,
        calibration_status=xrf_calibration_status,
        sample_status=xrf_sample_status,
        elements={"Fe": fe, "Cu": cu, "Ni": ni},
    )
    uvvis_flag = evaluate_uvvis(
        result_available=uvvis_result_available,
        wavelength_nm=wavelength_nm,
        absorbance=absorbance,
        baseline_status=uvvis_baseline_status,
        cell_status=uvvis_cell_status,
        bubble_check=uvvis_bubble_check,
    )
    quality = determine_quality(ph_flag, xrf_flag, uvvis_flag)

    st.header("제어 출력")
    st.json(
        {
            "PID_Output": control.PID_Output,
            "Flow_CMD_Final": control.Flow_CMD_Final,
            "Pump_CMD": control.Pump_CMD,
            "Valve_CMD": control.Valve_CMD,
            "PID_Mode": control.PID_Mode,
        }
    )

    st.header("품질 판정")
    badge = {"PASS": "✅", "HOLD": "⏸️", "FAIL": "❌"}[quality.Quality_Status]
    st.markdown(f"### {badge} Quality_Status: {quality.Quality_Status}")
    st.json(
        {
            "pH_Flag": quality.pH_Flag,
            "XRF_Flag": quality.XRF_Flag,
            "UVVIS_Flag": quality.UVVIS_Flag,
            "Quality_Status": quality.Quality_Status,
            "Transfer_To_Next_Process": quality.Transfer_To_Next_Process,
        }
    )

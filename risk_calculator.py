import streamlit as st
import numpy as np
import datetime
import os
import csv
import pandas as pd
import uuid

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Lung Cancer Risk Calculator",
    page_icon="🫁",
    layout="centered"
)

# ------------------- GLOBAL STYLING -------------------
st.markdown("""
<style>
.main { background-color: #f4f8fc; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
.section { margin-bottom: 10px; }
.result-card {
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.06);
    margin-bottom: 15px;
    text-align: center;
}
.stButton>button {
    background-color: #0057b8;
    color: white;
    font-weight: 600;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    border: none;
    transition: 0.2s ease;
}
.stButton>button:hover { background-color: #4da3ff; color: white; }
.footer { text-align: center; font-size: 13px; color: #6c757d; margin-top: 30px; }
</style>
""", unsafe_allow_html=True)

st.title("🫁 Lung Cancer Risk Calculator")
st.write("PLCOm2012 6-Year Risk Assessment")

# ------------------- SESSION-BASED USER ID -------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# ------------------- USAGE LOGGING -------------------
log_file = "usage_log.csv"

def log_usage(user_id, age, race, smoking_status, risk_percent, uspstf_eligible):
    fieldnames = ["timestamp", "user_id", "age", "race", "smoking_status", "risk_percent", "uspstf_eligible"]
    row = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": user_id,
        "age": age,
        "race": race,
        "smoking_status": smoking_status,
        "risk_percent": f"{risk_percent:.2f}",
        "uspstf_eligible": uspstf_eligible
    }
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# ------------------- PLCO FUNCTION -------------------
def logistic(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def plco_m2012(age, race, education, bmi, copd, cancer_hist, family_hist,
               smoking_status, smoking_intensity, duration_smoking, smoking_quit_time):
    race = race.lower()
    model = (
        0.0778868 * (age - 62)
        - 0.0812744 * (education - 4)
        - 0.0274194 * (bmi - 27)
        + 0.3553063 * copd
        + 0.4589971 * cancer_hist
        + 0.587185 * family_hist
        + 0.2597431 * smoking_status
        + 0.0317321 * (duration_smoking - 27)
        - 0.0308572 * (smoking_quit_time - 10)
        - 4.532506
    )
    if smoking_status == 1 and smoking_intensity > 0:
        model += -1.822606 * (((smoking_intensity / 10) ** (-1)) - 0.4021541613)
    if race == "black":
        model += 0.3944778
    elif race == "hispanic":
        model -= 0.7434744
    elif race == "asian":
        model -= 0.466585
    elif race in ["native hawaiian", "pacific islander"]:
        model += 1.027152
    return logistic(model)

# ------------------- INPUTS -------------------
st.subheader("Demographics")
age = st.number_input("Age", 40, 90, 60)
race = st.selectbox("Race", ["White", "Black", "Hispanic", "Asian", "Native Hawaiian", "Pacific Islander"])
education = st.number_input("Years of education (AFTER high school)", 0, 20, 0)

st.subheader("Height & Weight")
col1, col2 = st.columns(2)
with col1: height_ft = st.number_input("Height (feet)", 3, 8, 5)
with col2: height_in = st.number_input("Height (inches)", 0, 11, 8)
weight_lb = st.number_input("Weight (pounds)", 80, 500, 170)
total_height_inches = (height_ft * 12) + height_in
bmi = (weight_lb / (total_height_inches ** 2)) * 703
st.write(f"BMI: {bmi:.1f}")

st.subheader("Medical History")
copd = 1 if st.selectbox("COPD Diagnosis (Chronic Obstructive Pulmonary Disease)", ["No", "Yes"]) == "Yes" else 0
cancer_hist = 1 if st.selectbox("Personal History of Cancer?", ["No", "Yes"]) == "Yes" else 0
family_hist = 1 if st.selectbox("Family History of Lung Cancer?", ["No", "Yes"]) == "Yes" else 0

st.subheader("Smoking History")
smoking_choice = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
smoking_status = 0 if smoking_choice == "Never" else 1
smoking_intensity = 0
duration_smoking = 0
smoking_quit_time = 0
pack_years = 0

if smoking_choice != "Never":
    smoking_intensity = st.number_input("Cigarettes per day", 1, 100, 20)
    duration_smoking = st.number_input("Years of smoking", 1, 70, 20)
    pack_years = (smoking_intensity / 20) * duration_smoking
    st.write(f"Pack-years: {pack_years:.1f}")
    if smoking_choice == "Former":
        smoking_quit_time = st.number_input("Years since quitting", 0, 50, 5)

result_container = st.container()

# ------------------- CALCULATE -------------------
if st.button("Calculate Risk & Eligibility"):
    risk = plco_m2012(age, race, education, bmi, copd, cancer_hist, family_hist,
                       smoking_status, smoking_intensity, duration_smoking, smoking_quit_time)
    risk_percent = risk * 100

    uspstf_age = 50 <= age <= 80
    uspstf_pack = pack_years >= 20
    uspstf_quit = smoking_choice == "Current" or (smoking_choice == "Former" and smoking_quit_time <= 15)
    uspstf_eligible = uspstf_age and uspstf_pack and uspstf_quit
    plco_high_risk = risk_percent >= 1.3

    # Determine colors and labels
    if plco_high_risk or uspstf_eligible:
        bg_color = "#fdecea"
        risk_label = "High Risk — Screening Recommended"
    else:
        bg_color = "#e6f4ea"
        risk_label = "Low Risk — Routine Screening Not Recommended"

    eligibility_text = (
        "You meet USPSTF 2021 lung cancer screening criteria."
        if uspstf_eligible else
        "You do NOT meet USPSTF 2021 lung cancer screening criteria."
    )

    with result_container:
        st.markdown(
            f"""
            <div class="result-card" style="background:{bg_color};">
                <h3>Your estimated risk of developing lung cancer in the next 6 years is:</h3>
                <h2>{risk_percent:.2f}%</h2>
                <h3>{risk_label}</h3>
                <p style="margin-top: 10px; font-weight: 500;">{eligibility_text}</p>
            </div>
            """, unsafe_allow_html=True
        )

    # Log usage with session ID
    log_usage(st.session_state.user_id, age, race, smoking_choice, risk_percent, uspstf_eligible)

# ------------------- ADMIN ONLY -------------------
admin_password = "MySecret123"  # <-- change this
password_input = st.sidebar.text_input("Admin password", type="password")
if password_input == admin_password:
    if os.path.isfile(log_file):
        df = pd.read_csv(log_file)
        # fallback for old CSVs without user_id
        if "user_id" not in df.columns:
            df["user_id"] = df.index.astype(str)
        unique_users = df["user_id"].nunique()
        total_uses = df.shape[0]
        st.sidebar.success(f"🔹 Total clicks: {total_uses}\n🔹 Unique users: {unique_users}")
    else:
        st.sidebar.info("No usage yet.")

# ------------------- FOOTER -------------------
st.markdown("""
<div class="footer">
Based on the PLCOm2012 risk model. This tool is for educational purposes only and does not replace medical advice.
</div>
""", unsafe_allow_html=True)

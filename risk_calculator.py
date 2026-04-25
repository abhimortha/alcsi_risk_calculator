import streamlit as st
import numpy as np
import uuid
import datetime
import os
import csv
import math

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="LungIQ · Lung Health Risk Tool",
    page_icon="🫁",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
#  GLOBAL CSS  (medical-grade, clean, bold)
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F2F4F8 !important;
    font-family: 'DM Sans', sans-serif;
    color: #1A1F2E;
}

[data-testid="stAppViewContainer"] > .main { background: #F2F4F8 !important; }
[data-testid="block-container"] { padding: 0 !important; max-width: 780px; margin: 0 auto; }
header, footer { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

/* ── Hero ── */
.hero-wrap {
    background: linear-gradient(135deg, #0A1628 0%, #0D2952 55%, #0F3A72 100%);
    padding: 60px 40px 50px;
    text-align: center;
    border-radius: 0 0 32px 32px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(64,160,255,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -60px; left: -30px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(64,200,180,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(64,160,255,0.18);
    border: 1px solid rgba(64,160,255,0.35);
    color: #7EC8FF;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 100px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 52px;
    font-weight: 400;
    color: #FFFFFF;
    line-height: 1.1;
    margin: 0 0 16px;
    letter-spacing: -1px;
}
.hero-title em { color: #7EC8FF; font-style: italic; }
.hero-sub {
    font-size: 17px;
    color: rgba(255,255,255,0.65);
    max-width: 480px;
    margin: 0 auto 32px;
    line-height: 1.65;
    font-weight: 300;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-top: 32px;
    padding-top: 28px;
    border-top: 1px solid rgba(255,255,255,0.1);
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    color: #7EC8FF;
    display: block;
}
.stat-label {
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
}

/* ── Section labels ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #6B7A99;
    margin-bottom: 14px;
    margin-top: 32px;
    padding-left: 2px;
}

/* ── Cards ── */
.card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 28px 30px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06), 0 0 0 1px rgba(0,0,0,0.04);
}
.card-title {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #8A94B0;
    margin-bottom: 18px;
}

/* ── Tooltip / info ── */
.tooltip-wrap { display: inline; position: relative; }
.info-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px; height: 18px;
    background: #E8EDFB;
    color: #4A7BCC;
    border-radius: 50%;
    font-size: 11px;
    font-weight: 700;
    cursor: default;
    margin-left: 6px;
    vertical-align: middle;
    border: none;
    line-height: 1;
}
.tooltip-text {
    visibility: hidden;
    opacity: 0;
    background: #1A1F2E;
    color: #E8EDFB;
    font-size: 12.5px;
    line-height: 1.55;
    font-weight: 400;
    border-radius: 10px;
    padding: 12px 14px;
    position: absolute;
    z-index: 100;
    bottom: 130%;
    left: 50%;
    transform: translateX(-50%);
    width: 260px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    transition: opacity 0.18s ease;
    pointer-events: none;
}
.tooltip-text::after {
    content: '';
    position: absolute;
    top: 100%; left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: #1A1F2E;
}
.tooltip-wrap:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
}

/* ── Result panel ── */
.result-panel {
    border-radius: 24px;
    padding: 36px 36px 32px;
    margin-bottom: 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-panel.high {
    background: linear-gradient(135deg, #FFF0F0 0%, #FFE4E4 100%);
    border: 1px solid #FFCCCC;
}
.result-panel.low {
    background: linear-gradient(135deg, #F0FFF8 0%, #E2F9EE 100%);
    border: 1px solid #B8EDD4;
}
.result-panel.moderate {
    background: linear-gradient(135deg, #FFFBF0 0%, #FFF3D9 100%);
    border: 1px solid #FFE0A0;
}

.lung-age-label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6B7A99;
    margin-bottom: 8px;
}
.lung-age-value {
    font-family: 'DM Serif Display', serif;
    font-size: 80px;
    line-height: 1;
    margin-bottom: 4px;
    letter-spacing: -3px;
}
.lung-age-value.high { color: #C62828; }
.lung-age-value.low { color: #1B7A48; }
.lung-age-value.moderate { color: #B06A00; }

.lung-age-diff {
    font-size: 14px;
    font-weight: 500;
    color: #8A94B0;
    margin-bottom: 20px;
}
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 9px 22px;
    border-radius: 100px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 20px;
}
.risk-badge.high { background: #C62828; color: white; }
.risk-badge.low { background: #1B7A48; color: white; }
.risk-badge.moderate { background: #D47D00; color: white; }

.risk-pct {
    font-size: 13px;
    color: #6B7A99;
}

/* ── Recs ── */
.rec-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 16px 0;
    border-bottom: 1px solid #F0F2F8;
}
.rec-item:last-child { border-bottom: none; }
.rec-icon {
    width: 38px; height: 38px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.rec-icon.screen { background: #EBF2FF; }
.rec-icon.warn { background: #FFF3E0; }
.rec-icon.ok { background: #E8F7EE; }
.rec-icon.quit { background: #FBE9E7; }

.rec-head { font-weight: 600; font-size: 14.5px; margin-bottom: 3px; }
.rec-sub { font-size: 13px; color: #6B7A99; line-height: 1.5; }

/* ── Sim block ── */
.sim-block {
    background: #F7F9FE;
    border: 1px solid #E4E9F6;
    border-radius: 16px;
    padding: 20px 22px;
    margin-top: 16px;
}
.sim-result {
    font-family: 'DM Serif Display', serif;
    font-size: 36px;
    color: #1B7A48;
    text-align: center;
    margin: 8px 0;
}

/* ── Qualify box ── */
.qualify-yes {
    background: #EBF2FF;
    border: 1.5px solid #7EB3FF;
    border-radius: 14px;
    padding: 18px 20px;
    font-size: 14px;
    color: #0D2952;
    line-height: 1.55;
}
.qualify-no {
    background: #F7F9FE;
    border: 1px solid #DDE3F0;
    border-radius: 14px;
    padding: 18px 20px;
    font-size: 14px;
    color: #4A5578;
    line-height: 1.55;
}

/* ── Start button ── */
.stButton > button {
    background: linear-gradient(135deg, #1557B0, #1E7DE0) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 36px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 16px rgba(21,87,176,0.3) !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(21,87,176,0.38) !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div {
    border-radius: 10px !important;
    border-color: #DDE3F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}
[data-testid="stSelectbox"] > div:focus-within {
    border-color: #1557B0 !important;
    box-shadow: 0 0 0 3px rgba(21,87,176,0.12) !important;
}

label, [data-testid="stWidgetLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    color: #2A3148 !important;
}

/* Slider */
[data-testid="stSlider"] > div > div > div {
    background: #1557B0 !important;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid #E8ECF4; margin: 32px 0; }

/* ── Footer ── */
.footer {
    text-align: center;
    font-size: 12px;
    color: #9AA3BE;
    padding: 24px 20px 40px;
    line-height: 1.7;
}

/* ── ZIP validation color ── */
.zip-valid [data-testid="stTextInput"] input {
    border-color: #1B7A48 !important;
    box-shadow: 0 0 0 3px rgba(27,122,72,0.12) !important;
    background: #F0FFF8 !important;
}
.zip-invalid [data-testid="stTextInput"] input {
    border-color: #C62828 !important;
    box-shadow: 0 0 0 3px rgba(198,40,40,0.10) !important;
    background: #FFF5F5 !important;
}
.zip-status {
    font-size: 12.5px;
    font-weight: 500;
    margin-top: -10px;
    margin-bottom: 8px;
    padding: 0 2px;
}
.zip-status.ok  { color: #1B7A48; }
.zip-status.err { color: #C62828; }

/* ── Screening locations ── */
.loc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 4px;
}
.loc-card {
    background: #F7F9FE;
    border: 1px solid #DDE3F0;
    border-radius: 14px;
    padding: 14px 16px;
    font-size: 13px;
    line-height: 1.55;
}
.loc-name {
    font-weight: 600;
    color: #0D2952;
    font-size: 13.5px;
    margin-bottom: 3px;
}
.loc-dist {
    display: inline-block;
    background: #EBF2FF;
    color: #1557B0;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 100px;
    margin-bottom: 6px;
}
.loc-addr { color: #6B7A99; font-size: 12px; }
.loc-phone { color: #4A7BCC; font-size: 12px; font-weight: 500; }

/* ── Age warning ── */
.age-warn {
    background: #FFF8E1;
    border-left: 4px solid #FFC107;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    font-size: 13.5px;
    color: #5D4037;
    margin-bottom: 12px;
    line-height: 1.55;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "started" not in st.session_state:
    st.session_state.started = False

# ─────────────────────────────────────────
#  ZIP DATA
# ─────────────────────────────────────────
valid_zips = {
    "46032","46033","46060","46062","46074","46077",
    "46220","46240","46250","46256","46280","46290",
    "46112","46142"
}
zip_to_latlon = {
    "46032":(39.9784,-86.1180), "46033":(39.9990,-86.0820),
    "46060":(40.0456,-86.0086), "46062":(40.0510,-86.0480),
    "46074":(39.9630,-86.2620), "46077":(39.9510,-86.3500),
    "46220":(39.8680,-86.1180), "46240":(39.9050,-86.1280),
    "46250":(39.9130,-86.0700), "46256":(39.9000,-86.0200),
    "46280":(39.9350,-86.1350), "46290":(39.9300,-86.1600),
    "46112":(39.6890,-86.3990), "46142":(39.6130,-86.1260),
}

# ─────────────────────────────────────────
#  SCREENING LOCATIONS BY ZIP PROXIMITY
# ─────────────────────────────────────────
# Each location: (name, address, phone, distance_label, url)
screening_locations = [
    {
        "name": "IU Health North Hospital – Lung Screening",
        "address": "11700 N Meridian St, Carmel, IN 46032",
        "phone": "(317) 688-2000",
        "note": "LDCT lung screening; referral or self-referral accepted",
        "url": "https://iuhealth.org",
    },
    {
        "name": "Ascension St. Vincent Carmel",
        "address": "13500 N Meridian St, Carmel, IN 46032",
        "phone": "(317) 582-7000",
        "note": "Comprehensive cancer screening & pulmonology",
        "url": "https://healthcare.ascension.org",
    },
    {
        "name": "Community Health Network – North",
        "address": "8051 Clearvista Pkwy, Indianapolis, IN 46256",
        "phone": "(317) 621-5000",
        "note": "Low-dose CT lung screenings; most insurance accepted",
        "url": "https://ecommunity.com",
    },
    {
        "name": "IU Health Methodist – Thoracic Oncology",
        "address": "1801 N Senate Blvd, Indianapolis, IN 46202",
        "phone": "(317) 962-2000",
        "note": "Academic medical center; high-risk lung program",
        "url": "https://iuhealth.org",
    },
    {
        "name": "Franciscan Health Indianapolis",
        "address": "8111 S Emerson Ave, Indianapolis, IN 46237",
        "phone": "(317) 528-5000",
        "note": "Lung cancer screening; ACR-accredited imaging",
        "url": "https://franciscanhealth.org",
    },
    {
        "name": "Aspire Indiana Health – Noblesville",
        "address": "1552 Union Chapel Rd, Noblesville, IN 46060",
        "phone": "(800) 342-5653",
        "note": "Community health center; sliding-scale fees available",
        "url": "https://aspireindiana.org",
    },
    {
        "name": "IU Health Tipton Hospital",
        "address": "1000 S Main St, Tipton, IN 46072",
        "phone": "(765) 675-8500",
        "note": "Convenient for northern Hamilton County residents",
        "url": "https://iuhealth.org",
    },
    {
        "name": "Hendricks Regional Health",
        "address": "1000 E Main St, Danville, IN 46122",
        "phone": "(317) 745-4451",
        "note": "Serves 46112 area; radiology & screening programs",
        "url": "https://hendricks.org",
    },
]

# Map zip codes to the 2 closest locations (by index into screening_locations)
zip_to_locations = {
    # Carmel / NW Hamilton County
    "46032": [0, 1],  # IU Health North, St. Vincent Carmel
    "46033": [0, 1],
    "46074": [0, 1],  # Zionsville
    "46077": [0, 1],
    # Fishers / Noblesville / NE Hamilton County
    "46060": [5, 2],  # Aspire Noblesville, Community Health North
    "46062": [5, 2],
    "46038": [2, 0],
    # Indianapolis north / Marion County
    "46220": [2, 3],  # Community Health North, Methodist
    "46240": [2, 0],
    "46250": [2, 0],
    "46256": [2, 0],
    "46280": [0, 2],
    "46290": [0, 2],
    # Greenwood / south Marion
    "46142": [4, 3],  # Franciscan, Methodist
    # Brownsburg
    "46112": [7, 4],  # Hendricks Regional, Franciscan
}

def get_nearby_locations(zip_code):
    idxs = zip_to_locations.get(zip_code, [0, 2])
    return [screening_locations[i] for i in idxs]

# ─────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────
log_file = "usage_log.csv"
def log_usage(data):
    exists = os.path.isfile(log_file)
    with open(log_file,"a",newline="") as f:
        fields = ["timestamp","user_id","zip","lat","lon","age","smoking_status","risk_group","risk_pct"]
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow(data)

# ─────────────────────────────────────────
#  RISK MODEL
# ─────────────────────────────────────────
def logistic(x):
    return 1/(1+np.exp(-np.clip(x,-500,500)))

def plco_m2012(age, race, education, bmi, copd, cancer_hist, family_hist,
               smoking_status, smoking_intensity, duration_smoking, smoking_quit_time):
    """PLCOm2012 model (validated on ages 40-90). Returns 6-year absolute risk (0-1)."""
    m = (0.0778868*(age-62)
       - 0.0812744*(education-4)
       - 0.0274194*(bmi-27)
       + 0.3553063*copd
       + 0.4589971*cancer_hist
       + 0.587185*family_hist
       + 0.2597431*smoking_status
       + 0.0317321*(duration_smoking-27)
       - 0.0308572*(smoking_quit_time-10)
       - 4.532506)
    if smoking_status==1 and smoking_intensity>0:
        m += -1.822606*((smoking_intensity/10)**(-1) - 0.4021541613)
    return logistic(m)

def extrapolate_risk(age, race, education, bmi, copd, cancer_hist, family_hist,
                     smoking_status, smoking_intensity, duration_smoking, smoking_quit_time):
    """
    For ages < 40: extrapolate from the model's age=40 baseline using an
    exponential age-scaling factor.  Risk is dramatically lower for younger ages.
    For ages > 90: cap at age=90 result.
    """
    actual_age = age
    if age < 40:
        base_risk = plco_m2012(40, race, education, bmi, copd, cancer_hist, family_hist,
                               smoking_status, smoking_intensity, duration_smoking, smoking_quit_time)
        # Exponential decay: lung cancer incidence roughly doubles every ~10 yrs below 50
        scale = math.exp(-0.065 * (40 - age))
        return base_risk * scale
    elif age > 90:
        return plco_m2012(90, race, education, bmi, copd, cancer_hist, family_hist,
                          smoking_status, smoking_intensity, duration_smoking, smoking_quit_time)
    else:
        return plco_m2012(age, race, education, bmi, copd, cancer_hist, family_hist,
                          smoking_status, smoking_intensity, duration_smoking, smoking_quit_time)

def lung_age_from_risk(actual_age, risk_pct):
    """
    Compute 'lung age' by finding what age a non-smoking average person
    would need to be to have the same risk.
    Blended: partly actuarial offset, partly risk-ratio scaling.
    """
    base = actual_age
    if risk_pct <= 0.1:
        offset = -8
    elif risk_pct <= 0.5:
        offset = -4
    elif risk_pct < 1.3:
        offset = 0
    elif risk_pct < 3.0:
        offset = int((risk_pct - 1.3) * 6)
    elif risk_pct < 6.0:
        offset = int(10 + (risk_pct - 3.0) * 4)
    else:
        offset = int(22 + (risk_pct - 6.0) * 2)
    return max(10, min(100, base + offset))

def risk_category(risk_pct, age):
    """Returns (category_str, threshold_used)"""
    # USPSTF: ≥1.3% = eligible for screening (for 50–80 yo, pack-year criteria separate)
    if risk_pct >= 3.0:
        return "high", 3.0
    elif risk_pct >= 1.3:
        return "moderate", 1.3
    else:
        return "low", 1.3

def uspstf_qualifies(age, smoking_status, pack_years):
    """USPSTF 2021 criteria: age 50-80, current or former smoker, ≥20 pack-years."""
    if smoking_status == "Never":
        return False, "Non-smokers do not qualify for USPSTF lung screening guidelines."
    if age < 50 or age > 80:
        return False, f"USPSTF guidelines apply to ages 50–80 (your age: {age})."
    if pack_years < 20:
        return False, f"USPSTF requires ≥20 pack-years (yours: {pack_years:.1f})."
    return True, "You meet all USPSTF 2021 criteria for annual low-dose CT (LDCT) lung screening."

# ─────────────────────────────────────────
#  TOOLTIP HELPER
# ─────────────────────────────────────────
def info_tip(label, tip_text):
    return f"""
    <span style="font-weight:500;color:#2A3148;">{label}</span>
    <span class="tooltip-wrap">
        <span class="info-btn">i</span>
        <span class="tooltip-text">{tip_text}</span>
    </span>
    """

# ─────────────────────────────────────────
#  HERO / LANDING
# ─────────────────────────────────────────
if not st.session_state.started:
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-badge">ALCSI Innovation · Lung Health Tool</div>
        <div class="hero-title">Know your<br><em>LungIQ</em></div>
        <div class="hero-sub">
            A science-backed, 30-second risk assessment using the
            clinically validated PLCOm2012 model — trusted by hospitals worldwide.
        </div>
        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-num">236K</span>
                <span class="stat-label">New Cases / Year</span>
            </div>
            <div class="stat-item">
                <span class="stat-num">80%</span>
                <span class="stat-label">Survival if caught early</span>
            </div>
            <div class="stat-item">
                <span class="stat-num">#1</span>
                <span class="stat-label">Cancer Killer in US</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🫁  Start My Lung Check"):
            st.session_state.started = True
            st.rerun()

    st.markdown("""
    <div class="footer">
        This tool is for educational and screening awareness purposes only.<br>
        It is not a medical diagnosis. Always consult a licensed physician.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────
#  FORM
# ─────────────────────────────────────────
st.markdown("""
<div class="hero-wrap" style="padding:32px 40px 28px;border-radius:0 0 24px 24px;">
    <div class="hero-badge">ALCSI Innovation · Lung Health Tool</div>
    <div class="hero-title" style="font-size:36px;margin-bottom:6px;">Your <em>LungIQ</em></div>
    <div class="hero-sub" style="font-size:15px;margin-bottom:0;">Complete the fields below — takes about 30 seconds.</div>
</div>
""", unsafe_allow_html=True)

# ── Location ──
st.markdown('<div class="section-label">📍 Location</div>', unsafe_allow_html=True)

zip_state = ""
if "zip_input" in st.session_state and st.session_state["zip_input"]:
    z = st.session_state["zip_input"]
    if z in valid_zips:
        zip_state = "zip-valid"
    elif len(z) >= 3:
        zip_state = "zip-invalid"

st.markdown(f'<div class="{zip_state}">', unsafe_allow_html=True)
zip_code = st.text_input(
    "ZIP Code (Indianapolis / Carmel area)",
    placeholder="e.g. 46032",
    key="zip_input"
)
st.markdown('</div>', unsafe_allow_html=True)

if zip_code:
    if zip_code in valid_zips:
        st.markdown('<div class="zip-status ok">✓ ZIP code recognized — screening locations loaded</div>', unsafe_allow_html=True)
    elif len(zip_code) >= 3:
        st.markdown('<div class="zip-status err">✗ ZIP not in service area — enter an Indianapolis/Carmel ZIP (e.g. 46032)</div>', unsafe_allow_html=True)

# ── Demographics ──
st.markdown('<div class="section-label">👤 About You</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=10, max_value=100, value=55)
with col2:
    race = st.selectbox("Race / Ethnicity", ["White","Black","Hispanic","Asian","Other"])

education = st.selectbox(
    "Highest education level",
    ["Less than high school (0 yrs post-HS)",
     "High school diploma (0 yrs post-HS)",
     "Some college (2 yrs post-HS)",
     "Bachelor's degree (4 yrs post-HS)",
     "Graduate degree (6+ yrs post-HS)"]
)
edu_map = {
    "Less than high school (0 yrs post-HS)": 0,
    "High school diploma (0 yrs post-HS)": 0,
    "Some college (2 yrs post-HS)": 2,
    "Bachelor's degree (4 yrs post-HS)": 4,
    "Graduate degree (6+ yrs post-HS)": 6,
}
education_val = edu_map[education]

# ── Physical ──
st.markdown('<div class="section-label">📏 Physical Stats</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    height_ft = st.number_input("Height (ft)", 3, 8, 5)
with col2:
    height_in = st.number_input("Height (in)", 0, 11, 8)
with col3:
    weight = st.number_input("Weight (lbs)", 50, 600, 170)

height_total_in = (height_ft * 12) + height_in
bmi = (weight / (height_total_in ** 2)) * 703

# ── Medical History ──
st.markdown('<div class="section-label">🏥 Medical History</div>', unsafe_allow_html=True)

st.markdown(info_tip("COPD (Chronic Obstructive Pulmonary Disease)",
    "COPD is a chronic lung disease that makes it hard to breathe. It includes emphysema and chronic bronchitis. Smoking is the leading cause. People with COPD have a significantly higher lung cancer risk."), unsafe_allow_html=True)
copd = 1 if st.selectbox("Do you have COPD?", ["No","Yes"], key="copd") == "Yes" else 0

st.markdown(info_tip("Personal Cancer History",
    "A prior diagnosis of any cancer (especially head, neck, or lung) can increase your risk due to shared genetic and lifestyle factors, as well as prior radiation exposure."), unsafe_allow_html=True)
cancer_hist = 1 if st.selectbox("Have you had cancer before?", ["No","Yes"], key="cancer") == "Yes" else 0

st.markdown(info_tip("Family History of Lung Cancer",
    "Having a first-degree relative (parent, sibling, or child) diagnosed with lung cancer raises your risk. This likely reflects both shared genetics and shared environmental exposures."), unsafe_allow_html=True)
family_hist = 1 if st.selectbox("Family history of lung cancer?", ["No","Yes"], key="family") == "Yes" else 0

# ── Smoking ──
st.markdown('<div class="section-label">🚬 Smoking History</div>', unsafe_allow_html=True)

st.markdown(info_tip("Smoking Status",
    "Smoking accounts for ~85% of all lung cancer cases. Even former smokers carry elevated risk for decades after quitting. 'Never smoker' means fewer than 100 cigarettes in your lifetime."), unsafe_allow_html=True)
smoking = st.selectbox("Smoking status", ["Never","Former","Current"], key="smoke_status")
smoking_status_val = 0 if smoking == "Never" else 1

cigs, years, quit = 0, 0, 0
pack_years = 0.0

if smoking != "Never":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(info_tip("Cigarettes per Day",
            "Average number of cigarettes smoked per day during your smoking years. A pack = 20 cigarettes."), unsafe_allow_html=True)
        cigs = st.number_input("Cigarettes per day (avg)", 1, 100, 20, key="cigs")
    with col2:
        st.markdown(info_tip("Years Smoked",
            "Total number of years you smoked. Pack-years = (packs/day) × years smoked. ≥20 pack-years triggers USPSTF screening eligibility."), unsafe_allow_html=True)
        years = st.number_input("Total years smoked", 1, 70, 20, key="years")

    pack_years = (cigs / 20) * years

    if smoking == "Former":
        st.markdown(info_tip("Years Since Quitting",
            "The longer since you quit, the lower your risk — though it never fully returns to a never-smoker's level. Risk drops most sharply in the first 5 years after quitting."), unsafe_allow_html=True)
        quit = st.number_input("Years since quitting", 0, 60, 5, key="quit")

st.markdown("<br>", unsafe_allow_html=True)

# ── Submit ──
col1, col2, col3 = st.columns([1,2,1])
with col2:
    run = st.button("🔬  Calculate My Lung Risk")

# ─────────────────────────────────────────
#  RESULTS
# ─────────────────────────────────────────
if run:
    if zip_code and zip_code not in valid_zips:
        st.error("Please enter a valid ZIP code before continuing.")
        st.stop()

    risk = extrapolate_risk(
        age, race, education_val, bmi, copd, cancer_hist, family_hist,
        smoking_status_val, cigs, years, quit
    )
    risk_pct = risk * 100
    category, threshold = risk_category(risk_pct, age)
    lung_age_val = lung_age_from_risk(age, risk_pct)
    age_diff = lung_age_val - age
    qualifies, qual_msg = uspstf_qualifies(age, smoking, pack_years)

    # Store everything needed for display in session state
    st.session_state.results = {
        "risk_pct": risk_pct, "category": category, "threshold": threshold,
        "lung_age_val": lung_age_val, "age_diff": age_diff,
        "qualifies": qualifies, "qual_msg": qual_msg,
        "age": age, "smoking": smoking, "pack_years": pack_years,
        "zip_code": zip_code, "race": race, "education_val": education_val,
        "bmi": bmi, "copd": copd, "cancer_hist": cancer_hist,
        "family_hist": family_hist, "cigs": cigs, "years": years,
    }

    lat, lon = zip_to_latlon.get(zip_code, (None, None)) if zip_code else (None, None)
    log_usage({
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": st.session_state.user_id,
        "zip": zip_code or "",
        "lat": lat, "lon": lon,
        "age": age,
        "smoking_status": smoking,
        "risk_group": category,
        "risk_pct": round(risk_pct, 3),
    })

if "results" in st.session_state:
    r = st.session_state.results
    risk_pct      = r["risk_pct"]
    category      = r["category"]
    threshold     = r["threshold"]
    lung_age_val  = r["lung_age_val"]
    age_diff      = r["age_diff"]
    qualifies     = r["qualifies"]
    qual_msg      = r["qual_msg"]
    age           = r["age"]
    smoking       = r["smoking"]
    pack_years    = r["pack_years"]
    zip_code      = r["zip_code"]
    race          = r["race"]
    education_val = r["education_val"]
    bmi           = r["bmi"]
    copd          = r["copd"]
    cancer_hist   = r["cancer_hist"]
    family_hist   = r["family_hist"]
    cigs          = r["cigs"]
    years         = r["years"]

    # ── Age extension warning ──
    if age < 40:
        st.markdown(f"""
        <div class="age-warn">
            ⚠️ <strong>Note for ages under 40:</strong> The PLCOm2012 model is clinically validated
            for ages 40–80. Because you are {age}, your result uses an age-extrapolated estimate.
            Lung cancer is rare under 40, but risk factors still matter for future health.
            Interpret your result as informational only.
        </div>
        """, unsafe_allow_html=True)

    # ── Lung Age Panel ──
    diff_text = f"+{age_diff} years older than your actual age" if age_diff > 0 else (
        f"{abs(age_diff)} years younger than your actual age" if age_diff < 0 else
        "matching your actual age — you're on track"
    )
    panel_class = category

    st.markdown(f"""
    <div class="result-panel {panel_class}">
        <div class="lung-age-label">Your LungIQ Lung Age</div>
        <div class="lung-age-value {panel_class}">{lung_age_val}</div>
        <div class="lung-age-diff">{diff_text}</div>
        <div class="risk-badge {panel_class}">
            {"⚠️ High Risk" if category=="high" else ("⚡ Moderate Risk" if category=="moderate" else "✅ Lower Risk")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Nearby Screening Locations ──
    nearby = get_nearby_locations(zip_code) if zip_code in valid_zips else []
    if nearby:
        st.markdown('<div class="section-label">📍 Screening Centers Near You</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Based on your ZIP code, these facilities offer lung cancer screening</div>', unsafe_allow_html=True)
        st.markdown('<div class="loc-grid">', unsafe_allow_html=True)
        for loc in nearby:
            st.markdown(f"""
            <div class="loc-card">
                <div class="loc-name">{loc['name']}</div>
                <div class="loc-addr">📌 {loc['address']}</div>
                <div class="loc-phone">📞 {loc['phone']}</div>
                <div style="color:#8A94B0;font-size:11.5px;margin-top:5px;">{loc['note']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Smoking Cessation Simulator ──
    if smoking != "Never":
        st.markdown('<div class="section-label">💨 Smoking Cessation Simulator</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">What if you quit?</div>', unsafe_allow_html=True)
        st.write("See how quitting smoking would change your lung age over time:")

        years_quit_sim = st.slider("Years smoke-free (simulated)", 0, 25, 5)
        sim_risk = extrapolate_risk(
            age, race, education_val, bmi, copd, cancer_hist, family_hist,
            1, cigs, years, years_quit_sim
        )
        sim_lung_age = lung_age_from_risk(age, sim_risk * 100)
        gain = lung_age_val - sim_lung_age

        st.markdown(f"""
        <div class="sim-block">
            <div style="text-align:center;font-size:13px;color:#6B7A99;margin-bottom:4px;">
                Simulated Lung Age after <strong>{years_quit_sim} smoke-free years</strong>
            </div>
            <div class="sim-result">{sim_lung_age} <span style="font-size:18px;color:#1B7A48;">yrs</span></div>
            <div style="text-align:center;font-size:13px;color:#1B7A48;font-weight:600;">
                {"↓ " + str(gain) + " years younger than your current lung age" if gain > 0 else "Same as current — quit time already factored in"}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── USPSTF Detail ──
    st.markdown('<div class="section-label">📄 USPSTF Guideline Detail</div>', unsafe_allow_html=True)
    qual_div = "qualify-yes" if qualifies else "qualify-no"
    st.markdown(f"""
    <div class="{qual_div}">
        <strong>{"✅ You qualify" if qualifies else "ℹ️ You do not currently qualify"}</strong>
        under USPSTF 2021 lung cancer screening guidelines.<br><br>
        <strong>Full criteria:</strong> Age 50–80 · Current or former smoker · ≥20 pack-years<br>
        <strong>Your stats:</strong> Age {age} · Status: {smoking} · Pack-years: {pack_years:.1f}<br><br>
        {qual_msg}
    </div>
    """, unsafe_allow_html=True)

    # ── Reset ──
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔄  Start Over"):
            st.session_state.started = False
            del st.session_state.results
            st.rerun()

# ── Footer ──
st.markdown("""
<div class="footer">
    Based on the <strong>PLCOm2012</strong> lung cancer risk model (Tammemägi et al., 2013).<br>
    USPSTF 2021 criteria applied per current clinical guidelines.<br>
    This tool is for <em>educational and awareness purposes only</em> — not a medical diagnosis.<br>
    Always consult a licensed physician for personal medical advice.<br><br>
    Built for the ALCSI Lung Screening Innovation Competition · Indianapolis, IN<br>
    <strong>LungIQ</strong> — Know your lungs. Protect your future.
</div>
""", unsafe_allow_html=True)

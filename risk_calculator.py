import streamlit as st
import numpy as np
import datetime
import os
import csv
import math
import requests

SHEETS_WEBHOOK = "https://script.google.com/macros/s/AKfycbzZPiifkLT7iaqfv7JVWLEcQkYnRIjk2q0iAq5zsY7NFaVa3hcEnh7Hdq37DmpNB28Y/exec"

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
#  GLOBAL CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

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
.tooltip-wrap:hover .tooltip-text { visibility: visible; opacity: 1; }

.result-panel {
    border-radius: 24px;
    padding: 36px 36px 32px;
    margin-bottom: 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-panel.high { background: linear-gradient(135deg, #FFF0F0 0%, #FFE4E4 100%); border: 1px solid #FFCCCC; }
.result-panel.low { background: linear-gradient(135deg, #F0FFF8 0%, #E2F9EE 100%); border: 1px solid #B8EDD4; }
.result-panel.moderate { background: linear-gradient(135deg, #FFFBF0 0%, #FFF3D9 100%); border: 1px solid #FFE0A0; }

.lung-age-label { font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #6B7A99; margin-bottom: 8px; }
.lung-age-value { font-family: 'DM Serif Display', serif; font-size: 80px; line-height: 1; margin-bottom: 4px; letter-spacing: -3px; }
.lung-age-value.high { color: #C62828; }
.lung-age-value.low { color: #1B7A48; }
.lung-age-value.moderate { color: #B06A00; }

.lung-age-diff { font-size: 14px; font-weight: 500; color: #8A94B0; margin-bottom: 20px; }
.risk-badge {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 9px 22px; border-radius: 100px; font-size: 14px; font-weight: 600; margin-bottom: 20px;
}
.risk-badge.high { background: #C62828; color: white; }
.risk-badge.low { background: #1B7A48; color: white; }
.risk-badge.moderate { background: #D47D00; color: white; }
.risk-pct { font-size: 13px; color: #6B7A99; }

.rec-item { display: flex; align-items: flex-start; gap: 14px; padding: 16px 0; border-bottom: 1px solid #F0F2F8; }
.rec-item:last-child { border-bottom: none; }
.rec-icon { width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.rec-icon.screen { background: #EBF2FF; }
.rec-icon.warn { background: #FFF3E0; }
.rec-icon.ok { background: #E8F7EE; }
.rec-icon.quit { background: #FBE9E7; }
.rec-head { font-weight: 600; font-size: 14.5px; margin-bottom: 3px; }
.rec-sub { font-size: 13px; color: #6B7A99; line-height: 1.5; }

.sim-block { background: #F7F9FE; border: 1px solid #E4E9F6; border-radius: 16px; padding: 20px 22px; margin-top: 16px; }
.sim-result { font-family: 'DM Serif Display', serif; font-size: 36px; color: #1B7A48; text-align: center; margin: 8px 0; }

.qualify-yes { background: #EBF2FF; border: 1.5px solid #7EB3FF; border-radius: 14px; padding: 18px 20px; font-size: 14px; color: #0D2952; line-height: 1.55; }
.qualify-no { background: #F7F9FE; border: 1px solid #DDE3F0; border-radius: 14px; padding: 18px 20px; font-size: 14px; color: #4A5578; line-height: 1.55; }

.stButton > button {
    background: linear-gradient(135deg, #1557B0, #1E7DE0) !important;
    color: white !important; border: none !important; border-radius: 14px !important;
    padding: 14px 36px !important; font-size: 16px !important; font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important; width: 100% !important;
    cursor: pointer !important; transition: all 0.2s !important;
    box-shadow: 0 4px 16px rgba(21,87,176,0.3) !important; letter-spacing: 0.2px !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 22px rgba(21,87,176,0.38) !important; }

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div {
    border-radius: 10px !important; border-color: #DDE3F0 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 15px !important;
}
[data-testid="stSelectbox"] > div:focus-within { border-color: #1557B0 !important; box-shadow: 0 0 0 3px rgba(21,87,176,0.12) !important; }

label, [data-testid="stWidgetLabel"] { font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; font-size: 14px !important; color: #2A3148 !important; }
[data-testid="stSlider"] > div > div > div { background: #1557B0 !important; }
hr { border: none; border-top: 1px solid #E8ECF4; margin: 32px 0; }

.footer { text-align: center; font-size: 12px; color: #9AA3BE; padding: 24px 20px 40px; line-height: 1.7; }

.zip-valid [data-testid="stTextInput"] input { border-color: #1B7A48 !important; box-shadow: 0 0 0 3px rgba(27,122,72,0.12) !important; background: #F0FFF8 !important; }
.zip-status { font-size: 12.5px; font-weight: 500; margin-top: -10px; margin-bottom: 8px; padding: 0 2px; }
.zip-status.ok { color: #1B7A48; }
.zip-status.warn { color: #B06A00; }

.loc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 4px; }
.loc-card { background: #F7F9FE; border: 1px solid #DDE3F0; border-radius: 14px; padding: 14px 16px; font-size: 13px; line-height: 1.55; }
.loc-name { font-weight: 600; color: #0D2952; font-size: 13.5px; margin-bottom: 3px; }
.loc-dist { display: inline-block; background: #EBF2FF; color: #1557B0; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 100px; margin-bottom: 6px; }
.loc-addr { color: #6B7A99; font-size: 12px; }
.loc-phone { color: #4A7BCC; font-size: 12px; font-weight: 500; }

.age-warn { background: #FFF8E1; border-left: 4px solid #FFC107; border-radius: 0 10px 10px 0; padding: 14px 18px; font-size: 13.5px; color: #5D4037; margin-bottom: 12px; line-height: 1.55; }

[data-testid="stNumberInput"]:has(input[aria-label="Age"]) button { display: none !important; }
[data-testid="stNumberInput"]:has(input[aria-label="Age"]) > div { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────
if "started" not in st.session_state:
    st.session_state.started = False
if "user_ip" not in st.session_state:
    try:
        ip_resp = requests.get("https://api.ipify.org?format=json", timeout=3)
        st.session_state.user_ip = ip_resp.json().get("ip", "unknown")
    except Exception:
        st.session_state.user_ip = "unknown"

# ─────────────────────────────────────────
#  ZIP DATA — Indiana ZIPs (kept for curated screening lookup)
# ─────────────────────────────────────────
indiana_zips = {
    "46201","46202","46203","46204","46205","46206","46207","46208",
    "46209","46210","46211","46214","46216","46217","46218","46219",
    "46220","46221","46222","46224","46225","46226","46227","46228",
    "46229","46230","46231","46234","46235","46236","46237","46239",
    "46240","46241","46242","46244","46247","46249","46250","46251",
    "46253","46254","46255","46256","46259","46260","46262","46268",
    "46274","46275","46277","46278","46280","46282","46283","46285",
    "46290","46291","46295","46296","46298",
    "46032","46033","46034","46036","46037","46038","46040","46055",
    "46060","46061","46062","46063","46064","46074","46082",
    "46077","46112","46113","46118","46121","46122","46123","46149",
    "46158","46167",
    "46107","46131","46142","46143","46160","46161","46162","46163",
    "46164","46181","46183","46184",
    "46052","46075","46077",
    "46105","46120","46124","46128","46135","46157","46165","46170",
    "46172",
    "46106","46151","46158","46166",
    "46001","46011","46012","46013","46014","46015","46016","46017",
    "46030","46044","46045","46048","46049","46050","46051","46058",
    "46065","46069","46070","46071","46072","46076",
    "46140","46148","46150","46155","46156",
    "46176",
    "47201","47202","47203",
    "47401","47402","47403","47404","47405","47406","47407","47408",
    "47901","47902","47903","47904","47905","47906","47907","47909",
    "46801","46802","46803","46804","46805","46806","46807","46808",
    "46809","46814","46815","46816","46818","46819","46825","46835",
    "46845",
    "46530","46545","46550","46552","46554","46556","46560","46561",
    "46563","46565","46567","46570","46571","46572","46573","46574",
    "46580","46581","46582","46590","46595","46601","46604","46613",
    "46614","46615","46616","46617","46619","46620","46624","46626",
    "46628","46629","46634","46635","46637","46660","46680","46699",
    "46301","46302","46303","46304","46320","46321","46322","46323",
    "46324","46325","46327","46340","46341","46342","46345","46346",
    "46347","46348","46349","46350","46351","46352","46355","46356",
    "46373","46374","46375","46376","46377","46379","46380","46381",
    "46382","46383","46384","46385","46390","46391","46392","46393",
    "46394","46395","46396","46397","46398","46399","46401","46402",
    "46403","46404","46405","46406","46407","46408","46409","46410",
    "46411",
    "46514","46515","46516","46517","46526","46527","46528",
    "46901","46902","46903","46904",
    "47302","47303","47304","47305","47306","47307","47308",
    "47801","47802","47803","47804","47805","47807","47809",
    "47710","47711","47712","47713","47714","47715","47720","47721",
    "47722","47724","47725","47728",
    "47129","47130","47131","47132","47133","47134","47135","47136",
    "47140","47141","47142","47143","47144","47145","47146","47147",
    "47150","47151","47152","47160","47161","47162","47163","47164",
    "47165","47166","47167","47168","47170","47172","47174","47175",
    "47374","47375","47376",
    "47542","47546","47547","47549","47550","47553","47556","47557",
    "47558","47561","47562","47564","47567","47568","47573","47574",
    "47575","47576","47577","47578","47579","47580","47581","47584",
    "47585","47586","47588","47590","47591","47596","47597","47598",
    "47601","47610","47611","47612","47613","47614","47615","47616",
    "47617","47618","47619","47620","47629","47630","47631","47633",
    "47634","47635","47637","47638","47639","47640","47647","47648",
    "47649","47654","47660","47665","47666","47670","47683","47701",
    "47702","47703","47704","47705","47706","47708",
}

# ─────────────────────────────────────────
#  STATE → Major Lung Cancer Screening Centers fallback
#  Used when ZIP is outside Indiana AND Google Places unavailable
# ─────────────────────────────────────────
STATE_SCREENING_FALLBACK = {
    "AL": [{"name": "UAB Comprehensive Cancer Center", "address": "1802 6th Ave S, Birmingham, AL 35233", "phone": "(205) 934-5077"}],
    "AK": [{"name": "Providence Alaska Cancer Center", "address": "3340 Providence Dr, Anchorage, AK 99508", "phone": "(907) 212-3500"}],
    "AZ": [{"name": "Banner MD Anderson Cancer Center", "address": "2946 E Banner Gateway Dr, Gilbert, AZ 85234", "phone": "(480) 256-6444"}],
    "AR": [{"name": "Winthrop P. Rockefeller Cancer Institute", "address": "4320 W Markham St, Little Rock, AR 72205", "phone": "(501) 686-8000"}],
    "CA": [{"name": "UCLA Lung Cancer Screening", "address": "200 Medical Plaza, Los Angeles, CA 90095", "phone": "(310) 267-9400"}],
    "CO": [{"name": "UCHealth Lung Screening – Denver", "address": "1665 Aurora Ct, Aurora, CO 80045", "phone": "(720) 848-0000"}],
    "CT": [{"name": "Yale Cancer Center – Lung Screening", "address": "35 Park St, New Haven, CT 06519", "phone": "(203) 785-4095"}],
    "DE": [{"name": "Christiana Care Helen F. Graham Cancer Center", "address": "4701 Ogletown-Stanton Rd, Newark, DE 19713", "phone": "(302) 623-4500"}],
    "FL": [{"name": "Moffitt Cancer Center – Lung Screening", "address": "12902 USF Magnolia Dr, Tampa, FL 33612", "phone": "(813) 745-4673"}],
    "GA": [{"name": "Winship Cancer Institute – Emory", "address": "1365 Clifton Rd NE, Atlanta, GA 30322", "phone": "(404) 778-1900"}],
    "HI": [{"name": "University of Hawaii Cancer Center", "address": "701 Ilalo St, Honolulu, HI 96813", "phone": "(808) 586-3010"}],
    "ID": [{"name": "St. Luke's Mountain States Tumor Institute", "address": "100 E Idaho St, Boise, ID 83712", "phone": "(208) 381-2711"}],
    "IL": [{"name": "Robert H. Lurie Comprehensive Cancer Center", "address": "675 N St. Clair St, Chicago, IL 60611", "phone": "(312) 695-0990"}],
    "IN": [{"name": "IU Health Melvin & Bren Simon Cancer Center", "address": "535 Barnhill Dr, Indianapolis, IN 46202", "phone": "(317) 944-5000"}],
    "IA": [{"name": "University of Iowa Holden Comprehensive Cancer Center", "address": "200 Hawkins Dr, Iowa City, IA 52242", "phone": "(319) 356-4200"}],
    "KS": [{"name": "University of Kansas Cancer Center", "address": "4350 Shawnee Mission Pkwy, Westwood, KS 66205", "phone": "(913) 588-1227"}],
    "KY": [{"name": "UK Markey Cancer Center – Lung Screening", "address": "800 Rose St, Lexington, KY 40536", "phone": "(859) 257-4500"}],
    "LA": [{"name": "LSU Health New Orleans – Feist-Weiller Cancer Center", "address": "1501 Kings Hwy, Shreveport, LA 71103", "phone": "(318) 675-5000"}],
    "ME": [{"name": "Maine Medical Center – Cancer Care", "address": "22 Bramhall St, Portland, ME 04102", "phone": "(207) 662-0111"}],
    "MD": [{"name": "Johns Hopkins Sidney Kimmel Cancer Center", "address": "401 N Broadway, Baltimore, MD 21231", "phone": "(410) 955-8964"}],
    "MA": [{"name": "Dana-Farber/Brigham Lung Screening", "address": "450 Brookline Ave, Boston, MA 02215", "phone": "(617) 632-3000"}],
    "MI": [{"name": "University of Michigan Rogel Cancer Center", "address": "1500 E Medical Center Dr, Ann Arbor, MI 48109", "phone": "(800) 865-1125"}],
    "MN": [{"name": "Mayo Clinic – Lung Cancer Screening", "address": "200 First St SW, Rochester, MN 55905", "phone": "(507) 284-2511"}],
    "MS": [{"name": "University of Mississippi Medical Center – Cancer Center", "address": "2500 N State St, Jackson, MS 39216", "phone": "(601) 984-5590"}],
    "MO": [{"name": "Siteman Cancer Center – Washington University", "address": "4921 Parkview Pl, St. Louis, MO 63110", "phone": "(314) 747-7222"}],
    "MT": [{"name": "Billings Clinic Cancer Center", "address": "2800 10th Ave N, Billings, MT 59101", "phone": "(406) 238-2501"}],
    "NE": [{"name": "Fred & Pamela Buffett Cancer Center", "address": "987680 Nebraska Medical Center, Omaha, NE 68198", "phone": "(402) 559-5600"}],
    "NV": [{"name": "Nevada Cancer Research Foundation – Las Vegas", "address": "3838 Meadows Ln, Las Vegas, NV 89107", "phone": "(702) 384-0013"}],
    "NH": [{"name": "Dartmouth Health Norris Cotton Cancer Center", "address": "1 Medical Center Dr, Lebanon, NH 03756", "phone": "(603) 650-5527"}],
    "NJ": [{"name": "Rutgers Cancer Institute of New Jersey", "address": "195 Little Albany St, New Brunswick, NJ 08903", "phone": "(732) 235-2465"}],
    "NM": [{"name": "UNM Comprehensive Cancer Center", "address": "1201 Camino de Salud NE, Albuquerque, NM 87102", "phone": "(505) 272-4946"}],
    "NY": [{"name": "Memorial Sloan Kettering – Lung Screening", "address": "1275 York Ave, New York, NY 10065", "phone": "(212) 639-2000"}],
    "NC": [{"name": "UNC Lineberger Comprehensive Cancer Center", "address": "450 West Dr, Chapel Hill, NC 27599", "phone": "(984) 974-8200"}],
    "ND": [{"name": "Sanford Cancer Center – Fargo", "address": "801 Broadway N, Fargo, ND 58122", "phone": "(701) 234-2000"}],
    "OH": [{"name": "Cleveland Clinic Taussig Cancer Institute", "address": "9500 Euclid Ave, Cleveland, OH 44195", "phone": "(216) 444-7923"}],
    "OK": [{"name": "OU Health Stephenson Cancer Center", "address": "800 NE 10th St, Oklahoma City, OK 73104", "phone": "(405) 271-1111"}],
    "OR": [{"name": "OHSU Knight Cancer Institute", "address": "3181 SW Sam Jackson Park Rd, Portland, OR 97239", "phone": "(503) 494-1617"}],
    "PA": [{"name": "Penn Medicine Abramson Cancer Center", "address": "3400 Civic Center Blvd, Philadelphia, PA 19104", "phone": "(215) 662-6334"}],
    "RI": [{"name": "Lifespan Cancer Institute – Providence", "address": "593 Eddy St, Providence, RI 02903", "phone": "(401) 444-8550"}],
    "SC": [{"name": "MUSC Hollings Cancer Center", "address": "86 Jonathan Lucas St, Charleston, SC 29425", "phone": "(843) 792-9300"}],
    "SD": [{"name": "Avera Cancer Institute – Sioux Falls", "address": "1000 E 23rd St, Sioux Falls, SD 57105", "phone": "(605) 322-3800"}],
    "TN": [{"name": "Vanderbilt-Ingram Cancer Center", "address": "2220 Pierce Ave, Nashville, TN 37232", "phone": "(615) 936-1782"}],
    "TX": [{"name": "MD Anderson Cancer Center – Lung Screening", "address": "1515 Holcombe Blvd, Houston, TX 77030", "phone": "(877) 632-6789"}],
    "UT": [{"name": "Huntsman Cancer Institute – Lung Screening", "address": "2000 Circle of Hope Dr, Salt Lake City, UT 84112", "phone": "(801) 585-0303"}],
    "VT": [{"name": "UVM Cancer Center", "address": "89 Beaumont Ave, Burlington, VT 05405", "phone": "(802) 656-4414"}],
    "VA": [{"name": "UVA Cancer Center – Lung Screening", "address": "1240 Lee St, Charlottesville, VA 22908", "phone": "(434) 924-9333"}],
    "WA": [{"name": "Seattle Cancer Care Alliance – Lung Screening", "address": "825 Eastlake Ave E, Seattle, WA 98109", "phone": "(206) 606-7222"}],
    "WV": [{"name": "WVU Cancer Institute – Mary Babb Randolph", "address": "1 Medical Center Dr, Morgantown, WV 26506", "phone": "(304) 598-4500"}],
    "WI": [{"name": "UW Carbone Cancer Center – Lung Screening", "address": "600 Highland Ave, Madison, WI 53792", "phone": "(608) 265-1700"}],
    "WY": [{"name": "Wyoming Cancer Program – Cheyenne", "address": "2301 House Ave, Cheyenne, WY 82001", "phone": "(307) 635-4141"}],
    "DC": [{"name": "Georgetown Lombardi Comprehensive Cancer Center", "address": "3800 Reservoir Rd NW, Washington, DC 20007", "phone": "(202) 444-4000"}],
    "PR": [{"name": "UPR Comprehensive Cancer Center", "address": "PMB 711, 89 De Diego Ave Suite 105, San Juan, PR 00927", "phone": "(787) 772-8300"}],
}

# ZIP prefix → state code (first 3 digits cover most states)
ZIP_PREFIX_TO_STATE = {
    "005": "PR","006": "PR","007": "PR","008": "PR","009": "PR",
    "010": "MA","011": "MA","012": "MA","013": "MA","014": "MA","015": "MA","016": "MA","017": "MA","018": "MA","019": "MA",
    "020": "MA","021": "MA","022": "MA","023": "MA","024": "MA","025": "MA","026": "MA","027": "MA",
    "028": "RI","029": "RI",
    "030": "NH","031": "NH","032": "NH","033": "NH","034": "NH","035": "NH","036": "NH","037": "NH","038": "NH",
    "039": "ME","040": "ME","041": "ME","042": "ME","043": "ME","044": "ME","045": "ME","046": "ME","047": "ME","048": "ME","049": "ME",
    "050": "VT","051": "VT","052": "VT","053": "VT","054": "VT","056": "VT","057": "VT","058": "VT","059": "VT",
    "060": "CT","061": "CT","062": "CT","063": "CT","064": "CT","065": "CT","066": "CT","067": "CT","068": "CT","069": "CT",
    "070": "NJ","071": "NJ","072": "NJ","073": "NJ","074": "NJ","075": "NJ","076": "NJ","077": "NJ","078": "NJ","079": "NJ",
    "080": "NJ","081": "NJ","082": "NJ","083": "NJ","084": "NJ","085": "NJ","086": "NJ","087": "NJ","088": "NJ","089": "NJ",
    "100": "NY","101": "NY","102": "NY","103": "NY","104": "NY","105": "NY","106": "NY","107": "NY","108": "NY","109": "NY",
    "110": "NY","111": "NY","112": "NY","113": "NY","114": "NY","115": "NY","116": "NY","117": "NY","118": "NY","119": "NY",
    "120": "NY","121": "NY","122": "NY","123": "NY","124": "NY","125": "NY","126": "NY","127": "NY","128": "NY","129": "NY",
    "130": "NY","131": "NY","132": "NY","133": "NY","134": "NY","135": "NY","136": "NY","137": "NY","138": "NY","139": "NY",
    "140": "NY","141": "NY","142": "NY","143": "NY","144": "NY","145": "NY","146": "NY","147": "NY","148": "NY","149": "NY",
    "150": "PA","151": "PA","152": "PA","153": "PA","154": "PA","155": "PA","156": "PA","157": "PA","158": "PA","159": "PA",
    "160": "PA","161": "PA","162": "PA","163": "PA","164": "PA","165": "PA","166": "PA","167": "PA","168": "PA","169": "PA",
    "170": "PA","171": "PA","172": "PA","173": "PA","174": "PA","175": "PA","176": "PA","177": "PA","178": "PA","179": "PA",
    "180": "PA","181": "PA","182": "PA","183": "PA","184": "PA","185": "PA","186": "PA","187": "PA","188": "PA","189": "PA",
    "190": "PA","191": "PA","192": "PA","193": "PA","194": "PA","195": "PA","196": "PA",
    "197": "DE","198": "DE","199": "DE",
    "200": "DC","201": "DC","202": "DC","203": "DC","204": "DC","205": "DC",
    "206": "MD","207": "MD","208": "MD","209": "MD","210": "MD","211": "MD","212": "MD","213": "MD","214": "MD",
    "215": "MD","216": "MD","217": "MD","218": "MD","219": "MD",
    "220": "VA","221": "VA","222": "VA","223": "VA","224": "VA","225": "VA","226": "VA","227": "VA","228": "VA","229": "VA",
    "230": "VA","231": "VA","232": "VA","233": "VA","234": "VA","235": "VA","236": "VA","237": "VA","238": "VA","239": "VA",
    "240": "VA","241": "VA","242": "VA","243": "VA","244": "VA","245": "VA","246": "VA",
    "247": "WV","248": "WV","249": "WV","250": "WV","251": "WV","252": "WV","253": "WV","254": "WV","255": "WV",
    "256": "WV","257": "WV","258": "WV","259": "WV","260": "WV","261": "WV","262": "WV","263": "WV","264": "WV","265": "WV",
    "266": "WV","267": "WV","268": "WV",
    "270": "NC","271": "NC","272": "NC","273": "NC","274": "NC","275": "NC","276": "NC","277": "NC","278": "NC","279": "NC",
    "280": "NC","281": "NC","282": "NC","283": "NC","284": "NC","285": "NC","286": "NC","287": "NC","288": "NC","289": "NC",
    "290": "SC","291": "SC","292": "SC","293": "SC","294": "SC","295": "SC","296": "SC","297": "SC","298": "SC","299": "SC",
    "300": "GA","301": "GA","302": "GA","303": "GA","304": "GA","305": "GA","306": "GA","307": "GA","308": "GA","309": "GA",
    "310": "GA","311": "GA","312": "GA","313": "GA","314": "GA","315": "GA","316": "GA","317": "GA","318": "GA","319": "GA",
    "320": "FL","321": "FL","322": "FL","323": "FL","324": "FL","325": "FL","326": "FL","327": "FL","328": "FL","329": "FL",
    "330": "FL","331": "FL","332": "FL","333": "FL","334": "FL","335": "FL","336": "FL","337": "FL","338": "FL",
    "339": "FL","340": "FL","341": "FL","342": "FL","344": "FL","346": "FL","347": "FL","349": "FL",
    "350": "AL","351": "AL","352": "AL","354": "AL","355": "AL","356": "AL","357": "AL","358": "AL","359": "AL",
    "360": "AL","361": "AL","362": "AL","363": "AL","364": "AL","365": "AL","366": "AL","367": "AL","368": "AL","369": "AL",
    "370": "TN","371": "TN","372": "TN","373": "TN","374": "TN","375": "TN","376": "TN","377": "TN","378": "TN","379": "TN",
    "380": "TN","381": "TN","382": "TN","383": "TN","384": "TN","385": "TN",
    "386": "MS","387": "MS","388": "MS","389": "MS","390": "MS","391": "MS","392": "MS","393": "MS","394": "MS","395": "MS","396": "MS","397": "MS",
    "398": "GA","399": "GA",
    "400": "KY","401": "KY","402": "KY","403": "KY","404": "KY","405": "KY","406": "KY","407": "KY","408": "KY","409": "KY",
    "410": "KY","411": "KY","412": "KY","413": "KY","414": "KY","415": "KY","416": "KY","417": "KY","418": "KY",
    "420": "KY","421": "KY","422": "KY","423": "KY","424": "KY","425": "KY","426": "KY","427": "KY",
    "430": "OH","431": "OH","432": "OH","433": "OH","434": "OH","435": "OH","436": "OH","437": "OH","438": "OH","439": "OH",
    "440": "OH","441": "OH","442": "OH","443": "OH","444": "OH","445": "OH","446": "OH","447": "OH","448": "OH","449": "OH",
    "450": "OH","451": "OH","452": "OH","453": "OH","454": "OH","455": "OH","456": "OH","457": "OH","458": "OH",
    "460": "IN","461": "IN","462": "IN","463": "IN","464": "IN","465": "IN","466": "IN","467": "IN","468": "IN","469": "IN",
    "470": "IN","471": "IN","472": "IN","473": "IN","474": "IN","475": "IN","476": "IN","477": "IN","478": "IN","479": "IN",
    "480": "MI","481": "MI","482": "MI","483": "MI","484": "MI","485": "MI","486": "MI","487": "MI","488": "MI","489": "MI",
    "490": "MI","491": "MI","492": "MI","493": "MI","494": "MI","495": "MI","496": "MI","497": "MI","498": "MI","499": "MI",
    "500": "IA","501": "IA","502": "IA","503": "IA","504": "IA","505": "IA","506": "IA","507": "IA","508": "IA","509": "IA",
    "510": "IA","511": "IA","512": "IA","513": "IA","514": "IA","515": "IA","516": "IA","520": "IA","521": "IA","522": "IA",
    "523": "IA","524": "IA","525": "IA","526": "IA","527": "IA","528": "IA",
    "530": "WI","531": "WI","532": "WI","534": "WI","535": "WI","537": "WI","538": "WI","539": "WI",
    "540": "WI","541": "WI","542": "WI","543": "WI","544": "WI","545": "WI","546": "WI","547": "WI","548": "WI","549": "WI",
    "550": "MN","551": "MN","553": "MN","554": "MN","555": "MN","556": "MN","557": "MN","558": "MN","559": "MN",
    "560": "MN","561": "MN","562": "MN","563": "MN","564": "MN","565": "MN","566": "MN","567": "MN",
    "570": "SD","571": "SD","572": "SD","573": "SD","574": "SD","575": "SD","576": "SD","577": "SD",
    "580": "ND","581": "ND","582": "ND","583": "ND","584": "ND","585": "ND","586": "ND","587": "ND","588": "ND",
    "590": "MT","591": "MT","592": "MT","593": "MT","594": "MT","595": "MT","596": "MT","597": "MT","598": "MT","599": "MT",
    "600": "IL","601": "IL","602": "IL","603": "IL","604": "IL","605": "IL","606": "IL","607": "IL","608": "IL","609": "IL",
    "610": "IL","611": "IL","612": "IL","613": "IL","614": "IL","615": "IL","616": "IL","617": "IL","618": "IL","619": "IL",
    "620": "IL","621": "IL","622": "IL","623": "IL","624": "IL","625": "IL","626": "IL","627": "IL","628": "IL","629": "IL",
    "630": "MO","631": "MO","633": "MO","634": "MO","635": "MO","636": "MO","637": "MO","638": "MO","639": "MO",
    "640": "MO","641": "MO","644": "MO","645": "MO","646": "MO","647": "MO","648": "MO",
    "650": "MO","651": "MO","652": "MO","653": "MO","654": "MO","655": "MO","656": "MO","657": "MO","658": "MO",
    "660": "KS","661": "KS","662": "KS","664": "KS","665": "KS","666": "KS","667": "KS","668": "KS","669": "KS",
    "670": "KS","671": "KS","672": "KS","673": "KS","674": "KS","675": "KS","676": "KS","677": "KS","678": "KS","679": "KS",
    "680": "NE","681": "NE","683": "NE","684": "NE","685": "NE","686": "NE","687": "NE","688": "NE","689": "NE",
    "690": "NE","691": "NE","692": "NE","693": "NE",
    "700": "LA","701": "LA","703": "LA","704": "LA","705": "LA","706": "LA","707": "LA","708": "LA",
    "710": "LA","711": "LA","712": "LA","713": "LA","714": "LA",
    "716": "AR","717": "AR","718": "AR","719": "AR","720": "AR","721": "AR","722": "AR","723": "AR","724": "AR","725": "AR",
    "726": "AR","727": "AR","728": "AR","729": "AR",
    "730": "OK","731": "OK","733": "OK","734": "OK","735": "OK","736": "OK","737": "OK","738": "OK","739": "OK",
    "740": "OK","741": "OK","743": "OK","744": "OK","745": "OK","746": "OK","747": "OK","748": "OK","749": "OK",
    "750": "TX","751": "TX","752": "TX","753": "TX","754": "TX","755": "TX","756": "TX","757": "TX","758": "TX","759": "TX",
    "760": "TX","761": "TX","762": "TX","763": "TX","764": "TX","765": "TX","766": "TX","767": "TX","768": "TX","769": "TX",
    "770": "TX","771": "TX","772": "TX","773": "TX","774": "TX","775": "TX","776": "TX","777": "TX","778": "TX","779": "TX",
    "780": "TX","781": "TX","782": "TX","783": "TX","784": "TX","785": "TX","786": "TX","787": "TX","788": "TX","789": "TX",
    "790": "TX","791": "TX","792": "TX","793": "TX","794": "TX","795": "TX","796": "TX","797": "TX","798": "TX","799": "TX",
    "800": "CO","801": "CO","802": "CO","803": "CO","804": "CO","805": "CO","806": "CO","807": "CO","808": "CO","809": "CO",
    "810": "CO","811": "CO","812": "CO","813": "CO","814": "CO","815": "CO","816": "CO",
    "820": "WY","821": "WY","822": "WY","823": "WY","824": "WY","825": "WY","826": "WY","827": "WY","828": "WY","829": "WY","830": "WY","831": "WY",
    "832": "ID","833": "ID","834": "ID","835": "ID","836": "ID","837": "ID","838": "ID",
    "840": "UT","841": "UT","842": "UT","843": "UT","844": "UT","845": "UT","846": "UT","847": "UT",
    "850": "AZ","851": "AZ","852": "AZ","853": "AZ","855": "AZ","856": "AZ","857": "AZ","859": "AZ","860": "AZ","863": "AZ","864": "AZ","865": "AZ",
    "870": "NM","871": "NM","872": "NM","873": "NM","874": "NM","875": "NM","877": "NM","878": "NM","879": "NM","880": "NM","881": "NM","882": "NM","883": "NM","884": "NM",
    "885": "TX",
    "890": "NV","891": "NV","893": "NV","894": "NV","895": "NV","897": "NV","898": "NV",
    "900": "CA","901": "CA","902": "CA","903": "CA","904": "CA","905": "CA","906": "CA","907": "CA","908": "CA","910": "CA",
    "911": "CA","912": "CA","913": "CA","914": "CA","915": "CA","916": "CA","917": "CA","918": "CA","919": "CA","920": "CA",
    "921": "CA","922": "CA","923": "CA","924": "CA","925": "CA","926": "CA","927": "CA","928": "CA","930": "CA","931": "CA",
    "932": "CA","933": "CA","934": "CA","935": "CA","936": "CA","937": "CA","938": "CA","939": "CA","940": "CA","941": "CA",
    "942": "CA","943": "CA","944": "CA","945": "CA","946": "CA","947": "CA","948": "CA","949": "CA","950": "CA","951": "CA",
    "952": "CA","953": "CA","954": "CA","955": "CA","956": "CA","957": "CA","958": "CA","959": "CA","960": "CA","961": "CA",
    "967": "HI","968": "HI",
    "970": "OR","971": "OR","972": "OR","973": "OR","974": "OR","975": "OR","976": "OR","977": "OR","978": "OR","979": "OR",
    "980": "WA","981": "WA","982": "WA","983": "WA","984": "WA","985": "WA","986": "WA","988": "WA","989": "WA","990": "WA",
    "991": "WA","992": "WA","993": "WA","994": "WA",
    "995": "AK","996": "AK","997": "AK","998": "AK","999": "AK",
}

def get_state_from_zip(zip_code):
    """Return 2-letter state abbreviation from ZIP code."""
    if not zip_code or len(zip_code) < 3:
        return None
    return ZIP_PREFIX_TO_STATE.get(zip_code[:3], None)

# ─────────────────────────────────────────
#  INDIANA SCREENING LOCATIONS (curated)
# ─────────────────────────────────────────
screening_locations = [
    {"name": "IU Health North Hospital – Lung Screening", "address": "11700 N Meridian St, Carmel, IN 46032", "phone": "(317) 688-2000", "note": "LDCT lung screening; referral or self-referral accepted", "url": "https://iuhealth.org"},
    {"name": "Ascension St. Vincent Carmel", "address": "13500 N Meridian St, Carmel, IN 46032", "phone": "(317) 582-7000", "note": "Comprehensive cancer screening & pulmonology", "url": "https://healthcare.ascension.org"},
    {"name": "Community Health Network – North", "address": "8051 Clearvista Pkwy, Indianapolis, IN 46256", "phone": "(317) 621-5000", "note": "Low-dose CT lung screenings; most insurance accepted", "url": "https://ecommunity.com"},
    {"name": "IU Health Methodist – Thoracic Oncology", "address": "1801 N Senate Blvd, Indianapolis, IN 46202", "phone": "(317) 962-2000", "note": "Academic medical center; high-risk lung program", "url": "https://iuhealth.org"},
    {"name": "Franciscan Health Indianapolis", "address": "8111 S Emerson Ave, Indianapolis, IN 46237", "phone": "(317) 528-5000", "note": "Lung cancer screening; ACR-accredited imaging", "url": "https://franciscanhealth.org"},
    {"name": "Aspire Indiana Health – Noblesville", "address": "1552 Union Chapel Rd, Noblesville, IN 46060", "phone": "(800) 342-5653", "note": "Community health center; sliding-scale fees available", "url": "https://aspireindiana.org"},
    {"name": "IU Health Tipton Hospital", "address": "1000 S Main St, Tipton, IN 46072", "phone": "(765) 675-8500", "note": "Convenient for northern Hamilton County residents", "url": "https://iuhealth.org"},
    {"name": "Hendricks Regional Health", "address": "1000 E Main St, Danville, IN 46122", "phone": "(317) 745-4451", "note": "Serves Hendricks County area; radiology & screening programs", "url": "https://hendricks.org"},
    {"name": "Franciscan Health Mooresville", "address": "1201 Hadley Rd, Mooresville, IN 46158", "phone": "(317) 831-1160", "note": "Serves Morgan County; cancer screening available", "url": "https://franciscanhealth.org"},
    {"name": "IU Health Morgan Hospital", "address": "2209 John R Wooden Dr, Martinsville, IN 46151", "phone": "(765) 342-8441", "note": "Morgan County lung screening services", "url": "https://iuhealth.org"},
    {"name": "Putnam County Hospital", "address": "1542 Bloomington St, Greencastle, IN 46135", "phone": "(765) 653-5121", "note": "Serves Greencastle/DePauw area; imaging & screening", "url": "https://pchosp.org"},
    {"name": "Franciscan Health Crawfordsville", "address": "1710 Lafayette Rd, Crawfordsville, IN 47933", "phone": "(765) 362-2800", "note": "Serves west-central Indiana; cancer screening programs", "url": "https://franciscanhealth.org"},
    {"name": "IU Health Bloomington – Lung Screening", "address": "601 W 2nd St, Bloomington, IN 47403", "phone": "(812) 353-5555", "note": "Monroe County; comprehensive cancer & lung program", "url": "https://iuhealth.org"},
    {"name": "IU Health Fort Wayne", "address": "700 Broadway, Fort Wayne, IN 46802", "phone": "(260) 450-5000", "note": "Allen County lung cancer screening & pulmonology", "url": "https://iuhealth.org"},
    {"name": "Parkview Cancer Institute – Fort Wayne", "address": "11050 Parkview Circle, Fort Wayne, IN 46845", "phone": "(260) 266-4000", "note": "Dedicated cancer center; LDCT screening available", "url": "https://parkview.com"},
    {"name": "Memorial Hospital – South Bend", "address": "615 N Michigan St, South Bend, IN 46601", "phone": "(574) 647-1000", "note": "St. Joseph County; lung screening & oncology", "url": "https://beaconhealthsystem.org"},
    {"name": "Franciscan Health Lafayette", "address": "1701 S Creasy Ln, Lafayette, IN 47905", "phone": "(765) 502-4000", "note": "Serves Tippecanoe County; cancer screening programs", "url": "https://franciscanhealth.org"},
    {"name": "Deaconess Cancer Institute – Evansville", "address": "600 Mary St, Evansville, IN 47747", "phone": "(812) 450-5000", "note": "SW Indiana; comprehensive lung cancer program", "url": "https://deaconess.com"},
    {"name": "IU Health Ball Memorial – Muncie", "address": "2401 University Ave, Muncie, IN 47303", "phone": "(765) 747-3111", "note": "Delaware County; lung screening & pulmonology", "url": "https://iuhealth.org"},
    {"name": "Reid Health – Richmond", "address": "1401 Chester Blvd, Richmond, IN 47374", "phone": "(765) 983-3000", "note": "Wayne County; cancer screening & imaging services", "url": "https://reidhealth.org"},
]

DEFAULT_LOCATIONS = [3, 0]

def get_indiana_locations(zip_code):
    fine = {
        "46032": [0, 1], "46033": [0, 1], "46074": [0, 1], "46077": [0, 1],
        "46060": [5, 2], "46062": [5, 2], "46038": [2, 0],
        "46220": [2, 3], "46240": [2, 0], "46250": [2, 0],
        "46256": [2, 0], "46280": [0, 2], "46290": [0, 2],
        "46201": [3, 2], "46202": [3, 2], "46204": [3, 2],
        "46205": [3, 2], "46208": [3, 2],
        "46217": [4, 3], "46227": [4, 3], "46237": [4, 3],
        "46142": [4, 3], "46143": [4, 3], "46131": [4, 3],
        "46112": [7, 4], "46122": [7, 4], "46123": [7, 4],
        "46158": [8, 9], "46151": [9, 8],
        "46135": [10, 11], "46170": [10, 11], "46172": [10, 11],
        "47933": [11, 16],
        "47401": [12, 3], "47403": [12, 3], "47404": [12, 3],
        "47405": [12, 3], "47408": [12, 3],
        "46802": [13, 14], "46804": [13, 14], "46805": [13, 14],
        "46814": [13, 14], "46845": [14, 13],
        "46601": [15, 3], "46614": [15, 3], "46628": [15, 3],
        "47901": [16, 3], "47904": [16, 3], "47906": [16, 3],
        "47710": [17, 3], "47711": [17, 3], "47712": [17, 3],
        "47303": [18, 3], "47304": [18, 3], "47306": [18, 3],
        "47374": [19, 18],
        "46901": [6, 2], "46902": [6, 2],
        "46011": [2, 3], "46012": [2, 3], "46013": [2, 3],
    }
    routing = {
        "462": [3, 2], "460": [0, 1], "474": [12, 3],
        "468": [13, 14], "466": [15, 3], "479": [16, 3],
        "477": [17, 3], "473": [18, 3],
    }
    if zip_code in fine:
        idxs = fine[zip_code]
    elif zip_code[:3] in routing:
        idxs = routing[zip_code[:3]]
    else:
        idxs = DEFAULT_LOCATIONS
    return [screening_locations[i] for i in idxs]

def get_nearby_locations(zip_code):
    """Return screening locations. Indiana: curated. Other states: state-level fallback."""
    if not zip_code or len(zip_code) != 5 or not zip_code.isdigit():
        return [], None, None

    state = get_state_from_zip(zip_code)

    if zip_code in indiana_zips or state == "IN":
        locs = get_indiana_locations(zip_code)
        return [{"name": l["name"], "address": l["address"], "phone": l["phone"],
                 "note": l.get("note", ""), "is_fallback": False} for l in locs], state, False
    elif state and state in STATE_SCREENING_FALLBACK:
        locs = STATE_SCREENING_FALLBACK[state]
        return [{"name": l["name"], "address": l["address"], "phone": l["phone"],
                 "note": "Major cancer center in your state", "is_fallback": True} for l in locs], state, True
    else:
        return [], state, None

# ─────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────
log_file = "usage_log.csv"

def log_usage(data):
    exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        fields = list(data.keys())
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow(data)
    try:
        requests.post(SHEETS_WEBHOOK, json=data, timeout=5)
    except Exception:
        pass

# ─────────────────────────────────────────
#  RISK MODEL (PLCOm2012)
# ─────────────────────────────────────────
def logistic(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def plco_m2012(age, race, education, bmi, copd, cancer_hist, family_hist,
               smoking_status, smoking_intensity, duration_smoking, smoking_quit_time):
    m = (
          0.0778868  * (age - 62)
        - 0.0812744  * (education - 4)
        - 0.0274194  * (bmi - 27)
        + 0.3553063  * copd
        + 0.4589971  * cancer_hist
        + 0.587185   * family_hist
        + 0.2597431  * smoking_status
        + 0.0317321  * (duration_smoking - 27)
        - 0.0308572  * (smoking_quit_time - 10)
        - 4.532506
    )
    if smoking_status == 1 and smoking_intensity > 0:
        m += -1.822606 * ((smoking_intensity / 10) ** (-1) - 0.4021541613)
    return logistic(m)

def extrapolate_risk(age, race, education, bmi, copd, cancer_hist, family_hist,
                     smoking_status, smoking_intensity, duration_smoking, smoking_quit_time):
    if age < 40:
        base_risk = plco_m2012(40, race, education, bmi, copd, cancer_hist, family_hist,
                               smoking_status, smoking_intensity, duration_smoking, smoking_quit_time)
        scale = math.exp(-0.065 * (40 - age))
        return base_risk * scale
    elif age > 80:
        return plco_m2012(80, race, education, bmi, copd, cancer_hist, family_hist,
                          smoking_status, smoking_intensity, duration_smoking, smoking_quit_time)
    else:
        return plco_m2012(age, race, education, bmi, copd, cancer_hist, family_hist,
                          smoking_status, smoking_intensity, duration_smoking, smoking_quit_time)

def lung_age_from_risk(actual_age, risk_pct):
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
    return max(10, min(100, actual_age + offset))

def risk_category(risk_pct, age):
    if risk_pct >= 3.0:
        return "high", 3.0
    elif risk_pct >= 1.3:
        return "moderate", 1.3
    else:
        return "low", 1.3

def uspstf_qualifies(age, smoking_status, pack_years):
    if smoking_status == "Never":
        return False, "Non-smokers do not qualify for USPSTF lung screening guidelines."
    if age < 50 or age > 80:
        return False, f"USPSTF guidelines apply to ages 50–80 (your age: {age})."
    if pack_years < 20:
        return False, f"USPSTF requires ≥20 pack-years (yours: {pack_years:.1f})."
    return True, "You meet all USPSTF 2021 criteria for annual low-dose CT (LDCT) lung screening."

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
            <div class="stat-item"><span class="stat-num">236K</span><span class="stat-label">New Cases / Year</span></div>
            <div class="stat-item"><span class="stat-num">80%</span><span class="stat-label">Survival if caught early</span></div>
            <div class="stat-item"><span class="stat-num">#1</span><span class="stat-label">Cancer Killer in US</span></div>
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

zip_input_val = st.session_state.get("zip_input", "")
is_five_digits = len(zip_input_val) == 5 and zip_input_val.isdigit()
detected_state = get_state_from_zip(zip_input_val) if is_five_digits else None
is_in_indiana = zip_input_val in indiana_zips or detected_state == "IN"

zip_css_class = "zip-valid" if is_five_digits else ""
st.markdown(f'<div class="{zip_css_class}">', unsafe_allow_html=True)
zip_code = st.text_input("ZIP Code", placeholder="e.g. 46032", key="zip_input", max_chars=5)
st.markdown('</div>', unsafe_allow_html=True)

if zip_code:
    if is_five_digits and is_in_indiana:
        st.markdown('<div class="zip-status ok">✓ Indiana ZIP recognized — nearby screening locations loaded</div>', unsafe_allow_html=True)
    elif is_five_digits and detected_state:
        st.markdown(f'<div class="zip-status ok">✓ {detected_state} ZIP recognized — screening center for your state loaded</div>', unsafe_allow_html=True)
    elif is_five_digits:
        st.markdown('<div class="zip-status warn">⚠ ZIP code not recognized — please double-check and re-enter</div>', unsafe_allow_html=True)

# ── Urban/Rural ──
st.markdown(info_tip("Where do you live?",
    "Urban/rural setting affects lung cancer risk through differences in air quality, occupational exposures, access to healthcare, and smoking rates. This helps us understand screening gaps across different community types."), unsafe_allow_html=True)
area_type = st.selectbox(
    "Area type",
    ["City (urban)", "Suburb", "Rural / small town"],
    label_visibility="collapsed",
    key="area_type"
)

# ── Demographics ──
st.markdown('<div class="section-label">👤 About You</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=10, max_value=100, value=55, step=1, format="%d")
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

# Validate required fields before processing
if run and not zip_code:
    st.error("⚠️ Please enter your ZIP code before submitting.")
    run = False
elif run and not is_five_digits:
    st.error("⚠️ Please enter a valid 5-digit ZIP code.")
    run = False

# ─────────────────────────────────────────
#  RESULTS
# ─────────────────────────────────────────
if run:
    risk = extrapolate_risk(
        age, race, education_val, bmi, copd, cancer_hist, family_hist,
        smoking_status_val, cigs, years, quit
    )
    risk_pct = risk * 100
    category, threshold = risk_category(risk_pct, age)
    lung_age_val = lung_age_from_risk(age, risk_pct)
    age_diff = lung_age_val - age
    qualifies, qual_msg = uspstf_qualifies(age, smoking, pack_years)

    st.session_state.results = {
        "risk_pct": risk_pct, "category": category, "threshold": threshold,
        "lung_age_val": lung_age_val, "age_diff": age_diff,
        "qualifies": qualifies, "qual_msg": qual_msg,
        "age": age, "smoking": smoking, "pack_years": pack_years,
        "zip_code": zip_code, "race": race, "education_val": education_val,
        "bmi": bmi, "copd": copd, "cancer_hist": cancer_hist,
        "family_hist": family_hist, "cigs": cigs, "years": years,
        "area_type": area_type,
    }

    log_usage({
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": st.session_state.user_ip,
        "zip": zip_code or "",
        "state": get_state_from_zip(zip_code) or "",
        "area_type": area_type,                        # ← new field
        "age": age,
        "race": race,
        "education": education,
        "bmi": round(bmi, 1),
        "smoking_status": smoking,
        "pack_years": round(pack_years, 1),
        "copd": copd,
        "cancer_hist": cancer_hist,
        "family_hist": family_hist,
        "risk_pct": round(risk_pct, 3),
        "risk_group": category,
        "lung_age": lung_age_val,
        "uspstf_eligible": qualifies,
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
    area_type     = r["area_type"]

    if age < 40:
        st.markdown(f"""
        <div class="age-warn">
            ⚠️ <strong>Note for ages under 40:</strong> The PLCOm2012 model is clinically validated
            for ages 40–80. Because you are {age}, your result uses an age-extrapolated estimate.
            Lung cancer is rare under 40, but risk factors still matter for future health.
            Interpret your result as informational only.
        </div>
        """, unsafe_allow_html=True)

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

    # ── Screening Locations ──
    nearby, detected_state, is_fallback = get_nearby_locations(zip_code) if zip_code and len(zip_code) == 5 else ([], None, None)
    if nearby:
        st.markdown('<div class="section-label">📍 Screening Centers Near You</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if is_fallback:
            st.markdown(f'<div class="card-title">Major lung cancer screening center in {detected_state}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card-title">Facilities near your ZIP code that offer lung cancer screening</div>', unsafe_allow_html=True)
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

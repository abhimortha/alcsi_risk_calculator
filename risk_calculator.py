import streamlit as st
import numpy as np
import uuid
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
/* Always green outline when ZIP is exactly 5 digits (valid format) */
.zip-valid [data-testid="stTextInput"] input {
    border-color: #1B7A48 !important;
    box-shadow: 0 0 0 3px rgba(27,122,72,0.12) !important;
    background: #F0FFF8 !important;
}
/* No red for unrecognized — only green for valid 5-digit format */
.zip-status {
    font-size: 12.5px;
    font-weight: 500;
    margin-top: -10px;
    margin-bottom: 8px;
    padding: 0 2px;
}
.zip-status.ok  { color: #1B7A48; }
.zip-status.warn { color: #B06A00; }

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

/* Hide spinner buttons ONLY for the age input */
[data-testid="stNumberInput"]:has(input[aria-label="Age"]) button {
    display: none !important;
}
[data-testid="stNumberInput"]:has(input[aria-label="Age"]) > div {
    gap: 0 !important;
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
#  ZIP DATA — All Indiana ZIP codes (46xxx and 47xxx)
# ─────────────────────────────────────────
valid_zips = {
    # ── Marion County / Indianapolis ──
    "46201","46202","46203","46204","46205","46206","46207","46208",
    "46209","46210","46211","46214","46216","46217","46218","46219",
    "46220","46221","46222","46224","46225","46226","46227","46228",
    "46229","46230","46231","46234","46235","46236","46237","46239",
    "46240","46241","46242","46244","46247","46249","46250","46251",
    "46253","46254","46255","46256","46259","46260","46262","46268",
    "46274","46275","46277","46278","46280","46282","46283","46285",
    "46290","46291","46295","46296","46298",
    # ── Hamilton County (Carmel, Fishers, Noblesville, Westfield) ──
    "46032","46033","46034","46036","46037","46038","46040","46055",
    "46060","46061","46062","46063","46064","46074","46082",
    # ── Hendricks County (Avon, Brownsburg, Plainfield) ──
    "46077","46112","46113","46118","46121","46122","46123","46149",
    "46158","46167",
    # ── Johnson County (Greenwood, Franklin, Bargersville) ──
    "46107","46131","46142","46143","46160","46161","46162","46163",
    "46164","46181","46183","46184",
    # ── Boone County (Lebanon, Zionsville) ──
    "46052","46075","46077",
    # ── Putnam County (Greencastle / DePauw University area) ──
    "46105","46120","46124","46128","46135","46157","46165","46170",
    "46172",
    # ── Morgan County (Martinsville, Mooresville) ──
    "46106","46151","46158","46166",
    # ── Madison County (Anderson, Elwood) ──
    "46001","46011","46012","46013","46014","46015","46016","46017",
    "46030","46044","46045","46048","46049","46050","46051","46058",
    "46065","46069","46070","46071","46072","46076",
    # ── Hancock County (Greenfield) ──
    "46140","46148","46150","46155","46156",
    # ── Shelby County ──
    "46176",
    # ── Bartholomew County (Columbus) ──
    "47201","47202","47203",
    # ── Monroe County (Bloomington / IU) ──
    "47401","47402","47403","47404","47405","47406","47407","47408",
    # ── Tippecanoe County (Lafayette / Purdue) ──
    "47901","47902","47903","47904","47905","47906","47907","47909",
    # ── Allen County (Fort Wayne) ──
    "46801","46802","46803","46804","46805","46806","46807","46808",
    "46809","46814","46815","46816","46818","46819","46825","46835",
    "46845","46850","46851","46852","46853","46854","46855","46856",
    "46857","46858","46859","46860","46861","46862","46863","46864",
    "46865","46866","46867","46868","46869","46885","46895","46896",
    "46897","46898","46899",
    # ── St. Joseph County (South Bend, Mishawaka) ──
    "46530","46545","46550","46552","46554","46556","46560","46561",
    "46563","46565","46567","46570","46571","46572","46573","46574",
    "46580","46581","46582","46590","46595","46601","46604","46613",
    "46614","46615","46616","46617","46619","46620","46624","46626",
    "46628","46629","46634","46635","46637","46660","46680","46699",
    # ── Lake County (Gary, Hammond, Crown Point) ──
    "46301","46302","46303","46304","46320","46321","46322","46323",
    "46324","46325","46327","46340","46341","46342","46345","46346",
    "46347","46348","46349","46350","46351","46352","46355","46356",
    "46373","46374","46375","46376","46377","46379","46380","46381",
    "46382","46383","46384","46385","46390","46391","46392","46393",
    "46394","46395","46396","46397","46398","46399","46401","46402",
    "46403","46404","46405","46406","46407","46408","46409","46410",
    "46411",
    # ── Porter County (Valparaiso, Portage) ──
    "46304","46341","46370","46371","46372","46373","46374","46375",
    "46376","46382","46383","46384","46385","46390","46391","46392",
    # ── Elkhart County (Elkhart, Goshen) ──
    "46514","46515","46516","46517","46526","46527","46528",
    # ── Kosciusko County (Warsaw) ──
    "46580","46581","46582",
    # ── LaPorte County (Michigan City, La Porte) ──
    "46350","46352","46360","46361","46362","46365","46366","46367",
    "46368","46369",
    # ── Marshall County (Plymouth) ──
    "46563",
    # ── Cass County (Logansport) ──
    "46947","46950","46951",
    # ── Howard County (Kokomo) ──
    "46901","46902","46903","46904",
    # ── Grant County (Marion) ──
    "46952","46953","46960","46961","46962","46970","46971","46974",
    "46975","46978","46979","46980","46982","46984","46986","46987",
    "46988","46989","46990","46991","46992","46994","46995","46996",
    "46998",
    # ── Vigo County (Terre Haute) ──
    "47801","47802","47803","47804","47805","47807","47809",
    # ── Vanderburgh County (Evansville) ──
    "47710","47711","47712","47713","47714","47715","47720","47721",
    "47722","47724","47725","47728","47730","47731","47732","47733",
    "47734","47735","47736","47737","47738","47739","47740","47741",
    "47742","47743","47744","47747","47750",
    # ── Clark County (Jeffersonville, Clarksville) ──
    "47129","47130","47131","47132","47133","47134","47135","47136",
    "47140","47141","47142","47143","47144","47145","47146","47147",
    # ── Floyd County (New Albany) ──
    "47150","47151","47152","47160","47161","47162","47163","47164",
    "47165","47166","47167","47168","47170","47172","47174","47175",
    # ── Dearborn County (Lawrenceburg) ──
    "47001","47006","47010","47011","47012","47016","47017","47018",
    "47019","47020","47021","47022","47023","47024","47025",
    # ── Wayne County (Richmond) ──
    "47374","47375","47376",
    # ── Delaware County (Muncie) ──
    "47302","47303","47304","47305","47306","47307","47308",
    # ── Blackford / Jay County ──
    "47348","47356","47360","47361","47362","47366","47367","47368",
    "47369","47370","47371","47373","47380","47381","47382","47383",
    "47384","47385","47386","47387","47388","47390","47392","47393",
    "47394","47396",
    # ── Dubois County (Jasper) ──
    "47542","47546","47547","47549","47550","47553","47556","47557",
    "47558","47561","47562","47564","47567","47568","47573","47574",
    "47575","47576","47577","47578","47579","47580","47581","47584",
    "47585","47586","47588","47590","47591","47596","47597","47598",
    "47601","47610","47611","47612","47613","47614","47615","47616",
    "47617","47618","47619","47620","47629","47630","47631","47633",
    "47634","47635","47637","47638","47639","47640","47647","47648",
    "47649","47654","47660","47665","47666","47670","47683","47701",
    "47702","47703","47704","47705","47706","47708",
    # ── Additional southern Indiana ──
    "47102","47104","47106","47107","47108","47110","47111","47112",
    "47114","47115","47116","47117","47118","47119","47120","47122",
    "47123","47124","47125","47126","47137","47138","47139",
    # ── Additional central/northern Indiana ──
    "46101","46102","46103","46104","46105","46106","46107","46108",
    "46109","46110","46111","46113","46114","46115","46116","46117",
    "46118","46119","46120","46121","46122","46123","46124","46125",
    "46126","46127","46128","46129","46130","46131","46132","46133",
    "46135","46136","46138","46139","46140","46141","46142","46143",
    "46144","46145","46146","46147","46148","46149","46150","46151",
    "46152","46153","46154","46155","46156","46157","46158","46159",
    "46160","46161","46162","46163","46164","46165","46166","46167",
    "46168","46169","46170","46171","46172","46173","46174","46175",
    "46176","46177","46178","46179","46180","46181","46182","46183",
    "46184","46186","46187","46188",
    "46401","46402","46403","46404","46405","46406","46407","46408",
    "46409","46410","46411",
    "46501","46502","46504","46506","46507","46508","46510","46511",
    "46513","46514","46515","46516","46517","46524","46526","46527",
    "46528","46530","46531","46532","46534","46536","46537","46538",
    "46539","46540","46542","46543","46544","46545","46546","46550",
    "46552","46553","46554","46555","46556","46557","46558","46559",
    "46560","46561","46562","46563","46564","46565","46567","46570",
    "46571","46572","46573","46574","46580","46581","46582","46590",
    "46595",
    "46700","46701","46702","46703","46704","46705","46706","46710",
    "46711","46713","46714","46721","46723","46725","46730","46731",
    "46732","46733","46737","46738","46740","46741","46742","46743",
    "46745","46746","46747","46748","46750","46755","46759","46760",
    "46761","46763","46764","46765","46766","46767","46769","46770",
    "46771","46772","46773","46774","46775","46776","46777","46778",
    "46779","46780","46781","46782","46783","46784","46785","46786",
    "46787","46788","46789","46791","46792","46793","46794","46795",
    "46796","46797","46798","46799",
    "46900","46901","46902","46903","46904","46910","46911","46912",
    "46913","46914","46915","46916","46917","46919","46920","46921",
    "46922","46923","46924","46925","46926","46928","46929","46930",
    "46931","46932","46933","46935","46936","46937","46938","46939",
    "46940","46941","46942","46943","46945","46946","46947","46950",
    "46951","46952","46953","46954","46957","46958","46959","46960",
    "46961","46962","46963","46964","46965","46967","46968","46970",
    "46971","46974","46975","46978","46979","46980","46982","46984",
    "46985","46986","46987","46988","46989","46990","46991","46992",
    "46994","46995","46996","46998",
    "47001","47003","47006","47010","47011","47012","47016","47017",
    "47018","47019","47020","47021","47022","47023","47024","47025",
    "47030","47031","47032","47033","47034","47035","47036","47037",
    "47038","47039","47040","47041","47042","47043","47060",
    "47102","47104","47106","47107","47108","47110","47111","47112",
    "47114","47115","47116","47117","47118","47119","47120","47122",
    "47123","47124","47125","47126","47129","47130","47131","47132",
    "47135","47136","47137","47138","47140","47141","47142","47143",
    "47144","47145","47146","47147","47150","47151","47160","47161",
    "47162","47163","47164","47165","47166","47167","47170","47172",
    "47174","47175",
    "47201","47202","47203","47220","47224","47225","47226","47227",
    "47228","47229","47230","47231","47232","47234","47235","47236",
    "47240","47243","47244","47245","47246","47247","47250","47260",
    "47261","47262","47263","47264","47265","47270","47272","47273",
    "47274","47280","47281","47282","47283",
    "47302","47303","47304","47305","47306","47307","47308",
    "47320","47322","47324","47325","47326","47327","47330","47331",
    "47334","47335","47336","47337","47338","47339","47340","47341",
    "47342","47344","47345","47346","47348","47351","47352","47353",
    "47354","47355","47356","47357","47358","47359","47360","47361",
    "47362","47366","47367","47368","47369","47370","47371","47373",
    "47374","47375","47376","47380","47381","47382","47383","47384",
    "47385","47386","47387","47388","47390","47392","47393","47394",
    "47396",
    "47401","47402","47403","47404","47405","47406","47407","47408",
    "47420","47421","47424","47426","47427","47428","47429","47430",
    "47431","47432","47433","47434","47435","47436","47437","47438",
    "47439","47440","47441","47443","47445","47446","47448","47449",
    "47451","47452","47453","47454","47455","47456","47457","47458",
    "47459","47460","47462","47463","47464","47465","47467","47468",
    "47469","47470","47471","47490",
    "47501","47512","47513","47514","47515","47516","47519","47520",
    "47521","47522","47523","47524","47525","47527","47528","47529",
    "47531","47532","47535","47536","47537","47541","47542","47546",
    "47547","47549","47550","47551","47552","47553","47556","47557",
    "47558","47561","47562","47564","47567","47568","47573","47574",
    "47575","47576","47577","47578","47579","47580","47581","47584",
    "47585","47586","47588","47590","47591","47596","47597","47598",
    "47601","47610","47611","47612","47613","47614","47615","47616",
    "47617","47618","47619","47620","47629","47630","47631","47633",
    "47634","47635","47637","47638","47639","47640","47647","47648",
    "47649","47654","47660","47665","47666","47670","47683",
    "47701","47702","47703","47704","47705","47706","47708",
    "47710","47711","47712","47713","47714","47715","47720","47721",
    "47722","47724","47725","47728",
    "47801","47802","47803","47804","47805","47807","47809",
    "47831","47832","47833","47834","47836","47837","47838","47840",
    "47841","47842","47845","47846","47847","47848","47849","47850",
    "47853","47854","47855","47857","47858","47859","47860","47861",
    "47862","47863","47865","47866","47868","47869","47870","47871",
    "47872","47874","47875","47876","47878","47879","47880","47881",
    "47882","47884","47885",
    "47901","47902","47903","47904","47905","47906","47907","47909",
    "47916","47917","47918","47920","47921","47922","47923","47924",
    "47925","47926","47928","47929","47930","47932","47933","47940",
    "47941","47942","47943","47944","47946","47948","47949","47950",
    "47951","47952","47954","47955","47957","47958","47959","47960",
    "47962","47963","47964","47965","47966","47967","47968","47969",
    "47970","47971","47974","47975","47977","47978","47980","47981",
    "47982","47983","47984","47986","47987","47988","47989","47990",
    "47991","47992","47993","47994","47995",
}

# ─────────────────────────────────────────
#  SCREENING LOCATIONS BY ZIP PROXIMITY
# ─────────────────────────────────────────
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
        "note": "Serves Hendricks County area; radiology & screening programs",
        "url": "https://hendricks.org",
    },
    {
        "name": "Franciscan Health Mooresville",
        "address": "1201 Hadley Rd, Mooresville, IN 46158",
        "phone": "(317) 831-1160",
        "note": "Serves Morgan County; cancer screening available",
        "url": "https://franciscanhealth.org",
    },
    {
        "name": "IU Health Morgan Hospital",
        "address": "2209 John R Wooden Dr, Martinsville, IN 46151",
        "phone": "(765) 342-8441",
        "note": "Morgan County lung screening services",
        "url": "https://iuhealth.org",
    },
    {
        "name": "Putnam County Hospital",
        "address": "1542 Bloomington St, Greencastle, IN 46135",
        "phone": "(765) 653-5121",
        "note": "Serves Greencastle/DePauw area; imaging & screening",
        "url": "https://pchosp.org",
    },
    {
        "name": "Franciscan Health Crawfordsville",
        "address": "1710 Lafayette Rd, Crawfordsville, IN 47933",
        "phone": "(765) 362-2800",
        "note": "Serves west-central Indiana; cancer screening programs",
        "url": "https://franciscanhealth.org",
    },
    {
        "name": "IU Health Bloomington – Lung Screening",
        "address": "601 W 2nd St, Bloomington, IN 47403",
        "phone": "(812) 353-5555",
        "note": "Monroe County; comprehensive cancer & lung program",
        "url": "https://iuhealth.org",
    },
    {
        "name": "IU Health Fort Wayne",
        "address": "700 Broadway, Fort Wayne, IN 46802",
        "phone": "(260) 450-5000",
        "note": "Allen County lung cancer screening & pulmonology",
        "url": "https://iuhealth.org",
    },
    {
        "name": "Parkview Cancer Institute – Fort Wayne",
        "address": "11050 Parkview Circle, Fort Wayne, IN 46845",
        "phone": "(260) 266-4000",
        "note": "Dedicated cancer center; LDCT screening available",
        "url": "https://parkview.com",
    },
    {
        "name": "Memorial Hospital – South Bend",
        "address": "615 N Michigan St, South Bend, IN 46601",
        "phone": "(574) 647-1000",
        "note": "St. Joseph County; lung screening & oncology",
        "url": "https://beaconhealthsystem.org",
    },
    {
        "name": "Franciscan Health Lafayette",
        "address": "1701 S Creasy Ln, Lafayette, IN 47905",
        "phone": "(765) 502-4000",
        "note": "Serves Tippecanoe County; cancer screening programs",
        "url": "https://franciscanhealth.org",
    },
    {
        "name": "Deaconess Cancer Institute – Evansville",
        "address": "600 Mary St, Evansville, IN 47747",
        "phone": "(812) 450-5000",
        "note": "SW Indiana; comprehensive lung cancer program",
        "url": "https://deaconess.com",
    },
    {
        "name": "IU Health Ball Memorial – Muncie",
        "address": "2401 University Ave, Muncie, IN 47303",
        "phone": "(765) 747-3111",
        "note": "Delaware County; lung screening & pulmonology",
        "url": "https://iuhealth.org",
    },
    {
        "name": "Reid Health – Richmond",
        "address": "1401 Chester Blvd, Richmond, IN 47374",
        "phone": "(765) 983-3000",
        "note": "Wayne County; cancer screening & imaging services",
        "url": "https://reidhealth.org",
    },
]

# Default fallback locations for unrecognized ZIPs
DEFAULT_LOCATIONS = [3, 0]  # IU Methodist, IU Health North

def get_nearby_locations(zip_code):
    """Return 2 screening locations based on ZIP prefix geography."""
    if not zip_code or len(zip_code) < 5:
        return [screening_locations[i] for i in DEFAULT_LOCATIONS]

    prefix3 = zip_code[:3]
    prefix2 = zip_code[:2]

    # Routing by 3-digit prefix
    routing = {
        # Indianapolis core
        "462": [3, 2],   # IU Methodist + Community Health North
        # Hamilton County (Carmel, Fishers, Noblesville, Westfield)
        "460": [0, 1],   # IU North + St. Vincent Carmel
        # Hendricks County
        "461": [7, 4],   # Hendricks Regional + Franciscan
        # Johnson County / south Marion
        "461": [4, 3],   # Franciscan + IU Methodist
        # Putnam County (Greencastle / DePauw)
        "461": [10, 11], # Putnam County Hospital + Franciscan Crawfordsville
        # Bloomington / Monroe County
        "474": [12, 3],  # IU Bloomington + IU Methodist
        # Fort Wayne / Allen County
        "468": [13, 14], # IU Fort Wayne + Parkview
        # South Bend / St. Joseph County
        "466": [15, 3],  # Memorial SB + IU Methodist
        # Lafayette / Tippecanoe
        "479": [16, 3],  # Franciscan Lafayette + IU Methodist
        # Evansville / Vanderburgh
        "477": [17, 3],  # Deaconess + IU Methodist
        # Muncie / Delaware
        "473": [18, 3],  # Ball Memorial + IU Methodist
        # Richmond / Wayne County
        "473": [19, 18], # Reid Health + Ball Memorial
    }

    # Fine-grained overrides for specific ZIP codes
    fine = {
        # Carmel / NW Hamilton
        "46032": [0, 1], "46033": [0, 1], "46074": [0, 1], "46077": [0, 1],
        # Fishers / Noblesville / NE Hamilton
        "46060": [5, 2], "46062": [5, 2], "46038": [2, 0],
        # Indianapolis north / Broad Ripple
        "46220": [2, 3], "46240": [2, 0], "46250": [2, 0],
        "46256": [2, 0], "46280": [0, 2], "46290": [0, 2],
        # Indianapolis core
        "46201": [3, 2], "46202": [3, 2], "46204": [3, 2],
        "46205": [3, 2], "46208": [3, 2],
        # Indianapolis south
        "46217": [4, 3], "46227": [4, 3], "46237": [4, 3],
        # Greenwood / Johnson County
        "46142": [4, 3], "46143": [4, 3], "46131": [4, 3],
        # Brownsburg / Hendricks
        "46112": [7, 4], "46122": [7, 4], "46123": [7, 4],
        # Mooresville / Morgan County
        "46158": [8, 9], "46151": [9, 8],
        # Greencastle / DePauw area / Putnam County
        "46135": [10, 11], "46170": [10, 11], "46172": [10, 11],
        "46105": [10, 11], "46120": [10, 11],
        # Crawfordsville / Montgomery County
        "47933": [11, 16],
        # Bloomington / Monroe County
        "47401": [12, 3], "47403": [12, 3], "47404": [12, 3],
        "47405": [12, 3], "47408": [12, 3],
        # Fort Wayne
        "46802": [13, 14], "46804": [13, 14], "46805": [13, 14],
        "46814": [13, 14], "46845": [14, 13],
        # South Bend
        "46601": [15, 3], "46614": [15, 3], "46628": [15, 3],
        # Lafayette / Purdue
        "47901": [16, 3], "47904": [16, 3], "47906": [16, 3],
        # Evansville
        "47710": [17, 3], "47711": [17, 3], "47712": [17, 3],
        # Muncie
        "47303": [18, 3], "47304": [18, 3], "47306": [18, 3],
        # Richmond
        "47374": [19, 18],
        # Kokomo / Howard County
        "46901": [6, 2], "46902": [6, 2],
        # Anderson / Madison County
        "46011": [2, 3], "46012": [2, 3], "46013": [2, 3],
    }

    if zip_code in fine:
        idxs = fine[zip_code]
    elif prefix3 in routing:
        idxs = routing[prefix3]
    else:
        idxs = DEFAULT_LOCATIONS

    return [screening_locations[i] for i in idxs]

# ─────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────
log_file = "usage_log.csv"
def log_usage(data):
    # Local CSV backup
    exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        fields = list(data.keys())
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow(data)
    # Send to Google Sheets via Apps Script webhook
    try:
        requests.post(SHEETS_WEBHOOK, json=data, timeout=5)
    except Exception:
        pass  # Never crash the app if logging fails

# ─────────────────────────────────────────
#  RISK MODEL  (PLCOm2012 — Tammemägi et al., NEJM 2013)
# ─────────────────────────────────────────
def logistic(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def plco_m2012(age, race, education, bmi, copd, cancer_hist, family_hist,
               smoking_status, smoking_intensity, duration_smoking, smoking_quit_time):
    """
    PLCOm2012 model (Tammemägi et al., NEJM 2013).
    Returns 6-year absolute risk of lung cancer (0–1).
    Validated for ever-smokers aged 40–80.
    Coefficients sourced from the original publication.
    """
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
    # Smoking intensity term (inverse power): only applies to smokers
    if smoking_status == 1 and smoking_intensity > 0:
        m += -1.822606 * ((smoking_intensity / 10) ** (-1) - 0.4021541613)
    return logistic(m)

def extrapolate_risk(age, race, education, bmi, copd, cancer_hist, family_hist,
                     smoking_status, smoking_intensity, duration_smoking, smoking_quit_time):
    """
    For ages < 40: extrapolate from the model's age=40 baseline using an
    exponential age-scaling factor. Risk is dramatically lower for younger ages.
    For ages > 80: cap at age=80 result (model validated up to 80).
    """
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
    """
    Compute 'lung age' by estimating what age a baseline person
    would need to be to carry the same 6-year risk.
    """
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
    """Returns (category_str, threshold_used). Thresholds per clinical literature."""
    if risk_pct >= 3.0:
        return "high", 3.0
    elif risk_pct >= 1.3:
        return "moderate", 1.3
    else:
        return "low", 1.3

def uspstf_qualifies(age, smoking_status, pack_years):
    """USPSTF 2021 criteria: age 50–80, current or former smoker, ≥20 pack-years."""
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

zip_input_val = st.session_state.get("zip_input", "")
is_five_digits = len(zip_input_val) == 5 and zip_input_val.isdigit()
is_in_indiana = zip_input_val in valid_zips

# Green outline whenever the user has typed a valid 5-digit ZIP
zip_css_class = "zip-valid" if is_five_digits else ""

st.markdown(f'<div class="{zip_css_class}">', unsafe_allow_html=True)
zip_code = st.text_input(
    "ZIP Code",
    placeholder="e.g. 46032",
    key="zip_input",
    max_chars=5,
)
st.markdown('</div>', unsafe_allow_html=True)

if zip_code:
    if is_in_indiana:
        st.markdown('<div class="zip-status ok">✓ ZIP code recognized — screening locations loaded</div>', unsafe_allow_html=True)
    elif is_five_digits:
        st.markdown('<div class="zip-status warn">ZIP entered — note: screening locations shown for nearest Indiana facility</div>', unsafe_allow_html=True)

# ── Demographics ──
st.markdown('<div class="section-label">👤 About You</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    # Type-only age input (spinner buttons hidden via CSS)
    age = st.number_input(
        "Age",
        min_value=10,
        max_value=100,
        value=55,
        step=1,
        format="%d",
    )
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
    }

    log_usage({
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": st.session_state.user_id,
        "zip": zip_code or "",
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
    nearby = get_nearby_locations(zip_code) if zip_code and len(zip_code) == 5 else []
    if nearby:
        st.markdown('<div class="section-label">📍 Screening Centers Near You</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
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

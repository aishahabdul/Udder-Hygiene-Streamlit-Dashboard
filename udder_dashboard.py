import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

st.set_page_config(page_title="Udder Hygiene Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- URL parameters for client ID and access code ---
query_params = st.query_params
client_id = query_params.get("client", "").lower()
access_code = query_params.get("code", "")

# --- Define clients and access codes ---
client_map = {
    "QMPS-Mock-Up": {
        "name": "Cornell University QMPS Mock Up",
        "logo": "assets/Udder_hygiene_logo.png",
        "data": "data/udder_hygiene.csv",
        "code": "milk2025"
    }
}

# --- Access verification ---
if client_id not in client_map:
    st.error("Invalid client. Please check the URL.")
    st.stop()

if access_code != client_map[client_id]["code"]:
    st.error("Invalid access code. Access denied.")
    st.stop()

# --- Load client configuration ---
client_info = client_map[client_id]
client_name = client_info["name"]
logo_path = client_info["logo"]
data_path = client_info["data"]

# --- Load and cache data ---
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(data_path)
df['visit_date'] = pd.to_datetime(df['visit_date'], errors='coerce')

# --- Logo and title ---
st.image(logo_path, width=150)
theme_color = "#1F2A44" if not st.get_option("theme.base") or st.get_option("theme.base") == "light" else "#E0E0E0"
st.markdown(f"<h1 style='text-align: center; color: {theme_color};'>{client_name}</h1>", unsafe_allow_html=True)

# --- Remove flagged rows for visualizations ---
if 'data_issue' in df.columns:
    clean_df = df[df['data_issue'] != True]
else:
    clean_df = df.copy()

# --- Sidebar Info ---
st.sidebar.title("ℹ️ About Hygiene Scores")
st.sidebar.markdown("""
**What do udder hygiene scores mean?**

- **Score 1:** Very clean udder  
- **Score 2:** Slight dirt present  
- **Score 3:** Moderate contamination  
- **Score 4:** Heavily soiled

High percentages in **Score 3 or 4** are linked to mastitis risk and milk quality issues. A clean herd should have mostly Score 1 and 2.

Monitoring these scores over time helps track improvements, identify problem areas, and maintain milk safety.
""")

farms = clean_df['farm_name'].dropna().unique()
selected_farm = st.selectbox("Select Farm", farms)

def log_action(action):
    with open("analytics_log.txt", "a") as log:
        log.write(f"[{datetime.now()}] {action}\n")

log_action(f"Viewed farm: {selected_farm}")
farm_data = clean_df[clean_df['farm_name'] == selected_farm]

if st.checkbox("Show Last Visit Summary", value=True):
    latest = farm_data.sort_values('visit_date').iloc[-1]
    st.write(f"**Date:** {latest['visit_date'].date()} | **Group:** {latest['group_id']}")
    st.write({
        'Score 1 (%)': latest['score_1_pct'],
        'Score 2 (%)': latest['score_2_pct'],
        'Score 3 (%)': latest['score_3_pct'],
        'Score 4 (%)': latest['score_4_pct'],
    })
    log_action(f"Opened Last Visit Summary for: {selected_farm}")

if st.checkbox("Show Historical Averages", value=True):
    score_columns = [f'score_{i}_pct' for i in range(1, 5)]
    avg_scores = farm_data[score_columns].mean().round(2)
    st.write(avg_scores.to_dict())
    log_action(f"Opened Historical Averages for: {selected_farm}")

if st.checkbox("Show Group Hygiene Rankings"):
    group_avg = (
        farm_data.groupby('group_id')['score_3_pct']
        .mean().sort_values()
    )
    st.write("**Best Hygiene (lowest Score 3 %):**", group_avg.idxmin(), f"{group_avg.min():.2f}%")
    st.write("**Worst Hygiene (highest Score 3 %):**", group_avg.idxmax(), f"{group_avg.max():.2f}%")
    log_action(f"Opened Group Hygiene Rankings for: {selected_farm}")

if st.checkbox("Show Single Score Trend"):
    score_option = st.selectbox("Select Score to View Trend", ["score_1_pct", "score_2_pct", "score_3_pct", "score_4_pct"])
    trend_data = (
        farm_data.groupby('visit_date')[score_option]
        .mean()
        .reset_index()
        .sort_values('visit_date')
    )
    fig, ax = plt.subplots()
    ax.plot(trend_data['visit_date'], trend_data[score_option], marker='o')
    ax.set_title(f"{score_option.replace('_pct', '').capitalize()} Over Time")
    ax.set_ylabel("% of Cows")
    ax.set_xlabel("Visit Date")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate(rotation=45)
    st.pyplot(fig)
    log_action(f"Viewed Single Score Trend ({score_option}) for: {selected_farm}")

if st.checkbox("Show All Score Trends Together"):
    trend_df = (
        farm_data.groupby('visit_date')[
            ['score_1_pct', 'score_2_pct', 'score_3_pct', 'score_4_pct']
        ].mean().reset_index()
    )
    fig, ax = plt.subplots()
    for col in ['score_1_pct', 'score_2_pct', 'score_3_pct', 'score_4_pct']:
        ax.plot(trend_df['visit_date'], trend_df[col], marker='o', label=col.replace('_pct', '').capitalize())
    ax.set_title("All Hygiene Score Trends Over Time")
    ax.set_ylabel("% of Cows")
    ax.set_xlabel("Visit Date")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate(rotation=45)
    ax.legend()
    st.pyplot(fig)
    log_action(f"Viewed All Score Trends for: {selected_farm}")

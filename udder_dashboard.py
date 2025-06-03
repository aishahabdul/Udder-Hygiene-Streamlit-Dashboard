import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

st.set_page_config(page_title="Udder Hygiene Dashboard", layout="wide")

# --- Login screen ---
st.markdown("### 🔐 Client Login")
client_id = st.text_input("Client ID (e.g. qmps_mock_up)").strip().lower()
access_code = st.text_input("Access Code", type="password")

client = st.secrets[client_id]
# --- Validate credentials ---
if client_id not in st.secrets or access_code != client.code:
    st.error("❌ Unknown client ID or incorrect acces code.")
    st.stop()
else:
    client = st.secrets[client_id]

    # if access_code != client.code:
    #     st.error("❌ Incorrect access code.")
    #     st.stop()
    
    # --- Display client dashboard ---
    st.image(client.logo, width=150)
    st.markdown(f"<h1 style='text-align: center; color: #1F2A44;'>{client.name}</h1>", unsafe_allow_html=True)
    
    # --- Load data ---
    df = pd.read_csv(client.data)
    df['visit_date'] = pd.to_datetime(df['visit_date'], errors='coerce')
    
    # Remove flagged data
    if 'data_issue' in df.columns:
        clean_df = df[df['data_issue'] != True]
    else:
        clean_df = df.copy()
    
    # --- Logging (for your internal use) ---
    def log_action(action):
        with open("analytics_log.txt", "a") as f:
            f.write(f"[{datetime.now()}] {action}\n")
    
    # --- Sidebar explanation ---
    st.sidebar.title("ℹ️ About Hygiene Scores")
    st.sidebar.markdown("""
    **What do udder hygiene scores mean?**
    
    - **Score 1:** Very clean udder  
    - **Score 2:** Slight dirt present  
    - **Score 3:** Moderate contamination  
    - **Score 4:** Heavily soiled
    
    High Scores 3 & 4 increase mastitis risk. Tracking these helps improve milk quality and udder health.
    """)
    
    # --- Farm selection ---
    farms = clean_df['farm_name'].dropna().unique()
    selected_farm = st.selectbox("Select Farm", farms)
    farm_data = clean_df[clean_df['farm_name'] == selected_farm]
    log_action(f"Viewed farm: {selected_farm}")
    
    # --- Last visit summary ---
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
    
    # --- Historical Averages ---
    if st.checkbox("Show Historical Averages", value=True):
        score_cols = [f'score_{i}_pct' for i in range(1, 5)]
        st.write(farm_data[score_cols].mean().round(2).to_dict())
        log_action(f"Viewed Historical Averages for: {selected_farm}")
    
    # --- Group hygiene ranking ---
    if st.checkbox("Show Group Hygiene Rankings"):
        group_avg = farm_data.groupby("group_id")["score_3_pct"].mean().sort_values()
        st.write("**Best Hygiene:**", group_avg.idxmin(), f"{group_avg.min():.2f}%")
        st.write("**Worst Hygiene:**", group_avg.idxmax(), f"{group_avg.max():.2f}%")
        log_action(f"Viewed Group Hygiene Rankings for: {selected_farm}")
    
    # --- Single Score Trend ---
    if st.checkbox("Show Single Score Trend"):
        score_choice = st.selectbox("Score to View", ["score_1_pct", "score_2_pct", "score_3_pct", "score_4_pct"])
        trend = farm_data.groupby("visit_date")[score_choice].mean().reset_index()
        fig, ax = plt.subplots()
        ax.plot(trend['visit_date'], trend[score_choice], marker='o')
        ax.set_title(f"{score_choice.replace('_pct', '').capitalize()} Over Time")
        ax.set_ylabel("% of Cows")
        ax.set_xlabel("Visit Date")
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()
        st.pyplot(fig)
        log_action(f"Viewed {score_choice} trend for: {selected_farm}")
    
    # --- All Score Trends Together ---
    if st.checkbox("Show All Score Trends Together"):
        trend_all = farm_data.groupby("visit_date")[
            ['score_1_pct', 'score_2_pct', 'score_3_pct', 'score_4_pct']
        ].mean().reset_index()
        fig, ax = plt.subplots()
        for col in trend_all.columns[1:]:
            ax.plot(trend_all['visit_date'], trend_all[col], marker='o', label=col.replace('_pct', '').capitalize())
        ax.set_title("All Hygiene Score Trends Over Time")
        ax.set_ylabel("% of Cows")
        ax.set_xlabel("Visit Date")
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()
        ax.legend()
        st.pyplot(fig)
        log_action(f"Viewed All Score Trends for: {selected_farm}")

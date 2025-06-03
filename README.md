# 🐄 Udder Hygiene Dashboard (QMPS)

This Streamlit app delivers a secure, client-specific dashboard that automates the udder hygiene reporting workflow for the Quality Milk Production Services (QMPS) team. It replaces manual Excel entry and static PDF reports with dynamic, interactive insights.

## 🚀 Features

- 🔒 **Secure Login** using client-specific access codes (`st.secrets`)
- 📈 **Visual Insights**:
  - Last visit summaries
  - Historical hygiene averages
  - Group hygiene rankings
  - Trends for all hygiene score levels
- 🧼 **No Manual Uploading** for clients — dashboards are preloaded
- 🌐 **Branded Interface**: Client logos and theming
- 📂 **Mobile-friendly UI**

---

## 🧬 Why Udder Hygiene?

Hygiene scores help farms monitor udder cleanliness, a key factor in preventing mastitis and improving milk quality:

- **Score 1**: Very clean  
- **Score 2**: Slight dirt  
- **Score 3**: Moderate contamination  
- **Score 4**: Heavily soiled

A well-managed herd should see high percentages in **Scores 1 & 2**.

---

## 🔐 Accessing the Client Dashboard

Each client gets a personalized link to their dashboard.

Upon visiting, they enter:

- **Client ID**: `qmps_mock_up`
- **Access Code**: `milk2025`

🔗 [Demo Dashboard](https://qmps-mockup.streamlit.app)

> ⚠️ Only valid credentials will load the dashboard. This demo is for mockup/testing purposes.

---

## 🔐 Accessing the Admin Dashboard

🔗  [Admin Dashboard](https://udderdashboardapppy-dh6fmxmojvax2jgtkyfsoz.streamlit.app)  

---
## ⚙️ Tech Stack

- Python 3.10+
- Streamlit
- Pandas
- Matplotlib
- Hosted on [Streamlit Cloud](https://streamlit.io/cloud)

---

## 🧪 Data Handling

- Missing or invalid entries are **flagged**
- Flagged rows are **excluded** from all visualizations in the client dahboard 
- Flags are retained so data issues can be reviewed or **imputed later** in admin dashboard
- No client-side cleaning required

---

## 🛠 For Developers

Want to build your own version?

1. **Fork this repo**
2. Add your own data & logo to `/data/` and `/assets/`
3. Edit `.streamlit/secrets.toml` with:
    ```toml
    [your_client_id]
    name = "Your Display Name"
    code = "yourAccessCode"
    logo = "assets/your_logo.png"
    data = "data/your_data.csv"
    ```
4. Deploy via [Streamlit Cloud](https://streamlit.io/cloud)

---

## 📌 To Do

- [ ] Add logout button / session switching
- [ ] Admin dashboard for usage tracking
- [ ] Email alerts for hygiene issues

---

## 💡 Credits

Created by Aishah Abdul-Hakeem as a workflow optimization prototype for QMPS.  
For questions, contact: `aaa279@cornell.edu` 

---



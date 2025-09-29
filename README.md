# 🐄 Udder Hygiene Dashboard 

This Streamlit app delivers a secure, client-specific dashboard that automates the udder hygiene reporting workflow. It replaces manual Excel entry and static PDF reports with dynamic, interactive insights.

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

## 💡 Credits

Created by Aishah Abdul-Hakeem as a workflow optimization prototype for a company.  
For questions, contact: `aishah.a1809@gmail.com` 

---



import streamlit as st

from header import show_header
from theme import apply_theme

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Visionary InfoTech | About Project",
    page_icon="ℹ️",
    layout="wide"
)

apply_theme()
show_header()

st.title("🤖 AI Workforce Assistant")
st.caption("An AI-powered HR Analytics & Workforce Planning Solution")

st.markdown("""
## About this Project

The **AI HRBP Workforce Planner** is a portfolio project that demonstrates how Artificial Intelligence can support HR Business Partners in workforce planning, employee analytics, and decision-making.

This application combines HR analytics dashboards with an AI-powered workforce assistant to help HR teams analyze employee data, answer workforce-related questions, and generate actionable insights.

---

## Key Features

✅ Workforce Directory

✅ Workforce Analytics Dashboard

✅ HRBP Decision Center

✅ AI Workforce Assistant

✅ Interactive Charts

✅ Excel Report Export

✅ PDF Report Export

✅ Natural Language Queries

---

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- OpenAI / OpenRouter
- ReportLab
- OpenPyXL

---

## HR Use Cases

- Workforce Planning
- Headcount Analysis
- Department Analytics
- Gender Diversity Insights
- Location Analytics
- Employee Search
- Executive Reporting
- AI-powered HR Question Answering

---

## Disclaimer

**Visionary InfoTech Pvt. Ltd.** is a fictional company created solely for demonstrating HR analytics, workforce planning, and AI Workforce Assistant capabilities.

All employee information used in this application is synthetic and intended only for portfolio and demonstration purposes.
""")

st.markdown("---")

st.markdown("""
## 👩‍💻 About the Developer

**Gayathri Murali**

HR Professional with expertise in **HR Analytics, HR Business Partnering, Workforce Planning, and AI-driven HR solutions**. Passionate about leveraging technology to improve people processes and business decision-making.

🔗 **GitHub:** https://github.com/muraligayathri1991-cyber

""")
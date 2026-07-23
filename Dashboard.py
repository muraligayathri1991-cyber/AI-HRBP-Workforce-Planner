import streamlit as st

from header import show_header
from theme import apply_theme
from card import card

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Visionary InfoTech | About Project",
    page_icon="ℹ️",
    layout="wide"
)

apply_theme()
show_header()

# =====================================================
# HERO BANNER
# =====================================================

st.image(
    "assets/hero_banner.png",
    use_container_width=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.title("🤖 AI Workforce Assistant")
st.caption("AI-powered HR Analytics & Workforce Planning Solution")

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# ABOUT PROJECT
# =====================================================

with st.container():
    st.subheader("📘 About the Project")

    st.write("""
The **AI Workforce Assistant** is a portfolio project demonstrating how Artificial Intelligence can support HR Business Partners with workforce planning, employee analytics, and strategic decision-making.

The application combines interactive dashboards, workforce analytics, and an AI-powered assistant capable of answering HR-related questions using employee data. It showcases practical HR use cases such as headcount analysis, workforce distribution, diversity insights, executive reporting, and AI-assisted decision support.
""")

st.divider()

# =====================================================
# FEATURES + TECHNOLOGY
# =====================================================

left, right = st.columns([1, 1], gap="large")

with left:

    st.subheader("✨ Key Features")

    st.markdown("""
- 👥 Workforce Directory
- 📊 Workforce Analytics Dashboard
- 🎯 HRBP Decision Center
- 🤖 AI Workforce Assistant
- 📈 Interactive Charts
- 📄 Excel Report Export
- 📑 PDF Report Export
- 💬 Natural Language Queries
""")

with right:

    st.subheader("🛠 Technology Stack")

    st.markdown("""
- 🐍 Python
- ⚡ Streamlit
- 🐼 Pandas
- 📊 Plotly
- 🤖 OpenAI / OpenRouter
- 📄 ReportLab
- 📗 OpenPyXL
""")

st.divider()

# =====================================================
# HR USE CASES
# =====================================================

st.subheader("🎯 HR Use Cases")

col1, col2 = st.columns(2, gap="large")

with col1:

    st.markdown("""
- Workforce Planning
- Headcount Analysis
- Department Analytics
- Employee Search
""")

with col2:

    st.markdown("""
- Gender Diversity Insights
- Location Analytics
- Executive Reporting
- AI-powered HR Question Answering
""")

st.divider()

# =====================================================
# ABOUT THE DEVELOPER
# =====================================================

st.subheader("👩‍💻 About the Developer")

st.write("""
**Gayathri Murali**

HR Professional with expertise in **HR Analytics, HR Business Partnering, Workforce Planning, and AI-driven HR Solutions**.

Passionate about leveraging technology to improve people processes, business decision-making, and employee experiences through data and Artificial Intelligence.
""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
<div style="text-align:center; color:#6B7280; font-size:14px;">

<b>Portfolio Demonstration Notice</b><br><br>

Visionary InfoTech Pvt. Ltd. is a fictional organization created solely for demonstrating
HR Analytics, Workforce Planning, and AI Workforce Assistant capabilities.
All employee information displayed in this application is synthetic and intended exclusively
for portfolio and educational purposes. No real employee or organizational data has been used.

<br><br>

© 2026 <b>Gayathri Murali</b> • AI Workforce Assistant Portfolio

</div>
""",
    unsafe_allow_html=True,
)
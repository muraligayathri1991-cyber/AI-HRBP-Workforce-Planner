import streamlit as st
import pandas as pd
import plotly.express as px

from sidebar import sidebar_filters
from header import show_header

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Visionary InfoTech | Workforce Analytics",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# READ EMPLOYEE DATA
# =====================================================

employees = pd.read_excel(
    "data/Visionary_InfoTech_Employee_Master_Data.xlsx"
)

employees = sidebar_filters(employees)

employees["Joining Date"] = pd.to_datetime(
    employees["Joining Date"]
)

# =====================================================
# COMPANY HEADER
# =====================================================

show_header()

# =====================================================
# PAGE INTRODUCTION
# =====================================================

st.info(
"""
📈 **People Analytics**

Gain strategic workforce insights through interactive visualizations.

All charts below are interactive.

✔ Hover for values

✔ Zoom

✔ Pan

✔ Download as PNG

✔ Autoscale
"""
)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("📊 Executive Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👥 Employees",
    len(employees)
)

c2.metric(
    "🏢 Departments",
    employees["Department"].nunique()
)

c3.metric(
    "📍 Locations",
    employees["Location"].nunique()
)

c4.metric(
    "📈 Avg Experience",
    f"{employees['Experience (Years)'].mean():.1f} Years"
)

st.divider()

# =====================================================
# PREPARE DATA
# =====================================================

department = (
    employees["Department"]
    .value_counts()
    .reset_index()
)

department.columns = [
    "Department",
    "Employees"
]

location = (
    employees["Location"]
    .value_counts()
    .reset_index()
)

location.columns = [
    "Location",
    "Employees"
]

experience = (
    employees
    .groupby(
        "Department",
        as_index=False
    )[
        "Experience (Years)"
    ]
    .mean()
)

designation = (
    employees["Designation"]
    .value_counts()
    .reset_index()
)

designation.columns = [
    "Designation",
    "Employees"
]

experience_band = pd.cut(
    employees["Experience (Years)"],
    bins=[0,2,5,8,12,50],
    labels=[
        "0-2 Years",
        "2-5 Years",
        "5-8 Years",
        "8-12 Years",
        "12+ Years"
    ]
)

experience_distribution = (
    experience_band
    .value_counts()
    .sort_index()
    .reset_index()
)

experience_distribution.columns = [
    "Experience Band",
    "Employees"
]

joining = (
    employees["Joining Date"]
    .dt.year
    .value_counts()
    .sort_index()
    .reset_index()
)

joining.columns = [
    "Year",
    "Employees Joined"
]

# =====================================================
# ROW 1
# =====================================================

left, right = st.columns(2)

with left:

    fig1 = px.bar(
        department,
        x="Department",
        y="Employees",
        title="Department Workforce Distribution",
        text="Employees"
    )

    fig1.update_layout(
        height=420
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    fig2 = px.pie(
        location,
        names="Location",
        values="Employees",
        title="Location-wise Workforce Distribution",
        hole=0.35
    )

    fig2.update_layout(
        height=420
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# ROW 2
# =====================================================

left, right = st.columns(2)
with left:

    fig3 = px.bar(
        experience,
        x="Experience (Years)",
        y="Department",
        orientation="h",
        title="Department Experience Profile",
        text="Experience (Years)"
    )

    fig3.update_layout(
        height=420
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with right:

    fig4 = px.bar(
        designation,
        x="Employees",
        y="Designation",
        orientation="h",
        title="Workforce Distribution by Designation",
        text="Employees"
    )

    fig4.update_layout(
        height=420
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =====================================================
# ROW 3
# =====================================================

left, right = st.columns(2)

with left:

    fig5 = px.bar(
        experience_distribution,
        x="Experience Band",
        y="Employees",
        title="Experience Distribution",
        text="Employees"
    )

    fig5.update_layout(
        height=420
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

with right:

    fig6 = px.line(
        joining,
        x="Year",
        y="Employees Joined",
        title="Hiring Trend",
        markers=True
    )

    fig6.update_traces(
        line_width=3
    )

    fig6.update_layout(
        height=420
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

# =====================================================
# END OF DASHBOARD
# =====================================================

st.divider()

st.success(
    "✅ Interactive Workforce Analytics Dashboard | Visionary InfoTech Pvt. Ltd."
)
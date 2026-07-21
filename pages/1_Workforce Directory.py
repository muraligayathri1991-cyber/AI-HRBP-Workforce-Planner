import streamlit as st
import pandas as pd

from sidebar import sidebar_filters
from header import show_header

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Visionary InfoTech | Workforce Directory",
    page_icon="👥",
    layout="wide"
)

# =====================================================
# READ EMPLOYEE DATA
# =====================================================

employees = pd.read_excel(
    "data/Visionary_InfoTech_Employee_Master_Data.xlsx"
)

# Apply Sidebar Filters
employees = sidebar_filters(employees)

# =====================================================
# COMPANY HEADER
# =====================================================

show_header()

# =====================================================
# PAGE INTRODUCTION
# =====================================================

st.info(
    """
👥 **Workforce Directory**

Search, filter and review employee information across departments,
designations and locations. This directory enables HR Business Partners
to quickly access workforce information for operational and strategic decisions.
"""
)

# =====================================================
# WORKFORCE SUMMARY
# =====================================================

st.subheader("📋 Workforce Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "👥 Employees Displayed",
    len(employees)
)

col2.metric(
    "🏢 Departments",
    employees["Department"].nunique()
)

col3.metric(
    "📍 Locations",
    employees["Location"].nunique()
)

# =====================================================
# DOWNLOAD DIRECTORY
# =====================================================

st.divider()

csv = employees.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Employee Directory",
    data=csv,
    file_name="Visionary_InfoTech_Workforce_Directory.csv",
    mime="text/csv"
)

# =====================================================
# EMPLOYEE DIRECTORY
# =====================================================

st.divider()

st.subheader("👥 Employee Directory")

directory = employees[
    [
        "Employee ID",
        "Employee Name",
        "Department",
        "Designation",
        "Location",
        "Joining Date",
        "Experience (Years)"
    ]
]

st.dataframe(
    directory,
    use_container_width=True,
    hide_index=True
)
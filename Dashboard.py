import streamlit as st
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from io import BytesIO

from sidebar import sidebar_filters
from header import show_header
from theme import apply_theme

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Visionary InfoTech | Dashboard",
    page_icon="🏢",
    layout="wide"
)
apply_theme()

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
# DASHBOARD INTRODUCTION
# =====================================================

st.info(
    """
👋 **Welcome to the Visionary InfoTech Workforce Intelligence Dashboard**

This platform enables HR Business Partners to monitor workforce trends,
analyze organizational data, and make informed people decisions through
interactive analytics and AI-powered insights.
"""
)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("📊 Executive Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "👥 Total Employees",
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

col4, col5, col6 = st.columns(3)

col4.metric(
    "💼 Designations",
    employees["Designation"].nunique()
)

col5.metric(
    "📈 Avg Experience",
    f"{employees['Experience (Years)'].mean():.1f} Years"
)

col6.metric(
    "🆕 Latest Joiners",
    len(
        employees
        .sort_values("Joining Date", ascending=False)
        .head(5)
    )
)
# =====================================================
# WORKFORCE INSIGHTS
# =====================================================

st.divider()

st.subheader("📌 Workforce Insights")

department_count = employees["Department"].value_counts()

largest_department = department_count.idxmax()
largest_department_count = department_count.max()

location_count = employees["Location"].value_counts()

largest_location = location_count.idxmax()
largest_location_count = location_count.max()

average_experience = (
    employees
    .groupby("Department")["Experience (Years)"]
    .mean()
)

most_experienced_department = average_experience.idxmax()

highest_experience = average_experience.max()

colA, colB, colC = st.columns(3)

colA.metric(
    "🏢 Largest Department",
    largest_department,
    f"{largest_department_count} Employees"
)

colB.metric(
    "📍 Largest Location",
    largest_location,
    f"{largest_location_count} Employees"
)

colC.metric(
    "📈 Most Experienced Department",
    most_experienced_department,
    f"{highest_experience:.1f} Years"
)

# =====================================================
# RECENT JOINERS
# =====================================================

st.divider()

st.subheader("🆕 Recent Joiners")

employees["Joining Date"] = pd.to_datetime(
    employees["Joining Date"]
)

recent_joiners = (
    employees
    .sort_values(
        "Joining Date",
        ascending=False
    )
    .head(5)
)

col1, col2 = st.columns(2)

for i, (_, row) in enumerate(recent_joiners.iterrows()):

    if i % 2 == 0:
        with col1:
            st.write(
                f"👤 **{row['Employee Name']}**"
            )

            st.caption(
                f"{row['Designation']} | {row['Department']}"
            )

            st.caption(
                f"Joined on {row['Joining Date'].strftime('%d %b %Y')}"
            )

            st.markdown("")

    else:
        with col2:
            st.write(
                f"👤 **{row['Employee Name']}**"
            )

            st.caption(
                f"{row['Designation']} | {row['Department']}"
            )

            st.caption(
                f"Joined on {row['Joining Date'].strftime('%d %b %Y')}"
            )

            st.markdown("")

# =====================================================
# DASHBOARD REPORT EXPORT
# =====================================================

st.divider()

st.subheader("📥 Download Dashboard Report")

report_data = pd.DataFrame({
    "Metric": [
        "Total Employees",
        "Departments",
        "Locations",
        "Designations",
        "Average Experience",
        "Largest Department",
        "Largest Department Count",
        "Largest Location",
        "Largest Location Count",
        "Most Experienced Department",
        "Average Experience (Top Department)"
    ],
    "Value": [
        len(employees),
        employees["Department"].nunique(),
        employees["Location"].nunique(),
        employees["Designation"].nunique(),
        f"{employees['Experience (Years)'].mean():.1f} Years",
        largest_department,
        largest_department_count,
        largest_location,
        largest_location_count,
        most_experienced_department,
        f"{highest_experience:.1f} Years"
    ]
})

wb = Workbook()

ws = wb.active
ws.title = "Dashboard Summary"

ws.append(["Visionary InfoTech Pvt. Ltd."])
ws.append(["HR Workforce Dashboard Report"])
ws.append([])

ws.append(list(report_data.columns))

for cell in ws[4]:
    cell.font = Font(bold=True)

for row in report_data.itertuples(index=False):
    ws.append(row)

# Auto-fit columns
for column_cells in ws.columns:
    length = max(
        len(str(cell.value)) if cell.value is not None else 0
        for cell in column_cells
    )

    ws.column_dimensions[
        column_cells[0].column_letter
    ].width = length + 3

excel_file = BytesIO()

wb.save(excel_file)

excel_file.seek(0)

st.download_button(
    "📥 Download Dashboard Report",
    data=excel_file,
    file_name="Visionary_Workforce_Dashboard_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
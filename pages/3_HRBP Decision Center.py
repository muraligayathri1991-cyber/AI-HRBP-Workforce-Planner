import streamlit as st
import pandas as pd

from sidebar import sidebar_filters
from header import show_header
from theme import apply_theme

st.set_page_config(page_title="Visionary InfoTech | HRBP Decision Center",
                   page_icon="📊",
                   layout="wide")
apply_theme()

employees = pd.read_excel("data/Visionary_InfoTech_Employee_Master_Data.xlsx")
employees = sidebar_filters(employees)

employees["Joining Date"] = pd.to_datetime(employees["Joining Date"])
employees["Date of Birth"] = pd.to_datetime(employees["Date of Birth"])
today = pd.Timestamp.today()

show_header()

st.title("📊 HRBP Decision Center")

st.info("""
The HRBP Decision Center provides actionable workforce insights,
highlights workforce risks, and recommends priority actions to
support strategic people decisions.
""")

st.subheader("🏥 Workforce Health")

avg_exp = employees["Experience (Years)"].mean()
avg_age = ((today - employees["Date of Birth"]).dt.days / 365.25).mean()
avg_tenure = ((today - employees["Joining Date"]).dt.days / 365.25).mean()

male = employees["Gender"].str.lower().eq("male").sum()
female = employees["Gender"].str.lower().eq("female").sum()
total_emp = len(employees)

male_pct = (male / total_emp) * 100
female_pct = (female / total_emp) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Total Employees",
        total_emp
    )

with col2:
    st.metric(
        "📈 Avg Experience",
        f"{avg_exp:.1f} Years"
    )

with col3:
    st.metric(
        "🎂 Avg Age",
        f"{avg_age:.1f} Years"
    )

st.markdown("")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "🏢 Avg Tenure",
        f"{avg_tenure:.1f} Years"
    )

with col5:
    st.metric(
        "👨 Male Employees",
        f"{male_pct:.1f}%"
    )

with col6:
    st.metric(
        "👩 Female Employees",
        f"{female_pct:.1f}%"
    )

st.divider()
st.subheader("⚠ Workforce Risk Indicators")

dept_count = employees["Department"].value_counts()
dept_exp = employees.groupby("Department")["Experience (Years)"].mean()

low_exp = dept_exp.idxmin()
smallest = dept_count.idxmin()
largest_loc = employees["Location"].value_counts().idxmax()

st.warning(f"📉 {low_exp} has the lowest average experience ({dept_exp.min():.1f} years).")
st.warning(f"👥 {smallest} has the smallest workforce ({dept_count.min()} employees).")
st.warning(f"📍 {largest_loc} has the highest workforce concentration.")

# =====================================================
# HRBP BUSINESS PRIORITIES
# =====================================================

st.divider()

st.subheader("🚩 HRBP Business Priorities")

# Largest Department
largest_department = dept_count.idxmax()
largest_department_count = dept_count.max()

st.error(
    f"🔴 **High Priority:** {largest_department} is the largest department "
    f"with **{largest_department_count} employees**. "
    "Review succession planning and manager span of control."
)

# Lowest Experience Department
lowest_department = dept_exp.idxmin()
lowest_exp = dept_exp.min()

st.warning(
    f"🟠 **Learning Priority:** {lowest_department} has the lowest average "
    f"experience (**{lowest_exp:.1f} years**). "
    "Consider targeted learning and mentoring programs."
)

# Largest Location
location_count = employees["Location"].value_counts()

largest_location = location_count.idxmax()
largest_location_count = location_count.max()

st.info(
    f"🔵 **Location Review:** {largest_location} has "
    f"**{largest_location_count} employees**. "
    "Review workforce concentration and business continuity planning."
)

# Most Experienced Department
highest_department = dept_exp.idxmax()
highest_exp = dept_exp.max()

st.success(
    f"🟢 **Opportunity:** {highest_department} has the highest average "
    f"experience (**{highest_exp:.1f} years**). "
    "Use experienced employees as mentors across departments."
)
st.divider()
st.subheader("📅 Upcoming HR Activities")

left,right = st.columns(2)

with left:
    st.markdown("#### 🎂 Upcoming Birthdays")
    b = employees.copy()
    b["Event"] = b["Date of Birth"].apply(lambda x: x.replace(year=today.year))
    b["Days"] = (b["Event"]-today).dt.days
    b.loc[b["Days"]<0,"Days"] += 365
    for _,r in b.sort_values("Days").head(5).iterrows():
        st.write(f"🎉 {r['Employee Name']} ({r['Event'].strftime('%d %b')})")

with right:
    st.markdown("#### 🎉 Upcoming Work Anniversaries")
    a = employees.copy()
    a["Event"] = a["Joining Date"].apply(lambda x: x.replace(year=today.year))
    a["Days"] = (a["Event"]-today).dt.days
    a.loc[a["Days"]<0,"Days"] += 365
    for _,r in a.sort_values("Days").head(5).iterrows():
        years = today.year-r["Joining Date"].year
        st.write(f"🏅 {r['Employee Name']} - {years} Years ({r['Event'].strftime('%d %b')})")

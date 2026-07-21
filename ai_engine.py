import os
import re
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from openai import OpenAI

# =====================================================
# LOAD ENVIRONMENT
# =====================================================

load_dotenv()

# =====================================================
# MODEL CONFIGURATION
# =====================================================

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
def generate_chart(df, chart_type, x_col, y_col=None, title=""):
    """
    Generates a matplotlib chart based on the requested chart type.

    Returns
    -------
    matplotlib.figure.Figure
    """

    fig, ax = plt.subplots(figsize=(8, 5))

    if chart_type == "bar":
        ax.bar(df[x_col], df[y_col])

    elif chart_type == "horizontal_bar":
        ax.barh(df[x_col], df[y_col])

    elif chart_type == "pie":
        ax.pie(
            df[x_col],
            labels=df.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")

    elif chart_type == "line":
        ax.plot(df[x_col], df[y_col], marker="o")

    elif chart_type == "stacked_bar":

        df.plot(
            kind="bar",
            stacked=True,
            ax=ax
        )

    ax.set_title(title)

    if chart_type != "pie":
        ax.set_xlabel(x_col)

        if y_col:
            ax.set_ylabel(y_col)

        plt.xticks(rotation=45)

    plt.tight_layout()

    return fig
# =====================================================
# MAIN AI FUNCTION
# =====================================================

def get_ai_response(question, employees):

    employees = employees.copy()

    # =====================================================
    # DATA PREPARATION
    # =====================================================

    employees["Joining Date"] = pd.to_datetime(
        employees["Joining Date"],
        errors="coerce"
    )

    employees["Date of Birth"] = pd.to_datetime(
        employees["Date of Birth"],
        errors="coerce"
    )

    q = question.lower().strip()
    q = re.sub(r"[^\w\s]", "", q)
    
    # =====================================================
    # HELP / CAPABILITIES
    # =====================================================

    if re.search(
        r"\b(help|what can you do|capabilities|features|options|commands)\b",
        q
    ):

        return {
            "type": "text",
            "answer": """
👋 **I can help you with the following HR questions:**

### 👥 Employee Search
• Show employees in Chennai
• Show female employees in IT
• Show Managers in Bangalore
• Show employees with more than 10 years experience

### 📊 Workforce Analytics
• Show department-wise headcount
• Show location-wise headcount
• Show designation-wise headcount

### 💰 Salary Analytics
• Show average salary by department
• Show average salary by location
• Show average salary by designation

### 📈 Experience Analytics
• Show average experience by department
• Show average experience by location
• Show average experience by designation

### 👥 Diversity Analytics
• Show gender distribution
• Show gender distribution by department
• Show gender distribution by designation

### 🎂 Employee Information
• Show upcoming birthdays
• Show recent joiners

You can also combine filters, for example:

• Show female employees in Chennai
• Show Managers in IT
• Show employees with more than 8 years experience
"""
        }

    # =====================================================
    # GREETINGS
    # =====================================================

    if re.search(
        r"\b(hi|hello|hey|good morning|good afternoon|good evening)\b",
        q
    ):

        return {
            "type": "text",
            "answer": (
                "👋 Hello! I'm your AI Workforce Assistant.\n\n"
                "I can help you analyze workforce data, search employees, "
                "generate HR analytics, and answer questions about your organization.\n\n"
                "Type **Help** to see everything I can do."
            )
        }

    # =====================================================
    # THANK YOU
    # =====================================================

    if re.search(
        r"\b(thanks|thank you|thankyou)\b",
        q
    ):

        return {
            "type": "text",
            "answer": (
                "😊 You're welcome! If you need more workforce insights or HR analytics, I'm here to help."
            )
        }

    # =====================================================
    # GOODBYE
    # =====================================================

    if re.search(
        r"\b(bye|goodbye|see you|see ya)\b",
        q
    ):

        return {
            "type": "text",
            "answer": (
                "👋 Goodbye! Have a great day, and feel free to return whenever you need HR insights."
            )
        }

    # ============================================
    # FOLLOW-UP QUESTION DETECTION
    # ============================================

    follow_up_keywords = [
        "second",
        "highest",
        "lowest",
        "top",
        "bottom",
        "compare",
        "first",
        "last",
        "more about",
        "that department",
        "that location",
        "that designation",
        "which one",
        "tell me more"
    ]

    is_follow_up = any(keyword in q for keyword in follow_up_keywords)

    today = pd.Timestamp.today()

    # =====================================================
    # WORKFORCE METRICS
    # =====================================================

    total_employees = len(employees)

    avg_experience = round(
        employees["Experience (Years)"].mean(),
        1
    )

    average_salary = round(
        employees["Salary"].mean(),
        2
    )

    highest_salary = employees["Salary"].max()

    lowest_salary = employees["Salary"].min()

    # =====================================================
    # WORKFORCE SUMMARIES
    # =====================================================

    department_summary = (
        employees["Department"]
        .value_counts()
        .to_string()
    )

    designation_summary = (
        employees["Designation"]
        .value_counts()
        .head(10)
        .to_string()
    )

    location_summary = (
        employees["Location"]
        .value_counts()
        .to_string()
    )

    gender_summary = (
        employees["Gender"]
        .value_counts()
        .to_string()
    )

    department_salary = (
        employees
        .groupby("Department")["Salary"]
        .mean()
        .round(2)
        .to_string()
    )

    # =====================================================
    # RECENT JOINERS SUMMARY
    # =====================================================

    recent_joiners = (
        employees
        .sort_values(
            "Joining Date",
            ascending=False
        )
        .head(5)[
            [
                "Employee Name",
                "Department",
                "Designation",
                "Joining Date"
            ]
        ]
        .to_string(index=False)
    )

    # =====================================================
    # BIRTHDAY SUMMARIES
    # =====================================================

    todays_birthdays = employees[
        (employees["Date of Birth"].dt.day == today.day)
        &
        (employees["Date of Birth"].dt.month == today.month)
    ]

    if todays_birthdays.empty:

        todays_birthdays_summary = "No birthdays today."

    else:

        todays_birthdays_summary = (
            todays_birthdays[
                [
                    "Employee Name",
                    "Department",
                    "Designation"
                ]
            ]
            .to_string(index=False)
        )

    monthly_birthdays = (
        employees[
            employees["Date of Birth"].dt.month
            == today.month
        ]
        .sort_values("Date of Birth")
    )

    if monthly_birthdays.empty:

        monthly_birthdays_summary = "No birthdays this month."

    else:

        monthly_birthdays_summary = (
            monthly_birthdays[
                [
                    "Employee Name",
                    "Department",
                    "Date of Birth"
                ]
            ]
            .to_string(index=False)
        )

    # =====================================================
    # QUESTION TYPE CLASSIFICATION
    # =====================================================

        advisory_keywords = [

        # Strategy
        "strategy",
        "strategic",
        "business",
        "growth",
        "expand",
        "expansion",
        "prepare",
        "planning",
        "plan",

        # HRBP
        "recommend",
        "recommendation",
        "suggest",
        "advice",
        "initiative",
        "initiatives",
        "priority",
        "priorities",
        "focus",
        "improve",
        "improvement",
        "how can",
        "how should",
        "what should",
        "best way",

        # Workforce
        "attrition",
        "retention",
        "engagement",
        "succession",
        "workforce planning",
        "talent strategy",
        "career development",
        "leadership",
        "employee morale",
        "burnout",
        "productivity",
        "performance improvement",
        "risk",
        "analyse",
        "analyze"
    ]

    if any(word in q for word in advisory_keywords):

        question_type = "advisory"

    else:

        question_type = "search"

    # =====================================================
    # UNIFIED EMPLOYEE SEARCH ENGINE
    # =====================================================
        if question_type == "search":

        # =====================================================
        # SEARCHABLE COLUMNS
        # =====================================================

            result = employees.copy()

        display_columns = [
            "Employee Name",
            "Department",
            "Designation",
            "Location",
            "Gender",
            "Experience (Years)"
        ]

        filters_applied = []

        # =====================================================
        # GENDER FILTER
        # =====================================================

        if re.search(r"\b(female|women)\b", q):

            result = result[
                result["Gender"].str.lower() == "female"
            ]

            filters_applied.append("Female")

        elif re.search(r"\b(male|men)\b", q):

            result = result[
                result["Gender"].str.lower() == "male"
            ]

            filters_applied.append("Male")

        # =====================================================
        # LOCATION FILTER
        # =====================================================

        for location in employees["Location"].dropna().unique():

            if re.search(rf"\b{re.escape(location.lower())}\b", q):

                result = result[
                    result["Location"].str.lower()
                    == location.lower()
                ]

                filters_applied.append(location)

                break

        # =====================================================
        # DEPARTMENT FILTER
        # =====================================================

        for dept in employees["Department"].dropna().unique():

            if re.search(rf"\b{re.escape(dept.lower())}\b", q):

                result = result[
                    result["Department"].str.lower()
                    == dept.lower()
                ]

                filters_applied.append(dept)

                break

        # =====================================================
        # DESIGNATION FILTER
        # =====================================================

        for designation in employees["Designation"].dropna().unique():

            if re.search(rf"\b{re.escape(designation.lower())}\b", q):

                result = result[
                    result["Designation"].str.lower()
                    == designation.lower()
                ]

                filters_applied.append(designation)

                break

        # =====================================================
        # EXPERIENCE FILTER
        # =====================================================

        match = re.search(r"(\d+)", q)

        if (
            match
            and
            (
                "experience" in q
                or "year" in q
                or "years" in q
            )
        ):

            years = int(match.group())

            if any(
                word in q
                for word in [
                    "more",
                    "above",
                    "greater",
                    "over",
                    "at least",
                    "+"
                ]
            ):

                result = result[
                    result["Experience (Years)"] >= years
                ]

                filters_applied.append(
                    f"{years}+ Years Experience"
                )

            elif any(
                word in q
                for word in [
                    "less",
                    "below",
                    "under"
                ]
            ):

                result = result[
                    result["Experience (Years)"] <= years
                ]

                filters_applied.append(
                    f"≤ {years} Years Experience"
                )

            else:

                result = result[
                    result["Experience (Years)"] == years
                ]

                filters_applied.append(
                    f"{years} Years Experience"
                )

        # =====================================================
        # UPCOMING BIRTHDAYS
        # =====================================================

        if "birthday" in q or "birthdays" in q:

            birthdays = employees.copy()

            birthdays["Birthday This Year"] = birthdays[
                "Date of Birth"
            ].apply(
                lambda x: x.replace(year=today.year)
            )

            birthdays = birthdays[
                birthdays["Birthday This Year"] >= today
            ]

            birthdays = birthdays.sort_values(
                "Birthday This Year"
            )

            birthday_table = birthdays[
                [
                    "Employee Name",
                    "Department",
                    "Date of Birth"
                ]
            ].copy()

            birthday_table["Date of Birth"] = (
                birthday_table["Date of Birth"]
                .dt.strftime("%d %b")
            )

            return {
                "type": "table",
                "title": "🎂 Upcoming Birthdays",
                "summary": f"{len(birthday_table)} upcoming birthdays found.",
                "data": birthday_table
            }

        # =====================================================
        # RECENT JOINERS
        # =====================================================

        if any(
            word in q
            for word in [
                "recent joiner",
                "recent joiners",
                "joined recently",
                "new joiners"
            ]
        ):

            recent = (
                employees
                .sort_values(
                    "Joining Date",
                    ascending=False
                )
                [
                    [
                        "Employee Name",
                        "Department",
                        "Designation",
                        "Location",
                        "Joining Date"
                    ]
                ]
                .head(10)
                .reset_index(drop=True)
            )

            return {
                "type": "table",
                "title": "🆕 Recent Joiners",
                "summary": f"Showing latest {len(recent)} employees.",
                "data": recent
            }

        # =====================================================
        # DEPARTMENT HEADCOUNT
        # =====================================================

        if (
            (
                "department" in q
                or "departments" in q
                or "dept" in q
            )
            and
            (
                "headcount" in q
                or "count" in q
                or "number" in q
            )
        ):

            headcount = (
                employees
                .groupby("Department")
                .size()
                .reset_index(name="Employee Count")
                .sort_values(
                    "Employee Count",
                    ascending=False
                )
            )

            largest_dept = headcount.iloc[0]["Department"]
            largest_count = headcount.iloc[0]["Employee Count"]

            summary = (
                f"The organization has {len(headcount)} departments.\n\n"
                f"📌 {largest_dept} has the highest headcount with {largest_count} employees.\n\n"
                "HRBP Insight:\n"
                "• Review manager span of control.\n"
                "• Ensure succession planning for key roles.\n"
                "• Monitor employee engagement and workforce planning."
            )

            return {
                "type": "table",
                "title": "📊 Department-wise Headcount",
                "summary": summary,
                "data": headcount
            }
                # =====================================================
        # LOCATION HEADCOUNT
        # =====================================================

        if (
            (
                "location" in q
                or "locations" in q
            )
            and
            (
                "headcount" in q
                or "count" in q
                or "number" in q
                or "employees" in q
            )
        ):

            location_count = (
                employees
                .groupby("Location")
                .size()
                .reset_index(name="Employee Count")
                .sort_values(
                    "Employee Count",
                    ascending=False
                )
            )

            largest_location = location_count.iloc[0]["Location"]
            largest_count = location_count.iloc[0]["Employee Count"]

            summary = (
                f"The organization operates across "
                f"{len(location_count)} locations.\n\n"
                f"📍 {largest_location} has the highest headcount with "
                f"{largest_count} employees.\n\n"
                "HRBP Insight:\n"
                "• Review workforce distribution across locations.\n"
                "• Evaluate hiring needs based on business demand.\n"
                "• Monitor location-specific employee engagement and capacity planning."
            )

            return {
                "type": "table",
                "title": "📍 Location-wise Headcount",
                "summary": summary,
                "data": location_count
            }
        # =====================================================
        # GENDER DISTRIBUTION
        # =====================================================

        if (
            re.search(
                r"\b(gender|male|female|men|women)\b",
                q
            )
            and
            not re.search(
                r"\b(employee|employees|employee name|list|show|find|who|whose|working|works)\b",
                q
            )
            and
            not re.search(
                r"\b(department|departments|dept|designation|designations|role|roles)\b",
                q
            )
        ):

            gender_count = (
                employees
                .groupby("Gender")
                .size()
                .reset_index(name="Employee Count")
                .sort_values(
                    "Employee Count",
                    ascending=False
                )
            )

            total = gender_count["Employee Count"].sum()

            gender_count["Percentage"] = (
                (gender_count["Employee Count"] / total) * 100
            ).round(1)

            highest_gender = gender_count.iloc[0]["Gender"]
            highest_count = gender_count.iloc[0]["Employee Count"]

            summary = (
                f"The workforce consists of {total} employees.\n\n"
                f"👥 {highest_gender} employees form the largest group with "
                f"{highest_count} employees.\n\n"
                "HRBP Insight:\n"
                "• Monitor overall workforce gender diversity.\n"
                "• Promote equitable hiring and career development.\n"
                "• Track representation in leadership and critical roles."
            )

            return {
                "type": "table",
                "title": "👥 Gender Distribution",
                "summary": summary,
                "data": gender_count
            }
                        
            gender_count = (
                employees
                .groupby("Gender")
                .size()
                .reset_index(name="Employee Count")
                .sort_values(
                    "Employee Count",
                    ascending=False
                )
            )

            total = gender_count["Employee Count"].sum()

            gender_count["Percentage"] = (
                (
                    gender_count["Employee Count"] / total
                ) * 100
            ).round(1)

            highest_gender = gender_count.iloc[0]["Gender"]
            highest_count = gender_count.iloc[0]["Employee Count"]

            summary = (
                f"The workforce consists of {total} employees.\n\n"
                f"👥 {highest_gender} employees form the largest group with "
                f"{highest_count} employees.\n\n"
                "HRBP Insight:\n"
                "• Monitor overall workforce gender diversity.\n"
                "• Promote equitable hiring and career development.\n"
                "• Track representation in leadership and critical roles."
            )

            return {
                "type": "table",
                "title": "👥 Gender Distribution",
                "summary": summary,
                "data": gender_count
            }
        
        # =====================================================
        # DEPARTMENT-WISE AVERAGE EXPERIENCE
        # =====================================================

        if re.search(
            r"\b(experience|experienced)\b",
            q
        ) and re.search(
            r"\b(department|departments|dept)\b",
            q
        ):

            experience = (
                employees
                .groupby("Department")["Experience (Years)"]
                .mean()
                .round(1)
                .reset_index(name="Average Experience (Years)")
                .sort_values(
                    "Average Experience (Years)",
                    ascending=False
                )
            )

            highest_dept = experience.iloc[0]["Department"]
            highest_exp = experience.iloc[0]["Average Experience (Years)"]

            lowest_dept = experience.iloc[-1]["Department"]
            lowest_exp = experience.iloc[-1]["Average Experience (Years)"]

            if (
                "least" in q
                or "lowest" in q
                or "minimum" in q
            ):

                summary = (
                    f"📉 {lowest_dept} has the lowest average experience "
                    f"of {lowest_exp} years.\n\n"
                    "HRBP Insight:\n"
                    "• Consider additional onboarding and mentoring.\n"
                    "• Review hiring mix and capability development."
                )

            else:

                summary = (
                    f"📈 {highest_dept} has the highest average experience "
                    f"of {highest_exp} years.\n\n"
                    "HRBP Insight:\n"
                    "• Leverage experienced employees for mentoring.\n"
                    "• Strengthen succession planning and knowledge sharing."
                )

            return {
                "type": "table",
                "title": "📈 Department-wise Average Experience",
                "summary": summary,
                "data": experience
            }
        # =====================================================
        # DEPARTMENT-WISE AVERAGE SALARY
        # =====================================================

        if (
            re.search(r"\bsalary\b", q)
            and
            re.search(r"\b(department|departments|dept)\b", q)
        ):

            dept_salary = (
                employees
                .groupby("Department")["Salary"]
                .mean()
                .round(2)
                .reset_index(name="Average Salary")
                .sort_values(
                    "Average Salary",
                    ascending=False
                )
            )

            highest_dept = dept_salary.iloc[0]["Department"]
            highest_salary = dept_salary.iloc[0]["Average Salary"]

            lowest_dept = dept_salary.iloc[-1]["Department"]
            lowest_salary = dept_salary.iloc[-1]["Average Salary"]

            if (
                "lowest" in q
                or "least" in q
                or "minimum" in q
            ):

                summary = (
                    f"💰 {lowest_dept} has the lowest average salary "
                    f"of ₹{lowest_salary:,.2f}.\n\n"
                    "HRBP Insight:\n"
                    "• Review market competitiveness.\n"
                    "• Ensure compensation aligns with internal equity.\n"
                    "• Monitor retention risks in lower-paid functions."
                )

            else:

                summary = (
                    f"💰 {highest_dept} has the highest average salary "
                    f"of ₹{highest_salary:,.2f}.\n\n"
                    "HRBP Insight:\n"
                    "• Review pay equity across departments.\n"
                    "• Validate salary against role complexity and business impact.\n"
                    "• Monitor compensation trends for workforce planning."
                )

            return {
                "type": "table",
                "title": "💰 Department-wise Average Salary",
                "summary": summary,
                "data": dept_salary
            }
        # =====================================================
        # LOCATION-WISE AVERAGE EXPERIENCE
        # =====================================================

        if (
            re.search(r"\b(experience|experienced)\b", q)
            and
            re.search(r"\b(location|locations)\b", q)
        ):

            location_exp = (
                employees
                .groupby("Location")["Experience (Years)"]
                .mean()
                .round(1)
                .reset_index(name="Average Experience (Years)")
                .sort_values(
                    "Average Experience (Years)",
                    ascending=False
                )
            )

            highest_location = location_exp.iloc[0]["Location"]
            highest_exp = location_exp.iloc[0]["Average Experience (Years)"]

            lowest_location = location_exp.iloc[-1]["Location"]
            lowest_exp = location_exp.iloc[-1]["Average Experience (Years)"]

            if (
                "lowest" in q
                or "least" in q
                or "minimum" in q
            ):

                summary = (
                    f"📍 {lowest_location} has the lowest average experience "
                    f"of {lowest_exp} years.\n\n"
                    "HRBP Insight:\n"
                    "• Strengthen onboarding and capability building.\n"
                    "• Review hiring quality and retention strategies.\n"
                    "• Increase mentoring opportunities where required."
                )

            else:

                summary = (
                    f"📍 {highest_location} has the highest average experience "
                    f"of {highest_exp} years.\n\n"
                    "HRBP Insight:\n"
                    "• Utilize experienced employees for mentoring.\n"
                    "• Encourage cross-location knowledge sharing.\n"
                    "• Support succession planning for critical roles."
                )

            return {
                "type": "table",
                "title": "📍 Location-wise Average Experience",
                "summary": summary,
                "data": location_exp
            }
        # =====================================================
        # LOCATION-WISE AVERAGE SALARY
        # =====================================================

        if (
            re.search(r"\bsalary\b", q)
            and
            re.search(r"\b(location|locations)\b", q)
        ):

            location_salary = (
                employees
                .groupby("Location")["Salary"]
                .mean()
                .round(2)
                .reset_index(name="Average Salary")
                .sort_values(
                    "Average Salary",
                    ascending=False
                )
            )

            highest_location = location_salary.iloc[0]["Location"]
            highest_salary = location_salary.iloc[0]["Average Salary"]

            lowest_location = location_salary.iloc[-1]["Location"]
            lowest_salary = location_salary.iloc[-1]["Average Salary"]

            if (
                "lowest" in q
                or "least" in q
                or "minimum" in q
            ):

                summary = (
                    f"💰 {lowest_location} has the lowest average salary "
                    f"of ₹{lowest_salary:,.2f}.\n\n"
                    "HRBP Insight:\n"
                    "• Review compensation competitiveness.\n"
                    "• Assess retention risks for the location.\n"
                    "• Benchmark salaries against the local market."
                )

            else:

                summary = (
                    f"💰 {highest_location} has the highest average salary "
                    f"of ₹{highest_salary:,.2f}.\n\n"
                    "HRBP Insight:\n"
                    "• Validate salary alignment with business requirements.\n"
                    "• Monitor internal pay equity across locations.\n"
                    "• Consider cost-of-living differences while planning compensation."
                )

            return {
                "type": "table",
                "title": "💰 Location-wise Average Salary",
                "summary": summary,
                "data": location_salary
            }
        # =====================================================
        # DEPARTMENT-WISE GENDER DISTRIBUTION
        # =====================================================

        if (
            (
                re.search(r"\bgender\b", q)
                or re.search(r"\bmale\b", q)
                or re.search(r"\bfemale\b", q)
                or re.search(r"\bmen\b", q)
                or re.search(r"\bwomen\b", q)
                or re.search(r"\bsplit\b", q)
                or re.search(r"\bdiversity\b", q)
            )
            and
            (
                re.search(r"\bdepartment\b", q)
                or re.search(r"\bdepartments\b", q)
                or re.search(r"\bdept\b", q)
                or re.search(r"\bacross\b", q)
                or re.search(r"\bby\b", q)
            )
        ):

            gender_dept = (
                employees
                .groupby(["Department", "Gender"])
                .size()
                .reset_index(name="Employee Count")
                .sort_values(
                    ["Department", "Gender"]
                )
            )

            total_departments = (
                gender_dept["Department"].nunique()
            )

            summary = (
                f"Gender distribution is available across "
                f"{total_departments} departments.\n\n"
                "HRBP Insight:\n"
                "• Review gender diversity within each department.\n"
                "• Identify departments with low representation.\n"
                "• Support inclusive hiring and internal mobility initiatives."
            )

            return {
                "type": "table",
                "title": "👥 Department-wise Gender Distribution",
                "summary": summary,
                "data": gender_dept
            }
        
        # =====================================================
        # DESIGNATION-WISE HEADCOUNT
        # =====================================================

        if (
            re.search(r"\bdesignation\b", q)
            or re.search(r"\bdesignations\b", q)
            or re.search(r"\brole\b", q)
            or re.search(r"\broles\b", q)
        ) and (
            re.search(r"\bheadcount\b", q)
            or re.search(r"\bcount\b", q)
            or re.search(r"\bnumber\b", q)
            or re.search(r"\bemployees\b", q)
        ):

            designation_count = (
                employees
                .groupby("Designation")
                .size()
                .reset_index(name="Employee Count")
                .sort_values(
                    "Employee Count",
                    ascending=False
                )
            )

            top_designation = designation_count.iloc[0]["Designation"]
            top_count = designation_count.iloc[0]["Employee Count"]

            summary = (
                f"The organization has "
                f"{designation_count['Designation'].nunique()} designations.\n\n"
                f"👤 {top_designation} has the highest headcount with "
                f"{top_count} employees.\n\n"
                "HRBP Insight:\n"
                "• Review role distribution across the organization.\n"
                "• Identify critical roles with high staffing demand.\n"
                "• Support workforce planning and succession strategies."
            )

            return {
                "type": "table",
                "title": "👤 Designation-wise Headcount",
                "summary": summary,
                "data": designation_count
            }
        # =====================================================
        # DESIGNATION-WISE AVERAGE EXPERIENCE
        # =====================================================

        if (
            re.search(r"\b(experience|experienced)\b", q)
            and
            re.search(r"\b(designation|designations|role|roles)\b", q)
        ):

            designation_exp = (
                employees
                .groupby("Designation")["Experience (Years)"]
                .mean()
                .round(1)
                .reset_index(name="Average Experience (Years)")
                .sort_values(
                    "Average Experience (Years)",
                    ascending=False
                )
            )

            highest_role = designation_exp.iloc[0]["Designation"]
            highest_exp = designation_exp.iloc[0]["Average Experience (Years)"]

            lowest_role = designation_exp.iloc[-1]["Designation"]
            lowest_exp = designation_exp.iloc[-1]["Average Experience (Years)"]

            if (
                "least" in q
                or "lowest" in q
                or "minimum" in q
            ):

                summary = (
                    f"📉 {lowest_role} has the lowest average experience "
                    f"of {lowest_exp} years.\n\n"
                    "HRBP Insight:\n"
                    "• Review onboarding and capability development.\n"
                    "• Assess whether additional mentoring is required.\n"
                    "• Monitor workforce readiness for business needs."
                )

            else:

                summary = (
                    f"📈 {highest_role} has the highest average experience "
                    f"of {highest_exp} years.\n\n"
                    "HRBP Insight:\n"
                    "• Leverage experienced employees for mentoring.\n"
                    "• Strengthen succession planning for key roles.\n"
                    "• Encourage knowledge sharing across teams."
                )

            return {
                "type": "table",
                "title": "📈 Designation-wise Average Experience",
                "summary": summary,
                "data": designation_exp
            }
        # =====================================================
        # DESIGNATION-WISE AVERAGE SALARY
        # =====================================================

        if (
            re.search(r"\bsalary\b", q)
            and
            re.search(r"\b(designation|designations|role|roles)\b", q)
        ):

            designation_salary = (
                employees
                .groupby("Designation")["Salary"]
                .mean()
                .round(0)
                .reset_index(name="Average Salary")
                .sort_values(
                    "Average Salary",
                    ascending=False
                )
            )

            highest_role = designation_salary.iloc[0]["Designation"]
            highest_salary = designation_salary.iloc[0]["Average Salary"]

            lowest_role = designation_salary.iloc[-1]["Designation"]
            lowest_salary = designation_salary.iloc[-1]["Average Salary"]

            if (
                "least" in q
                or "lowest" in q
                or "minimum" in q
            ):

                summary = (
                    f"💰 {lowest_role} has the lowest average salary of "
                    f"₹{lowest_salary:,.0f}.\n\n"
                    "HRBP Insight:\n"
                    "• Review market competitiveness for this role.\n"
                    "• Assess compensation equity.\n"
                    "• Monitor retention risk."
                )

            else:

                summary = (
                    f"💰 {highest_role} has the highest average salary of "
                    f"₹{highest_salary:,.0f}.\n\n"
                    "HRBP Insight:\n"
                    "• Evaluate compensation against business impact.\n"
                    "• Support succession planning for critical roles.\n"
                    "• Maintain internal pay equity."
                )

            return {
                "type": "table",
                "title": "💰 Designation-wise Average Salary",
                "summary": summary,
                "data": designation_salary
            }
        # =====================================================
        # DESIGNATION-WISE GENDER DISTRIBUTION
        # =====================================================

        if (
            (
                re.search(r"\bgender\b", q)
                or re.search(r"\bmale\b", q)
                or re.search(r"\bfemale\b", q)
                or re.search(r"\bmen\b", q)
                or re.search(r"\bwomen\b", q)
                or re.search(r"\bdiversity\b", q)
                or re.search(r"\bsplit\b", q)
            )
            and
            (
                re.search(r"\bdesignation\b", q)
                or re.search(r"\bdesignations\b", q)
                or re.search(r"\brole\b", q)
                or re.search(r"\broles\b", q)
            )
        ):

            designation_gender = (
                employees
                .groupby(["Designation", "Gender"])
                .size()
                .reset_index(name="Employee Count")
                .sort_values(
                    ["Designation", "Gender"]
                )
            )

            total_designations = (
                designation_gender["Designation"].nunique()
            )

            summary = (
                f"Gender distribution is available across "
                f"{total_designations} designations.\n\n"
                "HRBP Insight:\n"
                "• Assess gender diversity across job roles.\n"
                "• Identify roles requiring balanced representation.\n"
                "• Support inclusive hiring and career progression."
            )

            return {
                "type": "table",
                "title": "👥 Designation-wise Gender Distribution",
                "summary": summary,
                "data": designation_gender
            }                                                                
        # =====================================================
        # RETURN FILTERED RESULTS
        # =====================================================

        if filters_applied:

            result = (
                result[display_columns]
                .reset_index(drop=True)
            )

            if result.empty:

                return {
                    "type": "text",
                    "answer": (
                        "❌ No matching employees found.\n\n"
                        "The filters you selected did not match any employee records.\n\n"
                        "Try one of the following:\n"
                        "• Check the department, designation or location name.\n"
                        "• Remove one or more filters.\n"
                        "• Try a broader search.\n"
                        "• Type Help to see supported questions."
                    )
                }

            title = " | ".join(filters_applied)

            return {
                "type": "table",
                "title": f"👥 {title}",
                "summary": f"{len(result)} employees found.",
                "data": result
            }
                        
    # =====================================================
    # AI HRBP ADVISORY
    # =====================================================

    prompt = f"""
You are a Senior HR Business Partner with expertise in Workforce Planning,
Employee Relations, Talent Management, Compensation, HR Operations and
People Analytics.

Use ONLY the workforce information below.

--------------------------------------------------------
RULES
--------------------------------------------------------

1. Never reveal:
   - Phone Numbers
   - Email IDs
   - Performance Ratings

2. Salary may be discussed ONLY as aggregated insights.

3. Date of Birth may be used ONLY for birthday-related questions.

4. Never invent or assume workforce data that is not available in the dataset.

5. If a question requires unavailable information (such as historical attrition, resignation data, engagement scores, absenteeism, promotion history or exit interviews), clearly state that the information is not available.

6. After mentioning the limitation, continue by analysing the available workforce data and provide meaningful HR insights instead of stopping the response.

7. For advisory questions, always use the following structure:

Assessment

Key Observations

Potential Risks

Recommended HR Actions

Business Impact

8. Write like a Senior HR Business Partner presenting to business leaders.

9. Avoid AI-style phrases such as:
- "snapshot"
- "information at hand"
- "quantitative score"
- "based on the provided context"

10. Keep the response practical, professional and concise.

--------------------------------------------------------
WORKFORCE SUMMARY
--------------------------------------------------------

Total Employees
{total_employees}

Department Distribution
{department_summary}

Designation Distribution
{designation_summary}

Location Distribution
{location_summary}

Gender Distribution
{gender_summary}

Average Experience
{avg_experience} years

Average Salary
₹{average_salary:,.2f}

Highest Salary
₹{highest_salary:,.2f}

Lowest Salary
₹{lowest_salary:,.2f}

Average Salary by Department

{department_salary}

Recent Joiners

{recent_joiners}

Today's Birthdays

{todays_birthdays_summary}

Birthdays This Month

{monthly_birthdays_summary}

--------------------------------------------------------
USER QUESTION
--------------------------------------------------------

{question}

Respond as a Senior HR Business Partner.

Do not stop after explaining the dataset limitations.

If information required to answer a question is unavailable, acknowledge the limitation and then continue by:

1. Analysing the available workforce data.
2. Highlighting meaningful observations.
3. Identifying possible workforce risks (without making unsupported claims).
4. Recommending practical HR actions.
5. Explaining the expected business impact.

Never fabricate statistics or historical trends.
"""

    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are a senior HR Business Partner who gives "
                        "professional HR recommendations."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )

        return {
            "type": "text",
            "answer": response.choices[0].message.content
        }

    except Exception as e:

        return {
            "type": "text",
            "answer": f"❌ Error: {e}"
        }
    
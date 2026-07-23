import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pdf_generator import generate_pdf
from openpyxl import Workbook
from openpyxl.styles import Font
from io import BytesIO
from datetime import datetime
from header import show_header
from sidebar import sidebar_filters
from ai_engine import get_ai_response
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Visionary InfoTech | AI Workforce Assistant",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# APPLY THEME
# =====================================================

apply_theme()

# =====================================================
# LOAD DATA
# =====================================================

employees = pd.read_excel(
    "data/Visionary_InfoTech_Employee_Master_Data.xlsx"
)


# =====================================================
# HEADER
# =====================================================

show_header()


# =====================================================
# SIDEBAR FILTERS
# =====================================================

filtered_employees = sidebar_filters(employees)


# =====================================================
# SESSION STATE
# =====================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

if "last_report" not in st.session_state:
    st.session_state.last_report = None


# =====================================================
# PAGE TITLE
# =====================================================

st.title("🤖 AI HR Assistant")

st.caption(
    "Ask questions about your workforce, departments, locations, hiring, employee information and HR analytics."
)


# =====================================================
# SUGGESTED QUESTIONS
# =====================================================

st.markdown("### 💡 Suggested Questions")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🏢 Department-wise Headcount",
        use_container_width=True
    ):
        st.session_state.selected_question = (
            "Show department-wise headcount."
        )

    if st.button(
        "📍 Employees by Location",
        use_container_width=True
    ):
        st.session_state.selected_question = (
            "Show employees by location."
        )

    if st.button(
        "👥 Employees in IT",
        use_container_width=True
    ):
        st.session_state.selected_question = (
            "Show all employees in the IT department."
        )


with col2:

    if st.button(
        "🎂 Upcoming Birthdays",
        use_container_width=True
    ):
        st.session_state.selected_question = (
            "List upcoming birthdays."
        )

    if st.button(
        "🆕 Recent Joiners",
        use_container_width=True
    ):
        st.session_state.selected_question = (
            "Show recent joiners."
        )

    if st.button(
        "📊 Workforce Summary",
        use_container_width=True
    ):
        st.session_state.selected_question = (
            "Give me the workforce summary."
        )


st.divider()


# =====================================================
# QUESTION INPUT
# =====================================================

question = st.text_input(
    "Ask your HR question",
    value=st.session_state.selected_question,
    placeholder="Example: Show employees in Chennai..."
)


# =====================================================
# ACTION BUTTONS
# =====================================================

col1, col2 = st.columns([1, 5])

with col1:

    ask = st.button(
        "Ask AI",
        type="primary",
        use_container_width=True
    )

with col2:

    clear = st.button(
        "Clear Chat",
        use_container_width=True
    )


# =====================================================
# CLEAR CHAT
# =====================================================

if clear:

    st.session_state.chat_history = []

    st.session_state.selected_question = ""

    st.rerun()

# =====================================================
# ASK AI
# =====================================================

if ask:

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:
        start_time = time.time()
        with st.spinner("🤖 AI is thinking..."):

            answer = get_ai_response(
                question,
                filtered_employees
            )
        response_time = round(time.time() - start_time, 2)
        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer,
                "response_time": response_time
            }
        )

        st.session_state.selected_question = ""

        st.rerun()
# =====================================================
# CONVERSATION
# =====================================================

if st.session_state.chat_history:

    st.markdown("## 💬 Conversation")

    for chat in reversed(st.session_state.chat_history):

        # ----------------------------
        # User Message
        # ----------------------------
        with st.chat_message("user"):
            st.write(chat["question"])

        # ----------------------------
        # Assistant Message
        # ----------------------------
        with st.chat_message("assistant"):

            answer = chat["answer"]

            if "response_time" in chat:
                st.caption(
                    f"⚡ Generated in {chat['response_time']} sec"
                )

            if isinstance(answer, dict):

                response_type = answer.get("type")

                # ----------------------------
                # TABLE RESPONSE
                # ----------------------------
                if response_type == "table":

                    if answer.get("title"):
                        st.subheader(answer["title"])

                    timestamp = datetime.now().strftime("%d %b %Y | %I:%M %p")

                    st.caption(f"📅 Generated on: {timestamp}")

                    if answer.get("summary"):
                        st.write(answer["summary"])

                    if answer.get("data") is not None:

                        df = answer["data"]

                        # Save the last report for follow-up questions
                        st.session_state.last_report = answer
                        
                        # =====================================================
                        # EXECUTIVE SNAPSHOT
                        # =====================================================

                        st.markdown("### 📊 Executive Snapshot")

                        # -----------------------------------------------------
                        # Employee Search Results
                        # -----------------------------------------------------
                        if "Employee Name" in df.columns:

                            total_employees = len(df)
                            departments = df["Department"].nunique()
                            locations = df["Location"].nunique()

                            male_count = 0
                            female_count = 0

                            if "Gender" in df.columns:
                                male_count = (
                                    df["Gender"]
                                    .str.lower()
                                    .eq("male")
                                    .sum()
                                )

                                female_count = (
                                    df["Gender"]
                                    .str.lower()
                                    .eq("female")
                                    .sum()
                                )

                            col1, col2, col3, col4 = st.columns(4)

                            col1.metric(
                                "👥 Employees Found",
                                total_employees
                            )

                            col2.metric(
                                "🏢 Departments",
                                departments
                            )

                            col3.metric(
                                "📍 Locations",
                                locations
                            )

                            col4.metric(
                                "👩 / 👨",
                                f"{female_count} / {male_count}"
                            )

                        # -----------------------------------------------------
                        # Analytics Reports
                        # -----------------------------------------------------
                        else:

                            total_records = len(df)

                            first_column = df.columns[0]
                            second_column = df.columns[-1]

                            highest_row = df.loc[df[second_column].idxmax()]
                            lowest_row = df.loc[df[second_column].idxmin()]

                            average_value = df[second_column].mean()

                            col1, col2, col3, col4 = st.columns(4)

                            col1.metric(
                                "Total Records",
                                total_records
                            )

                            col2.metric(
                                "Highest",
                                f"{highest_row[first_column]} ({highest_row[second_column]})"
                            )

                            col3.metric(
                                "Lowest",
                                f"{lowest_row[first_column]} ({lowest_row[second_column]})"
                            )

                            col4.metric(
                                "Average",
                                f"{average_value:.1f}"
                            )                        
                        # ============================================
                        # EXECUTIVE INSIGHTS
                        # ============================================

                        if answer.get("title") == "📊 Department-wise Headcount":

                            total_departments = len(df)

                            largest = df.iloc[0]

                            smallest = df.iloc[-1]

                            average = round(
                                df["Employee Count"].mean(),
                                1
                            )

                            st.info(
                                f"""
📌 **Executive Insights**

• Total Departments : **{total_departments}**

• Largest Department : **{largest['Department']}** ({largest['Employee Count']} employees)

• Smallest Department : **{smallest['Department']}** ({smallest['Employee Count']} employees)

• Average Employees per Department : **{average}**
"""
                            )

                        elif answer.get("title") == "📍 Location-wise Headcount":

                            largest = df.iloc[0]

                            smallest = df.iloc[-1]

                            st.info(
                                f"""
📌 **Executive Insights**

• Total Locations : **{len(df)}**

• Largest Location : **{largest['Location']}** ({largest['Employee Count']} employees)

• Smallest Location : **{smallest['Location']}** ({smallest['Employee Count']} employees)
"""
                            )

                        elif answer.get("title") == "👥 Gender Distribution":

                            total = df["Employee Count"].sum()

                            male = df.loc[
                                df["Gender"] == "Male",
                                "Employee Count"
                            ].sum()

                            female = df.loc[
                                df["Gender"] == "Female",
                                "Employee Count"
                            ].sum()

                            st.info(
                                f"""
📌 **Executive Insights**

• Total Employees : **{total}**

• Male Employees : **{male}**

• Female Employees : **{female}**

• Gender Diversity is available across the workforce.
"""
                            )

                        elif "Average Experience" in answer.get("title", ""):

                            highest = df.iloc[0]

                            lowest = df.iloc[-1]

                            column = df.columns[0]

                            st.info(
                                f"""
📌 **Executive Insights**

• Highest Average Experience : **{highest[column]}** ({highest['Average Experience (Years)']} years)

• Lowest Average Experience : **{lowest[column]}** ({lowest['Average Experience (Years)']} years)

• Organization-wide comparison completed.
"""
                            )

                        elif "Average Salary" in answer.get("title", ""):

                            highest = df.iloc[0]

                            lowest = df.iloc[-1]

                            column = df.columns[0]

                            gap = highest["Average Salary"] - lowest["Average Salary"]

                            st.info(
                                f"""
📌 **Executive Insights**

• Highest Average Salary : **{highest[column]}**

• Lowest Average Salary : **{lowest[column]}**

• Salary Difference : **₹{gap:,.0f}**
"""
                            )

                        elif "Gender Distribution" in answer.get("title", ""):

                            st.info(
                                """
📌 **Executive Insights**

• Gender representation is available across all groups.

• Review departments or roles with lower representation.

• Use this report to support diversity and inclusion initiatives.
"""
                            )

                        # ============================================
                        # AUTO CHARTS
                        # ============================================

                        # Department-wise Headcount
                        if answer.get("title") == "📊 Department-wise Headcount":

                            fig, ax = plt.subplots(figsize=(9, 5))

                            ax.bar(
                                df["Department"],
                                df["Employee Count"]
                            )

                            ax.set_title("Department-wise Headcount")
                            ax.set_xlabel("Department")
                            ax.set_ylabel("Employees")

                            plt.xticks(rotation=45)
                            plt.tight_layout()

                            st.pyplot(fig)
                                                    # Location-wise Headcount
                        elif answer.get("title") == "📍 Location-wise Headcount":

                            fig, ax = plt.subplots(figsize=(9, 5))

                            ax.bar(df["Location"], df["Employee Count"])

                            ax.set_title("Location-wise Headcount")
                            ax.set_xlabel("Location")
                            ax.set_ylabel("Employees")

                            plt.xticks(rotation=45)
                            plt.tight_layout()

                            st.pyplot(fig)

                        # Gender Distribution
                        elif answer.get("title") == "👥 Gender Distribution":

                            fig, ax = plt.subplots(figsize=(7, 7))

                            ax.pie(
                                df["Employee Count"],
                                labels=df["Gender"],
                                autopct="%1.1f%%",
                                startangle=90
                            )

                            ax.set_title("Gender Distribution")

                            st.pyplot(fig)

                        # Department-wise Average Experience
                        elif answer.get("title") == "📈 Department-wise Average Experience":

                            fig, ax = plt.subplots(figsize=(9, 5))

                            ax.bar(
                                df["Department"],
                                df["Average Experience (Years)"]
                            )

                            ax.set_title("Department-wise Average Experience")

                            plt.xticks(rotation=45)

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Department-wise Average Salary
                        elif answer.get("title") == "💰 Department-wise Average Salary":

                            fig, ax = plt.subplots(figsize=(9, 5))

                            ax.barh(
                                df["Department"],
                                df["Average Salary"]
                            )

                            ax.set_title("Department-wise Average Salary")

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Location-wise Average Experience
                        elif answer.get("title") == "📍 Location-wise Average Experience":

                            fig, ax = plt.subplots(figsize=(9, 5))

                            ax.bar(
                                df["Location"],
                                df["Average Experience (Years)"]
                            )

                            ax.set_title("Location-wise Average Experience")

                            plt.xticks(rotation=45)

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Location-wise Average Salary
                        elif answer.get("title") == "💰 Location-wise Average Salary":

                            fig, ax = plt.subplots(figsize=(9, 5))

                            ax.barh(
                                df["Location"],
                                df["Average Salary"]
                            )

                            ax.set_title("Location-wise Average Salary")

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Designation-wise Headcount
                        elif answer.get("title") == "👤 Designation-wise Headcount":

                            fig, ax = plt.subplots(figsize=(11, 5))

                            ax.bar(
                                df["Designation"],
                                df["Employee Count"]
                            )

                            ax.set_title("Designation-wise Headcount")

                            plt.xticks(rotation=45)

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Designation-wise Average Experience
                        elif answer.get("title") == "📈 Designation-wise Average Experience":

                            fig, ax = plt.subplots(figsize=(11, 5))

                            ax.bar(
                                df["Designation"],
                                df["Average Experience (Years)"]
                            )

                            ax.set_title("Designation-wise Average Experience")

                            plt.xticks(rotation=45)

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Designation-wise Average Salary
                        elif answer.get("title") == "💰 Designation-wise Average Salary":

                            fig, ax = plt.subplots(figsize=(11, 5))

                            ax.barh(
                                df["Designation"],
                                df["Average Salary"]
                            )

                            ax.set_title("Designation-wise Average Salary")

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Department-wise Gender Distribution
                        elif answer.get("title") == "👥 Department-wise Gender Distribution":

                            pivot = df.pivot(
                                index="Department",
                                columns="Gender",
                                values="Employee Count"
                            ).fillna(0)

                            fig, ax = plt.subplots(figsize=(10, 5))

                            pivot.plot(
                                kind="bar",
                                stacked=True,
                                ax=ax
                            )

                            plt.xticks(rotation=45)

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Designation-wise Gender Distribution
                        elif answer.get("title") == "👥 Designation-wise Gender Distribution":

                            pivot = df.pivot(
                                index="Designation",
                                columns="Gender",
                                values="Employee Count"
                            ).fillna(0)

                            fig, ax = plt.subplots(figsize=(12, 5))

                            pivot.plot(
                                kind="bar",
                                stacked=True,
                                ax=ax
                            )

                            plt.xticks(rotation=45)

                            plt.tight_layout()

                            st.pyplot(fig)

                        # Display Table
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )
                        # ============================================
                        # SUGGESTED FOLLOW-UP QUESTIONS
                        # ============================================

                        st.markdown("### 💡 Suggested Follow-up Questions")

                        suggestions = []

                        if answer.get("title") == "📊 Department-wise Headcount":

                            suggestions = [
                                "Show average salary by department",
                                "Show average experience by department",
                                "Show gender distribution by department"
                            ]

                        elif answer.get("title") == "📍 Location-wise Headcount":

                            suggestions = [
                                "Show average salary by location",
                                "Show average experience by location",
                                "Which location has the highest headcount?"
                            ]

                        elif answer.get("title") == "👥 Gender Distribution":

                            suggestions = [
                                "Show gender distribution by department",
                                "Show gender distribution by designation",
                                "Show department-wise headcount"
                            ]

                        elif "Average Salary" in answer.get("title", ""):

                            suggestions = [
                                "Show average experience by department",
                                "Show department-wise headcount",
                                "Show designation-wise average salary"
                            ]

                        elif "Average Experience" in answer.get("title", ""):

                            suggestions = [
                                "Show average salary by department",
                                "Show department-wise headcount",
                                "Show designation-wise average experience"
                            ]

                        elif "Gender Distribution" in answer.get("title", ""):

                            suggestions = [
                                "Show department-wise headcount",
                                "Show average salary by department",
                                "Show average experience by department"
                            ]

                        for suggestion in suggestions:

                            if st.button(
                                suggestion,
                                key=f"{chat['question']}_{suggestion}"
                            ):

                                st.session_state.selected_question = suggestion

                                st.rerun()

                        # ---------------------------------------------
                        # Export to Excel
                        # ---------------------------------------------

                        wb = Workbook()

                        ws = wb.active

                        ws.title = "Employee Search"

                        ws.append(["Visionary InfoTech Pvt. Ltd."])

                        ws.append([])

                        ws.append(list(df.columns))

                        for cell in ws[3]:
                            cell.font = Font(bold=True)

                        for row in df.itertuples(index=False):
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

                    report_name = (
                        answer["title"]
                        .replace("📊", "")
                        .replace("👥", "")
                        .replace("📍", "")
                        .replace("💰", "")
                        .replace("📈", "")
                        .strip()
                        .replace(" ", "_")
                    )

                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_file,
                        file_name=f"{report_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_excel_{chat['question']}_{len(df)}"
                    )
                    
                    # =====================================================
                    # PDF DOWNLOAD
                    # =====================================================

                    pdf = generate_pdf(
                        question=chat["question"],
                        summary=answer["summary"],
                        dataframe=df
                    )

                    report_name = (
                        answer["title"]
                        .replace("📊", "")
                        .replace("👥", "")
                        .replace("📍", "")
                        .replace("💰", "")
                        .replace("📈", "")
                        .strip()
                        .replace(" ", "_")
                    )

                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf,
                        file_name=f"{report_name}.pdf",
                        mime="application/pdf"
                    )
                # ----------------------------
                # TEXT RESPONSE
                # ----------------------------
                elif response_type == "text":

                    st.markdown(answer["answer"])

                    pdf = generate_pdf(
                        question=chat["question"],
                        summary=answer["answer"],
                        dataframe=None
                    )

                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf,
                        file_name="HRBP_AI_Report.pdf",
                        mime="application/pdf",
                        key=f"download_pdf_{chat['question']}"
                    )

                # ----------------------------
                # CHART RESPONSE
                # ----------------------------
                elif response_type == "chart":

                    if answer.get("title"):
                        st.subheader(answer["title"])

                    if answer.get("summary"):
                        st.write(answer["summary"])

                    if answer.get("chart") is not None:
                        st.pyplot(answer["chart"])

                    if answer.get("data") is not None:
                        st.dataframe(
                            answer["data"],
                            use_container_width=True,
                            hide_index=True
                        )

                # ----------------------------
                # UNKNOWN DICTIONARY
                # ----------------------------
                else:
                    st.write(answer)

            # ----------------------------
            # STRING RESPONSE
            # ----------------------------
            else:
                st.write(answer)

else:

    st.info(
        "👋 Ask an HR question or click one of the suggested questions above."
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Visionary InfoTech Pvt. Ltd. • AI Workforce Assistant • HR Analytics Portfolio Project"
)

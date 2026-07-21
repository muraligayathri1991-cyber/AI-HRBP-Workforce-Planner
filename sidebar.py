import streamlit as st


def sidebar_filters(employees):

    # ==========================================
    # WORKFORCE FILTERS
    # ==========================================

    st.sidebar.title("🔎 Workforce Filters")

    st.sidebar.markdown("---")

    # Department Filter
    department = st.sidebar.selectbox(
        "🏢 Department",
        ["All"] + sorted(employees["Department"].unique().tolist())
    )

    if department != "All":
        employees = employees[
            employees["Department"] == department
        ]

    # Location Filter
    location = st.sidebar.selectbox(
        "📍 Location",
        ["All"] + sorted(employees["Location"].unique().tolist())
    )

    if location != "All":
        employees = employees[
            employees["Location"] == location
        ]

    # Designation Filter
    designation = st.sidebar.selectbox(
        "💼 Designation",
        ["All"] + sorted(employees["Designation"].unique().tolist())
    )

    if designation != "All":
        employees = employees[
            employees["Designation"] == designation
        ]

    # Employee Search
    search = st.sidebar.text_input("🔍 Search Employee")

    if search:
        employees = employees[
            employees["Employee Name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    return employees
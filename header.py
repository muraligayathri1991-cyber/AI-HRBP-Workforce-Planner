import streamlit as st
from pathlib import Path


def show_header():

    logo_path = Path(__file__).parent / "assets" / "logo.png"

    col1, col2 = st.columns([1, 5])

    with col1:
        if logo_path.exists():
            st.image(str(logo_path), width=170)

    with col2:

        st.markdown(
            """
            <h1 style="margin-bottom:0px;
                       color:#0B3D91;">
                Visionary InfoTech Pvt. Ltd.
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <h3 style="margin-top:0px;
                       color:#555555;">
                AI Workforce Planning & HRBP Analytics Platform
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Empowering HR Leaders with Workforce Intelligence"
        )

    st.divider()
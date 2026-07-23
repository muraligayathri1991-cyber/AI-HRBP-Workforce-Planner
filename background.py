import streamlit as st
import base64
import os


def show_background(image_path):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, image_path)

    with open(full_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(255,255,255,0.90);
            z-index: -1;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
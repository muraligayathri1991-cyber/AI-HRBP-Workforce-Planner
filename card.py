import streamlit as st
from contextlib import contextmanager


@contextmanager
def card():

    st.markdown(
        """
        <div style="
            background: white;
            padding: 28px;
            border-radius: 18px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 8px 24px rgba(15,23,42,0.08);
            margin-bottom: 24px;
        ">
        """,
        unsafe_allow_html=True,
    )

    yield

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )
import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* ==========================
           Main App
        ========================== */

        .stApp{
            background-color:#F5F7FA;
        }

        /* ==========================
           Headers
        ========================== */

        h1{
            color:#0B3D91;
            font-weight:700;
        }

        h2,h3{
            color:#12355B;
        }

        /* ==========================
           Metric Cards
        ========================== */

        div[data-testid="stMetric"]{

            background:white;

            padding:18px;

            border-radius:12px;

            border:1px solid #E4E7EC;

            box-shadow:0px 2px 8px rgba(0,0,0,0.05);

        }

        /* ==========================
           Buttons
        ========================== */

        .stButton>button{

            width:100%;

            border-radius:10px;

            height:48px;

            font-weight:600;

            border:none;

            background:#0B5ED7;

            color:white;

        }

        .stButton>button:hover{

            background:#094DB1;

            color:white;

        }

        /* ==========================
           Text Input
        ========================== */

        .stTextInput input{

            border-radius:10px;

            border:1px solid #C9D3E0;

        }

        /* ==========================
           Dataframe
        ========================== */

        div[data-testid="stDataFrame"]{

            border-radius:12px;

            overflow:hidden;

            border:1px solid #E4E7EC;

        }

        /* ==========================
           Sidebar
        ========================== */

        section[data-testid="stSidebar"]{

            background:#FFFFFF;

        }

        /* ==========================
           Info / Success
        ========================== */

        div[data-baseweb="notification"]{

            border-radius:12px;

        }

        </style>
        """,
        unsafe_allow_html=True
    )
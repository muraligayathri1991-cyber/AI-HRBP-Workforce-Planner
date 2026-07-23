import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* ==========================================================
           MAIN APPLICATION
        ========================================================== */

        .stApp{

            color:#1F2937;

        }

        /* ==========================================================
           HEADINGS
        ========================================================== */

        h1{

            color:#FFFFFF;

            font-weight:800;

            letter-spacing:0.4px;

        }

        h2{

            color:#FFFFFF;

            font-weight:700;

        }

        h3{

            color:#FFFFFF;

            font-weight:700;

        }

        /* ==========================================================
           PARAGRAPHS
        ========================================================== */

        p{

            font-size:16px;

            line-height:1.7;

        }

        .stApp p{

            color:#4B5563;

        }

        .stButton p{

            color:#FFFFFF !important;

            font-weight:700 !important;

        }

        /* ==========================================================
           SIDEBAR
        ========================================================== */

        section[data-testid="stSidebar"]{

            background:linear-gradient(180deg,#103B73 0%,#0B2E59 100%);

            border-right:1px solid rgba(255,255,255,0.08);

        }

        section[data-testid="stSidebar"] *{

            color:white !important;

        }

        section[data-testid="stSidebar"] hr{

            border-color:rgba(255,255,255,0.15);

        }

        /* ==========================================================
           METRIC CARDS
        ========================================================== */

        div[data-testid="stMetric"]{

            background:white;

            padding:14px 18px;

            min-height:120px;

            border-radius:18px;

            border:1px solid #E5E7EB;

            box-shadow:
                0 8px 25px rgba(0,0,0,0.06);

            transition:0.3s;

        }

        div[data-testid="stMetric"]:hover{

            transform:translateY(-4px);

            box-shadow:
                0 15px 35px rgba(0,0,0,0.10);

        }

        /* KPI Labels */

        div[data-testid="stMetricLabel"]{

            color:#222222 !important;

            font-weight:600 !important;

            font-size:19px !important;

        }

        div[data-testid="stMetricLabel"] *{

            color:#222222 !important;

        }

        /* KPI Values */

        div[data-testid="stMetricValue"]{

            color:#111111 !important;

            font-weight:700 !important;

        }

        div[data-testid="stMetricValue"] *{

            color:#111111 !important;

            font-weight:700 !important;

            font-size:22px !important;

        }

        /* ==========================================================
           BUTTONS
        ========================================================== */

        .stButton > button{

            width:100%;

            height:56px;

            border:none;

            border-radius:14px;

            background:linear-gradient(90deg,#1565C0,#2196F3);

            color:#FFFFFF !important;

            font-size:17px;

            font-weight:700;

            transition:all 0.3s ease;

        }

        .stButton > button:hover{

            transform:translateY(-2px);

            background:linear-gradient(90deg,#0D47A1,#1976D2);

            color:#FFFFFF !important;

        }

        /* ==========================================================
           DOWNLOAD BUTTON
        ========================================================== */

        .stDownloadButton > button{

            width:100%;

            height:50px;

            border-radius:14px;

            border:none;

            background:linear-gradient(90deg,#00897B,#26A69A);

            color:white;

            font-weight:700;

        }

        .stDownloadButton > button:hover{

            background:linear-gradient(90deg,#00695C,#00897B);

            color:white;

        }

        /* ==========================================================
           TEXT INPUT
        ========================================================== */

        .stTextInput input{

            border-radius:12px;

            border:1px solid #D1D5DB;

            padding:10px;

            color:#222222 !important;

            background:white;

        }

        .stTextInput input::placeholder{

            color:#666666 !important;

            opacity:1;

        }

        /* ==========================================================
           SELECT BOX
        ========================================================== */

        div[data-baseweb="select"]{

            border-radius:12px;

            color:#222222 !important;

        }
        div[data-baseweb="select"] span{

            color:#222222 !important;

        }

        div[data-baseweb="select"] input{

            color:#222222 !important;

        }
        /* ==========================================================
           DATAFRAME
        ========================================================== */

        div[data-testid="stDataFrame"]{

            border-radius:18px;

            overflow:hidden;

            border:1px solid #E5E7EB;

            box-shadow:
                0 5px 18px rgba(0,0,0,0.05);

        }

        /* ==========================================================
           ALERTS
        ========================================================== */

        div[data-baseweb="notification"]{

            border-radius:16px;

            border:none;

        }

        /* ==========================================================
           HORIZONTAL RULE
        ========================================================== */

        hr{

            border:none;

            border-top:1px solid #D8E4F0;

        }

        /* ==========================================================
           IMAGE
        ========================================================== */

        img{

            border-radius:18px;

        }
    /* ==========================================================
    RECENT JOINERS CARDS
    ========================================================== */

            </style>
            """,
            unsafe_allow_html=True
        )
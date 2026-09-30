import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

st.set_page_config(
    page_title="EH Counter",
    page_icon="🔢",
    layout="centered"
)

EXCEL_FILE = "counter.xlsx"
BACKGROUND_IMAGE = "background.jpeg"


# -----------------------------
# Background
# -----------------------------

if os.path.exists(BACKGROUND_IMAGE):

    with open(BACKGROUND_IMAGE, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image: url(
                "data:image/jpeg;base64,{encoded}"
            );
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .counter-box {{
            background: rgba(255, 255, 255, 0.90);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin-top: 100px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.25);
        }}

        .counter-number {{
            font-size: 80px;
            font-weight: bold;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Load Excel safely
# -----------------------------

def load_data():

    if not os.path.exists(EXCEL_FILE):
        return pd.DataFrame(
            columns=["Date & Time", "Action", "Count"]
        )

    try:
        return pd.read_excel(EXCEL_FILE)

    except Exception:
        # If the Excel file is corrupted/invalid,
        # start with a fresh dataframe.
        return pd.DataFrame(
            columns=["Date & Time", "Action", "Count"]
        )


df = load_data()


# -----------------------------
# Current count
# -----------------------------

if df.empty:
    current_count = 0
else:
    current_count = int(df.iloc[-1]["Count"])


# -----------------------------
# Save to Excel
# -----------------------------

def save_action(action, count):

    global df

    new_row = pd.DataFrame({
        "Date & Time": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],
        "Action": [action],
        "Count": [count]
    })

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_excel(
        EXCEL_FILE,
        index=False
    )


# -----------------------------
# Counter display
# -----------------------------

st.markdown(
    f"""
    <div class="counter-box">

        <h1>🔢 Counter</h1>

        <div class="counter-number">
            {current_count}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


st.write("")


# -----------------------------
# Buttons
# -----------------------------

col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "➖ Decrease",
        use_container_width=True
    ):

        save_action(
            "Decrease",
            current_count - 1
        )

        st.rerun()


with col2:

    if st.button(
        "🔄 Reset",
        use_container_width=True
    ):

        save_action(
            "Reset",
            0
        )

        st.rerun()


with col3:

    if st.button(
        "➕ Increase",
        use_container_width=True
    ):

        save_action(
            "Increase",
            current_count + 1
        )

        st.rerun()


# -----------------------------
# Show history
# -----------------------------

with st.expander("📊 View saved data"):

    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True
        )
    else:
        st.info("No counter data yet.")

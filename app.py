import streamlit as st
import pandas as pd
import os
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------

st.set_page_config(
    page_title="Counter App",
    page_icon="🔢",
    layout="centered"
)

EXCEL_FILE = "counter.xlsx"
BACKGROUND_IMAGE = "background.jpg"


# -----------------------------
# Background Image
# -----------------------------

if os.path.exists(BACKGROUND_IMAGE):
    with open(BACKGROUND_IMAGE, "rb") as image_file:
        import base64

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .counter-box {{
            background: rgba(255, 255, 255, 0.88);
            padding: 35px;
            border-radius: 20px;
            text-align: center;
            max-width: 500px;
            margin: 100px auto 20px auto;
            box-shadow: 0px 8px 30px rgba(0,0,0,0.25);
        }}

        .counter-number {{
            font-size: 80px;
            font-weight: bold;
            margin: 10px;
        }}

        .counter-title {{
            font-size: 32px;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Create Excel file
# -----------------------------

if not os.path.exists(EXCEL_FILE):

    df = pd.DataFrame({
        "Date & Time": [],
        "Action": [],
        "Count": []
    })

    df.to_excel(EXCEL_FILE, index=False)


# -----------------------------
# Read current count
# -----------------------------

df = pd.read_excel(EXCEL_FILE)

if len(df) == 0:
    current_count = 0
else:
    current_count = int(df.iloc[-1]["Count"])


# -----------------------------
# Save action to Excel
# -----------------------------

def save_action(action, count):

    new_row = pd.DataFrame({
        "Date & Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Action": [action],
        "Count": [count]
    })

    existing_df = pd.read_excel(EXCEL_FILE)

    updated_df = pd.concat(
        [existing_df, new_row],
        ignore_index=True
    )

    updated_df.to_excel(
        EXCEL_FILE,
        index=False
    )


# -----------------------------
# Display Counter
# -----------------------------

st.markdown(
    f"""
    <div class="counter-box">

        <div class="counter-title">
            🔢 Counter
        </div>

        <div class="counter-number">
            {current_count}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Buttons
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "➖ Decrease",
        use_container_width=True
    ):

        new_count = current_count - 1

        save_action(
            "Decrease",
            new_count
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

        new_count = current_count + 1

        save_action(
            "Increase",
            new_count
        )

        st.rerun()


# -----------------------------
# Show Excel Data
# -----------------------------

st.write("")

with st.expander("📊 View saved data"):

    saved_data = pd.read_excel(EXCEL_FILE)

    st.dataframe(
        saved_data,
        use_container_width=True
    )

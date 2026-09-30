
import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

st.set_page_config(
    page_title="Counter",
    page_icon="🔢",
    layout="centered"
)

EXCEL_FILE = "counter.xlsx"
BACKGROUND_IMAGE = "background.jpg"


# -----------------------------
# Background Image
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
            background: rgba(255, 255, 255, 0.92);
            padding: 40px;
            border-radius: 25px;
            text-align: center;
            margin-top: 80px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.30);
        }}

        .counter-title {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .counter-number {{
            font-size: 110px;
            font-weight: 900;
            line-height: 1;
            margin: 20px 0;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Load Excel
# -----------------------------

def load_data():

    if not os.path.exists(EXCEL_FILE):
        return pd.DataFrame(
            columns=["Date & Time", "Action", "Count"]
        )

    try:
        return pd.read_excel(EXCEL_FILE)

    except Exception:
        return pd.DataFrame(
            columns=["Date & Time", "Action", "Count"]
        )


df = load_data()


# -----------------------------
# Current Count
# -----------------------------

if df.empty:
    current_count = 0
else:
    current_count = int(df.iloc[-1]["Count"])


# -----------------------------
# Display Counter
# -----------------------------

st.markdown(
    f"""
    <div class="counter-box">

        <div class="counter-title">
            🔢 COUNTER
        </div>

        <div class="counter-number">
            {current_count}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


st.write("")


# -----------------------------
# Counter Buttons
# -----------------------------

col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "➖ Decrease",
        use_container_width=True
    ):

        new_count = current_count - 1

        new_row = pd.DataFrame({
            "Date & Time": [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ],
            "Action": ["Decrease"],
            "Count": [new_count]
        })

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        df.to_excel(EXCEL_FILE, index=False)

        st.rerun()


with col2:

    if st.button(
        "🔄 Reset",
        use_container_width=True
    ):

        new_row = pd.DataFrame({
            "Date & Time": [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ],
            "Action": ["Reset"],
            "Count": [0]
        })

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        df.to_excel(EXCEL_FILE, index=False)

        st.rerun()


with col3:

    if st.button(
        "➕ Increase",
        use_container_width=True
    ):

        new_count = current_count + 1

        new_row = pd.DataFrame({
            "Date & Time": [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ],
            "Action": ["Increase"],
            "Count": [new_count]
        })

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        df.to_excel(EXCEL_FILE, index=False)

        st.rerun()


# -----------------------------
# Save Button
# -----------------------------

st.write("")

if st.button(
    "💾 SAVE CURRENT COUNT",
    use_container_width=True
):

    # Save the current count as a separate record
    new_row = pd.DataFrame({
        "Date & Time": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],
        "Action": ["Saved"],
        "Count": [current_count]
    })

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_excel(
        EXCEL_FILE,
        index=False
    )

    st.success(
        f"Count {current_count} saved successfully! ✅"
    )


# -----------------------------
# Excel History
# -----------------------------

with st.expander("📊 View Saved Data"):

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info("No data saved yet.")


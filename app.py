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
BACKGROUND_IMAGE = "background.jpeg"


# =========================
# BACKGROUND IMAGE
# =========================

if os.path.exists(BACKGROUND_IMAGE):
    with open(BACKGROUND_IMAGE, "rb") as f:
        image = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================
# LOAD EXCEL
# =========================

def load_excel():

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


df = load_excel()


# =========================
# CURRENT COUNT
# =========================

if df.empty:
    current_count = 0
else:
    current_count = int(df.iloc[-1]["Count"])


# =========================
# SAVE TO EXCEL
# =========================

def save_to_excel(action, count):

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


# =========================
# TITLE
# =========================

st.markdown(
    """
    <div style="
        text-align: center;
        color: white;
        font-size: 55px;
        font-weight: 900;
        margin-top: 30px;
        margin-bottom: 15px;
    ">
        COUNTER
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# BIG COUNT
# =========================

st.markdown(
    f"""
    <div style="
        text-align: center;
        color: white;
        font-size: 150px;
        font-weight: 900;
        line-height: 1;
        margin-top: 20px;
        margin-bottom: 50px;
    ">
        {current_count}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# BUTTONS
# =========================

col1, col2, col3 = st.columns(3)


# DECREASE
with col1:

    if st.button(
        "➖ Decrease",
        use_container_width=True
    ):

        new_count = current_count - 1

        save_to_excel(
            "Decrease",
            new_count
        )

        st.rerun()


# RESET
with col2:

    if st.button(
        "🔄 Reset",
        use_container_width=True
    ):

        save_to_excel(
            "Reset",
            0
        )

        st.rerun()


# INCREASE
with col3:

    if st.button(
        "➕ Increase",
        use_container_width=True
    ):

        new_count = current_count + 1

        save_to_excel(
            "Increase",
            new_count
        )

        st.rerun()


# =========================
# SAVE CURRENT COUNT
# =========================

st.write("")

if st.button(
    "💾 SAVE CURRENT COUNT",
    use_container_width=True
):

    save_to_excel(
        "Manual Save",
        current_count
    )

    st.success(
        f"Count {current_count} has been saved! ✅"
    )


# =========================
# VIEW EXCEL DATA
# =========================

with st.expander("📊 View Excel Data"):

    if df.empty:

        st.info("No data yet.")

    else:

        st.dataframe(
            df,
            use_container_width=True
        )

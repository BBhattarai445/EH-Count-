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


# -----------------------------
# Background image
# -----------------------------
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


# -----------------------------
# Load Excel
# -----------------------------
def load_excel():
    if not os.path.exists(EXCEL_FILE):
        return pd.DataFrame(columns=["Date & Time", "Action", "Count", "Note"])

    try:
        return pd.read_excel(EXCEL_FILE)
    except Exception:
        return pd.DataFrame(columns=["Date & Time", "Action", "Count", "Note"])


df = load_excel()


# -----------------------------
# Get current count
# -----------------------------
if df.empty:
    current_count = 0
else:
    current_count = int(df.iloc[-1]["Count"])


# -----------------------------
# Save data to Excel
# -----------------------------
def save_to_excel(action, count, note=""):
    global df

    new_data = pd.DataFrame({
        "Date & Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Action": [action],
        "Count": [count],
        "Note": [note]
    })

    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)


# -----------------------------
# TITLE
# -----------------------------
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
       SUSMA EH COUNTER
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# NOTE - below title
# -----------------------------
note = st.text_area(
    "📝 Number of counters is equal to the number of kisses",
)


# -----------------------------
# BIG NUMBER
# -----------------------------
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


# -----------------------------
# BUTTONS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➖ Decrease", use_container_width=True):
        new_count = current_count - 1
        save_to_excel("Decrease", new_count, note)
        st.rerun()

with col2:
    if st.button("🔄 Reset", use_container_width=True):
        save_to_excel("Reset", 0, note)
        st.rerun()

with col3:
    if st.button("➕ Increase", use_container_width=True):
        new_count = current_count + 1
        save_to_excel("Increase", new_count, note)
        st.rerun()


# -----------------------------
# SAVE BUTTON
# -----------------------------
st.write("")

if st.button("💾 SAVE CURRENT COUNT", use_container_width=True):
    save_to_excel("Manual Save", current_count, note)
    st.success(f"Count {current_count} and note saved! ✅")


# -----------------------------
# VIEW EXCEL DATA
# -----------------------------
with st.expander("📊 View Excel Data"):
    if df.empty:
        st.info("No data yet.")
    else:
        st.dataframe(df, use_container_width=True)


import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Counter",
    page_icon="🔢",
    layout="centered"
)

EXCEL_FILE = "counter.xlsx"
BACKGROUND_IMAGE = "background.jpeg"
st.title("EH Counter SUSMA")
note = st.text_area(
    "Number of KISSES is equal to the count number ",
    color: black !important;
    height=100
)
# ==========================================
# BACKGROUND IMAGE
# ==========================================

if os.path.exists(BACKGROUND_IMAGE):

    with open(BACKGROUND_IMAGE, "rb") as f:
        image = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
                url("data:image/jpeg;base64,{image}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .counter-box {{
            background: rgba(255, 255, 255, 0.90);
            padding: 40px;
            border-radius: 25px;
            text-align: center;
            margin-top: 80px;
            box-shadow: 0px 8px 30px rgba(0,0,0,0.30);
        }}

        .counter-title {{
            font-size: 32px;
            font-weight: 700;
        }}

        .counter-number {{
            font-size: 120px;
            font-weight: 900;
            line-height: 1;
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# LOAD EXCEL
# ==========================================

def load_excel():

    if not os.path.exists(EXCEL_FILE):
        return pd.DataFrame(
            columns=[
                "Date & Time",
                "Action",
                "Count"
            ]
        )

    try:
        return pd.read_excel(EXCEL_FILE)

    except Exception:
        return pd.DataFrame(
            columns=[
                "Date & Time",
                "Action",
                "Count"
            ]
        )


df = load_excel()


# ==========================================
# GET CURRENT COUNT
# ==========================================

if df.empty:
    current_count = 0
else:
    current_count = int(df.iloc[-1]["Count"])


# ==========================================
# SAVE TO EXCEL
# ==========================================

def save_to_excel(action, count):

    global df

    new_data = pd.DataFrame({
        "Date & Time": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],
        "Action": [action],
        "Count": [count]
    })

    df = pd.concat(
        [df, new_data],
        ignore_index=True
    )

    df.to_excel(
        EXCEL_FILE,
        index=False
    )


# ==========================================
# DISPLAY COUNTER
# ==========================================

# ==========================================
# DISPLAY BIG COUNTER NUMBER
# ==========================================

st.markdown(
    f"""
    <div style="
        text-align: center;
        font-size: 150px;
        font-weight: 900;
        line-height: 1;
        margin-top: 100px;
        margin-bottom: 50px;
    ">
        {current_count}
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# BUTTONS
# ==========================================

st.write("")

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


# ==========================================
# SAVE BUTTON
# ==========================================

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
        f"Count {current_count} has been saved to Excel! ✅"
    )


# ==========================================
# SHOW EXCEL DATA
# ==========================================

st.write("")

with st.expander("📊 View Excel Data"):

    if df.empty:

        st.info("No data yet.")

    else:

        st.dataframe(
            df,
            use_container_width=True
        )


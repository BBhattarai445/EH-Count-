import streamlit as st

st.title("🔢 Susma EH counter ")

# Initialize counter
if "count" not in st.session_state:
    st.session_state.count = 0

# Display count
st.metric("Count", st.session_state.count)

# Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Increase"):
        st.session_state.count += 1
        st.rerun()

with col2:
    if st.button("➖ Decrease"):
        st.session_state.count -= 1
        st.rerun()

with col3:
    if st.button("🔄 Reset"):
        st.session_state.count = 0
        st.rerun()

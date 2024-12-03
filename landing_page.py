import streamlit as st

st.set_page_config(page_title="My Streamlit Apps", page_icon="🚀", layout="wide")

st.title("Welcome to My Streamlit Apps")

st.write("Choose an app to launch:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("WBCal"):
        st.markdown("[Go to App 1](https://caldash-eoewkytd6u7jyxfm2haaxn.streamlit.app)")

with col2:
    if st.button("KCF LIMS"):
        st.markdown("[Go to App 2](https://4ekgis64qetw42fdkrynsn.streamlit.app)")

with col3:
    if st.button("PO Request"):
        st.markdown("[Go to App 3](https://ntsmv7uynenkazkeftozjx.streamlit.app)")

st.write("---")
st.write("Each app opens in a new tab. You can always come back here to launch a different app.")

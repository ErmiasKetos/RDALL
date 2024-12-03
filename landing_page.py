import streamlit as st

st.set_page_config(page_title="My Streamlit Apps", page_icon="🚀", layout="wide")

st.title("Welcome to My Streamlit Apps")

st.write("Choose an app to launch:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Launch App 1"):
        st.markdown("[Go to App 1](https://your-app-1-url.streamlit.app)")

with col2:
    if st.button("Launch App 2"):
        st.markdown("[Go to App 2](https://your-app-2-url.streamlit.app)")

with col3:
    if st.button("Launch App 3"):
        st.markdown("[Go to App 3](https://your-app-3-url.streamlit.app)")

st.write("---")
st.write("Each app opens in a new tab. You can always come back here to launch a different app.")

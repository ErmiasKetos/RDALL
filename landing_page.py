import streamlit as st

st.set_page_config(page_title="My Streamlit Apps", page_icon="🚀", layout="wide")

st.title("Welcome to My Streamlit Apps")

st.write("Choose an app to launch:")

# Custom CSS to improve button appearance
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        height: 75px;
        font-size: 20px;
    }
    .app-description {
        margin-top: 10px;
        font-size: 14px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("WBCal"):
        st.markdown("[Go to WBCal](https://caldash-eoewkytd6u7jyxfm2haaxn.streamlit.app)")
    st.markdown('<p class="app-description">Probe calibration and management tool</p>', unsafe_allow_html=True)

with col2:
    if st.button("KCF LIMS"):
        st.markdown("[Go to KCF LIMS](https://4ekgis64qetw42fdkrynsn.streamlit.app)")
    st.markdown('<p class="app-description">Laboratory Information Management System</p>', unsafe_allow_html=True)

with col3:
    if st.button("PO Request"):
        st.markdown("[Go to PO Request](https://ntsmv7uynenkazkeftozjx.streamlit.app)")
    st.markdown('<p class="app-description">Purchase Order Request management</p>', unsafe_allow_html=True)

st.write("---")
st.write("Each app opens in a new tab. You can always come back here to launch a different app.")

# Additional information section
st.subheader("About Our Apps")
st.write("""
- **WBCal**: Our probe calibration and management tool helps ensure accurate measurements and maintains calibration records.
- **KCF LIMS**: Our Laboratory Information Management System streamlines lab operations and data management.
- **PO Request**: Simplify your purchase order process with our dedicated PO Request application.
""")

# Footer
st.markdown("---")
st.markdown("© 2023 Your Company Name. All rights reserved.")


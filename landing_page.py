import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Page configuration
st.set_page_config(page_title="My Streamlit Apps", page_icon="🚀", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        color: #ffffff;
        background-color: #4CAF50;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .app-description {
        margin-top: 10px;
        font-size: 16px;
        color: #666;
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    h1 {
        color: #2E86C1;
    }
    .stSubheader {
        font-size: 24px;
        color: #2E86C1;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("Welcome to Our Streamlit Apps Suite")

# Lottie Animation
lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, height=200, key="lottie")

st.write("Explore our powerful tools designed to streamline your workflow.")

# App buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("Launch WBCal", "https://caldash-eoewkytd6u7jyxfm2haaxn.streamlit.app", use_container_width=True)
    st.markdown('<p class="app-description">Advanced probe calibration and management tool</p>', unsafe_allow_html=True)

with col2:
    st.link_button("Launch KCF LIMS", "https://4ekgis64qetw42fdkrynsn.streamlit.app", use_container_width=True)
    st.markdown('<p class="app-description">Comprehensive Laboratory Information Management System</p>', unsafe_allow_html=True)

with col3:
    st.link_button("Launch PO Request", "https://ntsmv7uynenkazkeftozjx.streamlit.app", use_container_width=True)
    st.markdown('<p class="app-description">Efficient Purchase Order Request management</p>', unsafe_allow_html=True)

# Additional information section
st.subheader("About Our Apps")

with st.expander("WBCal - Probe Calibration and Management"):
    st.write("""
    WBCal is our state-of-the-art probe calibration and management tool. It offers:
    - Precise calibration tracking
    - Automated reminder system for recalibration
    - Comprehensive calibration history
    - Data visualization for calibration trends
    """)

with st.expander("KCF LIMS - Laboratory Information Management System"):
    st.write("""
    KCF LIMS streamlines your laboratory operations with features like:
    - Sample tracking and management
    - Instrument integration and monitoring
    - Customizable workflows and reporting
    - Quality control and assurance tools
    """)

with st.expander("PO Request - Purchase Order Management"):
    st.write("""
    Simplify your purchase order process with our PO Request app:
    - Easy-to-use request forms
    - Approval workflow automation
    - Budget tracking and reporting
    - Vendor management and performance analytics
    """)

# User guide
st.subheader("How to Use")
st.info("""
1. Click on the app button you want to launch.
2. The selected app will open in a new browser tab.
3. You can always return to this page to access other apps.
""")

# Footer
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("© 2023 Your Company Name. All rights reserved.")
with col2:
    st.markdown("For support, contact: support@yourcompany.com")


import streamlit as st
from streamlit_lottie import st_lottie
import requests
import re

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def is_valid_ketos_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@ketos\.com$'
    return re.match(pattern, email) is not None

# Page configuration
st.set_page_config(page_title="KETOS Streamlit Apps", page_icon="🧪", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    .main {
        background-color: #f0f8ff;
        padding: 2rem;
    }
    
    h1, h2, h3 {
        color: #2E86C1;
    }
    
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        color: #ffffff;
        background-color: #2E86C1;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2874A6;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .app-description {
        margin-top: 10px;
        font-size: 16px;
        color: #666;
    }
    
    .stSubheader {
        font-size: 24px;
        color: #2E86C1;
        margin-top: 2rem;
    }
    
    .hero-section {
        background-color: #e8f4fd;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False

# Login Form
if not st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.title("Welcome to KETOS Apps")
    email = st.text_input("Enter your KETOS email")
    if st.button("Login"):
        if is_valid_ketos_email(email):
            login()
        else:
            st.error("Please enter a valid KETOS email address.")
    st.markdown('</div>', unsafe_allow_html=True)

# Main Content (only shown when logged in)
if st.session_state.logged_in:
    # Header
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.title("KETOS Streamlit Apps Suite")
    st.write("Explore our powerful tools designed to streamline your workflow.")

    # Lottie Animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
    lottie_json = load_lottieurl(lottie_url)
    st_lottie(lottie_json, height=200, key="lottie")

    st.markdown('</div>', unsafe_allow_html=True)

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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("© 2023 KETOS. All rights reserved.")
    with col2:
        st.markdown("For support, contact: support@ketos.com")
    with col3:
        if st.button("Logout"):
            logout()


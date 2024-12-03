import streamlit as st
from streamlit_lottie import st_lottie
import requests
import re
import hmac
import hashlib

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.session_state["password_correct"]):
            st.session_state.authenticated = True
            del st.session_state["password"]  # Don't store password
            del st.session_state["password_correct"]
            return True
        else:
            st.session_state.authenticated = False
            st.error("😕 Password incorrect")
            return False

    if "authenticated" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Password", type="password", key="password",
            on_change=password_entered)
        return False
    elif not st.session_state.authenticated:
        # Password not correct, show input + error
        st.text_input(
            "Password", type="password", key="password",
            on_change=password_entered)
        return False
    else:
        # Password correct
        return True

def is_valid_ketos_email(email):
    """Validate if email is a ketos.co domain"""
    pattern = r'^[a-zA-Z0-9._%+-]+@ketos\.co$'
    return re.match(pattern, email) is not None

# Page configuration
st.set_page_config(
    page_title="KETOS Apps Login",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match KETOS branding
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button {
        background-color: #2E86C1;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #2874A6;
    }
    
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .ketos-title {
        color: #2E86C1;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 4px;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-footer {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main login interface
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # KETOS logo and title
        st.image("https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png", width=150)
        st.markdown('<p class="ketos-title">Welcome to KETOS Apps</p>', unsafe_allow_html=True)
        
        # Login form
        email = st.text_input("Email", placeholder="Enter your KETOS email")
        st.session_state["password_correct"] = "your_secure_password"  # In production, use proper authentication
        
        if st.button("Login"):
            if is_valid_ketos_email(email):
                if check_password():
                    st.session_state.authenticated = True
                    st.rerun()
            else:
                st.error("Please enter a valid KETOS email address (@ketos.co)")
        
        st.markdown('<div class="login-footer">Access restricted to KETOS employees only.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Main content after authentication
    st.title("KETOS Internal Applications")
    
    # App navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.link_button(
            "Launch WBCal",
            "https://caldash-eoewkytd6u7jyxfm2haaxn.streamlit.app",
            use_container_width=True
        )
        st.markdown("Probe calibration and management system")
        
    with col2:
        st.link_button(
            "Launch KCF LIMS",
            "https://4ekgis64qetw42fdkrynsn.streamlit.app",
            use_container_width=True
        )
        st.markdown("Laboratory Information Management System")
        
    with col3:
        st.link_button(
            "Launch PO Request",
            "https://ntsmv7uynenkazkeftozjx.streamlit.app",
            use_container_width=True
        )
        st.markdown("Purchase Order Request System")
    
    # Logout option
    if st.button("Logout", key="logout"):
        st.session_state.authenticated = False
        st.rerun()


import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import pathlib
import requests as http_requests

# Google OAuth credentials
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/userinfo.email']

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

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
    
    .google-button {
        background-color: white !important;
        color: #757575 !important;
        border: 1px solid #ddd !important;
        display: flex !important;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
    }
    
    .google-button:hover {
        background-color: #f5f5f5 !important;
    }
</style>
""", unsafe_allow_html=True)

def is_valid_ketos_email(email):
    """Validate if email is a ketos.co domain"""
    return email.lower().endswith('@ketos.co')

def initialize_google_auth():
    """Initialize Google OAuth flow"""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8501/callback'
    )
    return flow

def verify_google_token(token):
    """Verify Google OAuth token and extract user information"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
        return idinfo['email']
    except ValueError:
        return None

# Main login interface
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # KETOS logo and title
        st.image("https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png", width=150)
        st.markdown('<p class="ketos-title">Welcome to KETOS Apps</p>', unsafe_allow_html=True)
        
        # Google Sign-In button
        if st.button("Sign in with Google", key="google_signin"):
            try:
                flow = initialize_google_auth()
                authorization_url, state = flow.authorization_url()
                st.session_state.oauth_state = state
                st.markdown(f'<meta http-equiv="refresh" content="0;url={authorization_url}">', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Authentication error: {str(e)}")
        
        st.markdown('<div class="login-footer">Access restricted to KETOS employees only.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Callback handler
elif 'code' in st.experimental_get_query_params():
    code = st.experimental_get_query_params()['code'][0]
    flow = initialize_google_auth()
    flow.fetch_token(code=code)
    
    credentials = flow.credentials
    email = verify_google_token(credentials.id_token)
    
    if email and is_valid_ketos_email(email):
        st.session_state.authenticated = True
        st.session_state.user_email = email
        st.rerun()
    else:
        st.error("Please sign in with your KETOS email (@ketos.co)")
        st.session_state.authenticated = False
        if st.button("Try Again"):
            st.rerun()

# Main content after authentication
else:
    st.title("KETOS Internal Applications")
    
    # Display user info
    st.markdown(f"Logged in as: {st.session_state.user_email}")
    
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
        st.session_state.user_email = None
        st.rerun()


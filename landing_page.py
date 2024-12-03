import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os

# Google OAuth credentials
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

# Allowed email addresses
ALLOWED_EMAILS = {
    "user1@ketos.co",
    "user2@ketos.co",
    "user3@ketos.co"
    # Add more allowed email addresses here
}

# Check if credentials are set
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or not REDIRECT_URI:
    st.error("""
    Google OAuth credentials are not set. Please ensure you've added the following secrets in your Streamlit Cloud app settings:
    - GOOGLE_CLIENT_ID
    - GOOGLE_CLIENT_SECRET
    - REDIRECT_URI
    """)
    st.stop()

# Create a Flow object
flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },
    scopes=['https://www.googleapis.com/auth/userinfo.email', 'openid'],
    redirect_uri=REDIRECT_URI
)

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

def is_allowed_email(email):
    """Validate if email is in the allowed list"""
    return email.lower() in ALLOWED_EMAILS

def verify_google_token(token):
    """Verify Google OAuth token and extract user information"""
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
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
            authorization_url, _ = flow.authorization_url(prompt='consent')
            st.markdown(f'<meta http-equiv="refresh" content="0;url={authorization_url}">', unsafe_allow_html=True)
        
        st.markdown('<div class="login-footer">Access restricted to authorized KETOS employees only.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Callback handler
elif 'code' in st.experimental_get_query_params():
    code = st.experimental_get_query_params()['code'][0]
    flow.fetch_token(code=code)
    
    credentials = flow.credentials
    email = verify_google_token(credentials.id_token)
    
    if email and is_allowed_email(email):
        st.session_state.authenticated = True
        st.session_state.user_email = email
        st.rerun()
    else:
        st.error("Access denied. Please contact your administrator if you believe this is an error.")
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


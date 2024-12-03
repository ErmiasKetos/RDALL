import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import json
from urllib.parse import quote

# Google OAuth credentials
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

# Allowed email addresses
ALLOWED_EMAILS = {
    "ermias@ketos.co",
    "user2@ketos.co",
    "user3@ketos.co"
}

# Configure OAuth flow with additional parameters
client_config = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [REDIRECT_URI],
        "javascript_origins": [REDIRECT_URI.rstrip('/')]
    }
}

try:
    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=[
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
    )
    flow.redirect_uri = REDIRECT_URI
except Exception as e:
    st.error(f"Error configuring OAuth: {str(e)}")
    st.stop()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'oauth_state' not in st.session_state:
    st.session_state.oauth_state = None

# Page configuration
st.set_page_config(
    page_title="KETOS Apps Login",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

def generate_auth_url():
    """Generate Google OAuth URL with proper parameters"""
    try:
        auth_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            state=st.session_state.oauth_state
        )
        st.session_state.oauth_state = state
        return auth_url
    except Exception as e:
        st.error(f"Error generating auth URL: {str(e)}")
        return None

def verify_oauth_state(received_state):
    """Verify OAuth state parameter"""
    return received_state == st.session_state.oauth_state

def handle_oauth_callback(code):
    """Handle OAuth callback and token exchange"""
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        
        email = id_info.get('email', '').lower()
        if email in ALLOWED_EMAILS:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            return True
        else:
            st.error("Access denied. Email not authorized.")
            return False
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False

# Main login interface
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # KETOS logo and title
        st.image("https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png", width=150)
        st.markdown('<p class="ketos-title">Welcome to KETOS Apps</p>', unsafe_allow_html=True)
        
        # Handle OAuth callback
        query_params = st.experimental_get_query_params()
        if 'code' in query_params:
            code = query_params['code'][0]
            state = query_params.get('state', [None])[0]
            
            if verify_oauth_state(state):
                if handle_oauth_callback(code):
                    st.rerun()
            else:
                st.error("Invalid OAuth state. Please try again.")
        
        # Google Sign-In button
        if st.button("Sign in with Google", key="google_signin"):
            auth_url = generate_auth_url()
            if auth_url:
                st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
        
        st.markdown('<div class="login-footer">Access restricted to authorized KETOS employees only.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

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
        st.session_state.oauth_state = None
        st.rerun()


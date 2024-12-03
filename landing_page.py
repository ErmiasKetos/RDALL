import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import json
from urllib.parse import quote, urlencode

# Google OAuth credentials
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

# Allowed email addresses
ALLOWED_EMAILS = {
    "user1@ketos.co",
    "user2@ketos.co",
    "user3@ketos.co"
}

# Debug mode
DEBUG = True

def get_redirect_uri():
    """Get the correct redirect URI based on the environment"""
    if 'HOSTNAME' in os.environ:  # Streamlit Cloud
        return f"https://{os.environ['HOSTNAME']}/_oauth/callback"
    return "http://localhost:8501/_oauth/callback"  # Local development

# Configure OAuth flow with explicit redirect URI
flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [get_redirect_uri()],
        }
    },
    scopes=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ],
    redirect_uri=get_redirect_uri()
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = {}

# Page configuration
st.set_page_config(
    page_title="KETOS Apps Login",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# [Previous CSS styles remain the same]

def generate_auth_url():
    """Generate Google OAuth URL with state parameter"""
    return flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',
        state=json.dumps({'redirect_uri': get_redirect_uri()})
    )[0]

def verify_oauth2_token(token):
    """Verify the OAuth2 token with enhanced error handling"""
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        return idinfo
    except ValueError as e:
        if DEBUG:
            st.session_state.debug_info['token_verification_error'] = str(e)
        return None

# Debug information display
if DEBUG and not st.session_state.authenticated:
    with st.expander("Debug Information"):
        st.write("Current Redirect URI:", get_redirect_uri())
        st.write("Query Parameters:", st.experimental_get_query_params())
        if 'debug_info' in st.session_state:
            st.write("Debug Info:", st.session_state.debug_info)

# Main login interface
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # KETOS logo and title
        st.image("https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png", width=150)
        st.markdown('<p class="ketos-title">Welcome to KETOS Apps</p>', unsafe_allow_html=True)
        
        # Handle OAuth callback with enhanced error handling
        if 'code' in st.experimental_get_query_params():
            code = st.experimental_get_query_params()['code'][0]
            try:
                flow.fetch_token(code=code)
                credentials = flow.credentials
                
                if DEBUG:
                    st.session_state.debug_info['token_fetch'] = 'successful'
                    st.session_state.debug_info['has_id_token'] = hasattr(credentials, 'id_token')
                
                token_info = verify_oauth2_token(credentials.id_token)
                
                if token_info:
                    if token_info['email'] in ALLOWED_EMAILS:
                        st.session_state.authenticated = True
                        st.session_state.user_email = token_info['email']
                        st.rerun()
                    else:
                        st.error(f"Access denied. Email {token_info['email']} not authorized.")
                else:
                    st.error("Token verification failed. Please check debug information.")
            except Exception as e:
                if DEBUG:
                    st.session_state.debug_info['token_fetch_error'] = str(e)
                st.error(f"Authentication error. Please check debug information.")
        
        # Google Sign-In button
        if st.button("Sign in with Google", key="google_signin"):
            auth_url = generate_auth_url()
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
        st.rerun()


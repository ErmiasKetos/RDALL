import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import json
from urllib.parse import quote, urlencode

# Configuration
APP_TITLE = "KETOS Internal Apps"
APP_ICON = "🌊"
COMPANY_LOGO = "https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png"

# Security Configuration
ALLOWED_DOMAIN = "ketos.co"
ALLOWED_EMAILS = {
    "ermias@ketos.co",
    "user2@ketos.co",
    "user3@ketos.co"
}

# App URLs
APPS = {
    "WBCal": {
        "url": "https://caldash-eoewkytd6u7jyxfm2haaxn.streamlit.app",
        "description": "Probe calibration and management system"
    },
    "KCF LIMS": {
        "url": "https://4ekgis64qetw42fdkrynsn.streamlit.app",
        "description": "Laboratory Information Management System"
    },
    "PO Request": {
        "url": "https://ntsmv7uynenkazkeftozjx.streamlit.app",
        "description": "Purchase Order Request System"
    }
}

# Custom styles
CUSTOM_CSS = """
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
        width: 100%;
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
        text-align: center;
    }
    
    .app-card {
        padding: 1.5rem;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 1rem;
        background-color: white;
        transition: transform 0.2s;
    }
    
    .app-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .user-info {
        padding: 0.5rem 1rem;
        background-color: #f8f9fa;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    
    .logout-button {
        float: right;
    }
</style>
"""

# Initialize Google OAuth flow
def init_oauth_flow():
    return Flow.from_client_config(
        client_config={
            "web": {
                "client_id": st.secrets["GOOGLE_CLIENT_ID"],
                "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
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

def get_redirect_uri():
    """Get the correct redirect URI based on the environment"""
    if 'HOSTNAME' in os.environ:
        return f"https://{os.environ['HOSTNAME']}/_oauth/callback"
    return "http://localhost:8501/_oauth/callback"

def verify_oauth2_token(token):
    """Verify the OAuth2 token and check domain/email restrictions"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            st.secrets["GOOGLE_CLIENT_ID"]
        )
        
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None, "Invalid token issuer"
            
        email = idinfo['email']
        domain = email.split('@')[1]
        
        # Check if email is specifically allowed
        if email in ALLOWED_EMAILS:
            return idinfo, None
            
        # Check domain
        if domain != ALLOWED_DOMAIN:
            return None, f"Access restricted to @{ALLOWED_DOMAIN} domain only"
            
        return None, "Your email is not authorized. Please contact your administrator."
            
    except ValueError as e:
        return None, f"Token verification failed: {str(e)}"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'auth_error' not in st.session_state:
    st.session_state.auth_error = None

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize OAuth flow
flow = init_oauth_flow()

def render_login_page():
    """Render the login page"""
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo and title
        st.image(COMPANY_LOGO, width=150, use_column_width=True)
        st.markdown(f'<p class="ketos-title">{APP_TITLE}</p>', unsafe_allow_html=True)
        
        # Handle OAuth callback
        if 'code' in st.experimental_get_query_params():
            code = st.experimental_get_query_params()['code'][0]
            try:
                flow.fetch_token(code=code)
                token_info, error_message = verify_oauth2_token(flow.credentials.id_token)
                
                if token_info:
                    st.session_state.authenticated = True
                    st.session_state.user_email = token_info['email']
                    st.rerun()
                else:
                    st.error(error_message)
                    st.session_state.auth_error = error_message
            except Exception as e:
                st.error("Authentication failed. Please try again or contact support.")
                st.session_state.auth_error = str(e)
        
        # Sign-in button
        if not st.session_state.auth_error or "Authentication failed" in st.session_state.auth_error:
            st.markdown("""
                <div style='text-align: center; margin-bottom: 1rem;'>
                    <p>Please sign in with your KETOS email account.</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Sign in with Google", key="google_signin"):
                auth_url = flow.authorization_url(
                    access_type='offline',
                    include_granted_scopes='true',
                    prompt='consent'
                )[0]
                st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
        
        st.markdown("""
            <div style='text-align: center; margin-top: 2rem; color: #666;'>
                <small>Access restricted to KETOS employees only.<br>
                For access requests, please contact IT support.</small>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_app_dashboard():
    """Render the main application dashboard"""
    # Header with user info and logout
    st.markdown("""
        <div class="user-info">
            <span>👤 Logged in as: <strong>{}</strong></span>
        </div>
    """.format(st.session_state.user_email), unsafe_allow_html=True)
    
    if st.button("🚪 Logout", key="logout"):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.auth_error = None
        st.rerun()
    
    st.title(APP_TITLE)
    st.markdown("---")
    
    # Display apps in grid
    cols = st.columns(len(APPS))
    for col, (app_name, app_info) in zip(cols, APPS.items()):
        with col:
            st.markdown(f"""
                <div class="app-card">
                    <h3>{app_name}</h3>
                    <p>{app_info['description']}</p>
                </div>
            """, unsafe_allow_html=True)
            st.link_button(
                f"Launch {app_name}",
                app_info['url'],
                use_container_width=True
            )

# Main app logic
if not st.session_state.authenticated:
    render_login_page()
else:
    render_app_dashboard()

import streamlit as st
import hashlib
from datetime import datetime, timedelta

# Configuration
APP_TITLE = "KETOS Internal Apps"
APP_ICON = "🌊"
COMPANY_LOGO = "https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png"

# User credentials - In production, use a secure database or secret management system
# Format: "email": {"password": "hashed_password", "name": "User Name"}
AUTHORIZED_USERS = {
    "ermias@ketos.co": {
        "password": "18221822",  
        "name": "User One"
    },
    "user2@ketos.co": {
        "password": "18221822",
        "name": "User Two"
    },
    "user3@ketos.co": {
        "password": "18221822",
        "name": "User Three"
    }
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

# Custom CSS
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    
    .form-container {
        margin-top: 1rem;
    }
    
    .centered-text {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(email, password):
    """Verify user credentials"""
    if email not in AUTHORIZED_USERS:
        return False
    
    hashed_password = hash_password(password)
    return AUTHORIZED_USERS[email]["password"] == hashed_password

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'lockout_until' not in st.session_state:
    st.session_state.lockout_until = None

def render_login_form():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo and title
        st.image(COMPANY_LOGO, width=150, use_column_width=True)
        st.markdown(f'<p class="ketos-title">{APP_TITLE}</p>', unsafe_allow_html=True)
        
        # Check if account is locked
        if st.session_state.lockout_until and datetime.now() < st.session_state.lockout_until:
            remaining_time = (st.session_state.lockout_until - datetime.now()).seconds
            st.error(f"Account locked. Please try again in {remaining_time} seconds.")
            return

        # Login form
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@ketos.co")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Sign In"):
                if verify_credentials(email, password):
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.login_attempts = 0
                    st.session_state.lockout_until = None
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 3:
                        st.session_state.lockout_until = datetime.now() + timedelta(minutes=5)
                        st.error("Too many failed attempts. Account locked for 5 minutes.")
                    else:
                        st.error("Invalid email or password")

        st.markdown("""
            <div style='text-align: center; margin-top: 2rem; color: #666;'>
                <small>Access restricted to KETOS employees only.<br>
                For access requests, please contact IT support.</small>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    # Header with user info and logout
    st.markdown(f"""
        <div class="user-info">
            <span>👤 Logged in as: <strong>{st.session_state.user_email}</strong></span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Logout", key="logout"):
        st.session_state.authenticated = False
        st.session_state.user_email = None
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
    render_login_form()
else:
    render_dashboard()

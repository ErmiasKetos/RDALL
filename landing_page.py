import streamlit as st
from datetime import datetime, timedelta

# Configuration
APP_TITLE = "KETOS Internal Portal"
APP_ICON = "🌊"
COMPANY_LOGO = "https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png"

# User credentials with simple password
AUTHORIZED_USERS = {
    "user1@ketos.co": {"name": "User One"},
    "user2@ketos.co": {"name": "User Two"},
    "user3@ketos.co": {"name": "User Three"}
}

MASTER_PASSWORD = "18221822"

# App and Tool Links
INTERNAL_APPS = {
    "WBCal": {
        "url": "https://caldash-eoewkytd6u7jyxfm2haaxn.streamlit.app",
        "description": "Probe calibration and management system",
        "icon": "🔧",
        "color": "#2E86C1"
    },
    "KCF LIMS": {
        "url": "https://4ekgis64qetw42fdkrynsn.streamlit.app",
        "description": "Laboratory Information Management System",
        "icon": "🧪",
        "color": "#27AE60"
    },
    "PO Request": {
        "url": "https://ntsmv7uynenkazkeftozjx.streamlit.app",
        "description": "Purchase Order Request System",
        "icon": "📝",
        "color": "#8E44AD"
    }
}

TOOLS = {
    "ClickUp": {
        "url": "https://app.clickup.com",
        "description": "Project and task management platform",
        "icon": "✅",
        "color": "#7B68EE"
    },
    "Slack": {
        "url": "https://ketos.slack.com",
        "description": "Team communication platform",
        "icon": "💬",
        "color": "#E91E63"
    },
    "Google Drive": {
        "url": "https://drive.google.com",
        "description": "Document storage and collaboration",
        "icon": "📁",
        "color": "#FF9800"
    }
}

# Custom CSS with more vibrant design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button {
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
        width: 100%;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
    }
    
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .ketos-title {
        background: linear-gradient(90deg, #2E86C1, #3498DB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .welcome-message {
        font-size: 18px;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    .app-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        background: white;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid #e0e0e0;
    }
    
    .app-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .user-info {
        padding: 1rem;
        background: linear-gradient(145deg, #f8f9fa, #ffffff);
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        color: #2C3E50;
        padding-left: 0.5rem;
        border-left: 4px solid #2E86C1;
    }
    
    .card-icon {
        font-size: 24px;
        margin-bottom: 0.5rem;
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2C3E50;
    }
    
    .quick-tip {
        background: #E8F6FF;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 4px solid #3498DB;
    }
    
    .help-text {
        color: #666;
        font-size: 14px;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'lockout_until' not in st.session_state:
    st.session_state.lockout_until = None

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

def verify_credentials(email, password):
    return email in AUTHORIZED_USERS and password == MASTER_PASSWORD

def render_login_form():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo and title
        st.image(COMPANY_LOGO, width=150, use_column_width=True)
        st.markdown(f'<p class="ketos-title">{APP_TITLE}</p>', unsafe_allow_html=True)
        
        # Welcome message
        st.markdown("""
            <p class="welcome-message">
                Welcome to the KETOS Internal Portal! 🌊<br>
                Your gateway to all KETOS tools and resources.
            </p>
        """, unsafe_allow_html=True)
        
        if st.session_state.lockout_until and datetime.now() < st.session_state.lockout_until:
            remaining_time = (st.session_state.lockout_until - datetime.now()).seconds
            st.error(f"⚠️ Account locked. Please try again in {remaining_time} seconds.")
            return

        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="your.email@ketos.co")
            password = st.text_input("🔑 Password", type="password")
            
            st.markdown('<div class="help-text">Need help? Contact IT Support</div>', unsafe_allow_html=True)
            
            if st.form_submit_button("Sign In", use_container_width=True):
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
                        st.error("🔒 Too many failed attempts. Account locked for 5 minutes.")
                    else:
                        st.error("❌ Invalid email or password")

def render_dashboard():
    # Header with user info and logout
    st.markdown(f"""
        <div class="user-info">
            <span>👋 Welcome back, <strong>{st.session_state.user_email}</strong>!</span>
        </div>
    """, unsafe_allow_html=True)
    
    col_logout, = st.columns([1])
    with col_logout:
        if st.button("🚪 Logout", key="logout", type="primary"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.rerun()

    # Quick Tips Section
    st.markdown("""
        <div class="quick-tip">
            <h4>🌟 Quick Tip of the Day</h4>
            <p>Use the search function in ClickUp to quickly find your tasks and projects. 
            Press 'Ctrl + K' or 'Cmd + K' for quick navigation!</p>
        </div>
    """, unsafe_allow_html=True)

    # Internal Apps Section
    st.markdown('<h2 class="section-title">Internal Applications</h2>', unsafe_allow_html=True)
    cols_apps = st.columns(len(INTERNAL_APPS))
    for col, (app_name, app_info) in zip(cols_apps, INTERNAL_APPS.items()):
        with col:
            st.markdown(f"""
                <div class="app-card" style="border-top: 4px solid {app_info['color']}">
                    <div class="card-icon">{app_info['icon']}</div>
                    <div class="card-title">{app_name}</div>
                    <p>{app_info['description']}</p>
                </div>
            """, unsafe_allow_html=True)
            st.link_button(
                f"Launch {app_name}",
                app_info['url'],
                use_container_width=True,
            )

    # External Tools Section
    st.markdown('<h2 class="section-title">Quick Access Tools</h2>', unsafe_allow_html=True)
    cols_tools = st.columns(len(TOOLS))
    for col, (tool_name, tool_info) in zip(cols_tools, TOOLS.items()):
        with col:
            st.markdown(f"""
                <div class="app-card" style="border-top: 4px solid {tool_info['color']}">
                    <div class="card-icon">{tool_info['icon']}</div>
                    <div class="card-title">{tool_name}</div>
                    <p>{tool_info['description']}</p>
                </div>
            """, unsafe_allow_html=True)
            st.link_button(
                f"Open {tool_name}",
                tool_info['url'],
                use_container_width=True,
            )

    # Instructions and Help Section
    with st.expander("📚 Instructions & Help"):
        st.markdown("""
            ### Getting Started
            1. **Internal Apps**: Access KETOS-specific applications
                - WBCal: Manage probe calibrations
                - KCF LIMS: Laboratory data management
                - PO Request: Submit purchase orders
            
            2. **Quick Access Tools**:
                - ClickUp: Task and project management
                - Slack: Team communication
                - Google Drive: Document storage
            
            ### Need Help?
            - For technical issues: Contact IT Support
            - For app-specific questions: Reach out to the respective team leads
            - For access requests: Submit through IT support ticket
            
            ### Quick Tips
            - Bookmark this portal for easy access
            - Keep your password secure and don't share it
            - Log out when you're done for security
        """)

# Main app logic
if not st.session_state.authenticated:
    render_login_form()
else:
    render_dashboard()

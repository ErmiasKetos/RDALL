# landing_page.py

import streamlit as st
from datetime import datetime, timedelta
import random

# Must be the first Streamlit command
st.set_page_config(
    page_title="KETOS Internal Portal",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Basic Configuration
APP_TITLE = "KETOS Internal Portal"
APP_ICON = "🌊"
COMPANY_LOGO = "https://internal.ktplatformservices.com/assets/logo-alt.png"

# Authorized Users
AUTHORIZED_USERS = {
    "ermias@ketos.co": {"name": "Ermias"},
    "fiseha@ketos.co": {"name": "Fiseha"},
    "girma.seifu@ketos.co": {"name": "Girma"},
    "shengcun.ma@ketos.co": {"name": "Shengcun"}
}

MASTER_PASSWORD = "18221822"

# Internal Applications Configuration
INTERNAL_APPS = {
    "WBCal": {
        "url": "https://jbrbbrprox6eahhujtmwls.streamlit.app/",
        "description": "Probe calibration and management system",
        "icon": "🔧",
        "color": "#2E86C1"
    },
    "KCF LIMS": {
        "url": "https://cftrayopt-r6gdayozdmjhkjchvypgw9.streamlit.app/",
        "description": "KCTray Management",
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

# Custom SVG Icons
CLICKUP_ICON = """<svg viewBox="0 0 100 100" style="width: 1.5em; height: 1.5em;">
    <path d="M50 25 L75 40 L75 60 L50 75 L25 60 L25 40 Z" fill="url(#clickup-gradient)" />
    <defs>
        <linearGradient id="clickup-gradient" gradientTransform="rotate(90)">
            <stop offset="0%" stop-color="#FF6B8B"/>
            <stop offset="50%" stop-color="#FF8E3C"/>
            <stop offset="100%" stop-color="#40A9FF"/>
        </linearGradient>
    </defs>
</svg>"""

GDRIVE_ICON = """<svg viewBox="0 0 100 100" style="width: 1.5em; height: 1.5em;">
    <path d="M6.4 87.5l8.3-14.1h71l-8.3 14.1z" fill="#3777E3"/>
    <path d="M49.8 25.3l-20.2 34.9 20.2 34.9 20.2-34.9z" fill="#FFCF63"/>
    <path d="M6.4 87.5l20.2-34.9 20.2-34.9h-20.2l-20.2 34.9z" fill="#11A861"/>
    <path d="M93.6 87.5l-20.2-34.9-20.2-34.9h20.2l20.2 34.9z" fill="#E53F35"/>
</svg>"""

QUARTZY_ICON = """<svg viewBox="0 0 100 100" style="width: 1.5em; height: 1.5em;">
    <circle cx="50" cy="50" r="45" fill="#FF6B42"/>
    <path d="M35 30h30v25c0 15-15 15-15 15s-15 0-15-15V30z" fill="white"/>
    <circle cx="50" cy="45" r="5" fill="#FF6B42"/>
</svg>"""

SLACK_ICON = """<svg viewBox="0 0 100 100" style="width: 1.5em; height: 1.5em;">
    <rect x="20" y="50" width="15" height="15" rx="4" fill="#36C5F0"/>
    <rect x="50" y="50" width="15" height="15" rx="4" fill="#2EB67D"/>
    <rect x="35" y="35" width="15" height="15" rx="4" fill="#ECB22E"/>
    <rect x="35" y="65" width="15" height="15" rx="4" fill="#E01E5A"/>
</svg>"""

SDS_ICON = """<svg viewBox="0 0 100 100" style="width: 1.5em; height: 1.5em;">
    <rect x="20" y="10" width="60" height="80" rx="5" fill="#4CAF50"/>
    <rect x="30" y="20" width="40" height="10" rx="2" fill="white"/>
    <path d="M30 40h40v5h-40zM30 50h40v5h-40zM30 60h40v5h-40z" fill="white"/>
    <path d="M35 70h15v15h-15z" fill="white"/>
    <text x="38" y="82" font-size="12" fill="#4CAF50">SDS</text>
</svg>"""

# External Tools Configuration
TOOLS = {
    "ClickUp": {
        "url": "https://app.clickup.com",
        "description": "Project and task management platform",
        "icon": CLICKUP_ICON,
        "color": "#7B68EE"
    },
    "Slack": {
        "url": "https://ketos.slack.com",
        "description": "Team communication platform",
        "icon": SLACK_ICON,
        "color": "#E01E5A"
    },
    "Google Drive": {
        "url": "https://drive.google.com",
        "description": "Document storage and collaboration",
        "icon": GDRIVE_ICON,
        "color": "#0F9D58"
    },
    "SDS Search": {
        "url": "https://chemicalsafety.com/sds-search/",
        "description": "Safety Data Sheet search database",
        "icon": SDS_ICON,
        "color": "#4CAF50"
    },
    "Lab Inventory": {
        "url": "https://app.quartzy.com",
        "description": "Laboratory inventory management system",
        "icon": QUARTZY_ICON,
        "color": "#FF6B42"
    }
}

# Quick Tips Configuration
QUICK_TIPS = [
    {
        "icon": "⚡",
        "title": "ClickUp Shortcut",
        "tip": "Use 'Ctrl + K' or 'Cmd + K' in ClickUp to quickly find tasks and projects."
    },
    {
        "icon": "🔍", 
        "title": "SDS Search Tip",
        "tip": "Bookmark frequently accessed Safety Data Sheets for quick reference in future searches."
    },
    # Add all your other tips here...
]

# Continue from previous part...

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'lockout_until' not in st.session_state:
    st.session_state.lockout_until = None
if 'last_tip_date' not in st.session_state:
    st.session_state.last_tip_date = datetime.now().date()
if 'current_tip' not in st.session_state:
    st.session_state.current_tip = None
if 'last_login_timestamp' not in st.session_state:
    st.session_state.last_login_timestamp = None

# Modern CSS Styling
st.markdown("""
<style>
    /* Base styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf5 100%) !important;
    }
    
    /* Modern Card Styles */
    .modern-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Header Styles */
    .dashboard-header {
        background: linear-gradient(120deg, #0071ba, #00a6fb);
        color: white;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Profile Section */
    .profile-section {
        display: flex;
        align-items: center;
        gap: 15px;
        background: rgba(255, 255, 255, 0.1);
        padding: 12px 20px;
        border-radius: 12px;
    }
    
    .profile-avatar {
        width: 45px;
        height: 45px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #0071ba;
    }
    
    /* App Grid */
    .app-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        padding: 20px 0;
    }
    
    .app-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Tool Cards */
    .tool-card {
        display: flex;
        align-items: center;
        gap: 15px;
        background: white;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Quick Tip Section */
    .quick-tip {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    
    .tip-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    /* Button Styles */
    .modern-button {
        background: linear-gradient(135deg, #0071ba 0%, #00a6fb 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .modern-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 113, 186, 0.3);
    }
    
    /* Login Form */
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .app-grid {
            grid-template-columns: 1fr;
        }
        
        .dashboard-header {
            flex-direction: column;
            text-align: center;
        }
        
        .profile-section {
            margin-top: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def get_new_tip():
    """Get a new random tip."""
    if st.session_state.current_tip is None:
        return random.choice(QUICK_TIPS)
    available_tips = [tip for tip in QUICK_TIPS if tip != st.session_state.current_tip]
    return random.choice(available_tips)

def check_and_update_daily_tip():
    """Update tip if it's a new day."""
    today = datetime.now().date()
    if st.session_state.last_tip_date != today:
        st.session_state.current_tip = get_new_tip()
        st.session_state.last_tip_date = today

def verify_credentials(email, password):
    """Verify user credentials."""
    is_valid = email in AUTHORIZED_USERS and password == MASTER_PASSWORD
    if is_valid:
        st.session_state.current_tip = get_new_tip()
        st.session_state.last_login_timestamp = datetime.now()
    return is_valid

# Continue from previous part...

def render_login_form():
    """Render the modern login form."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <div class="login-container">
                <div style="text-align: center; margin-bottom: 30px;">
                    <img src="{logo}" style="width: 60px; margin-bottom: 15px;">
                    <h1 style="color: #0071ba; font-size: 24px; margin: 0;">
                        {title}
                    </h1>
                    <p style="color: #666; margin-top: 10px;">
                        Welcome to the KETOS Internal Portal! 🌊
                    </p>
                </div>
            """.format(logo=COMPANY_LOGO, title=APP_TITLE), unsafe_allow_html=True)

        # Handle lockout
        if st.session_state.lockout_until and datetime.now() < st.session_state.lockout_until:
            remaining_time = (st.session_state.lockout_until - datetime.now()).seconds
            st.error(f"⚠️ Account locked. Please try again in {remaining_time} seconds.")
            return

        # Login Form
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "📧 Email",
                placeholder="your.email@ketos.co",
                help="Enter your KETOS email address"
            )
            
            password = st.text_input(
                "🔑 Password",
                type="password",
                help="Enter your password"
            )

            st.markdown("""
                <div style="height: 20px;"></div>
            """, unsafe_allow_html=True)

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
        
        st.markdown("""
            <div style="text-align: center; margin-top: 20px; color: #666; font-size: 14px;">
                Need help? Contact IT Support
            </div>
            </div>
        """, unsafe_allow_html=True)

def render_dashboard():
    """Render the modern dashboard."""
    check_and_update_daily_tip()
    user_name = AUTHORIZED_USERS[st.session_state.user_email]["name"]

    # Header with User Profile
    st.markdown(f"""
        <div class="dashboard-header">
            <div style="flex: 1;">
                <h1 style="margin: 0; font-size: 24px;">KETOS Internal Portal</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">
                    Welcome to your workspace
                </p>
            </div>
            <div class="profile-section">
                <div class="profile-avatar">
                    {user_name[0].upper()}
                </div>
                <div>
                    <div style="font-weight: 500;">{user_name}</div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        {st.session_state.user_email}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Quick Tip Section
    current_tip = st.session_state.current_tip
    st.markdown(f"""
        <div class="quick-tip">
            <div class="tip-header">
                <span style="font-size: 24px;">{current_tip['icon']}</span>
                <h3 style="margin: 0; color: #0071ba;">Daily Tip</h3>
            </div>
            <div style="margin-top: 10px;">
                <h4 style="margin: 0 0 5px 0; color: #2c3e50;">
                    {current_tip['title']}
                </h4>
                <p style="margin: 0; color: #34495e;">
                    {current_tip['tip']}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main Content Area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Internal Apps Section
        st.markdown("""
            <h2 style="color: #2c3e50; margin-bottom: 20px;">
                Internal Applications
            </h2>
        """, unsafe_allow_html=True)

        for app_name, app_info in INTERNAL_APPS.items():
            st.markdown(f"""
                <a href="{app_info['url']}" target="_blank" style="text-decoration: none;">
                    <div class="app-card" style="border-left: 4px solid {app_info['color']}">
                        <div style="font-size: 24px; margin-bottom: 10px;">
                            {app_info['icon']}
                        </div>
                        <h3 style="margin: 0 0 10px 0; color: #2c3e50;">
                            {app_name}
                        </h3>
                        <p style="margin: 0; color: #666;">
                            {app_info['description']}
                        </p>
                    </div>
                </a>
            """, unsafe_allow_html=True)

    with col2:
        # Quick Tools Section
        st.markdown("""
            <h2 style="color: #2c3e50; margin-bottom: 20px;">
                Quick Tools
            </h2>
        """, unsafe_allow_html=True)

        for tool_name, tool_info in TOOLS.items():
            st.markdown(f"""
                <a href="{tool_info['url']}" target="_blank" style="text-decoration: none;">
                    <div class="tool-card">
                        <div style="color: {tool_info['color']};">
                            {tool_info['icon']}
                        </div>
                        <div>
                            <h4 style="margin: 0 0 5px 0; color: #2c3e50;">
                                {tool_name}
                            </h4>
                            <p style="margin: 0; font-size: 14px; color: #666;">
                                {tool_info['description']}
                            </p>
                        </div>
                    </div>
                </a>
            """, unsafe_allow_html=True)

    # Footer Section
    st.markdown("""
        <div style="margin-top: 40px; padding: 20px; background: white; 
                    border-radius: 12px; text-align: center;">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">
                Need Help?
            </h3>
            <div style="display: flex; justify-content: center; gap: 20px;">
                <a href="#" class="modern-button">
                    Contact Support
                </a>
                <a href="#" class="modern-button">
                    Documentation
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Logout Button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.rerun()

# Main App Logic
def main():
    if not st.session_state.authenticated:
        render_login_form()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()

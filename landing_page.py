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

# Configuration
APP_TITLE = "KETOS Internal Portal"
APP_ICON = "🌊"
COMPANY_LOGO = "https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png"

# Add QUICK_TIPS configuration here
QUICK_TIPS = [
    # Existing general tips
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
    {
        "icon": "📦",
        "title": "Lab Inventory Management",
        "tip": "Always update Quartzy immediately after using or receiving materials to maintain accurate inventory."
    },
    
    # New R&D specific tips
    {
        "icon": "📝",
        "title": "Data Recording",
        "tip": "Document all experimental parameters, including environmental conditions, equipment settings, and any deviations from protocols."
    },
    {
        "icon": "🔬",
        "title": "Lab Notebook Practice",
        "tip": "Record observations in real-time. Never rely on memory when it comes to experimental data."
    },
    {
        "icon": "📸",
        "title": "Visual Documentation",
        "tip": "Take photos of experimental setups and unusual observations. A picture is worth a thousand words in R&D."
    },
    {
        "icon": "🎯",
        "title": "Calibration Records",
        "tip": "Always verify and document calibration status of equipment before starting experiments."
    },
    {
        "icon": "⚖️",
        "title": "Raw Data Preservation",
        "tip": "Save all raw data files with clear naming conventions and dates. Never overwrite original data."
    },
    {
        "icon": "🔄",
        "title": "Version Control",
        "tip": "Maintain version control for analysis scripts and protocols. Document what changed and why."
    },
    {
        "icon": "❌",
        "title": "Error Documentation",
        "tip": "Document errors and failed experiments - they're valuable learning opportunities and part of the R&D process."
    },
    {
        "icon": "🔗",
        "title": "Data Traceability",
        "tip": "Ensure all data can be traced back to its source. Link raw data files to your experimental notes."
    },
    {
        "icon": "📊",
        "title": "Data Backup",
        "tip": "Back up your data in multiple locations. Follow the 3-2-1 rule: 3 copies, 2 different media types, 1 off-site."
    },
    {
        "icon": "📅",
        "title": "Timeline Documentation",
        "tip": "Record dates and times for all experimental steps, especially for time-sensitive procedures."
    },
    {
        "icon": "🧪",
        "title": "Method Documentation",
        "tip": "Document detailed methods including lot numbers, concentrations, and any deviations from SOPs."
    },
    {
        "icon": "🏷️",
        "title": "Sample Labeling",
        "tip": "Use clear, consistent labeling for all samples. Include date, experiment ID, and conditions."
    },
    {
        "icon": "📈",
        "title": "Data Analysis",
        "tip": "Document all data processing steps and statistical methods used in your analysis."
    },
    {
        "icon": "🤝",
        "title": "Collaboration",
        "tip": "When sharing data, include metadata and context so others can understand and reproduce your work."
    },
    {
        "icon": "🔐",
        "title": "Data Security",
        "tip": "Protect sensitive R&D data. Use appropriate access controls and never share credentials."
    },
    {
        "icon": "✔️",
        "title": "Quality Checks",
        "tip": "Implement regular quality checks of your documentation. Peer review can help catch missing information."
    }
]

# User credentials with simple password
AUTHORIZED_USERS = {
    "ermias@ketos.co": {"name": "Ermias"},
    "fiseha@ketos.co": {"name": "Fiseha"},
    "girma.seifu@ketos.co": {"name": "Girma"},
    "shengcun.ma@ketos.co": {"name": "Shengcun"}
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
    },
    "SDS Search": {
        "url": "https://chemicalsafety.com/sds-search/",
        "description": "Safety Data Sheet search database",
        "icon": "🔍",
        "color": "#4CAF50"
    },
    "Lab Inventory": {
        "url": "https://app.quartzy.com",
        "description": "Laboratory inventory management system",
        "icon": "📦",
        "color": "#009688"
    }
}

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

# Add tip management functions
def get_new_tip():
    """Get a new random tip, ensuring it's different from the current one"""
    if st.session_state.current_tip is None:
        return random.choice(QUICK_TIPS)
    
    # Get all tips except the current one
    available_tips = [tip for tip in QUICK_TIPS if tip != st.session_state.current_tip]
    return random.choice(available_tips)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* KETOS themed background - fixed version */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf5 100%) !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf5 100%) !important;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf5 100%) !important;
    }
    
    /* Make cards stand out more against the background */
    .app-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.9) !important;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid rgba(46, 134, 193, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .app-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(46, 134, 193, 0.1);
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Updated user info banner */
    .user-info {
        padding: 1rem;
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(46, 134, 193, 0.1);
        border: 1px solid rgba(46, 134, 193, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Quick tip section styling */
    .quick-tip {
        background: rgba(232, 246, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 4px solid #3498DB;
        backdrop-filter: blur(10px);
    }
    
    /* Section titles */
    .section-title {
        color: #2C3E50;
        font-size: 24px;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-left: 0.5rem;
        border-left: 4px solid #2E86C1;
        background: rgba(255, 255, 255, 0.7);
        padding: 0.5rem;
        border-radius: 4px;
    }
    
    /* Other styling remains the same */
    .stButton > button {
        background-color: #2E86C1;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
        width: 100%;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2874A6;
        transform: scale(1.02);
    }
    
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(46, 134, 193, 0.1);
        border: 1px solid rgba(46, 134, 193, 0.1);
        backdrop-filter: blur(10px);
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
    
    /* Style adjustments for better contrast */
    .card-title {
        color: #2E86C1;
        font-weight: 600;
    }
    
    .card-description {
        color: #2C3E50;
    }
    .clickable-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.9) !important;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid rgba(46, 134, 193, 0.1);
        backdrop-filter: blur(10px);
        cursor: pointer;
    }
    
    .clickable-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(46, 134, 193, 0.1);
        background: rgba(255, 255, 255, 0.95) !important;
    }

    /* Add link styling */
    .card-link {
        text-decoration: none;
        color: inherit;
    }
    
    .card-link:hover {
        text-decoration: none;
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

def verify_credentials(email, password):
    """Verify credentials and update tip if successful"""
    is_valid = email in AUTHORIZED_USERS and password == MASTER_PASSWORD
    if is_valid:
        # Update tip on successful login
        st.session_state.current_tip = get_new_tip()
        st.session_state.last_login_timestamp = datetime.now()
    return is_valid

def check_and_update_daily_tip():
    """Check if it's a new day and update tip if needed"""
    today = datetime.now().date()
    if st.session_state.last_tip_date != today:
        st.session_state.current_tip = get_new_tip()
        st.session_state.last_tip_date = today

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
    # First check if we need to update the daily tip
    check_and_update_daily_tip()
    
    user_name = AUTHORIZED_USERS[st.session_state.user_email]["name"]
    st.markdown(f"""
        <div class="user-info">
            <span>👋 Welcome back, <strong>{user_name}</strong>!</span>
        </div>
    """, unsafe_allow_html=True)
    
    col_logout, = st.columns([1])
    with col_logout:
        if st.button("🚪 Logout", key="logout", type="primary"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            # Don't reset the tip here, it will update on next login
            st.rerun()

    # Display the current tip
    current_tip = st.session_state.current_tip
    st.markdown(f"""
        <div class="quick-tip">
            <h4>{current_tip['icon']} Quick Tip: {current_tip['title']}</h4>
            <p>{current_tip['tip']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Internal Apps Section
    st.markdown('<h2 class="section-title">Internal Applications</h2>', unsafe_allow_html=True)
    cols_apps = st.columns(len(INTERNAL_APPS))
    for col, (app_name, app_info) in zip(cols_apps, INTERNAL_APPS.items()):
        with col:
            st.markdown(f"""
                <a href="{app_info['url']}" target="_blank" class="card-link">
                    <div class="clickable-card" style="border-top: 4px solid {app_info['color']}">
                        <div class="card-icon">{app_info['icon']}</div>
                        <div class="card-title">{app_name}</div>
                        <p>{app_info['description']}</p>
                    </div>
                </a>
            """, unsafe_allow_html=True)

    # External Tools Section
    st.markdown('<h2 class="section-title">Quick Access Tools</h2>', unsafe_allow_html=True)
    
    # Calculate number of columns needed (3 cards per row)
    num_tools = len(TOOLS)
    num_rows = (num_tools + 2) // 3  # Round up division
    
    # Create tools grid
    for row in range(num_rows):
        cols = st.columns(3)
        for col_idx in range(3):
            tool_idx = row * 3 + col_idx
            if tool_idx < num_tools:
                tool_name = list(TOOLS.keys())[tool_idx]
                tool_info = TOOLS[tool_name]
                with cols[col_idx]:
                    st.markdown(f"""
                        <a href="{tool_info['url']}" target="_blank" class="card-link">
                            <div class="clickable-card" style="border-top: 4px solid {tool_info['color']}">
                                <div class="card-icon">{tool_info['icon']}</div>
                                <div class="card-title">{tool_name}</div>
                                <p>{tool_info['description']}</p>
                            </div>
                        </a>
                    """, unsafe_allow_html=True)

    # Instructions and Help Section
    with st.expander("📚 Instructions & Help"):
        st.markdown("""
            ### Getting Started
            1. **Internal Apps**: Access KETOS-specific applications
                - WBCal: Manage probe calibrations
                - KCF LIMS: KCTray Management
                - PO Request: Submit purchase orders
            
            2. **Quick Access Tools**:
                - ClickUp: Task and project management
                - Slack: Team communication
                - Google Drive: Document storage
                - SDS Search: Safety Data Sheet database
                - Lab Inventory: R&D Lab Chemical inventory management
            
            ### Need Help?
            - For technical issues: Contact R&D Support
            - For app-specific questions: Reach out to the respective team leads
            - For access requests: Submit through R&D Ops support ticket
            
            ### Quick Tips
            - Click directly on any card to open the respective application
            - Keep your password secure and don't share it
            - Log out when you're done for security
        """)

# Main app logic
if not st.session_state.authenticated:
    render_login_form()
else:
    render_dashboard()

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
COMPANY_LOGO = "https://internal.ktplatformservices.com/assets/logo-alt.png"

# Add QUICK_TIPS configuration here
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
    {
        "icon": "📦",
        "title": "Lab Inventory Management",
        "tip": "Always update Quartzy immediately after using or receiving materials to maintain accurate inventory."
    },

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

# Custom SVG icons as strings
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

# New custom SDS icon
SDS_ICON = """<svg viewBox="0 0 100 100" style="width: 1.5em; height: 1.5em;">
    <rect x="20" y="10" width="60" height="80" rx="5" fill="#4CAF50"/>
    <rect x="30" y="20" width="40" height="10" rx="2" fill="white"/>
    <path d="M30 40h40v5h-40zM30 50h40v5h-40zM30 60h40v5h-40z" fill="white"/>
    <path d="M35 70h15v15h-15z" fill="white"/>
    <text x="38" y="82" font-size="12" fill="#4CAF50">SDS</text>
</svg>"""

# Updated TOOLS dictionary
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
    /* Base styles and fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Force background color */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf5 100%) !important;
    }
    
    /* Override Streamlit's default background */
    .main {
        background-color: transparent !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: transparent !important;
    }
    
    /* Login form styling */
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 1);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(46, 134, 193, 0.1);
        border: 1px solid rgba(46, 134, 193, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Page title styling */
    .ketos-title {
        background: linear-gradient(90deg, #2E86C1, #3498DB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Welcome message */
    .welcome-message {
        font-size: 18px;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2E86C1 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        border: none !important;
        font-weight: 500 !important;
        width: 100% !important;
        transition: transform 0.2s, background-color 0.2s !important;
    }
    
    .stButton > button:hover {
        background-color: #2874A6 !important;
        transform: scale(1.02) !important;
    }
    
    /* User info banner */
    .user-info {
        padding: 1rem;
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(46, 134, 193, 0.1);
        border: 1px solid rgba(46, 134, 193, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Quick tip section */
    .quick-tip {
        background: rgba(232, 246, 255, 0.95) !important;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #3498DB;
        backdrop-filter: blur(10px);
    }
    
    .quick-tip h4 {
        color: #2E86C1;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    /* Section titles */
    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        color: #2C3E50;
        padding: 0.5rem 0.5rem 0.5rem 1rem;
        border-left: 4px solid #2E86C1;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 4px;
    }
    
    /* Large cards for internal apps */
    .internal-app-card {
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        background: rgba(255, 255, 255, 0.95) !important;
        transition: transform 0.3s, box-shadow 0.3s;
        border: 1px solid rgba(46, 134, 193, 0.1);
        backdrop-filter: blur(10px);
        cursor: pointer;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .internal-app-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 24px rgba(46, 134, 193, 0.15);
    }
    
    .internal-app-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .internal-app-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #2C3E50;
    }
    
    /* Smaller cards for external tools */
    .external-tool-card {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.9) !important;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid rgba(46, 134, 193, 0.1);
        cursor: pointer;
        height: 140px;
    }
    
    .external-tool-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(46, 134, 193, 0.1);
    }
    
    .external-tool-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .external-tool-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
        color: #2C3E50;
    }
    
    /* Card links */
    .card-link {
        text-decoration: none !important;
        color: inherit !important;
    }
    
    .card-link:hover {
        text-decoration: none !important;
        color: inherit !important;
    }
    
    /* Help text */
    .help-text {
        color: #666;
        font-size: 14px;
        margin-top: 0.5rem;
        text-align: center;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 8px !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        color: #666;
        font-size: 0.875rem;
    }
    
    /* Error messages */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px);
    }
    /* Icon container styling */
    .tool-icon {
        display: flex;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    /* SVG icon styling */
    .tool-icon svg {
        margin-right: 0.5rem;
        transition: transform 0.2s;
    }
    
    .external-tool-card:hover .tool-icon svg {
        transform: scale(1.1);
    }
    
    /* Card title alignment with icon */
    .external-tool-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2C3E50;
        display: flex;
        align-items: center;
    }
    
    /* Description text sizing */
    .external-tool-card p {
        font-size: 0.9rem;
        line-height: 1.4;
        color: #666;
    }
    
    /* Adjust card height for consistent sizing */
    .external-tool-card {
        height: auto;
        min-height: 120px;
        display: flex;
        flex-direction: column;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Previous existing CSS remains the same */

    /* New styles for app cards */
    .stMarkdown div > a.app-card {
        display: block;
        margin-bottom: 1rem;
    }

    .app-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
    }

    .app-card {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 1rem;
        text-decoration: none;
        transition: transform 0.3s, box-shadow 0.3s;
        border: 1px solid rgba(46, 134, 193, 0.1);
    }

    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(46, 134, 193, 0.1);
    }

    .app-icon {
        font-size: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        border-radius: 12px;
        margin-right: 1rem;
    }

    .app-info {
        flex-grow: 1;
    }

    .app-info h3 {
        margin: 0 0 0.5rem 0;
        color: #2C3E50;
        font-size: 1.2rem;
    }

    .app-info p {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
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
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="{COMPANY_LOGO}" width="60">
                <p class="ketos-title">{APP_TITLE}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
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
            
            st.markdown('<div class="help-text">Need help? Contact R&D Support</div>', unsafe_allow_html=True)
            
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
    """Render the modern dashboard layout."""
    # First check if we need to update the daily tip
    check_and_update_daily_tip()
    
    user_name = AUTHORIZED_USERS[st.session_state.user_email]["name"]
    
    # Header with user info and logout
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
            st.rerun()

    # Display the current tip
    current_tip = st.session_state.current_tip
    st.markdown(f"""
        <div class="quick-tip">
            <h4>{current_tip['icon']} Quick Tip: {current_tip['title']}</h4>
            <p>{current_tip['tip']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Add enhanced dashboard header and styling
    st.markdown(f"""
        <div class="dashboard-header">
            <div class="profile-section">
                <div class="profile-avatar">
                    {user_name[0].upper()}
                </div>
                <div class="profile-info">
                    <h3>Welcome back, {user_name}!</h3>
                    <p>Have a great day at work 🌟</p>
                </div>
            </div>
        </div>

        <div class="quick-actions-bar">
            <div class="action-buttons">
                <button onclick="window.open('https://app.clickup.com', '_blank')" class="action-button">
                    <i class="fas fa-tasks"></i> Tasks
                </button>
                <button onclick="window.open('https://ketos.slack.com', '_blank')" class="action-button">
                    <i class="fas fa-comment"></i> Chat
                </button>
                <button onclick="window.open('https://drive.google.com', '_blank')" class="action-button">
                    <i class="fas fa-folder"></i> Drive
                </button>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Internal Apps Section
        st.markdown('<h2 class="section-title">Internal Applications</h2>', unsafe_allow_html=True)

        # Create a container to hold the app cards
        app_cards_html = """
        <div class="app-grid">
        """

        for app_name, app_info in INTERNAL_APPS.items():
            app_cards_html += f"""
            <a href="{app_info['url']}" target="_blank" class="app-card">
                <div class="app-icon" style="background: {app_info['color']}20">
                    {app_info['icon']}
                </div>
                <div class="app-info">
                    <h3>{app_name}</h3>
                    <p>{app_info['description']}</p>
                </div>
            </a>
            """

        app_cards_html += "</div>"

        # Render the app cards
        st.markdown(app_cards_html, unsafe_allow_html=True)

    with col2:
        # Quick Tools Section
        st.markdown('<h2 class="section-title">Quick Tools</h2>', unsafe_allow_html=True)
        
        for tool_name, tool_info in TOOLS.items():
            st.markdown(f"""
                <a href="{tool_info['url']}" target="_blank" class="tool-card">
                    <div class="tool-icon" style="color: {tool_info['color']}">
                        {tool_info['icon']}
                    </div>
                    <div class="tool-info">
                        <h4>{tool_name}</h4>
                        <p>{tool_info['description']}</p>
                    </div>
                </a>
            """, unsafe_allow_html=True)

    # Dashboard Footer with Support Section
    st.markdown("""
        <div class="dashboard-footer">
            <div class="support-section">
                <h4>Need Help?</h4>
                <div class="support-links">
                    <a href="#" class="support-link">
                        <i class="fas fa-question-circle"></i>
                        Support Center
                    </a>
                    <a href="#" class="support-link">
                        <i class="fas fa-book"></i>
                        Documentation
                    </a>
                    <a href="#" class="support-link">
                        <i class="fas fa-hands-helping"></i>
                        IT Support
                    </a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

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
                - SDS Search: Safety Data Sheet database
                - Lab Inventory: Quartzy inventory management
            
            ### Need Help?
            - For technical issues: Contact IT Support
            - For app-specific questions: Reach out to the respective team leads
            - For access requests: Submit through IT support ticket
            
            ### Quick Tips
            - Click directly on any card to open the respective application
            - Keep your password secure and don't share it
            - Log out when you're done for security
        """)

    # Add the enhanced CSS for dashboard elements
    st.markdown("""
    <style>
        /* Modern Dashboard Styles */
        .dashboard-header {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        }

        .profile-section {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .profile-avatar {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #0071ba 0%, #00a6fb 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }

        .quick-actions-bar {
            background: #ffffff;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .action-buttons {
            display: flex;
            gap: 1rem;
            overflow-x: auto;
            padding: 0.5rem;
        }

        .action-button {
            background: #f8f9fa;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            color: #2c3e50;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .action-button:hover {
            background: #e9ecef;
            transform: translateY(-2px);
        }

        /* App Cards and Grid Styles */
        .app-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }

        .app-card {
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 1rem;
            text-decoration: none;
            transition: transform 0.3s, box-shadow 0.3s;
            border: 1px solid rgba(46, 134, 193, 0.1);
        }

        .app-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(46, 134, 193, 0.1);
        }

        .app-icon {
            font-size: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
            border-radius: 12px;
            margin-right: 1rem;
        }

        .app-info {
            flex-grow: 1;
        }

        .app-info h3 {
            margin: 0 0 0.5rem 0;
            color: #2C3E50;
            font-size: 1.2rem;
        }

        .app-info p {
            margin: 0;
            color: #666;
            font-size: 0.9rem;
        }

        /* Dashboard Footer Styles */
        .dashboard-footer {
            background: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            margin-top: 3rem;
        }

        .support-section h4 {
            margin-bottom: 1rem;
            color: #2c3e50;
        }

        .support-links {
            display: flex;
            gap: 2rem;
            margin-top: 1rem;
        }

        .support-link {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
            color: #2c3e50;
            transition: all 0.2s;
        }

        .support-link:hover {
            color: #0071ba;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .app-grid {
                grid-template-columns: 1fr;
            }
            
            .support-links {
                flex-direction: column;
                gap: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    

# Main app logic
if not st.session_state.authenticated:
    render_login_form()
else:
    render_dashboard()

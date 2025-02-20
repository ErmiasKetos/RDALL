

import streamlit as st
from datetime import datetime, timedelta
import random

# Authentication check 
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_authentication(email, password):
    """Verify user email is authorized and password is correct."""
    return (email in st.secrets.auth.allowed_emails and 
            password == st.secrets.auth.password)

# Authentication UI 
if not st.session_state.authenticated:
    st.markdown("""
        <style>
            .login-container {
                max-width: 400px;
                margin: 50px auto;
                padding: 30px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            .stButton > button {
                background: #0071ba;
                color: white;
                width: 100%;
            }
        </style>
        
        <div class="login-container">
            <h2 style='text-align: center; color: #0071ba; margin-bottom: 20px;'>
                🧪 KETOS R&D Hub
            </h2>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login", use_container_width=True):
            if check_authentication(email, password):
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Invalid email or password. Access restricted to authorized users only.")
    st.stop()

# Must be the first Streamlit command
st.set_page_config(
    page_title="KETOS R&D Hub",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Basic Configuration
APP_TITLE = "KETOS R&D Hub"
APP_ICON = "🧪"
COMPANY_LOGO = "https://internal.ktplatformservices.com/assets/logo-alt.png"

# Internal Applications Configuration
INTERNAL_APPS = {
    "WBCal": {
        "url": "https://jbrbbrprox6eahhujtmwls.streamlit.app/",
        "description": "Probe calibration and management system",
        "icon": "🔧",
        "color": "#2E86C1"
    },
    "KELAB": {
        "url": "https://ejwzx8kdgasjxeef2wsjjw.streamlit.app/",
        "description": "KELAB Scalability & Profitability Modeling",
        "icon": "📊",
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

# Quick Links Configuration
QUICK_LINKS = {
    "ClickUp": {
        "url": "https://app.clickup.com",
        "description": "Task and project management",
        "icon": "📋",
        "color": "#7B68EE"
    },
    "Lab Inventory": {
        "url": "https://app.quartzy.com",
        "description": "Quartzy inventory management",
        "icon": "📦",
        "color": "#FF6B42"
    },
    "SDS Search": {
        "url": "https://chemicalsafety.com/sds-search/",
        "description": "Safety Data Sheet database",
        "icon": "🔍",
        "color": "#4CAF50"
    },
    "Slack": {
        "url": "https://ketos.slack.com",
        "description": "Team communication",
        "icon": "💬",
        "color": "#E01E5A"
    },
    "Google Drive": {
        "url": "https://drive.google.com",
        "description": "Document storage",
        "icon": "📁",
        "color": "#0F9D58"
    }
}

# Lab Tips
LAB_TIPS = [
    {
        "icon": "⚗️",
        "title": "Lab Protocol Tip",
        "tip": "Always record any deviations from standard protocols in your lab notebook."
    },
    {
        "icon": "🧪",
        "title": "Sample Management",
        "tip": "Label all samples with date, ID, and conditions immediately after collection."
    },
    {
        "icon": "📊",
        "title": "Data Recording",
        "tip": "Take photos of experimental setups for better documentation and reproducibility."
    },
    {
        "icon": "🔍",
        "title": "Quality Control",
        "tip": "Regularly check and calibrate instruments before starting experiments."
    }
]

def get_random_tip():
    """Get a random lab tip."""
    return random.choice(LAB_TIPS)

# Apply Modern Styling
st.markdown("""
<style>
    /* Modern Theme */
    :root {
        --primary: #0071ba;
        --secondary: #27ae60;
        --background: #f8f9fa;
        --text: #2c3e50;
    }

    .stApp {
        background: linear-gradient(135deg, var(--background), #e4ecf5) !important;
    }

    /* Header Styling */
    .hub-header {
        background: linear-gradient(120deg, var(--primary), var(--secondary));
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* Card Styling */
    .app-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
        border: 1px solid rgba(0,0,0,0.1);
    }

    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }

    /* Quick Links */
    .quick-link {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        transition: transform 0.2s ease;
    }

    .quick-link:hover {
        transform: translateX(5px);
    }

    /* Tip Box */
    .tip-box {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .hub-header {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def render_header():
    """Render the hub header."""
    st.markdown(f"""
        <div class="hub-header">
            <h1 style="margin-bottom: 0.5rem;">{APP_ICON} {APP_TITLE}</h1>
            <p style="opacity: 0.9;">Your centralized platform for R&D tools and resources</p>
        </div>
    """, unsafe_allow_html=True)

def render_lab_tip():
    """Render the lab tip section."""
    tip = get_random_tip()
    st.markdown(f"""
        <div class="tip-box">
            <h3 style="margin: 0; color: #0071ba;">
                {tip['icon']} Lab Tip of the Day
            </h3>
            <h4 style="margin: 0.5rem 0; color: #2c3e50;">
                {tip['title']}
            </h4>
            <p style="margin: 0; color: #34495e;">
                {tip['tip']}
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_apps_section():
    """Render the internal applications section."""
    st.markdown("### 🔬 R&D Applications")
    
    cols = st.columns(len(INTERNAL_APPS))
    for col, (app_name, app_info) in zip(cols, INTERNAL_APPS.items()):
        with col:
            st.markdown(f"""
                <a href="{app_info['url']}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="app-card" style="border-left: 4px solid {app_info['color']}">
                        <div style="font-size: 2rem;">{app_info['icon']}</div>
                        <h3 style="margin: 1rem 0;">{app_name}</h3>
                        <p style="color: #666;">{app_info['description']}</p>
                    </div>
                </a>
            """, unsafe_allow_html=True)

def render_quick_links():
    """Render the quick links section."""
    st.markdown("### 🔗 Quick Links")
    
    for tool_name, tool_info in QUICK_LINKS.items():
        st.markdown(f"""
            <a href="{tool_info['url']}" target="_blank" style="text-decoration: none; color: inherit;">
                <div class="quick-link">
                    <div style="font-size: 1.5rem; color: {tool_info['color']};">
                        {tool_info['icon']}
                    </div>
                    <div>
                        <h4 style="margin: 0;">{tool_name}</h4>
                        <p style="margin: 0; color: #666; font-size: 0.9rem;">
                            {tool_info['description']}
                        </p>
                    </div>
                </div>
            </a>
        """, unsafe_allow_html=True)

def main():
    """Main function to render the R&D Hub."""
    render_header()
    render_lab_tip()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_apps_section()
    
    with col2:
        render_quick_links()
    
    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 1rem;">
            <p style="color: #666;">Need help? Contact the R&D Support Team</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

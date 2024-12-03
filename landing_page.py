import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Page configuration
st.set_page_config(page_title="Chemistry Lab Suite", page_icon="⚗️", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    .main {
        background-color: #f0f8ff;
    }
    
    h1, h2, h3 {
        color: #1e3d59;
    }
    
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        color: #ffffff;
        background-color: #1e3d59;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2b506e;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .app-description {
        margin-top: 10px;
        font-size: 16px;
        color: #555;
    }
    
    .stSubheader {
        font-size: 24px;
        color: #1e3d59;
        margin-top: 2rem;
    }
    
    .hero-section {
        background-color: #e8f4fd;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="hero-section">', unsafe_allow_html=True)
st.title("Chemistry Lab Suite")
st.write("Empowering chemists with cutting-edge digital tools for precision and efficiency.")

# Lottie Animation
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_q7wkifyr.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, height=200, key="lottie")

st.markdown('</div>', unsafe_allow_html=True)

# App buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("Launch SpectraAnalyzer", "https://caldash-eoewkytd6u7jyxfm2haaxn.streamlit.app", use_container_width=True)
    st.markdown('<p class="app-description">Advanced spectroscopic data analysis and visualization tool</p>', unsafe_allow_html=True)

with col2:
    st.link_button("Launch ChemLIMS", "https://4ekgis64qetw42fdkrynsn.streamlit.app", use_container_width=True)
    st.markdown('<p class="app-description">Comprehensive Laboratory Information Management System for chemistry labs</p>', unsafe_allow_html=True)

with col3:
    st.link_button("Launch ReagentInventory", "https://ntsmv7uynenkazkeftozjx.streamlit.app", use_container_width=True)
    st.markdown('<p class="app-description">Efficient chemical reagent and inventory management system</p>', unsafe_allow_html=True)

# Additional information section
st.subheader("Our Chemistry Lab Applications")

with st.expander("SpectraAnalyzer - Spectroscopic Data Analysis"):
    st.markdown("""
    <div class="info-box">
    SpectraAnalyzer is our state-of-the-art spectroscopic data analysis tool. It offers:
    
    - Advanced peak detection and analysis
    - Multi-spectrum overlay and comparison
    - Customizable data processing workflows
    - Integration with major spectrometer brands
    - Exportable reports and publication-ready graphics
    </div>
    """, unsafe_allow_html=True)

with st.expander("ChemLIMS - Laboratory Information Management"):
    st.markdown("""
    <div class="info-box">
    ChemLIMS streamlines your chemistry laboratory operations with features like:
    
    - Sample tracking from reception to disposal
    - Experiment workflow management
    - Quality control and assurance protocols
    - Instrument calibration and maintenance logs
    - Regulatory compliance documentation
    - Data security and audit trails
    </div>
    """, unsafe_allow_html=True)

with st.expander("ReagentInventory - Chemical Management"):
    st.markdown("""
    <div class="info-box">
    Optimize your chemical inventory with ReagentInventory:
    
    - Real-time tracking of chemical stocks
    - Automated reorder notifications
    - Safety Data Sheet (SDS) management
    - Barcode integration for easy check-in/check-out
    - Usage analytics and cost tracking
    - Compatibility checks and storage optimization
    </div>
    """, unsafe_allow_html=True)

# User guide
st.subheader("Getting Started")
st.info("""
1. Click on the application button you wish to launch.
2. Each app will open in a new browser tab for seamless multitasking.
3. Use this landing page as your central hub for accessing all chemistry lab tools.
4. For optimal performance, ensure your browser is up-to-date.
""")

# Footer
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("© 2023 ChemTech Solutions. All rights reserved.")
with col2:
    st.markdown("For support, contact: support@chemtechsolutions.com")


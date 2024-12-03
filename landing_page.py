import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os

# Debug mode
DEBUG = True

# Google OAuth credentials
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

# Define redirect URI
REDIRECT_URI = "https://2kdjdf2ktdyukylfaxdtbf.streamlit.app/_oauth/callback"
if DEBUG:
    st.write("Using redirect URI:", REDIRECT_URI)

# Configure OAuth flow
flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI],
        }
    },
    scopes=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ],
    redirect_uri=REDIRECT_URI
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'auth_error' not in st.session_state:
    st.session_state.auth_error = None

# Page config
st.set_page_config(
    page_title="KETOS Apps Login",
    page_icon="🌊",
    layout="wide"
)

# Main authentication flow
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.image("https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png", width=150)
        st.title("KETOS Apps Login")
        
        if DEBUG:
            st.write("Current Query Parameters:", st.experimental_get_query_params())
        
        if 'code' in st.experimental_get_query_params():
            code = st.experimental_get_query_params()['code'][0]
            try:
                if DEBUG:
                    st.write("Attempting to fetch token with code:", code)
                
                flow.fetch_token(code=code)
                if DEBUG:
                    st.write("Token fetch successful")
                
                credentials = flow.credentials
                idinfo = id_token.verify_oauth2_token(
                    credentials.id_token,
                    requests.Request(),
                    GOOGLE_CLIENT_ID
                )
                
                if DEBUG:
                    st.write("Token verification successful")
                    st.write("Email:", idinfo.get('email'))
                
                # Check email domain
                email = idinfo['email']
                if email.endswith('@ketos.co'):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Please use your KETOS email address to login.")
                
            except Exception as e:
                if DEBUG:
                    st.error(f"Authentication error: {str(e)}")
                st.session_state.auth_error = str(e)
        
        if st.button("Sign in with Google"):
            auth_url = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )[0]
            
            if DEBUG:
                st.write("Generated Auth URL:", auth_url)
            
            st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)

else:
    st.success("Authentication successful!")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.auth_error = None
        st.rerun()

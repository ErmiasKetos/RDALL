import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os

# Enable debug mode
DEBUG = True

# Google OAuth credentials
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

# Get the actual redirect URI
def get_redirect_uri():
    if DEBUG:
        st.write("Current hostname:", os.environ.get('HOSTNAME', 'localhost:8501'))
    return f"https://2kdjdf2ktdyukylfaxdtbf.streamlit.app/_oauth/callback"

# Configure OAuth flow
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

# Page config
st.set_page_config(page_title="KETOS Apps Login", page_icon="🌊")

# Debug information
if DEBUG:
    st.write("Current Query Parameters:", st.experimental_get_query_params())
    st.write("Redirect URI:", get_redirect_uri())

# Main authentication flow
if not st.session_state.authenticated:
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
            
            st.session_state.authenticated = True
            st.rerun()
        except Exception as e:
            if DEBUG:
                st.error(f"Authentication error: {str(e)}")
    
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
        st.rerun()

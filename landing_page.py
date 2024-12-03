import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os

# Debug mode
DEBUG = True

# OAuth Configuration
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
BASE_URL = "https://2kdjdf2ktdyukylfaxdtbf.streamlit.app"
REDIRECT_URI = f"{BASE_URL}/_oauth/callback"

# Page config
st.set_page_config(
    page_title="KETOS Apps Login",
    page_icon="🌊",
    layout="wide"
)


# Initialize OAuth flow
flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI]
        }
    },
    scopes=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
)
flow.redirect_uri = REDIRECT_URI
    
    if DEBUG:
        st.write("Flow initialized successfully")
except Exception as e:
    if DEBUG:
        st.error(f"Flow initialization error: {str(e)}")

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'auth_error' not in st.session_state:
    st.session_state.auth_error = None

# Main app
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.image("https://www.ketos.co/wp-content/uploads/2022/03/ketos-logo-1.png", width=150)
        st.title("KETOS Apps Login")
        
        # Debug current state
        if DEBUG:
            st.write("Query Parameters:", st.experimental_get_query_params())
        
        # Handle OAuth callback
        if 'code' in st.experimental_get_query_params():
            code = st.experimental_get_query_params()['code'][0]
            try:
                if DEBUG:
                    st.write("Processing OAuth callback with code")
                
                flow.fetch_token(code=code)
                credentials = flow.credentials
                
                idinfo = id_token.verify_oauth2_token(
                    credentials.id_token,
                    requests.Request(),
                    GOOGLE_CLIENT_ID
                )
                
                if DEBUG:
                    st.write("Token Info:", {k: v for k, v in idinfo.items() if k != 'email'})
                
                email = idinfo.get('email', '')
                if email.endswith('@ketos.co'):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Please use your KETOS email address to login.")
                    
            except Exception as e:
                if DEBUG:
                    st.error(f"Authentication error: {str(e)}")
                st.session_state.auth_error = str(e)
        
        # Sign in button
        if st.button("Sign in with Google"):
            try:
                auth_url = flow.authorization_url(
                    access_type='offline',
                    include_granted_scopes='true',
                    prompt='consent'
                )[0]
                
                if DEBUG:
                    st.write("Generated Auth URL:", auth_url)
                
                st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
            except Exception as e:
                if DEBUG:
                    st.error(f"Error generating auth URL: {str(e)}")

else:
    st.success("Successfully authenticated!")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.auth_error = None
        st.rerun()

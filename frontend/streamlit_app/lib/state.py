import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'token' not in st.session_state:
        st.session_state.token = None

def login_user(user_data, token):
    """Login user and store in session"""
    st.session_state.authenticated = True
    st.session_state.user = user_data
    st.session_state.token = token

def logout_user():
    """Logout user and clear session"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get current user data"""
    return st.session_state.get('user', None)

def get_token():
    """Get current auth token"""
    return st.session_state.get('token', None)
import streamlit as st
from lib.state import is_authenticated, get_current_user, logout_user

st.set_page_config(page_title="Dashboard", page_icon="📊")

# Check authentication
if not is_authenticated():
    st.error("Please login first")
    st.stop()

user = get_current_user()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 Equipment Dashboard")
with col2:
    if st.button("Logout", type="secondary"):
        logout_user()
        st.rerun()

st.markdown("---")

# Dashboard content
user_name = user.get('name', user.get('email', 'User'))
st.success(f"Hello {user_name}! This is the dashboard page.")

st.info("🚧 Dashboard features will be implemented here")

# User info in sidebar
with st.sidebar:
    st.markdown("### 👤 User Profile")
    if 'picture' in user and user['picture']:
        st.image(user['picture'], width=60)
    st.write(f"**Name:** {user_name}")
    st.write(f"**Email:** {user.get('email', 'N/A')}")
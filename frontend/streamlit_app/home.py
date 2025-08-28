import streamlit as st
from lib.api import api_client
from lib.state import initialize_session_state, login_user, logout_user, is_authenticated, get_current_user

st.set_page_config(
    page_title="Smart Rental Tracker",
    page_icon="🏗️",
    layout="wide"
)

# Initialize session state
initialize_session_state()

def show_login_page():
    """Show login page with demo authentication"""
    st.title("🏗️ Smart Rental Tracker")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>Welcome to Smart Rental Tracker</h2>
            <p>Equipment Rental Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo dealer login
        if st.button("🏢 Sign in as Dealer", type="primary", use_container_width=True):
            demo_user = {
                'uid': 'dealer_123',
                'email': 'dealer@smartrental.com',
                'name': 'ABC Equipment Rental',
                'picture': ''
            }
            demo_token = 'demo_jwt_dealer_token'
            login_user(demo_user, demo_token)
            st.rerun()
        
        st.markdown("---")
        
        # Firebase test section
        with st.expander("🔧 System Status"):
            if st.button("Test Backend Connection"):
                firebase_config = api_client.get_firebase_config()
                if firebase_config:
                    st.success("✅ Backend connection successful!")
                    st.json(firebase_config)
                else:
                    st.error("❌ Backend connection failed")
            
            st.info("""
            **System Status**:
            - ✅ Backend API endpoints
            - ✅ JWT token system  
            - ✅ Session management
            - ✅ Equipment tracking ready
            - 🚧 Google OAuth (coming soon)
            """)

def show_dashboard():
    """Show main dashboard"""
    user = get_current_user()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🏗️ Smart Rental Tracker Dashboard")
    with col2:
        if st.button("Logout", type="secondary"):
            logout_user()
            st.rerun()
    
    st.markdown("---")
    
    # User info
    user_name = user.get('name', user.get('email', 'User'))
    st.success(f"Welcome back, {user_name}! 👋")
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Equipment", "156", "12 new")
    with col2:
        st.metric("Currently Rented", "89", "-3")
    with col3:
        st.metric("Available", "67", "5 returned")
    with col4:
        st.metric("Maintenance", "8", "2 new")
    
    st.markdown("---")
    
    # Feature showcase
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "⚡ Quick Actions", "📈 Analytics"])
    
    with tab1:
        st.subheader("Equipment Overview")
        
        # Sample data visualization
        import pandas as pd
        import plotly.express as px
        
        # Create sample equipment data
        equipment_data = {
            'Equipment Type': ['Excavator', 'Crane', 'Bulldozer', 'Grader', 'Loader'],
            'Total': [45, 32, 28, 18, 33],
            'Rented': [23, 18, 15, 12, 21],
            'Available': [22, 14, 13, 6, 12]
        }
        
        df = pd.DataFrame(equipment_data)
        
        # Create bar chart
        fig = px.bar(df, x='Equipment Type', y=['Total', 'Rented', 'Available'],
                    title="Equipment Status by Type")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.button("➕ Add Equipment", use_container_width=True)
            st.button("📋 Check Out", use_container_width=True)
        
        with col2:
            st.button("📥 Check In", use_container_width=True)
            st.button("🔧 Schedule Maintenance", use_container_width=True)
        
        with col3:
            st.button("📊 Generate Report", use_container_width=True)
            st.button("🔍 Track Equipment", use_container_width=True)
    
    with tab3:
        st.subheader("Usage Analytics")
        
        # Sample usage chart
        usage_data = {
            'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'Usage Hours': [120, 135, 110, 145, 160, 155, 140, 165, 170, 155,
                          180, 175, 160, 185, 190, 175, 195, 200, 185, 210,
                          205, 190, 215, 220, 205, 225, 230, 215, 235, 240]
        }
        
        usage_df = pd.DataFrame(usage_data)
        
        fig_usage = px.line(usage_df, x='Date', y='Usage Hours',
                          title="Daily Equipment Usage (Hours)")
        st.plotly_chart(fig_usage, use_container_width=True)
    
    # User profile in sidebar
    with st.sidebar:
        st.markdown("### 👤 Dealer Profile")
        if 'picture' in user and user['picture']:
            st.image(user['picture'], width=60)
        else:
            st.write("🏢")
        st.write(f"**Company:** {user_name}")
        st.write(f"**Email:** {user.get('email', 'N/A')}")
        st.write(f"**Dealer ID:** {user.get('uid', 'N/A')}")
        
        st.markdown("---")
        st.markdown("### 🚀 Your Fleet")
        st.metric("Total Equipment", "47", "5 this week")
        st.metric("Active Rentals", "23", "-2 today")
        st.metric("Monthly Revenue", "$45,230", "+12%")

# Main app logic
if is_authenticated():
    show_dashboard()
else:
    show_login_page()
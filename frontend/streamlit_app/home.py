# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# from lib.api import api_client
# from lib.state import initialize_session_state, login_user, logout_user, is_authenticated, get_current_user
# from lib.data import get_sample_equipment_data, get_usage_analytics_data, get_overdue_equipment
# from lib.components import render_metric_card, render_equipment_card, render_alert_card
# from lib.styles import apply_custom_css

# st.set_page_config(
#     page_title="Smart Rental Tracker",
#     page_icon="🏗️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Apply custom CSS
# apply_custom_css()

# # Initialize session state
# initialize_session_state()

# def show_login_page():
#     """Enhanced login page with better styling"""
    
#     # Hero section
#     st.markdown("""
#     <div class="hero-section">
#         <div class="hero-content">
#             <h1>🏗️ Smart Rental Tracker</h1>
#             <p class="hero-subtitle">Intelligent Equipment Rental Management System</p>
#             <p class="hero-description">Track, monitor, and optimize your equipment rental operations with real-time insights and predictive analytics.</p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Features grid
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown("""
#         <div class="feature-card">
#             <div class="feature-icon">📍</div>
#             <h3>Real-time Tracking</h3>
#             <p>Monitor equipment location and status in real-time with GPS tracking and QR code scanning.</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div class="feature-card">
#             <div class="feature-icon">📊</div>
#             <h3>Usage Analytics</h3>
#             <p>Get insights into equipment utilization, downtime, and performance metrics.</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#         <div class="feature-card">
#             <div class="feature-icon">🔮</div>
#             <h3>Demand Forecasting</h3>
#             <p>Predict equipment demand and optimize your fleet allocation with AI-powered insights.</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Login section
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         st.markdown("""
#         <div class="login-section">
#             <h2>Get Started</h2>
#             <p>Sign in to access your equipment dashboard</p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Demo login buttons
#         if st.button("🏢 Sign in as Equipment Dealer", type="primary", use_container_width=True):
#             demo_user = {
#                 'uid': 'dealer_123',
#                 'email': 'dealer@smartrental.com',
#                 'name': 'ABC Equipment Rental Co.',
#                 'picture': '',
#                 'role': 'dealer'
#             }
#             demo_token = 'demo_jwt_dealer_token'
#             login_user(demo_user, demo_token)
#             st.rerun()
        
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         # System status
#         with st.expander("🔧 System Status & Testing"):
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 if st.button("Test Backend Connection", use_container_width=True):
#                     with st.spinner("Connecting..."):
#                         firebase_config = api_client.get_firebase_config()
#                         if firebase_config:
#                             st.success("✅ Backend connected!")
#                         else:
#                             st.error("❌ Connection failed")
            
#             with col2:
#                 if st.button("Check API Health", use_container_width=True):
#                     st.success("✅ All systems operational")
            
#             st.markdown("""
#             **Current Status:**
#             - ✅ FastAPI Backend Running
#             - ✅ JWT Authentication System
#             - ✅ Firebase Integration Ready
#             - ✅ Real-time Data Processing
#             - ✅ Equipment Tracking Module
#             - 🚧 Mobile App (Coming Soon)
#             """)

# def show_dashboard():
#     """Enhanced main dashboard with modular components"""
#     user = get_current_user()
#     user_name = user.get('name', user.get('email', 'User'))
    
#     # Header with user info
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.markdown(f"""
#         <div class="dashboard-header">
#             <h1>🏗️ Smart Rental Dashboard</h1>
#             <p>Welcome back, <strong>{user_name}</strong> 👋</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         if st.button("🚪 Logout", type="secondary", use_container_width=True):
#             logout_user()
#             st.rerun()
    
#     st.markdown("---")
    
#     # Key Metrics Row
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         render_metric_card("Total Equipment", "156", "+12 this month", "🏗️", "#1f77b4")
    
#     with col2:
#         render_metric_card("Currently Rented", "89", "-3 today", "📋", "#ff7f0e")
    
#     with col3:
#         render_metric_card("Available", "67", "+5 returned", "✅", "#2ca02c")
    
#     with col4:
#         render_metric_card("Under Maintenance", "8", "+2 scheduled", "🔧", "#d62728")
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Alerts and Notifications
#     render_alert_section()
    
#     # Main content tabs
#     tab1, tab2, tab3, tab4 = st.tabs(["📊 Fleet Overview", "📈 Analytics", "⚡ Quick Actions", "🔔 Alerts"])
    
#     with tab1:
#         show_fleet_overview()
    
#     with tab2:
#         show_analytics()
    
#     with tab3:
#         show_quick_actions()
    
#     with tab4:
#         show_alerts_tab()
    
#     # Sidebar content
#     render_sidebar(user)

# def render_alert_section():
#     """Render critical alerts section"""
#     overdue_equipment = get_overdue_equipment()
    
#     if overdue_equipment:
#         st.markdown("### 🚨 Critical Alerts")
        
#         alert_col1, alert_col2 = st.columns(2)
        
#         with alert_col1:
#             render_alert_card(
#                 "Overdue Returns", 
#                 f"{len(overdue_equipment)} equipment items",
#                 "High Priority",
#                 "🚨"
#             )
        
#         with alert_col2:
#             render_alert_card(
#                 "Maintenance Due", 
#                 "3 equipment items",
#                 "Medium Priority", 
#                 "🔧"
#             )
        
#         st.markdown("<br>", unsafe_allow_html=True)

# def show_fleet_overview():
#     """Fleet overview tab content"""
#     st.markdown("### Equipment Fleet Overview")
    
#     equipment_data = get_sample_equipment_data()
    
#     # Equipment summary by type
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         # Equipment status chart
#         status_summary = equipment_data.groupby(['Type', 'Status']).size().unstack(fill_value=0)
        
#         fig = px.bar(
#             status_summary, 
#             title="Equipment Status by Type",
#             color_discrete_map={
#                 'Available': '#2ca02c',
#                 'Rented': '#ff7f0e', 
#                 'Maintenance': '#d62728',
#                 'Reserved': '#9467bd'
#             }
#         )
#         fig.update_layout(
#             showlegend=True,
#             legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
#         )
#         st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         st.markdown("#### Fleet Utilization")
        
#         # Utilization metrics
#         total_equipment = len(equipment_data)
#         rented_equipment = len(equipment_data[equipment_data['Status'] == 'Rented'])
#         utilization_rate = (rented_equipment / total_equipment) * 100
        
#         st.metric("Utilization Rate", f"{utilization_rate:.1f}%", "2.3%")
#         st.metric("Average Revenue/Day", "$2,850", "$150")
#         st.metric("Fleet Efficiency", "87.5%", "1.2%")
    
#     # Equipment table
#     st.markdown("#### Recent Equipment Activity")
#     display_columns = ['Equipment ID', 'Type', 'Status', 'Location', 'Last Update']
#     recent_activity = equipment_data[display_columns].head(10)
#     st.dataframe(recent_activity, use_container_width=True, hide_index=True)

# def show_analytics():
#     """Analytics tab content"""
#     st.markdown("### Usage Analytics & Insights")
    
#     # Time period selector
#     col1, col2 = st.columns([1, 3])
#     with col1:
#         time_period = st.selectbox("Time Period", ["Last 7 days", "Last 30 days", "Last 3 months", "Last year"])
    
#     # Usage analytics
#     usage_data = get_usage_analytics_data()
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Daily usage hours
#         fig_usage = px.line(
#             usage_data, 
#             x='Date', 
#             y='Usage Hours',
#             title="Daily Equipment Usage Trends"
#         )
#         fig_usage.update_traces(line_color='#1f77b4', line_width=3)
#         fig_usage.update_layout(showlegend=False)
#         st.plotly_chart(fig_usage, use_container_width=True)
    
#     with col2:
#         # Revenue trend
#         fig_revenue = px.area(
#             usage_data,
#             x='Date',
#             y='Revenue',
#             title="Daily Revenue Trends"
#         )
#         fig_revenue.update_traces(fill='tonexty', fillcolor='rgba(31, 119, 180, 0.2)')
#         st.plotly_chart(fig_revenue, use_container_width=True)
    
#     # Equipment performance metrics
#     st.markdown("#### Equipment Performance Metrics")
    
#     equipment_data = get_sample_equipment_data()
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         # Most utilized equipment
#         utilization_data = equipment_data.nlargest(5, 'Total Hours')
#         fig_util = px.bar(
#             utilization_data,
#             x='Equipment ID',
#             y='Total Hours',
#             title="Top 5 Most Utilized Equipment"
#         )
#         st.plotly_chart(fig_util, use_container_width=True)
    
#     with col2:
#         # Equipment by location
#         location_summary = equipment_data.groupby('Location').size().reset_index(name='Count')
#         fig_location = px.pie(
#             location_summary,
#             values='Count',
#             names='Location',
#             title="Equipment Distribution by Location"
#         )
#         st.plotly_chart(fig_location, use_container_width=True)
    
#     with col3:
#         # Idle time analysis
#         idle_data = equipment_data[equipment_data['Idle Hours'] > 0].nlargest(5, 'Idle Hours')
#         fig_idle = px.bar(
#             idle_data,
#             x='Equipment ID',
#             y='Idle Hours',
#             title="Equipment with High Idle Time",
#             color_discrete_sequence=['#d62728']
#         )
#         st.plotly_chart(fig_idle, use_container_width=True)

# def show_quick_actions():
#     """Quick actions tab content"""
#     st.markdown("### Quick Actions")
    
#     # Action categories
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown("#### 📋 Equipment Operations")
#         if st.button("➕ Add New Equipment", use_container_width=True):
#             st.success("Redirecting to Add Equipment page...")
        
#         if st.button("📥 Check In Equipment", use_container_width=True):
#             st.success("Redirecting to Check In page...")
        
#         if st.button("📤 Check Out Equipment", use_container_width=True):
#             st.success("Redirecting to Check Out page...")
        
#         if st.button("🔍 Track Equipment", use_container_width=True):
#             st.success("Opening equipment tracker...")
    
#     with col2:
#         st.markdown("#### 🔧 Maintenance & Service")
#         if st.button("🔧 Schedule Maintenance", use_container_width=True):
#             st.success("Opening maintenance scheduler...")
        
#         if st.button("📋 Maintenance History", use_container_width=True):
#             st.success("Viewing maintenance records...")
        
#         if st.button("⚠️ Report Issue", use_container_width=True):
#             st.success("Opening issue reporter...")
        
#         if st.button("🛠️ Service Requests", use_container_width=True):
#             st.success("Viewing service requests...")
    
#     with col3:
#         st.markdown("#### 📊 Reports & Analytics")
#         if st.button("📈 Generate Report", use_container_width=True):
#             st.success("Opening report generator...")
        
#         if st.button("📊 Usage Analytics", use_container_width=True):
#             st.success("Redirecting to Analytics page...")
        
#         if st.button("💰 Revenue Report", use_container_width=True):
#             st.success("Generating revenue report...")
        
#         if st.button("📋 Export Data", use_container_width=True):
#             st.success("Preparing data export...")
    
#     st.markdown("---")
    
#     # Quick stats and shortcuts
#     st.markdown("#### 🚀 Today's Quick Stats")
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.metric("Today's Check-outs", "12", "+3")
#     with col2:
#         st.metric("Today's Check-ins", "8", "-2")
#     with col3:
#         st.metric("Pending Returns", "23", "+5")
#     with col4:
#         st.metric("Today's Revenue", "$4,250", "+15%")

# def show_alerts_tab():
#     """Alerts and notifications tab"""
#     st.markdown("### 🔔 Alerts & Notifications")
    
#     # Alert categories
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("#### 🚨 High Priority Alerts")
        
#         alerts = [
#             {"type": "Overdue", "equipment": "EX1001 - Excavator", "days": "3 days overdue"},
#             {"type": "Maintenance", "equipment": "CR2002 - Crane", "days": "Due today"},
#             {"type": "Location", "equipment": "BD3003 - Bulldozer", "days": "Location unknown"}
#         ]
        
#         for alert in alerts:
#             st.error(f"**{alert['type']}:** {alert['equipment']} - {alert['days']}")
    
#     with col2:
#         st.markdown("#### 💡 Medium Priority Notifications")
        
#         notifications = [
#             {"type": "Return", "equipment": "LD4004 - Loader", "info": "Scheduled return tomorrow"},
#             {"type": "Booking", "equipment": "GR5005 - Grader", "info": "New booking request"},
#             {"type": "Update", "equipment": "System", "info": "Location data synced"}
#         ]
        
#         for notif in notifications:
#             st.info(f"**{notif['type']}:** {notif['equipment']} - {notif['info']}")
    
#     # Demand forecasting alerts
#     st.markdown("#### 🔮 Demand Forecasting Insights")
    
#     st.warning("**Peak Demand Alert:** High demand expected for Excavators next week (March 15-22). Consider reallocating equipment from Site B to Site A.")
#     st.info("**Optimization Suggestion:** Bulldozer BD3003 has been idle for 5+ days. Consider offering promotional rates or relocating to Site C.")
#     st.success("**Efficiency Update:** Fleet utilization increased by 12% this month. Great job!")

# def render_sidebar(user):
#     """Enhanced sidebar content"""
#     with st.sidebar:
#         # User profile
#         st.markdown("### 👤 Dealer Profile")
        
#         user_name = user.get('name', 'User')
#         if 'picture' in user and user['picture']:
#             st.image(user['picture'], width=80)
#         else:
#             st.markdown("🏢")
        
#         st.markdown(f"**Company:** {user_name}")
#         st.markdown(f"**Email:** {user.get('email', 'N/A')}")
#         st.markdown(f"**Dealer ID:** {user.get('uid', 'N/A')}")
        
#         st.markdown("---")
        
#         # Fleet summary
#         st.markdown("### 🚀 Your Fleet Summary")
#         st.metric("Total Fleet Size", "156 units")
#         st.metric("Active Rentals", "89 units")
#         st.metric("Monthly Revenue", "$127,850")
#         st.metric("Utilization Rate", "87.5%")
        
#         st.markdown("---")
        
#         # Quick navigation
#         st.markdown("### 🧭 Quick Navigation")
        
#         if st.button("📊 Dashboard", use_container_width=True):
#             st.switch_page("home.py")
        
#         if st.button("🏗️ Equipment", use_container_width=True):
#             st.switch_page("pages/Equipment.py")
        
#         if st.button("📈 Analytics", use_container_width=True):
#             st.switch_page("pages/Usage.py")
        
#         if st.button("🔮 Forecasting", use_container_width=True):
#             st.switch_page("pages/Forecasting.py")
        
#         st.markdown("---")
        
#         # System info
#         st.markdown("### ℹ️ System Info")
#         st.caption("Version: 1.0.0")
#         st.caption("Last Updated: Aug 28, 2025")
#         st.caption("Status: ✅ Online")

# # Main app logic
# if __name__ == "__main__":
#     if is_authenticated():
#         show_dashboard()
#     else:
#         show_login_page()



import streamlit as st
from lib.api import api_client
from lib.state import initialize_session_state, login_user, logout_user, is_authenticated, get_current_user, get_token
from lib.components import render_metric_card, render_alert_card
from lib.styles import apply_custom_css

st.set_page_config(page_title="Smart Rental Tracker", page_icon="🏗️", layout="wide", initial_sidebar_state="expanded")
apply_custom_css()
initialize_session_state()

def fetch_equipment():
    token = get_token()
    data = api_client.get_equipment_list(token)
    return data if isinstance(data, list) else []

def show_login_page():
    st.markdown("""
    <div class="hero-section">
      <div class="hero-content">
        <h1>🏗️ Smart Rental Tracker</h1>
        <p class="hero-subtitle">Intelligent Equipment Rental Management System</p>
        <p class="hero-description">Track, monitor, and optimize your equipment rental operations with real-time insights.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Sign in (demo)")
    if st.button("Continue (Demo)", type="primary", use_container_width=True):
        # In dev we don't need a real JWT. If your backend needs JWT, replace this with real login.
        demo_user = {'uid': 'demo_user', 'email': 'demo@example.com', 'name': 'Demo Dealer', 'picture': '', 'role': 'dealer'}
        demo_token = None  # set a real JWT if SEND_AUTH=True
        login_user(demo_user, demo_token)
        st.rerun()

    with st.expander("🔧 Backend status"):
        ok = api_client.health_check()
        st.write("API healthy ✅" if ok else "API not reachable ❌")

def show_dashboard():
    user = get_current_user()
    token = get_token()
    equipment = fetch_equipment()

    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown(f"""
        <div class="dashboard-header">
            <h1>🏗️ Smart Rental Dashboard</h1>
            <p>Welcome back, <strong>{user.get('name', user.get('email','User'))}</strong> 👋</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout_user(); st.rerun()
    st.markdown("---")

    # ---- Metrics computed from backend list ----
    total = len(equipment)
    by_status = {"available":0,"in_use":0,"maintenance":0,"out_of_service":0}
    for e in equipment:
        by_status[str(e.get("status","")).lower()] = by_status.get(str(e.get("status","")).lower(),0)+1

    col1,col2,col3,col4 = st.columns(4)
    with col1: render_metric_card("Total Equipment", f"{total}", "+ realtime", "🏗️", "#1f77b4")
    with col2: render_metric_card("Available", f"{by_status.get('available',0)}", "", "✅", "#2ca02c")
    with col3: render_metric_card("In Use", f"{by_status.get('in_use',0)}", "", "📋", "#ff7f0e")
    with col4: render_metric_card("Maintenance", f"{by_status.get('maintenance',0)}", "", "🔧", "#d62728")

    st.markdown("### Recent Equipment")
    if equipment:
        # show a small table
        cols = ["id","name","type","status","current_location","rental_rate_per_day","hours_used","updated_at"]
        rows = [{c: item.get(c) for c in cols} for item in equipment[:15]]
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No equipment yet. Import CSV or add via API.")

    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Dealer Profile")
        st.write(f"**Name:** {user.get('name','User')}")
        st.write(f"**Email:** {user.get('email','N/A')}")
        st.write(f"**Dealer ID:** {user.get('uid','N/A')}")
        st.markdown("---")
        st.markdown("### Quick Links")
        st.page_link("pages/Equipment.py", label="🏗️ Equipment", icon="🏗️")
        st.page_link("pages/Forecasting.py", label="🔮 Forecasting", icon="🔮")
        st.page_link("pages/Usage.py", label="📊 Usage", icon="📊")
        st.page_link("pages/Sharing.py", label="🤝 Sharing", icon="🤝")

if __name__ == "__main__":
    if is_authenticated():
        show_dashboard()
    else:
        show_login_page()

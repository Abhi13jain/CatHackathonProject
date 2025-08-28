# # # import streamlit as st
# # # import pandas as pd
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # from datetime import datetime, timedelta
# # # import numpy as np
# # # import random
# # # from lib.state import is_authenticated, get_current_user, logout_user, get_auth_token
# # # from lib.api import api_client
# # # from lib.components import render_metric_card, render_alert_card
# # # from lib.styles import apply_custom_css, get_status_color

# # # st.set_page_config(
# # #     page_title="Machine Sharing",
# # #     page_icon="🤝",
# # #     layout="wide"
# # # )

# # # # Apply custom CSS
# # # apply_custom_css()

# # # # Check authentication
# # # if not is_authenticated():
# # #     st.error("🔒 Please login first")
# # #     st.stop()

# # # def get_real_sharing_data():
# # #     """Get real sharing data from Firebase via API"""
# # #     try:
# # #         token = get_auth_token()
# # #         if not token:
# # #             return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
# # #         # Get sharing requests
# # #         sharing_requests = api_client.get_sharing_requests(token)
# # #         if sharing_requests:
# # #             requests_df = pd.DataFrame(sharing_requests)
# # #         else:
# # #             requests_df = pd.DataFrame()
        
# # #         # Get equipment list for users
# # #         equipment_list = api_client.get_equipment_list(token)
# # #         if equipment_list:
# # #             equipment_df = pd.DataFrame(equipment_list)
# # #         else:
# # #             equipment_df = pd.DataFrame()
        
# # #         # For now, create minimal sharing history (this would come from Firebase in production)
# # #         sharing_history = pd.DataFrame([
# # #             {
# # #                 "sharing_id": "SH001",
# # #                 "equipment_type": "Excavator",
# # #                 "users": ["Construction Co A", "BuildMax Solutions"],
# # #                 "location": "Downtown Area",
# # #                 "duration": "4 days",
# # #                 "cost_saved": "$1,200",
# # #                 "completion_date": "2024-08-25",
# # #                 "rating": 4.5
# # #             }
# # #         ])
        
# # #         return equipment_df, requests_df, sharing_history
        
# # #     except Exception as e:
# # #         st.error(f"Error fetching data: {e}")
# # #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# # # def render_sharing_dashboard(sharing_requests, sharing_history):
# # #     """Render sharing dashboard overview with real data"""
    
# # #     st.markdown("### 🤝 Machine Sharing Overview")
    
# # #     # Key metrics
# # #     col1, col2, col3, col4 = st.columns(4)
    
# # #     with col1:
# # #         if not sharing_requests.empty:
# # #             active_requests = len(sharing_requests[sharing_requests['status'] == 'active'])
# # #             render_metric_card("Active Requests", str(active_requests), "+2 today", "📋", "#1f77b4")
# # #         else:
# # #             render_metric_card("Active Requests", "0", "No requests", "📋", "#1f77b4")
    
# # #     with col2:
# # #         if not sharing_requests.empty:
# # #             matched_requests = len(sharing_requests[sharing_requests['status'] == 'matched'])
# # #             render_metric_card("Matched Today", str(matched_requests), "+1 match", "🎯", "#2ca02c")
# # #         else:
# # #             render_metric_card("Matched Today", "0", "No matches", "🎯", "#2ca02c")
    
# # #     with col3:
# # #         if not sharing_history.empty:
# # #             total_savings = sum([int(h['cost_saved'].replace('$', '').replace(',', '')) for h in sharing_history.to_dict('records')])
# # #             render_metric_card("Total Savings", f"${total_savings:,}", "+$3,900", "💰", "#ff7f0e")
# # #         else:
# # #             render_metric_card("Total Savings", "$0", "No savings yet", "💰", "#ff7f0e")
    
# # #     with col4:
# # #         if not sharing_history.empty:
# # #             avg_rating = sharing_history['rating'].mean()
# # #             render_metric_card("Avg Rating", f"{avg_rating:.1f}★", "+0.2", "⭐", "#9467bd")
# # #         else:
# # #             render_metric_card("Avg Rating", "0.0★", "No ratings", "⭐", "#9467bd")
    
# # #     st.markdown("<br>", unsafe_allow_html=True)
    
# # #     # Active requests alert
# # #     if not sharing_requests.empty:
# # #         expiring_soon = sharing_requests[
# # #             (sharing_requests['status'] == 'active') & 
# # #             (pd.to_datetime(sharing_requests['expires_at']) < datetime.now() + timedelta(hours=6))
# # #         ]
        
# # #         if not expiring_soon.empty:
# # #             st.warning(f"⚠️ **Urgent**: {len(expiring_soon)} sharing requests expire within 6 hours!")

# # # def render_new_sharing_request():
# # #     """Render form to create new sharing request with Firebase integration"""
    
# # #     st.markdown("### ➕ Create New Sharing Request")
    
# # #     with st.form("sharing_request_form"):
# # #         col1, col2 = st.columns(2)
        
# # #         with col1:
# # #             user_name = st.text_input("Your Company Name", placeholder="ABC Construction Co.")
# # #             location = st.selectbox("Your Location", [
# # #                 "Downtown - Block 1", "Downtown - Block 2", "Downtown - Block 3",
# # #                 "Industrial Area - Zone A", "Industrial Area - Zone B", 
# # #                 "Airport Road - Sector 1", "Airport Road - Sector 2",
# # #                 "Highway Extension", "Tech Park Area"
# # #             ])
# # #             equipment_type = st.selectbox("Equipment Type", [
# # #                 "excavator", "crane", "bulldozer", "grader", "loader", "compactor", "forklift", "concrete_mixer"
# # #             ])
# # #             duration = st.selectbox("Rental Duration (days)", [1, 2, 3, 4, 5, 7, 14])
        
# # #         with col2:
# # #             start_date = st.date_input("Start Date", min_value=datetime.now().date())
# # #             max_distance = st.slider("Maximum Distance (km)", 1, 10, 5)
# # #             cost_split = st.selectbox("Preferred Cost Split", [
# # #                 "50-50", "60-40", "70-30", "Negotiable"
# # #             ])
# # #             contact_info = st.text_input("Contact Information", placeholder="phone/email")
        
# # #         project_name = st.text_input("Project Name", placeholder="Foundation Construction Project")
# # #         description = st.text_area("Project Description", 
# # #                                   placeholder="Describe your project and why you're looking for a sharing partner...")
        
# # #         submit_button = st.form_submit_button("🔍 Find Sharing Partner", type="primary", use_container_width=True)
        
# # #         if submit_button:
# # #             if user_name and location and equipment_type and description and project_name:
# # #                 try:
# # #                     # Create sharing request data
# # #                     request_data = {
# # #                         "requester_name": user_name,
# # #                         "equipment_type": equipment_type,
# # #                         "project_name": project_name,
# # #                         "project_description": description,
# # #                         "project_duration_days": duration,
# # #                         "project_location": location,
# # #                         "latitude": 12.9716,  # Default Chennai coordinates
# # #                         "longitude": 77.5946,
# # #                         "start_date": start_date.isoformat(),
# # #                         "end_date": (start_date + timedelta(days=duration)).isoformat(),
# # #                         "max_distance_km": max_distance,
# # #                         "preferred_cost_split": cost_split,
# # #                         "contact_preferences": {"contact_info": contact_info}
# # #                     }
                    
# # #                     # Submit to Firebase via API
# # #                     token = get_auth_token()
# # #                     if token:
# # #                         result = api_client.create_sharing_request(token, request_data)
# # #                         if result:
# # #                             st.success("🎉 Sharing request created successfully!")
# # #                             st.info(f"✉️ **Notification sent** to nearby partners. Request expires in 24 hours.")
# # #                             st.success(f"🔔 **Request ID: {result.get('id', 'N/A')}** - Save this for tracking!")
# # #                         else:
# # #                             st.error("Failed to create sharing request. Please try again.")
# # #                     else:
# # #                         st.error("Authentication failed. Please login again.")
                        
# # #                 except Exception as e:
# # #                     st.error(f"Error creating request: {e}")
# # #             else:
# # #                 st.error("Please fill in all required fields!")

# # # def render_active_requests(sharing_requests):
# # #     """Render active sharing requests from Firebase"""
    
# # #     st.markdown("### 📋 Active Sharing Requests")
    
# # #     if sharing_requests.empty:
# # #         st.info("No active sharing requests at the moment.")
# # #         return
    
# # #     active_requests = sharing_requests[sharing_requests['status'] == 'active']
    
# # #     if active_requests.empty:
# # #         st.info("No active sharing requests at the moment.")
# # #         return
    
# # #     for _, request in active_requests.iterrows():
# # #         try:
# # #             expires_at = pd.to_datetime(request['expires_at'])
# # #             hours_left = int((expires_at - datetime.now()).total_seconds() / 3600)
# # #             urgency_color = "#dc3545" if hours_left < 6 else "#ffc107" if hours_left < 12 else "#28a745"
            
# # #             # Create container for each request
# # #             with st.container():
# # #                 st.markdown(f"""
# # #                 <div style="border-left: 4px solid {urgency_color}; padding: 1.5rem; margin: 1rem 0; 
# # #                             background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
# # #                     <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
# # #                         <h4>🏗️ {request.get('equipment_type', 'Unknown')} - {request.get('project_location', 'Unknown')}</h4>
# # #                         <span style="background: {urgency_color}; color: white; padding: 0.3rem 0.8rem; 
# # #                                    border-radius: 15px; font-size: 0.8rem;">
# # #                             ⏰ {hours_left}h left
# # #                         </span>
# # #                     </div>
                    
# # #                     <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
# # #                         <div>
# # #                             <strong>👤 Company:</strong> {request.get('requester_name', 'Unknown')}<br>
# # #                             <strong>📅 Duration:</strong> {request.get('project_duration_days', 'Unknown')} days<br>
# # #                             <strong>📍 Max Distance:</strong> {request.get('max_distance_km', 'Unknown')} km
# # #                         </div>
# # #                         <div>
# # #                             <strong>💰 Cost Split:</strong> {request.get('preferred_cost_split', 'Unknown')}<br>
# # #                             <strong>🗓️ Start Date:</strong> {request.get('start_date', 'Unknown')}<br>
# # #                             <strong>🆔 Request ID:</strong> {request.get('id', 'Unknown')}
# # #                         </div>
# # #                     </div>
                    
# # #                     <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 6px; margin-bottom: 1rem;">
# # #                         <strong>📝 Description:</strong> {request.get('project_description', 'No description')}
# # #                     </div>
# # #                 </div>
# # #                 """, unsafe_allow_html=True)
                
# # #                 # Interactive buttons
# # #                 col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                
# # #                 with col1:
# # #                     if st.button(f"🤝 Express Interest", key=f"interest_{request.get('id', 'unknown')}", use_container_width=True):
# # #                         st.success(f"✅ Interest expressed for {request.get('id', 'Unknown')}! We'll notify {request.get('requester_name', 'Unknown')} immediately.")
# # #                         st.balloons()
                
# # #                 with col2:
# # #                     if st.button(f"📞 Contact User", key=f"contact_{request.get('id', 'unknown')}", use_container_width=True):
# # #                         st.info(f"📧 Contact details for {request.get('requester_name', 'Unknown')} have been sent to your registered email.")
                
# # #                 with col3:
# # #                     if st.button(f"ℹ️ More Details", key=f"details_{request.get('id', 'unknown')}", use_container_width=True):
# # #                         with st.expander(f"Detailed Information - {request.get('id', 'Unknown')}", expanded=True):
# # #                             st.markdown(f"""
# # #                             **📋 Project Details:**
# # #                             - **Project Name:** {request.get('project_name', 'Unknown')}
# # #                             - **Project Type:** {request.get('equipment_type', 'Unknown')} Operation
# # #                             - **Duration:** {request.get('project_duration_days', 'Unknown')} days
                            
# # #                             **💰 Cost Breakdown:**
# # #                             - **Equipment Rental:** $850/day (estimated)
# # #                             - **Your Share:** Based on {request.get('preferred_cost_split', 'Unknown')} arrangement
                            
# # #                             **📍 Location Details:**
# # #                             - **Address:** {request.get('project_location', 'Unknown')}
# # #                             - **Coordinates:** {request.get('latitude', 'N/A')}, {request.get('longitude', 'N/A')}
# # #                             """)
                
# # #                 with col4:
# # #                     if st.button(f"🚫 Not Interested", key=f"decline_{request.get('id', 'unknown')}", use_container_width=True):
# # #                         st.warning(f"Request {request.get('id', 'Unknown')} marked as 'Not Interested'.")
                
# # #                 st.markdown("---")
                
# # #         except Exception as e:
# # #             st.error(f"Error rendering request: {e}")
# # #             continue

# # # def render_sharing_analytics():
# # #     """Render sharing analytics with real data from Firebase"""
    
# # #     st.markdown("### 📊 Sharing Analytics")
    
# # #     try:
# # #         token = get_auth_token()
# # #         if not token:
# # #             st.error("Authentication failed. Please login again.")
# # #             return
        
# # #         # Get utilization forecast
# # #         col1, col2 = st.columns(2)
        
# # #         with col1:
# # #             st.markdown("#### 🚀 Equipment Utilization Forecast")
# # #             forecast_days = st.slider("Forecast Days", 7, 90, 30)
            
# # #             if st.button("Get Forecast", key="get_forecast"):
# # #                 forecast_data = api_client.get_equipment_utilization_forecast(token, forecast_days)
# # #                 if forecast_data and 'forecast' in forecast_data:
# # #                     st.success(f"Forecast generated for {forecast_days} days")
                    
# # #                     # Show sample forecast data
# # #                     if forecast_data['forecast']:
# # #                         sample_day = forecast_data['forecast'][0]
# # #                         st.write(f"**Sample Day: {sample_day['date']} ({sample_day['day_of_week']})**")
                        
# # #                         for equipment in sample_day['equipment_forecasts'][:3]:  # Show first 3
# # #                             st.write(f"• {equipment['equipment_name']}: {equipment['predicted_utilization']}% utilization")
# # #                 else:
# # #                     st.error("Failed to get forecast data")
        
# # #         with col2:
# # #             st.markdown("#### 🎯 Sharing Opportunities")
# # #             max_distance = st.slider("Max Distance (km)", 5, 20, 10)
            
# # #             if st.button("Find Opportunities", key="find_opportunities"):
# # #                 opportunities = api_client.get_sharing_opportunities(token, max_distance)
# # #                 if opportunities and 'opportunities' in opportunities:
# # #                     st.success(f"Found {len(opportunities['opportunities'])} opportunities")
                    
# # #                     # Show top opportunities
# # #                     for opp in opportunities['opportunities'][:3]:
# # #                         st.write(f"• {opp['equipment_type']}: Score {opp['opportunity_score']} - {opp['recommendation']}")
# # #                 else:
# # #                     st.error("Failed to get opportunities data")
        
# # #         # Analytics insights
# # #         st.markdown("#### 💡 Analytics Insights")
        
# # #         col1, col2, col3 = st.columns(3)
        
# # #         with col1:
# # #             st.info("""
# # #             **🏆 Equipment Utilization**
# # #             Monitor your equipment usage patterns and optimize scheduling
            
# # #             **💰 Revenue Optimization**
# # #             Identify high-demand periods for better pricing
# # #             """)
        
# # #         with col2:
# # #             st.success("""
# # #             **🤝 Sharing Opportunities**
# # #             Find nearby projects for equipment sharing
            
# # #             **📈 Market Trends**
# # #             Understand seasonal demand patterns
# # #             """)
        
# # #         with col3:
# # #             st.warning("""
# # #             **🎯 Recommendations**
# # #             AI-powered suggestions for equipment management
            
# # #             **📊 Performance Metrics**
# # #             Track key performance indicators
# # #             """)
            
# # #     except Exception as e:
# # #         st.error(f"Error loading analytics: {e}")

# # # def main():
# # #     user = get_current_user()
    
# # #     # Header
# # #     col1, col2 = st.columns([3, 1])
# # #     with col1:
# # #         st.markdown("""
# # #         <div class="dashboard-header">
# # #             <h1>🤝 Machine Sharing Platform</h1>
# # #             <p>Connect with nearby users to share equipment costs and maximize utilization</p>
# # #         </div>
# # #         """, unsafe_allow_html=True)
    
# # #     with col2:
# # #         if st.button("🚪 Logout", type="secondary", use_container_width=True):
# # #             logout_user()
# # #             st.rerun()
    
# # #     st.markdown("---")
    
# # #     # Load real sharing data from Firebase
# # #     equipment_data, sharing_requests, sharing_history = get_real_sharing_data()
    
# # #     # Main tabs
# # #     tab1, tab2, tab3, tab4 = st.tabs([
# # #         "📊 Dashboard", "➕ New Request", "📋 Active Requests", "📈 Analytics"
# # #     ])
    
# # #     with tab1:
# # #         render_sharing_dashboard(sharing_requests, sharing_history)
        
# # #         # Recent activity
# # #         st.markdown("---")
# # #         st.markdown("### 🕒 Recent Activity")
        
# # #         if not sharing_requests.empty:
# # #             recent_requests = sharing_requests.head(3)
# # #             for _, request in recent_requests.iterrows():
# # #                 created_time = pd.to_datetime(request.get('created_at', datetime.now()))
# # #                 time_ago = datetime.now() - created_time
# # #                 hours_ago = int(time_ago.total_seconds() / 3600)
                
# # #                 st.markdown(f"🆕 **{hours_ago} hours ago** - New sharing request created ({request.get('requester_name', 'Unknown')} - {request.get('equipment_type', 'Unknown')})")
# # #         else:
# # #             st.info("No recent activity to display")
    
# # #     with tab2:
# # #         render_new_sharing_request()
    
# # #     with tab3:
# # #         render_active_requests(sharing_requests)
    
# # #     with tab4:
# # #         render_sharing_analytics()

# # # if __name__ == "__main__":
# # #     main()


# # import streamlit as st
# # import pandas as pd
# # from datetime import datetime, timedelta

# # from lib.state import is_authenticated, get_current_user, logout_user, get_token
# # from lib.api import api_client
# # from lib.components import render_metric_card
# # from lib.styles import apply_custom_css

# # st.set_page_config(page_title="Machine Sharing", page_icon="🤝", layout="wide")
# # apply_custom_css()

# # if not is_authenticated():
# #     st.error("🔒 Please login first"); st.stop()

# # def get_real_sharing_data():
# #     token = get_token()
# #     requests = api_client.get_sharing_requests(token) or []
# #     equipment = api_client.get_equipment_list(token) or []
# #     return pd.DataFrame(equipment), pd.DataFrame(requests)

# # def render_sharing_dashboard(req_df):
# #     st.markdown("### 🤝 Machine Sharing Overview")
# #     active = len(req_df[req_df["status"]=="active"]) if not req_df.empty and "status" in req_df else 0
# #     m1,m2 = st.columns(2)
# #     with m1: render_metric_card("Active Requests", str(active), "", "📋", "#1f77b4")
# #     with m2: render_metric_card("Total Requests", str(len(req_df)), "", "🧾", "#2ca02c")

# # def render_new_request():
# #     st.markdown("### ➕ Create New Sharing Request")
# #     with st.form("sharing_req"):
# #         c1,c2 = st.columns(2)
# #         with c1:
# #             requester = st.text_input("Your Company Name")
# #             eq_type = st.selectbox("Equipment Type",
# #                                    ["excavator","crane","bulldozer","grader","loader","compactor","forklift","concrete_mixer"])
# #             duration = st.number_input("Duration (days)", 1, 60, 5)
# #             start = st.date_input("Start Date", datetime.now().date())
# #         with c2:
# #             location = st.text_input("Project Location / Address")
# #             distance = st.slider("Max Distance (km)", 1, 50, 10)
# #             split = st.selectbox("Preferred Cost Split", ["50-50","60-40","70-30","Negotiable"])
# #             contact = st.text_input("Contact info")
# #         name = st.text_input("Project Name")
# #         desc = st.text_area("Project Description")
# #         submit = st.form_submit_button("Create", type="primary")
# #         if submit:
# #             token = get_token()
# #             payload = {
# #                 "requester_name": requester or "Demo Co",
# #                 "equipment_type": eq_type,
# #                 "project_name": name or "Untitled Project",
# #                 "project_description": desc or "N/A",
# #                 "project_duration_days": int(duration),
# #                 "project_location": location or "Unknown",
# #                 "latitude": 12.9716,
# #                 "longitude": 77.5946,
# #                 "start_date": start.isoformat(),
# #                 "end_date": (start + timedelta(days=int(duration))).isoformat(),
# #                 "max_distance_km": float(distance),
# #                 "preferred_cost_split": split,
# #                 "contact_preferences": {"contact_info": contact or ""}
# #             }
# #             res = api_client.create_sharing_request(token, payload)
# #             if res:
# #                 st.success(f"Created! ID: {res.get('id','(server generated)')}")

# # def main():
# #     user = get_current_user()
# #     c1,c2 = st.columns([3,1])
# #     with c1:
# #         st.markdown("""
# #         <div class="dashboard-header">
# #           <h1>🤝 Machine Sharing</h1>
# #           <p>Create & view sharing requests (live)</p>
# #         </div>
# #         """, unsafe_allow_html=True)
# #     with c2:
# #         if st.button("🚪 Logout", type="secondary", use_container_width=True):
# #             logout_user(); st.rerun()

# #     st.markdown("---")

# #     equipment_df, req_df = get_real_sharing_data()

# #     tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ New Request", "📋 Active Requests"])
# #     with tab1:
# #         render_sharing_dashboard(req_df)
# #     with tab2:
# #         render_new_request()
# #     with tab3:
# #         if req_df.empty:
# #             st.info("No requests yet.")
# #         else:
# #             st.dataframe(req_df, use_container_width=True, hide_index=True)

# # if __name__ == "__main__":
# #     main()


# import streamlit as st
# import pandas as pd
# from datetime import datetime, timedelta
# from typing import Tuple

# from lib.state import is_authenticated, get_current_user, logout_user, get_token
# from lib.api import api_client
# from lib.components import render_metric_card
# from lib.styles import apply_custom_css

# # ---------- Page setup ----------
# st.set_page_config(page_title="Machine Sharing", page_icon="🤝", layout="wide")
# apply_custom_css()

# # ---------- Auth guard ----------
# if not is_authenticated():
#     st.error("🔒 Please login first")
#     st.stop()

# # ---------- Helpers ----------
# def _to_df(rows) -> pd.DataFrame:
#     if not rows:
#         return pd.DataFrame()
#     try:
#         df = pd.DataFrame(rows)
#     except Exception:
#         return pd.DataFrame()
#     # Normalize datetimes if present
#     for col in ("created_at", "updated_at", "expires_at", "start_date", "end_date"):
#         if col in df.columns:
#             df[col] = pd.to_datetime(df[col], errors="coerce")
#     return df

# def fetch_all_data(token: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
#     """
#     Returns:
#       equipment_df, sharing_df
#     """
#     equipment = api_client.get_equipment_list(token)  # list[dict] or None
#     sharing = api_client.get_sharing_requests(token)  # list[dict] or None
#     return _to_df(equipment), _to_df(sharing)

# def time_left(expires_at: pd.Timestamp) -> str:
#     if pd.isna(expires_at):
#         return "N/A"
#     delta = expires_at - datetime.now()
#     if delta.total_seconds() <= 0:
#         return "Expired"
#     hours = int(delta.total_seconds() // 3600)
#     minutes = int((delta.total_seconds() % 3600) // 60)
#     return f"{hours}h {minutes}m"

# def status_badge_color(status: str) -> str:
#     return {
#         "active": "#28a745",
#         "matched": "#1f7aec",
#         "pending": "#6c757d",
#         "closed": "#6c757d",
#         "expired": "#dc3545",
#     }.get(str(status).lower(), "#6c757d")

# # ---------- UI Sections ----------
# def render_sharing_dashboard(sharing_df: pd.DataFrame):
#     st.markdown("### 🤝 Machine Sharing Overview")

#     total = len(sharing_df)
#     active = len(sharing_df[sharing_df.get("status", "").astype(str).str.lower() == "active"]) if not sharing_df.empty else 0
#     matched = len(sharing_df[sharing_df.get("status", "").astype(str).str.lower() == "matched"]) if not sharing_df.empty else 0

#     # Expiring in 6 hours
#     expiring_soon = 0
#     if not sharing_df.empty and "expires_at" in sharing_df.columns:
#         expiring_soon = len(
#             sharing_df[
#                 (sharing_df["expires_at"].notna())
#                 & (sharing_df["expires_at"] > datetime.now())
#                 & (sharing_df["expires_at"] <= datetime.now() + timedelta(hours=6))
#             ]
#         )

#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         render_metric_card("Total Requests", str(total), "+", "📦", "#1f77b4")
#     with col2:
#         render_metric_card("Active", str(active), "+", "📋", "#28a745")
#     with col3:
#         render_metric_card("Matched", str(matched), "+", "🎯", "#9467bd")
#     with col4:
#         render_metric_card("Expiring < 6h", str(expiring_soon), "+", "⏰", "#ff7f0e")

#     if expiring_soon > 0:
#         st.warning(f"⚠️ {expiring_soon} request(s) are expiring within 6 hours.")

# def render_new_sharing_request(token: str):
#     st.markdown("### ➕ Create New Sharing Request")

#     with st.form("sharing_request_form", clear_on_submit=False):
#         c1, c2 = st.columns(2)
#         with c1:
#             requester_name = st.text_input("Your Company Name", placeholder="ABC Construction Co.")
#             project_name = st.text_input("Project Name", placeholder="Foundation Construction Project")
#             equipment_type = st.selectbox(
#                 "Equipment Type",
#                 ["excavator", "crane", "bulldozer", "grader", "loader", "compactor", "forklift", "concrete_mixer", "generator", "air_compressor"],
#             )
#             project_duration_days = st.selectbox("Project Duration (days)", [1, 2, 3, 4, 5, 7, 10, 14, 21, 30], index=6)
#             preferred_cost_split = st.selectbox("Preferred Cost Split", ["50-50", "60-40", "70-30", "Negotiable"], index=0)
#             max_distance_km = st.slider("Maximum Distance (km)", min_value=1, max_value=50, value=10, step=1)
#         with c2:
#             project_location = st.text_input("Project Location (address/area)", placeholder="Downtown - Block 1")
#             latitude = st.number_input("Latitude", value=12.9716, format="%.6f")
#             longitude = st.number_input("Longitude", value=77.5946, format="%.6f")
#             start_date = st.date_input("Start Date", min_value=datetime.now().date())
#             end_date = start_date + timedelta(days=project_duration_days)
#             st.caption(f"End Date will be set to **{end_date.isoformat()}** based on duration.")

#             contact_info = st.text_input("Contact Info (phone/email)", placeholder="98765 43210 / abc@company.com")

#         project_description = st.text_area(
#             "Project Description",
#             placeholder="Describe your project and the sharing need..."
#         )

#         submitted = st.form_submit_button("🔍 Submit Request", type="primary", use_container_width=True)

#         if submitted:
#             if not (requester_name and project_name and project_location and project_description):
#                 st.error("Please fill in all required fields.")
#                 return

#             data = {
#                 # server will override requester_id/name from JWT; we still send name to display immediately on UI
#                 "requester_name": requester_name,
#                 "equipment_type": equipment_type,
#                 "project_name": project_name,
#                 "project_description": project_description,
#                 "project_duration_days": int(project_duration_days),
#                 "project_location": project_location,
#                 "latitude": float(latitude),
#                 "longitude": float(longitude),
#                 "start_date": datetime.combine(start_date, datetime.min.time()).isoformat(),
#                 "end_date": datetime.combine(end_date, datetime.min.time()).isoformat(),
#                 "max_distance_km": float(max_distance_km),
#                 "preferred_cost_split": preferred_cost_split,
#                 "contact_preferences": {"contact_info": contact_info},
#             }

#             result = api_client.create_sharing_request(token, data)
#             if result:
#                 st.success("🎉 Sharing request created successfully!")
#                 rid = result.get("id", "N/A")
#                 st.info(f"🔔 **Request ID:** {rid} (auto-expires in 24 hours)")
#             else:
#                 st.error("Failed to create sharing request. Please try again.")

# def render_active_requests(sharing_df: pd.DataFrame):
#     st.markdown("### 📋 Active Sharing Requests")

#     if sharing_df.empty:
#         st.info("No sharing requests found. Create one in the **New Request** tab.")
#         return

#     active_df = sharing_df[sharing_df["status"].astype(str).str.lower() == "active"] if "status" in sharing_df.columns else sharing_df
#     if active_df.empty:
#         st.info("No **active** requests right now.")
#         return

#     # Sort by nearest expiry first if available
#     if "expires_at" in active_df.columns:
#         active_df = active_df.sort_values("expires_at")

#     for _, r in active_df.iterrows():
#         equip = r.get("equipment_type", "Unknown")
#         loc = r.get("project_location", "Unknown")
#         req_id = r.get("id", "Unknown")
#         status = str(r.get("status", "active"))
#         color = status_badge_color(status)
#         expires = r.get("expires_at", pd.NaT)
#         left = time_left(expires)

#         st.markdown(
#             f"""
#             <div style="border-left: 4px solid {color}; padding: 1.2rem; margin: 0.8rem 0;
#                         background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
#               <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
#                 <h4 style="margin:0;">🏗️ {equip} — {loc}</h4>
#                 <span style="background:{color}; color:white; padding:0.25rem 0.6rem; border-radius:12px; font-size:0.8rem;">
#                   {status.upper()}
#                 </span>
#               </div>
#               <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 0.8rem;">
#                 <div>
#                   <strong>🆔 Request ID:</strong> {req_id}<br/>
#                   <strong>👤 Company:</strong> {r.get('requester_name','Unknown')}<br/>
#                   <strong>📅 Duration:</strong> {r.get('project_duration_days','?')} days
#                 </div>
#                 <div>
#                   <strong>⏰ Time Left:</strong> {left}<br/>
#                   <strong>💰 Cost Split:</strong> {r.get('preferred_cost_split', '—')}<br/>
#                   <strong>📍 Max Distance:</strong> {r.get('max_distance_km','—')} km
#                 </div>
#               </div>
#               <div style="background:#f8f9fa; padding:0.6rem; border-radius:6px; margin-top:0.8rem;">
#                 <strong>📝 Description:</strong> {r.get('project_description', '—')}
#               </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         c1, c2, c3 = st.columns([1, 1, 1])
#         with c1:
#             if st.button("🤝 Express Interest", key=f"interest_{req_id}", use_container_width=True):
#                 st.success("✅ Interest recorded (demo). In production, this would notify the requester.")
#         with c2:
#             if st.button("📞 Contact", key=f"contact_{req_id}", use_container_width=True):
#                 contact = r.get("contact_preferences", {}) or {}
#                 st.info(f"Contact: {contact.get('contact_info', 'N/A')}")
#         with c3:
#             if st.button("ℹ️ Details", key=f"details_{req_id}", use_container_width=True):
#                 st.write({k: v for k, v in r.items() if k not in ["contact_preferences"]})

#         st.markdown("---")

# def render_analytics(token: str):
#     st.markdown("### 📊 Sharing Analytics")

#     c1, c2 = st.columns(2)
#     with c1:
#         st.markdown("#### 🚀 Utilization Forecast")
#         days = st.slider("Days Ahead", 7, 60, 30, key="forecast_days")
#         if st.button("Get Forecast", key="btn_forecast"):
#             data = api_client.get_equipment_utilization_forecast(token, days)
#             if data and data.get("forecast"):
#                 st.success(f"Forecast generated for {data.get('forecast_period_days', days)} days")
#                 # Flatten top-day snapshot for quick view
#                 sample = data["forecast"][0]
#                 st.write(f"**{sample['date']} ({sample['day_of_week']}) — {sample['season']}**")
#                 samp_df = pd.DataFrame(sample["equipment_forecasts"])
#                 if not samp_df.empty:
#                     st.dataframe(
#                         samp_df[["equipment_name", "equipment_type", "predicted_utilization", "potential_revenue", "recommendation"]],
#                         use_container_width=True,
#                         hide_index=True,
#                     )
#             else:
#                 st.info("No forecast available (you may need to add equipment first).")

#     with c2:
#         st.markdown("#### 🎯 Sharing Opportunities")
#         max_km = st.slider("Max Distance (km)", 5, 50, 10, key="opp_distance")
#         if st.button("Find Opportunities", key="btn_opps"):
#             opps = api_client.get_sharing_opportunities(token, max_km)
#             if opps and opps.get("opportunities"):
#                 opp_df = pd.DataFrame(opps["opportunities"])
#                 st.success(f"Found {len(opp_df)} opportunities")
#                 show_cols = ["equipment_type", "requester_name", "opportunity_score", "potential_revenue", "recommendation"]
#                 st.dataframe(opp_df[show_cols], use_container_width=True, hide_index=True)
#             else:
#                 st.info("No opportunities found.")

# # ---------- Main ----------
# user = get_current_user()

# hdr1, hdr2 = st.columns([3, 1])
# with hdr1:
#     st.markdown(
#         """
#         <div class="dashboard-header">
#             <h1>🤝 Machine Sharing Platform</h1>
#             <p>Fetch/submit real requests via your FastAPI + Firestore backend</p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
# with hdr2:
#     if st.button("🚪 Logout", type="secondary", use_container_width=True):
#         logout_user()
#         st.rerun()

# st.markdown("---")

# token = get_token()
# if not token:
#     st.error("Missing auth token. Please log in again.")
#     st.stop()

# equipment_df, sharing_df = fetch_all_data(token)

# tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "➕ New Request", "📋 Active Requests", "📈 Analytics"])

# with tab1:
#     render_sharing_dashboard(sharing_df)
#     st.markdown("---")
#     st.markdown("#### Recent Requests")
#     if not sharing_df.empty:
#         # Most recent first if we have created_at
#         if "created_at" in sharing_df.columns:
#             sharing_df = sharing_df.sort_values("created_at", ascending=False)
#         cols = ["id", "equipment_type", "requester_name", "project_location", "project_duration_days", "status", "expires_at"]
#         present = [c for c in cols if c in sharing_df.columns]
#         st.dataframe(sharing_df[present].head(10), use_container_width=True, hide_index=True)
#     else:
#         st.info("No requests yet. Create one in the next tab.")

# with tab2:
#     render_new_sharing_request(token)

# with tab3:
#     render_active_requests(sharing_df)

# with tab4:
#     render_analytics(token)


# frontend/streamlit_app/pages/sharing.py

import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from typing import Tuple

from lib.state import is_authenticated, get_current_user, logout_user, get_token
from lib.api import api_client
from lib.components import render_metric_card
from lib.styles import apply_custom_css

# ---------- Page setup ----------
st.set_page_config(page_title="Machine Sharing", page_icon="🤝", layout="wide")
apply_custom_css()

# ---------- Auth guard ----------
if not is_authenticated():
    st.error("🔒 Please login first")
    st.stop()

# ---------- Helpers ----------
def _to_df(rows) -> pd.DataFrame:
    """Safe list[dict] -> DataFrame with parsed datetime columns."""
    if not rows:
        return pd.DataFrame()
    try:
        df = pd.DataFrame(rows)
    except Exception:
        return pd.DataFrame()

    for col in ("created_at", "updated_at", "expires_at", "start_date", "end_date"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def fetch_all_data(token: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns: (equipment_df, sharing_df)
    Pulls live data from the backend. Any API error -> empty DataFrames.
    """
    equipment = api_client.get_equipment_list(token)          # list[dict] or None
    sharing = api_client.get_sharing_requests(token)          # list[dict] or None
    return _to_df(equipment), _to_df(sharing)


def time_left(expires_at: pd.Timestamp) -> str:
    if pd.isna(expires_at):
        return "N/A"
    delta = expires_at - datetime.now()
    if delta.total_seconds() <= 0:
        return "Expired"
    hours = int(delta.total_seconds() // 3600)
    minutes = int((delta.total_seconds() % 3600) // 60)
    return f"{hours}h {minutes}m"


def status_badge_color(status: str) -> str:
    return {
        "active": "#28a745",
        "matched": "#1f7aec",
        "pending": "#6c757d",
        "closed": "#6c757d",
        "expired": "#dc3545",
    }.get(str(status).lower(), "#6c757d")


# ---------- UI Sections ----------
def render_sharing_dashboard(sharing_df: pd.DataFrame):
    st.markdown("### 🤝 Machine Sharing Overview")

    total = len(sharing_df)

    if not sharing_df.empty and "status" in sharing_df.columns:
        s = sharing_df["status"].astype(str).str.lower()
        active = int((s == "active").sum())
        matched = int((s == "matched").sum())
    else:
        active = matched = 0

    # expiring within 6h
    expiring_soon = 0
    if not sharing_df.empty and "expires_at" in sharing_df.columns:
        now = datetime.now()
        soon = now + timedelta(hours=6)
        mask = (sharing_df["expires_at"].notna()) & (sharing_df["expires_at"] > now) & (sharing_df["expires_at"] <= soon)
        expiring_soon = int(mask.sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total Requests", str(total), "+", "📦", "#1f77b4")
    with c2:
        render_metric_card("Active", str(active), "+", "📋", "#28a745")
    with c3:
        render_metric_card("Matched", str(matched), "+", "🎯", "#9467bd")
    with c4:
        render_metric_card("Expiring < 6h", str(expiring_soon), "+", "⏰", "#ff7f0e")

    if expiring_soon > 0:
        st.warning(f"⚠️ {expiring_soon} request(s) are expiring within 6 hours.")


def render_new_sharing_request(token: str):
    st.markdown("### ➕ Create New Sharing Request")

    with st.form("sharing_request_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            requester_name = st.text_input("Your Company Name", placeholder="ABC Construction Co.")
            project_name = st.text_input("Project Name", placeholder="Foundation Construction Project")
            equipment_type = st.selectbox(
                "Equipment Type",
                [
                    "excavator", "crane", "bulldozer", "grader", "loader",
                    "compactor", "forklift", "concrete_mixer", "generator", "air_compressor",
                ],
            )
            project_duration_days = st.selectbox("Project Duration (days)", [1, 2, 3, 4, 5, 7, 10, 14, 21, 30], index=6)
            preferred_cost_split = st.selectbox("Preferred Cost Split", ["50-50", "60-40", "70-30", "Negotiable"], index=0)
            max_distance_km = st.slider("Maximum Distance (km)", min_value=1, max_value=50, value=10, step=1)
        with c2:
            project_location = st.text_input("Project Location (address/area)", placeholder="Downtown - Block 1")
            latitude = st.number_input("Latitude", value=12.9716, format="%.6f")
            longitude = st.number_input("Longitude", value=77.5946, format="%.6f")
            start_date = st.date_input("Start Date", min_value=datetime.now().date())
            end_date = start_date + timedelta(days=int(project_duration_days))
            st.caption(f"End Date will be set to **{end_date.isoformat()}** based on duration.")

            contact_info = st.text_input("Contact Info (phone/email)", placeholder="98765 43210 / abc@company.com")

        project_description = st.text_area(
            "Project Description",
            placeholder="Describe your project and the sharing need...",
        )

        submitted = st.form_submit_button("🔍 Submit Request", type="primary", use_container_width=True)

        if submitted:
            if not (requester_name and project_name and project_location and project_description):
                st.error("Please fill in all required fields.")
                return

            data = {
                # server will override requester_id/name from JWT; we still send name to show immediately on UI
                "requester_name": requester_name,
                "equipment_type": equipment_type,
                "project_name": project_name,
                "project_description": project_description,
                "project_duration_days": int(project_duration_days),
                "project_location": project_location,
                "latitude": float(latitude),
                "longitude": float(longitude),
                "start_date": datetime.combine(start_date, datetime.min.time()).isoformat(),
                "end_date": datetime.combine(end_date, datetime.min.time()).isoformat(),
                "max_distance_km": float(max_distance_km),
                "preferred_cost_split": preferred_cost_split,
                "contact_preferences": {"contact_info": contact_info},
            }

            result = api_client.create_sharing_request(token, data)
            if result:
                st.success("🎉 Sharing request created successfully!")
                rid = result.get("id", "N/A")
                st.info(f"🔔 **Request ID:** {rid} (auto-expires in 24 hours)")
            else:
                st.error("Failed to create sharing request. Please try again.")


def render_active_requests(sharing_df: pd.DataFrame):
    st.markdown("### 📋 Active Sharing Requests")

    if sharing_df.empty:
        st.info("No sharing requests found. Create one in the **New Request** tab.")
        return

    if "status" in sharing_df.columns:
        active_df = sharing_df[sharing_df["status"].astype(str).str.lower() == "active"].copy()
    else:
        active_df = sharing_df.copy()

    if active_df.empty:
        st.info("No **active** requests right now.")
        return

    # Sort by nearest expiry first if available
    if "expires_at" in active_df.columns:
        active_df = active_df.sort_values("expires_at")

    for _, r in active_df.iterrows():
        equip = r.get("equipment_type", "Unknown")
        loc = r.get("project_location", "Unknown")
        req_id = r.get("id", "Unknown")
        status = str(r.get("status", "active"))
        color = status_badge_color(status)
        expires = r.get("expires_at", pd.NaT)
        left = time_left(expires)

        st.markdown(
            f"""
            <div style="border-left: 4px solid {color}; padding: 1.2rem; margin: 0.8rem 0;
                        background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                <h4 style="margin:0;">🏗️ {equip} — {loc}</h4>
                <span style="background:{color}; color:white; padding:0.25rem 0.6rem; border-radius:12px; font-size:0.8rem;">
                  {status.upper()}
                </span>
              </div>
              <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 0.8rem;">
                <div>
                  <strong>🆔 Request ID:</strong> {req_id}<br/>
                  <strong>👤 Company:</strong> {r.get('requester_name','Unknown')}<br/>
                  <strong>📅 Duration:</strong> {r.get('project_duration_days','?')} days
                </div>
                <div>
                  <strong>⏰ Time Left:</strong> {left}<br/>
                  <strong>💰 Cost Split:</strong> {r.get('preferred_cost_split', '—')}<br/>
                  <strong>📍 Max Distance:</strong> {r.get('max_distance_km','—')} km
                </div>
              </div>
              <div style="background:#f8f9fa; padding:0.6rem; border-radius:6px; margin-top:0.8rem;">
                <strong>📝 Description:</strong> {r.get('project_description', '—')}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("🤝 Express Interest", key=f"interest_{req_id}", use_container_width=True):
                st.success("✅ Interest recorded (demo). In production, this would notify the requester.")
        with c2:
            if st.button("📞 Contact", key=f"contact_{req_id}", use_container_width=True):
                contact = r.get("contact_preferences", {}) or {}
                st.info(f"Contact: {contact.get('contact_info', 'N/A')}")
        with c3:
            if st.button("ℹ️ Details", key=f"details_{req_id}", use_container_width=True):
                st.write({k: v for k, v in r.items() if k not in ["contact_preferences"]})

        st.markdown("---")


def render_analytics(token: str):
    st.markdown("### 📊 Sharing Analytics")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 🚀 Utilization Forecast")
        days = st.slider("Days Ahead", 7, 60, 30, key="forecast_days")
        if st.button("Get Forecast", key="btn_forecast"):
            data = api_client.get_equipment_utilization_forecast(token, days)
            if data and data.get("forecast"):
                st.success(f"Forecast generated for {data.get('forecast_period_days', days)} days")
                # Show snapshot for the first day
                sample = data["forecast"][0]
                st.write(f"**{sample['date']} ({sample['day_of_week']}) — {sample['season']}**")
                samp_df = pd.DataFrame(sample.get("equipment_forecasts", []))
                if not samp_df.empty:
                    cols = ["equipment_name", "equipment_type", "predicted_utilization", "potential_revenue", "recommendation"]
                    show = [c for c in cols if c in samp_df.columns]
                    st.dataframe(samp_df[show], use_container_width=True, hide_index=True)
                else:
                    st.info("No per-equipment forecasts available.")
            else:
                st.info("No forecast available (you may need to add equipment first).")

    with c2:
        st.markdown("#### 🎯 Sharing Opportunities")
        max_km = st.slider("Max Distance (km)", 5, 50, 10, key="opp_distance")
        if st.button("Find Opportunities", key="btn_opps"):
            opps = api_client.get_sharing_opportunities(token, max_km)
            if opps and opps.get("opportunities"):
                opp_df = pd.DataFrame(opps["opportunities"])
                st.success(f"Found {len(opp_df)} opportunities")
                show_cols = ["equipment_type", "requester_name", "opportunity_score", "potential_revenue", "recommendation"]
                present = [c for c in show_cols if c in opp_df.columns]
                st.dataframe(opp_df[present], use_container_width=True, hide_index=True)
            else:
                st.info("No opportunities found.")


# ---------- Main ----------
user = get_current_user()

h1, h2 = st.columns([3, 1])
with h1:
    st.markdown(
        """
        <div class="dashboard-header">
            <h1>🤝 Machine Sharing Platform</h1>
            <p>Fetch/submit real requests via your FastAPI + Firestore backend</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with h2:
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        logout_user()
        st.rerun()

st.markdown("---")

token = get_token()
if not token:
    st.error("Missing auth token. Please log in again.")
    st.stop()

equipment_df, sharing_df = fetch_all_data(token)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "➕ New Request", "📋 Active Requests", "📈 Analytics"])

with tab1:
    render_sharing_dashboard(sharing_df)
    st.markdown("---")
    st.markdown("#### Recent Requests")
    if not sharing_df.empty:
        df = sharing_df.copy()
        if "created_at" in df.columns:
            df = df.sort_values("created_at", ascending=False)
        cols = ["id", "equipment_type", "requester_name", "project_location", "project_duration_days", "status", "expires_at"]
        present = [c for c in cols if c in df.columns]
        st.dataframe(df[present].head(10), use_container_width=True, hide_index=True)
    else:
        st.info("No requests yet. Create one in the next tab.")

with tab2:
    render_new_sharing_request(token)

with tab3:
    render_active_requests(sharing_df)

with tab4:
    render_analytics(token)

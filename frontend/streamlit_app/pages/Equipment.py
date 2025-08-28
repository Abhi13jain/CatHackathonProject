# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import qrcode
# from io import BytesIO
# import base64
# from lib.state import is_authenticated, get_current_user, logout_user
# from lib.data import get_sample_equipment_data, get_overdue_equipment, get_maintenance_due
# from lib.components import render_metric_card, render_equipment_card, render_equipment_status_chart
# from lib.styles import apply_custom_css, get_status_color

# st.set_page_config(
#     page_title="Equipment Management",
#     page_icon="🏗️",
#     layout="wide"
# )

# # Apply custom CSS
# apply_custom_css()

# # Check authentication
# if not is_authenticated():
#     st.error("🔒 Please login first")
#     st.stop()

# def generate_qr_code(equipment_id):
#     """Generate QR code for equipment"""
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr_data = f"https://smartrental.com/equipment/{equipment_id}"
#     qr.add_data(qr_data)
#     qr.make(fit=True)
    
#     img = qr.make_image(fill_color="black", back_color="white")
    
#     # Convert to base64 for display
#     buffered = BytesIO()
#     img.save(buffered)
#     img_str = base64.b64encode(buffered.getvalue()).decode()
    
#     return img_str

# def show_equipment_details(equipment_data, equipment_id):
#     """Show detailed view of selected equipment"""
#     equipment = equipment_data[equipment_data['Equipment ID'] == equipment_id].iloc[0]
    
#     col1, col2, col3 = st.columns([2, 1, 1])
    
#     with col1:
#         st.markdown(f"### 🏗️ {equipment['Equipment ID']} - {equipment['Type']}")
        
#         # Status badge
#         status_color = get_status_color(equipment['Status'])
#         st.markdown(f"""
#         <span style="background-color: {status_color}; color: white; padding: 0.3rem 0.8rem; 
#         border-radius: 20px; font-size: 0.9rem; font-weight: 500;">
#         {equipment['Status']}
#         </span>
#         """, unsafe_allow_html=True)
        
#         st.markdown("---")
        
#         # Equipment details
#         details_col1, details_col2 = st.columns(2)
        
#         with details_col1:
#             st.markdown(f"**📍 Location:** {equipment['Location']}")
#             st.markdown(f"**⏰ Engine Hours:** {equipment['Engine Hours']:,}")
#             st.markdown(f"**🔧 Total Hours:** {equipment['Total Hours']:,}")
#             st.markdown(f"**⏸️ Idle Hours:** {equipment['Idle Hours']:,}")
        
#         with details_col2:
#             st.markdown(f"**📅 Operational Days:** {equipment['Operational Days']}")
#             st.markdown(f"**⛽ Fuel Level:** {equipment['Fuel Level']}%")
#             st.markdown(f"**🔧 Next Maintenance:** {equipment['Next Maintenance']}")
#             st.markdown(f"**📊 Last Update:** {equipment['Last Update']}")
    
#     with col2:
#         # QR Code
#         st.markdown("#### QR Code")
#         qr_img = generate_qr_code(equipment_id)
#         st.markdown(f"""
#         <div style="text-align: center;">
#             <img src="data:image/png;base64,{qr_img}" width="150">
#             <p style="font-size: 0.8rem; color: #7f8c8d;">Scan for quick access</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         # Action buttons
#         st.markdown("#### Quick Actions")
        
#         if equipment['Status'] == 'Available':
#             if st.button("📤 Check Out", use_container_width=True, type="primary"):
#                 st.success(f"Equipment {equipment_id} checked out successfully!")
#                 st.rerun()
        
#         elif equipment['Status'] == 'Rented':
#             if st.button("📥 Check In", use_container_width=True, type="primary"):
#                 st.success(f"Equipment {equipment_id} checked in successfully!")
#                 st.rerun()
        
#         if st.button("🔧 Schedule Maintenance", use_container_width=True):
#             st.info("Maintenance scheduling opened")
        
#         if st.button("📍 Update Location", use_container_width=True):
#             st.info("Location update opened")
        
#         if st.button("📊 View History", use_container_width=True):
#             st.info("Equipment history opened")
    
#     # Performance charts
#     st.markdown("---")
#     st.markdown("#### 📊 Equipment Performance")
    
#     chart_col1, chart_col2 = st.columns(2)
    
#     with chart_col1:
#         # Usage trend (simulated data)
#         usage_dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
#         usage_hours = [equipment['Engine Hours']/30 + i*2 + (i%7)*5 for i in range(30)]
        
#         usage_df = pd.DataFrame({
#             'Date': usage_dates,
#             'Daily Hours': usage_hours
#         })
        
#         fig_usage = px.line(usage_df, x='Date', y='Daily Hours', 
#                            title=f"Daily Usage Trend - {equipment_id}")
#         fig_usage.update_traces(line_color='#1f77b4')
#         st.plotly_chart(fig_usage, use_container_width=True)
    
#     with chart_col2:
#         # Fuel efficiency
#         fuel_dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
#         fuel_levels = [equipment['Fuel Level'] - i*10 + (i%3)*5 for i in range(7)]
#         fuel_levels = [max(20, min(100, level)) for level in fuel_levels]  # Keep within bounds
        
#         fuel_df = pd.DataFrame({
#             'Date': fuel_dates,
#             'Fuel Level': fuel_levels
#         })
        
#         fig_fuel = px.line(fuel_df, x='Date', y='Fuel Level',
#                           title=f"Fuel Level Trend - {equipment_id}")
#         fig_fuel.update_traces(line_color='#ff7f0e')
#         fig_fuel.update_layout(yaxis=dict(range=[0, 100]))
#         st.plotly_chart(fig_fuel, use_container_width=True)

# def main():
#     user = get_current_user()
    
#     # Header
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.markdown("""
#         <div class="dashboard-header">
#             <h1>🏗️ Equipment Management</h1>
#             <p>Manage and track your equipment fleet</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         if st.button("🚪 Logout", type="secondary", use_container_width=True):
#             logout_user()
#             st.rerun()
    
#     st.markdown("---")
    
#     # Load data
#     equipment_data = get_sample_equipment_data()
#     overdue_equipment = get_overdue_equipment()
#     maintenance_due = get_maintenance_due()
    
#     # Quick stats
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         render_metric_card("Total Equipment", f"{len(equipment_data)}", "+12 this month", "🏗️", "#1f77b4")
    
#     with col2:
#         available_count = len(equipment_data[equipment_data['Status'] == 'Available'])
#         render_metric_card("Available", f"{available_count}", "+5 returned", "✅", "#2ca02c")
    
#     with col3:
#         rented_count = len(equipment_data[equipment_data['Status'] == 'Rented'])
#         render_metric_card("Currently Rented", f"{rented_count}", "-3 today", "📋", "#ff7f0e")
    
#     with col4:
#         maintenance_count = len(equipment_data[equipment_data['Status'] == 'Maintenance'])
#         render_metric_card("Under Maintenance", f"{maintenance_count}", "+2 scheduled", "🔧", "#d62728")
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Main tabs
#     tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Equipment List", "🔍 Equipment Details", "🚨 Alerts", "📊 Analytics", "⚡ Quick Actions"])
    
#     with tab1:
#         st.markdown("### Equipment Fleet Overview")
        
#         # Filters
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             type_filter = st.selectbox("Filter by Type", 
#                                      ["All"] + list(equipment_data['Type'].unique()))
        
#         with col2:
#             status_filter = st.selectbox("Filter by Status",
#                                        ["All"] + list(equipment_data['Status'].unique()))
        
#         with col3:
#             location_filter = st.selectbox("Filter by Location",
#                                          ["All"] + list(equipment_data['Location'].unique()))
        
#         with col4:
#             search_term = st.text_input("Search Equipment ID", placeholder="EX1001")
        
#         # Apply filters
#         filtered_data = equipment_data.copy()
        
#         if type_filter != "All":
#             filtered_data = filtered_data[filtered_data['Type'] == type_filter]
        
#         if status_filter != "All":
#             filtered_data = filtered_data[filtered_data['Status'] == status_filter]
        
#         if location_filter != "All":
#             filtered_data = filtered_data[filtered_data['Location'] == location_filter]
        
#         if search_term:
#             filtered_data = filtered_data[filtered_data['Equipment ID'].str.contains(search_term, case=False)]
        
#         st.markdown(f"**Showing {len(filtered_data)} of {len(equipment_data)} equipment**")
        
#         # Equipment cards grid
#         if not filtered_data.empty:
#             # Create columns for cards (3 per row)
#             for i in range(0, len(filtered_data), 3):
#                 cols = st.columns(3)
#                 for j, (_, equipment) in enumerate(filtered_data.iloc[i:i+3].iterrows()):
#                     with cols[j]:
#                         render_equipment_card(
#                             equipment['Equipment ID'],
#                             equipment['Type'],
#                             equipment['Status'],
#                             equipment['Location'],
#                             equipment['Last Update']
#                         )
#         else:
#             st.info("No equipment found matching the filters.")
        
#         # Data table view
#         if st.checkbox("Show detailed table view"):
#             display_columns = ['Equipment ID', 'Type', 'Status', 'Location', 
#                              'Engine Hours', 'Total Hours', 'Fuel Level', 'Last Update']
#             st.dataframe(filtered_data[display_columns], use_container_width=True, hide_index=True)
    
#     with tab2:
#         st.markdown("### Equipment Details")
        
#         # Equipment selector
#         equipment_ids = equipment_data['Equipment ID'].tolist()
#         selected_equipment = st.selectbox("Select Equipment", equipment_ids)
        
#         if selected_equipment:
#             show_equipment_details(equipment_data, selected_equipment)
    
#     with tab3:
#         st.markdown("### 🚨 Alerts & Notifications")
        
#         # Overdue equipment
#         if overdue_equipment:
#             st.markdown("#### Overdue Returns")
            
#             for equipment in overdue_equipment:
#                 st.error(f"**{equipment['Equipment ID']}** ({equipment['Type']}) - "
#                         f"{equipment['Days Overdue']} days overdue at {equipment['Location']}")
        
#         # Maintenance due
#         if maintenance_due:
#             st.markdown("#### Maintenance Due")
            
#             for equipment in maintenance_due:
#                 if equipment['Days Until Maintenance'] <= 0:
#                     st.error(f"**{equipment['Equipment ID']}** ({equipment['Type']}) - "
#                             f"Maintenance overdue by {abs(equipment['Days Until Maintenance'])} days")
#                 elif equipment['Days Until Maintenance'] <= 3:
#                     st.warning(f"**{equipment['Equipment ID']}** ({equipment['Type']}) - "
#                               f"Maintenance due in {equipment['Days Until Maintenance']} days")
#                 else:
#                     st.info(f"**{equipment['Equipment ID']}** ({equipment['Type']}) - "
#                            f"Maintenance due in {equipment['Days Until Maintenance']} days")
        
#         # Other alerts
#         st.markdown("#### System Alerts")
#         st.warning("🔋 Low fuel alert: 3 equipment units below 25% fuel level")
#         st.info("📍 Location sync: All equipment GPS data updated successfully")
#         st.success("✅ Daily maintenance check completed for 12 equipment units")
    
#     with tab4:
#         st.markdown("### 📊 Equipment Analytics")
        
#         # Equipment distribution charts
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Status distribution
#             status_fig = render_equipment_status_chart(equipment_data)
#             st.plotly_chart(status_fig, use_container_width=True)
        
#         with col2:
#             # Equipment by type
#             type_counts = equipment_data['Type'].value_counts()
#             fig_type = px.bar(x=type_counts.index, y=type_counts.values,
#                              title="Equipment Count by Type")
#             fig_type.update_layout(xaxis_title="Equipment Type", yaxis_title="Count")
#             st.plotly_chart(fig_type, use_container_width=True)
        
#         # Location distribution
#         col1, col2 = st.columns(2)
        
#         with col1:
#             location_counts = equipment_data['Location'].value_counts()
#             fig_location = px.pie(values=location_counts.values, names=location_counts.index,
#                                  title="Equipment Distribution by Location")
#             st.plotly_chart(fig_location, use_container_width=True)
        
#         with col2:
#             # Utilization analysis
#             equipment_data['Utilization'] = (equipment_data['Engine Hours'] / 
#                                            equipment_data['Total Hours']) * 100
            
#             top_utilized = equipment_data.nlargest(10, 'Utilization')
#             fig_util = px.bar(top_utilized, x='Equipment ID', y='Utilization',
#                              title="Top 10 Most Utilized Equipment")
#             fig_util.update_layout(xaxis_title="Equipment ID", yaxis_title="Utilization %")
#             st.plotly_chart(fig_util, use_container_width=True)
        
#         # Performance metrics table
#         st.markdown("#### Performance Summary")
        
#         performance_summary = equipment_data.groupby('Type').agg({
#             'Engine Hours': ['mean', 'sum'],
#             'Total Hours': 'sum',
#             'Idle Hours': 'sum'
#         }).round(2)
        
#         performance_summary.columns = ['Avg Engine Hours', 'Total Engine Hours', 
#                                       'Total Hours', 'Total Idle Hours']
        
#         st.dataframe(performance_summary, use_container_width=True)
    
#     with tab5:
#         st.markdown("### ⚡ Quick Actions")
        
#         # Action categories
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             st.markdown("#### Equipment Operations")
            
#             if st.button("➕ Add New Equipment", use_container_width=True):
#                 st.success("Add Equipment form opened")
            
#             if st.button("📤 Bulk Check Out", use_container_width=True):
#                 st.success("Bulk check out process started")
            
#             if st.button("📥 Bulk Check In", use_container_width=True):
#                 st.success("Bulk check in process started")
            
#             if st.button("🔄 Transfer Equipment", use_container_width=True):
#                 st.success("Equipment transfer form opened")
        
#         with col2:
#             st.markdown("#### Maintenance & Service")
            
#             if st.button("🔧 Schedule Bulk Maintenance", use_container_width=True):
#                 st.success("Bulk maintenance scheduler opened")
            
#             if st.button("📋 Generate Service Report", use_container_width=True):
#                 st.success("Service report generation started")
            
#             if st.button("⚠️ Flag Equipment Issues", use_container_width=True):
#                 st.success("Equipment issue reporter opened")
            
#             if st.button("🛠️ Update Maintenance Records", use_container_width=True):
#                 st.success("Maintenance records updater opened")
        
#         with col3:
#             st.markdown("#### Data & Reports")
            
#             if st.button("📊 Export Equipment Data", use_container_width=True):
#                 csv = equipment_data.to_csv(index=False)
#                 st.download_button(
#                     label="⬇️ Download CSV",
#                     data=csv,
#                     file_name=f"equipment_data_{datetime.now().strftime('%Y%m%d')}.csv",
#                     mime="text/csv"
#                 )
            
#             if st.button("📈 Generate Utilization Report", use_container_width=True):
#                 st.success("Utilization report generated")
            
#             if st.button("💰 Revenue Analysis", use_container_width=True):
#                 st.success("Revenue analysis opened")
            
#             if st.button("🔍 Equipment Audit", use_container_width=True):
#                 st.success("Equipment audit process started")
        
#         # Bulk operations
#         st.markdown("---")
#         st.markdown("#### Bulk Operations")
        
#         selected_equipment = st.multiselect(
#             "Select equipment for bulk operations:",
#             equipment_data['Equipment ID'].tolist()
#         )
        
#         if selected_equipment:
#             bulk_col1, bulk_col2, bulk_col3 = st.columns(3)
            
#             with bulk_col1:
#                 if st.button("📍 Update Location", use_container_width=True):
#                     st.success(f"Location update applied to {len(selected_equipment)} equipment")
            
#             with bulk_col2:
#                 if st.button("🔧 Schedule Maintenance", use_container_width=True):
#                     st.success(f"Maintenance scheduled for {len(selected_equipment)} equipment")
            
#             with bulk_col3:
#                 if st.button("📊 Generate Report", use_container_width=True):
#                     st.success(f"Report generated for {len(selected_equipment)} equipment")

# if __name__ == "__main__":
#     main()



import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import base64
import qrcode

from lib.state import is_authenticated, get_current_user, logout_user, get_token
from lib.api import api_client
from lib.components import render_metric_card, render_equipment_card
from lib.styles import apply_custom_css

st.set_page_config(page_title="Equipment Management", page_icon="🏗️", layout="wide")
apply_custom_css()

if not is_authenticated():
    st.error("🔒 Please login first"); st.stop()

def generate_qr_base64(text: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=8, border=3)
    qr.add_data(text); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO(); img.save(buf)
    return base64.b64encode(buf.getvalue()).decode()

def fetch_equipment(filters=None):
    token = get_token()
    data = api_client.get_equipment_list(token, filters or {})
    return data if isinstance(data, list) else []

def normalize_rows(items):
    # Convert backend fields to nicer labels for UI/table
    rows = []
    for e in items:
        rows.append({
            "ID": e.get("id"),
            "Name": e.get("name"),
            "Type": str(e.get("type","")).capitalize(),
            "Status": str(e.get("status","")).replace("_"," ").title(),
            "Location": e.get("current_location"),
            "Hours Used": e.get("hours_used"),
            "Daily Rate": e.get("rental_rate_per_day"),
            "Updated": e.get("updated_at")
        })
    return rows

def main():
    user = get_current_user()

    # Header
    c1, c2 = st.columns([3,1])
    with c1:
        st.markdown("""
        <div class="dashboard-header">
          <h1>🏗️ Equipment Management</h1>
          <p>Manage and track your equipment fleet (live from backend)</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout_user(); st.rerun()

    st.markdown("---")

    # Fetch all equipment first
    equipment = fetch_equipment()
    total = len(equipment)
    by_status = {"available":0,"in_use":0,"maintenance":0,"out_of_service":0}
    for e in equipment:
        by_status[str(e.get("status","")).lower()] = by_status.get(str(e.get("status","")).lower(),0)+1

    col1,col2,col3,col4 = st.columns(4)
    with col1: render_metric_card("Total Equipment", f"{total}", "", "🏗️", "#1f77b4")
    with col2: render_metric_card("Available", f"{by_status.get('available',0)}", "", "✅", "#2ca02c")
    with col3: render_metric_card("In Use", f"{by_status.get('in_use',0)}", "", "📋", "#ff7f0e")
    with col4: render_metric_card("Maintenance", f"{by_status.get('maintenance',0)}", "", "🔧", "#d62728")

    st.markdown("<br>", unsafe_allow_html=True)

    tab_list, tab_details = st.tabs(["📋 Equipment List", "🔍 Equipment Details"])

    with tab_list:
        # Filters mapped to backend Enums
        types = sorted({str(e.get("type","")).lower() for e in equipment if e.get("type")})
        statuses = ["available","in_use","maintenance","out_of_service"]
        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            type_sel = st.selectbox("Type", ["(all)"] + types)
        with colf2:
            status_sel = st.selectbox("Status", ["(all)"] + statuses)
        with colf3:
            name_query = st.text_input("Search name/ID")

        params = {}
        if type_sel != "(all)":
            params["equipment_type"] = type_sel  # FastAPI expects enum string (lowercase)
        if status_sel != "(all)":
            params["status"] = status_sel

        items = fetch_equipment(params) if (params) else equipment

        if name_query:
            q = name_query.lower()
            items = [e for e in items if q in (e.get("name","").lower()+e.get("id","").lower())]

        st.caption(f"Showing {len(items)} of {len(equipment)}")
        rows = normalize_rows(items)
        st.dataframe(rows, use_container_width=True, hide_index=True)

        # Card grid
        if items:
            for i in range(0, len(items), 3):
                cols = st.columns(3)
                for j, e in enumerate(items[i:i+3]):
                    if j < len(cols):
                        with cols[j]:
                            render_equipment_card(
                                e.get("id"),
                                str(e.get("type","")).capitalize(),
                                str(e.get("status","")).replace("_"," ").title(),
                                e.get("current_location",""),
                                e.get("updated_at",""),
                            )
        else:
            st.info("No equipment found with current filters.")

    with tab_details:
        if not equipment:
            st.info("No equipment yet."); return
        ids = [e.get("id") for e in equipment]
        chosen = st.selectbox("Select Equipment", ids)
        e = next((x for x in equipment if x.get("id")==chosen), None)
        if not e:
            st.warning("Not found"); return

        c1,c2 = st.columns([2,1])
        with c1:
            st.subheader(f"{e.get('name','(unnamed)')} • {e.get('id')}")
            st.write(f"**Type:** {e.get('type')}")
            st.write(f"**Status:** {e.get('status')}")
            st.write(f"**Location:** {e.get('current_location')}")
            st.write(f"**Hours Used:** {e.get('hours_used')}")
            st.write(f"**Daily Rate:** {e.get('rental_rate_per_day')}")
            st.write(f"**Updated:** {e.get('updated_at')}")
        with c2:
            st.markdown("#### QR Code")
            qr_b64 = generate_qr_base64(f"https://smartrental/equipment/{e.get('id')}")
            st.markdown(f'<img src="data:image/png;base64,{qr_b64}" width="150">', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

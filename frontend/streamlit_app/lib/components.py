# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go

# def render_metric_card(title, value, delta, icon, color="#1f77b4"):
#     """Render a styled metric card"""
    
#     delta_color = "normal"
#     if delta.startswith("+"):
#         delta_color = "normal"
#     elif delta.startswith("-"):
#         delta_color = "inverse"
    
#     st.markdown(f"""
#     <div class="metric-card" style="border-left: 4px solid {color};">
#         <div class="metric-header">
#             <span class="metric-icon">{icon}</span>
#             <span class="metric-title">{title}</span>
#         </div>
#         <div class="metric-value">{value}</div>
#         <div class="metric-delta" style="color: {'#28a745' if delta_color == 'normal' and delta.startswith('+') else '#dc3545' if delta_color == 'inverse' or delta.startswith('-') else '#6c757d'};">
#             {delta}
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# def render_equipment_card(equipment_id, equipment_type, status, location, last_update):
#     """Render an equipment card"""
    
#     status_colors = {
#         'Available': '#28a745',
#         'Rented': '#ffc107', 
#         'Maintenance': '#dc3545',
#         'Reserved': '#6f42c1'
#     }
    
#     status_color = status_colors.get(status, '#6c757d')
    
#     st.markdown(f"""
#     <div class="equipment-card">
#         <div class="equipment-header">
#             <h4>{equipment_id}</h4>
#             <span class="equipment-status" style="background-color: {status_color};">{status}</span>
#         </div>
#         <div class="equipment-details">
#             <p><strong>Type:</strong> {equipment_type}</p>
#             <p><strong>Location:</strong> {location}</p>
#             <p><strong>Last Update:</strong> {last_update}</p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# def render_alert_card(title, message, priority, icon):
#     """Render an alert notification card"""
    
#     priority_colors = {
#         'High Priority': '#dc3545',
#         'Medium Priority': '#ffc107', 
#         'Low Priority': '#28a745'
#     }
    
#     color = priority_colors.get(priority, '#6c757d')
    
#     st.markdown(f"""
#     <div class="alert-card" style="border-left: 4px solid {color};">
#         <div class="alert-header">
#             <span class="alert-icon">{icon}</span>
#             <span class="alert-title">{title}</span>
#             <span class="alert-priority" style="background-color: {color};">{priority}</span>
#         </div>
#         <div class="alert-message">{message}</div>
#     </div>
#     """, unsafe_allow_html=True)

# def render_equipment_status_chart(equipment_data):
#     """Render equipment status distribution chart"""
    
#     status_counts = equipment_data['Status'].value_counts()
    
#     colors = ['#28a745', '#ffc107', '#dc3545', '#6f42c1']
    
#     fig = go.Figure(data=[go.Pie(
#         labels=status_counts.index,
#         values=status_counts.values,
#         hole=.3,
#         marker_colors=colors
#     )])
    
#     fig.update_layout(
#         title="Equipment Status Distribution",
#         showlegend=True,
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#         height=400
#     )
    
#     return fig

# def render_utilization_gauge(utilization_rate):
#     """Render utilization rate as a gauge chart"""
    
#     fig = go.Figure(go.Indicator(
#         mode = "gauge+number+delta",
#         value = utilization_rate,
#         domain = {'x': [0, 1], 'y': [0, 1]},
#         title = {'text': "Fleet Utilization Rate"},
#         delta = {'reference': 80},
#         gauge = {
#             'axis': {'range': [None, 100]},
#             'bar': {'color': "darkblue"},
#             'steps': [
#                 {'range': [0, 50], 'color': "lightgray"},
#                 {'range': [50, 80], 'color': "gray"}
#             ],
#             'threshold': {
#                 'line': {'color': "red", 'width': 4},
#                 'thickness': 0.75,
#                 'value': 90
#             }
#         }
#     ))
    
#     fig.update_layout(height=300)
#     return fig

# def render_revenue_trend_chart(analytics_data):
#     """Render revenue trend chart"""
    
#     fig = px.area(
#         analytics_data,
#         x='Date',
#         y='Revenue', 
#         title="Revenue Trend (Last 30 Days)",
#         color_discrete_sequence=['#1f77b4']
#     )
    
#     fig.update_traces(fill='tonexty', fillcolor='rgba(31, 119, 180, 0.2)')
#     fig.update_layout(
#         showlegend=False,
#         height=400,
#         xaxis_title="Date",
#         yaxis_title="Revenue ($)"
#     )
    
#     return fig

# def render_equipment_location_map(equipment_data):
#     """Render equipment location distribution"""
    
#     location_summary = equipment_data.groupby('Location').size().reset_index(name='Count')
    
#     fig = px.bar(
#         location_summary,
#         x='Location',
#         y='Count',
#         title="Equipment Distribution by Location",
#         color='Count',
#         color_continuous_scale='Blues'
#     )
    
#     fig.update_layout(
#         showlegend=False,
#         height=400,
#         xaxis_title="Location",
#         yaxis_title="Number of Equipment"
#     )
    
#     return fig

# def render_maintenance_schedule_chart(maintenance_data):
#     """Render maintenance schedule timeline"""
    
#     fig = px.timeline(
#         maintenance_data,
#         x_start="Start Date",
#         x_end="End Date", 
#         y="Equipment ID",
#         color="Type",
#         title="Upcoming Maintenance Schedule"
#     )
    
#     fig.update_layout(height=400)
#     return fig

# def render_demand_forecast_chart(forecast_data):
#     """Render demand forecasting chart"""
    
#     fig = px.line(
#         forecast_data,
#         x='Date',
#         y='Predicted Demand',
#         color='Equipment Type',
#         title="Equipment Demand Forecast (Next 30 Days)",
#         line_shape='spline'
#     )
    
#     fig.update_layout(
#         height=500,
#         showlegend=True,
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#         xaxis_title="Date",
#         yaxis_title="Predicted Demand"
#     )
    
#     return fig

# def render_performance_radar_chart(equipment_data):
#     """Render equipment performance radar chart"""
    
#     # Calculate performance metrics
#     metrics = {
#         'Utilization': 85,
#         'Efficiency': 78,
#         'Reliability': 92,
#         'Cost Effectiveness': 88,
#         'Customer Satisfaction': 91
#     }
    
#     categories = list(metrics.keys())
#     values = list(metrics.values())
    
#     fig = go.Figure()
    
#     fig.add_trace(go.Scatterpolar(
#         r=values,
#         theta=categories,
#         fill='toself',
#         name='Fleet Performance'
#     ))
    
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 100]
#             )),
#         title="Fleet Performance Overview",
#         showlegend=False,
#         height=400
#     )
    
#     return fig

# def render_status_timeline(equipment_id, status_history):
#     """Render equipment status timeline"""
    
#     fig = px.timeline(
#         status_history,
#         x_start="Start",
#         x_end="End",
#         y="Status", 
#         color="Status",
#         title=f"Status Timeline - {equipment_id}"
#     )
    
#     fig.update_layout(height=300)
#     return fig

# def render_fuel_consumption_chart(equipment_data):
#     """Render fuel consumption analysis"""
    
#     # Sample fuel consumption data
#     fuel_data = equipment_data.nlargest(10, 'Engine Hours')[['Equipment ID', 'Engine Hours']]
#     fuel_data['Fuel Consumption'] = fuel_data['Engine Hours'] * 0.8 + (fuel_data['Engine Hours'] * 0.1).apply(lambda x: x * (1 + (hash(str(x)) % 100 - 50) / 500))
    
#     fig = px.scatter(
#         fuel_data,
#         x='Engine Hours',
#         y='Fuel Consumption',
#         hover_data=['Equipment ID'],
#         title="Fuel Consumption vs Engine Hours",
#         trendline="ols"
#     )
    
#     fig.update_layout(
#         height=400,
#         xaxis_title="Engine Hours",
#         yaxis_title="Fuel Consumption (L)"
#     )
    
#     return fig

# def render_idle_time_analysis(equipment_data):
#     """Render idle time analysis chart"""
    
#     idle_data = equipment_data[equipment_data['Idle Hours'] > 0].nlargest(10, 'Idle Hours')
    
#     fig = px.bar(
#         idle_data,
#         x='Equipment ID',
#         y='Idle Hours',
#         color='Type',
#         title="Equipment with Highest Idle Time",
#         hover_data=['Location', 'Status']
#     )
    
#     fig.update_layout(
#         height=400,
#         xaxis_title="Equipment ID",
#         yaxis_title="Idle Hours"
#     )
    
#     return fig

# def render_notification_panel():
#     """Render notification panel"""
    
#     notifications = [
#         {"type": "info", "message": "Equipment EX1001 returned successfully", "time": "5 min ago"},
#         {"type": "warning", "message": "Maintenance due for CR2002 in 2 days", "time": "1 hour ago"},
#         {"type": "error", "message": "BD3003 is 3 days overdue", "time": "2 hours ago"},
#         {"type": "success", "message": "New equipment LD4010 added to fleet", "time": "1 day ago"}
#     ]
    
#     st.markdown("### 🔔 Recent Notifications")
    
#     for notif in notifications:
#         if notif["type"] == "info":
#             st.info(f"{notif['message']} - {notif['time']}")
#         elif notif["type"] == "warning":
#             st.warning(f"{notif['message']} - {notif['time']}")
#         elif notif["type"] == "error":
#             st.error(f"{notif['message']} - {notif['time']}")
#         elif notif["type"] == "success":
#             st.success(f"{notif['message']} - {notif['time']}")

# def render_quick_stats_grid(stats_data):
#     """Render quick stats grid"""
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.metric(
#             "Today's Rentals", 
#             stats_data.get('todays_rentals', 12),
#             delta=stats_data.get('rentals_delta', '+3')
#         )
    
#     with col2:
#         st.metric(
#             "Returns Due", 
#             stats_data.get('returns_due', 8),
#             delta=stats_data.get('returns_delta', '-2')
#         )
    
#     with col3:
#         st.metric(
#             "Maintenance Alert", 
#             stats_data.get('maintenance_alerts', 3),
#             delta=stats_data.get('maintenance_delta', '+1')
#         )
    
#     with col4:
#         st.metric(
#             "Fleet Efficiency", 
#             f"{stats_data.get('efficiency', 87.5)}%",
#             delta=stats_data.get('efficiency_delta', '+2.1%')
#         )


import streamlit as st
from textwrap import dedent
import plotly.express as px
import plotly.graph_objects as go

def _render_html(html: str):
    """Safely render raw HTML without Markdown turning it into a code block."""
    html = dedent(html).strip()
    # Streamlit >= 1.32 has st.html(); older versions fall back to markdown
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)

def render_metric_card(title, value, delta, icon, color="#1f77b4"):
    """Render a styled metric card without stray </div> appearing."""
    # Determine delta color
    delta_color = (
        "#28a745" if str(delta).strip().startswith("+")
        else "#dc3545" if str(delta).strip().startswith("-")
        else "#6c757d"
    )

    _render_html(f"""
<div class="metric-card" style="border-left: 4px solid {color};">
  <div class="metric-header">
    <span class="metric-icon">{icon}</span>
    <span class="metric-title">{title}</span>
  </div>
  <div class="metric-value">{value}</div>
  <div class="metric-delta" style="color: {delta_color};">{delta}</div>
</div>
""")

def render_equipment_card(equipment_id, equipment_type, status, location, last_update):
    """Render an equipment card."""
    status_colors = {
        'Available': '#28a745',
        'Rented': '#ffc107',
        'Maintenance': '#dc3545',
        'Reserved': '#6f42c1'
    }
    status_color = status_colors.get(status, '#6c757d')

    _render_html(f"""
<div class="equipment-card">
  <div class="equipment-header">
    <h4>{equipment_id}</h4>
    <span class="equipment-status" style="background-color: {status_color};">{status}</span>
  </div>
  <div class="equipment-details">
    <p><strong>Type:</strong> {equipment_type}</p>
    <p><strong>Location:</strong> {location}</p>
    <p><strong>Last Update:</strong> {last_update}</p>
  </div>
</div>
""")

def render_alert_card(title, message, priority, icon):
    """Render an alert notification card."""
    priority_colors = {
        'High Priority': '#dc3545',
        'Medium Priority': '#ffc107',
        'Low Priority': '#28a745'
    }
    color = priority_colors.get(priority, '#6c757d')

    _render_html(f"""
<div class="alert-card" style="border-left: 4px solid {color};">
  <div class="alert-header">
    <span class="alert-icon">{icon}</span>
    <span class="alert-title">{title}</span>
    <span class="alert-priority" style="background-color: {color};">{priority}</span>
  </div>
  <div class="alert-message">{message}</div>
</div>
""")

# ---- the rest of your plotting helpers below are unchanged ----
def render_equipment_status_chart(equipment_data):
    status_counts = equipment_data['Status'].value_counts()
    colors = ['#28a745', '#ffc107', '#dc3545', '#6f42c1']
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=.3,
        marker_colors=colors
    )])
    fig.update_layout(
        title="Equipment Status Distribution",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    return fig

def render_utilization_gauge(utilization_rate):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = utilization_rate,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Fleet Utilization Rate"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig.update_layout(height=300)
    return fig

def render_revenue_trend_chart(analytics_data):
    fig = px.area(analytics_data, x='Date', y='Revenue',
                  title="Revenue Trend (Last 30 Days)",
                  color_discrete_sequence=['#1f77b4'])
    fig.update_traces(fill='tonexty', fillcolor='rgba(31, 119, 180, 0.2)')
    fig.update_layout(showlegend=False, height=400, xaxis_title="Date", yaxis_title="Revenue ($)")
    return fig

# ... keep the rest of your chart functions as-is ...

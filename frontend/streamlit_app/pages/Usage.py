# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import numpy as np
# from lib.state import is_authenticated, get_current_user, logout_user
# from lib.data import get_sample_equipment_data, get_usage_analytics_data
# from lib.components import render_metric_card, render_utilization_gauge, render_performance_radar_chart
# from lib.styles import apply_custom_css, format_currency, format_hours

# st.set_page_config(
#     page_title="Usage Analytics",
#     page_icon="📊",
#     layout="wide"
# )

# # Apply custom CSS
# apply_custom_css()

# # Check authentication
# if not is_authenticated():
#     st.error("🔒 Please login first")
#     st.stop()

# def calculate_efficiency_metrics(equipment_data):
#     """Calculate equipment efficiency metrics"""
    
#     metrics = {}
    
#     # Overall fleet utilization
#     total_equipment = len(equipment_data)
#     rented_equipment = len(equipment_data[equipment_data['Status'] == 'Rented'])
#     metrics['utilization_rate'] = (rented_equipment / total_equipment) * 100
    
#     # Average engine hours
#     metrics['avg_engine_hours'] = equipment_data['Engine Hours'].mean()
    
#     # Efficiency ratio (engine hours / total hours)
#     equipment_data['Efficiency'] = (equipment_data['Engine Hours'] / 
#                                    equipment_data['Total Hours']) * 100
#     metrics['avg_efficiency'] = equipment_data['Efficiency'].mean()
    
#     # Idle time analysis
#     metrics['avg_idle_hours'] = equipment_data['Idle Hours'].mean()
#     metrics['high_idle_count'] = len(equipment_data[equipment_data['Idle Hours'] > 100])
    
#     # Revenue calculations (estimated)
#     hourly_rate = 85  # Average hourly rate
#     daily_revenue = rented_equipment * hourly_rate * 8  # 8 hours per day
#     metrics['estimated_daily_revenue'] = daily_revenue
#     metrics['monthly_projection'] = daily_revenue * 30
    
#     return metrics

# def render_usage_trends(analytics_data):
#     """Render usage trend charts"""
    
#     st.markdown("### 📈 Usage Trends Analysis")
    
#     # Time period selector
#     col1, col2 = st.columns([1, 3])
#     with col1:
#         time_range = st.selectbox("Time Range", 
#                                 ["Last 7 days", "Last 30 days", "Last 3 months"])
    
#     # Main trend charts
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Usage hours trend
#         fig_usage = px.line(analytics_data, x='Date', y='Usage Hours',
#                            title="Daily Equipment Usage Hours",
#                            color_discrete_sequence=['#1f77b4'])
        
#         fig_usage.add_hline(y=analytics_data['Usage Hours'].mean(), 
#                            line_dash="dash", line_color="red",
#                            annotation_text=f"Avg: {analytics_data['Usage Hours'].mean():.0f} hrs")
        
#         fig_usage.update_layout(showlegend=False, height=400)
#         st.plotly_chart(fig_usage, use_container_width=True)
    
#     with col2:
#         # Revenue trend
#         fig_revenue = px.area(analytics_data, x='Date', y='Revenue',
#                              title="Daily Revenue Trend",
#                              color_discrete_sequence=['#2ca02c'])
        
#         fig_revenue.update_traces(fill='tonexty', fillcolor='rgba(44, 160, 44, 0.2)')
#         fig_revenue.update_layout(showlegend=False, height=400)
#         st.plotly_chart(fig_revenue, use_container_width=True)
    
#     # Utilization trend
#     fig_utilization = px.line(analytics_data, x='Date', y='Utilization Rate',
#                              title="Fleet Utilization Rate Trend",
#                              color_discrete_sequence=['#ff7f0e'])
    
#     fig_utilization.update_layout(yaxis=dict(range=[0, 100]))
#     fig_utilization.add_hline(y=80, line_dash="dash", line_color="green",
#                              annotation_text="Target: 80%")
#     fig_utilization.update_layout(showlegend=False, height=400)
#     st.plotly_chart(fig_utilization, use_container_width=True)

# def render_equipment_performance(equipment_data):
#     """Render equipment performance analysis"""
    
#     st.markdown("### 🏆 Equipment Performance Analysis")
    
#     # Performance categories
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Top performers
#         st.markdown("#### Top Performing Equipment")
        
#         equipment_data['Performance Score'] = (
#             (equipment_data['Engine Hours'] / equipment_data['Engine Hours'].max()) * 40 +
#             ((equipment_data['Total Hours'] - equipment_data['Idle Hours']) / 
#              equipment_data['Total Hours']) * 30 +
#             (equipment_data['Operational Days'] / equipment_data['Operational Days'].max()) * 30
#         )
        
#         top_performers = equipment_data.nlargest(10, 'Performance Score')[
#             ['Equipment ID', 'Type', 'Performance Score', 'Engine Hours', 'Status']
#         ]
        
#         for _, equipment in top_performers.iterrows():
#             score = equipment['Performance Score']
#             color = '#28a745' if score >= 80 else '#ffc107' if score >= 60 else '#dc3545'
            
#             st.markdown(f"""
#             <div style="border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; 
#                         background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
#                 <strong>{equipment['Equipment ID']}</strong> - {equipment['Type']}<br>
#                 <span style="color: {color}; font-weight: bold;">Score: {score:.1f}/100</span><br>
#                 <small>Engine Hours: {equipment['Engine Hours']:,} | Status: {equipment['Status']}</small>
#             </div>
#             """, unsafe_allow_html=True)
    
#     with col2:
#         # Underperforming equipment
#         st.markdown("#### Attention Required")
        
#         underperformers = equipment_data.nsmallest(10, 'Performance Score')[
#             ['Equipment ID', 'Type', 'Performance Score', 'Idle Hours', 'Status']
#         ]
        
#         for _, equipment in underperformers.iterrows():
#             score = equipment['Performance Score']
            
#             st.markdown(f"""
#             <div style="border-left: 4px solid #dc3545; padding: 1rem; margin: 0.5rem 0; 
#                         background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
#                 <strong>{equipment['Equipment ID']}</strong> - {equipment['Type']}<br>
#                 <span style="color: #dc3545; font-weight: bold;">Score: {score:.1f}/100</span><br>
#                 <small>Idle Hours: {equipment['Idle Hours']:,} | Status: {equipment['Status']}</small>
#             </div>
#             """, unsafe_allow_html=True)
    
#     # Performance distribution chart
#     st.markdown("#### Performance Distribution")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Performance score histogram
#         fig_perf = px.histogram(equipment_data, x='Performance Score',
#                                title="Performance Score Distribution",
#                                nbins=20, color_discrete_sequence=['#1f77b4'])
#         fig_perf.update_layout(showlegend=False, height=400)
#         st.plotly_chart(fig_perf, use_container_width=True)
    
#     with col2:
#         # Engine hours vs Idle hours scatter
#         fig_scatter = px.scatter(equipment_data, x='Engine Hours', y='Idle Hours',
#                                 color='Type', size='Total Hours',
#                                 title="Engine Hours vs Idle Hours",
#                                 hover_data=['Equipment ID'])
#         fig_scatter.update_layout(height=400)
#         st.plotly_chart(fig_scatter, use_container_width=True)

# def render_location_analysis(equipment_data):
#     """Render location-based usage analysis"""
    
#     st.markdown("### 📍 Location-based Usage Analysis")
    
#     location_stats = equipment_data.groupby('Location').agg({
#         'Equipment ID': 'count',
#         'Engine Hours': ['mean', 'sum'],
#         'Idle Hours': 'sum',
#         'Total Hours': 'sum'
#     }).round(2)
    
#     location_stats.columns = ['Equipment Count', 'Avg Engine Hours', 
#                              'Total Engine Hours', 'Total Idle Hours', 'Total Hours']
    
#     location_stats['Utilization %'] = ((location_stats['Total Engine Hours'] / 
#                                        location_stats['Total Hours']) * 100).round(1)
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Location utilization chart
#         fig_loc_util = px.bar(location_stats.reset_index(), 
#                              x='Location', y='Utilization %',
#                              title="Utilization Rate by Location",
#                              color='Utilization %',
#                              color_continuous_scale='RdYlGn')
#         fig_loc_util.update_layout(height=400)
#         st.plotly_chart(fig_loc_util, use_container_width=True)
    
#     with col2:
#         # Equipment distribution by location
#         fig_loc_dist = px.pie(location_stats.reset_index(), 
#                              values='Equipment Count', names='Location',
#                              title="Equipment Distribution by Location")
#         st.plotly_chart(fig_loc_dist, use_container_width=True)
    
#     # Location performance table
#     st.markdown("#### Location Performance Summary")
#     st.dataframe(location_stats, use_container_width=True)

# def render_financial_analysis(equipment_data, analytics_data):
#     """Render financial performance analysis"""
    
#     st.markdown("### 💰 Financial Performance Analysis")
    
#     # Revenue calculations
#     hourly_rates = {
#         'Excavator': 95,
#         'Crane': 120,
#         'Bulldozer': 85,
#         'Grader': 75,
#         'Loader': 80,
#         'Compactor': 65,
#         'Forklift': 45
#     }
    
#     # Calculate equipment revenue
#     equipment_data['Hourly Rate'] = equipment_data['Type'].map(hourly_rates)
#     equipment_data['Estimated Revenue'] = (equipment_data['Engine Hours'] * 
#                                           equipment_data['Hourly Rate'])
    
#     # Financial metrics
#     total_revenue = equipment_data['Estimated Revenue'].sum()
#     avg_revenue_per_unit = equipment_data['Estimated Revenue'].mean()
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         render_metric_card("Total Revenue", format_currency(total_revenue), 
#                           "+15.3%", "💰", "#2ca02c")
    
#     with col2:
#         render_metric_card("Avg Revenue/Unit", format_currency(avg_revenue_per_unit),
#                           "+8.7%", "📊", "#1f77b4")
    
#     with col3:
#         monthly_projection = analytics_data['Revenue'].sum()
#         render_metric_card("Monthly Total", format_currency(monthly_projection),
#                           "+12.4%", "📈", "#ff7f0e")
    
#     with col4:
#         roi_percentage = 23.4  # Simulated ROI
#         render_metric_card("ROI", f"{roi_percentage}%", "+2.1%", "📊", "#9467bd")
    
#     # Revenue breakdown charts
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Revenue by equipment type
#         revenue_by_type = equipment_data.groupby('Type')['Estimated Revenue'].sum().sort_values(ascending=False)
        
#         fig_rev_type = px.bar(x=revenue_by_type.index, y=revenue_by_type.values,
#                              title="Revenue by Equipment Type",
#                              color=revenue_by_type.values,
#                              color_continuous_scale='Blues')
#         fig_rev_type.update_layout(showlegend=False, height=400)
#         st.plotly_chart(fig_rev_type, use_container_width=True)
    
#     with col2:
#         # Revenue trend over time
#         fig_rev_trend = px.area(analytics_data, x='Date', y='Revenue',
#                                title="Revenue Trend Analysis")
#         fig_rev_trend.update_traces(fill='tonexty', fillcolor='rgba(44, 160, 44, 0.2)')
#         fig_rev_trend.update_layout(showlegend=False, height=400)
#         st.plotly_chart(fig_rev_trend, use_container_width=True)
    
#     # Top revenue generating equipment
#     st.markdown("#### Top Revenue Generators")
#     top_revenue = equipment_data.nlargest(10, 'Estimated Revenue')[
#         ['Equipment ID', 'Type', 'Engine Hours', 'Hourly Rate', 'Estimated Revenue', 'Status']
#     ]
    
#     # Format the revenue column
#     top_revenue['Estimated Revenue'] = top_revenue['Estimated Revenue'].apply(format_currency)
#     st.dataframe(top_revenue, use_container_width=True, hide_index=True)

# def main():
#     user = get_current_user()
    
#     # Header
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.markdown("""
#         <div class="dashboard-header">
#             <h1>📊 Usage Analytics & Insights</h1>
#             <p>Comprehensive equipment usage analysis and performance metrics</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         if st.button("🚪 Logout", type="secondary", use_container_width=True):
#             logout_user()
#             st.rerun()
    
#     st.markdown("---")
    
#     # Load data
#     equipment_data = get_sample_equipment_data()
#     analytics_data = get_usage_analytics_data()
#     efficiency_metrics = calculate_efficiency_metrics(equipment_data)
    
#     # Key Metrics Row
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         render_metric_card("Fleet Utilization", f"{efficiency_metrics['utilization_rate']:.1f}%", 
#                           "+2.3%", "📊", "#1f77b4")
    
#     with col2:
#         render_metric_card("Avg Efficiency", f"{efficiency_metrics['avg_efficiency']:.1f}%",
#                           "+1.8%", "⚡", "#2ca02c")
    
#     with col3:
#         render_metric_card("Daily Revenue", format_currency(efficiency_metrics['estimated_daily_revenue']),
#                           "+12.5%", "💰", "#ff7f0e")
    
#     with col4:
#         render_metric_card("High Idle Alert", f"{efficiency_metrics['high_idle_count']}", 
#                           "-2", "⚠️", "#d62728")
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Main analytics tabs
#     tab1, tab2, tab3, tab4, tab5 = st.tabs([
#         "📈 Usage Trends", "🏆 Performance", "📍 Location Analysis", 
#         "💰 Financial", "📋 Summary Report"
#     ])
    
#     with tab1:
#         render_usage_trends(analytics_data)
        
#         # Additional usage insights
#         st.markdown("---")
#         st.markdown("### 🔍 Usage Insights")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             st.markdown("#### Peak Usage Hours")
            
#             # Simulate hourly usage data
#             hours = list(range(24))
#             usage_by_hour = [30 + 20*np.sin((h-8)*np.pi/12) + np.random.randint(-5,5) for h in hours]
#             usage_by_hour = [max(0, u) for u in usage_by_hour]  # Ensure non-negative
            
#             hourly_df = pd.DataFrame({
#                 'Hour': hours,
#                 'Usage': usage_by_hour
#             })
            
#             fig_hourly = px.bar(hourly_df, x='Hour', y='Usage',
#                                title="Equipment Usage by Hour of Day",
#                                color='Usage', color_continuous_scale='Blues')
#             fig_hourly.update_layout(showlegend=False, height=350)
#             st.plotly_chart(fig_hourly, use_container_width=True)
        
#         with col2:
#             st.markdown("#### Weekly Patterns")
            
#             days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#             weekly_usage = [85, 92, 88, 90, 87, 45, 32]  # Higher on weekdays
            
#             weekly_df = pd.DataFrame({
#                 'Day': days,
#                 'Usage %': weekly_usage
#             })
            
#             fig_weekly = px.line(weekly_df, x='Day', y='Usage %',
#                                title="Weekly Usage Pattern",
#                                markers=True, color_discrete_sequence=['#ff7f0e'])
#             fig_weekly.update_layout(showlegend=False, height=350)
#             st.plotly_chart(fig_weekly, use_container_width=True)
        
#         with col3:
#             st.markdown("#### Equipment Type Usage")
            
#             type_usage = equipment_data.groupby('Type')['Engine Hours'].sum().sort_values(ascending=True)
            
#             fig_type_usage = px.bar(y=type_usage.index, x=type_usage.values,
#                                    orientation='h', title="Total Hours by Equipment Type",
#                                    color=type_usage.values, color_continuous_scale='Greens')
#             fig_type_usage.update_layout(showlegend=False, height=350)
#             st.plotly_chart(fig_type_usage, use_container_width=True)
    
#     with tab2:
#         render_equipment_performance(equipment_data)
        
#         # Additional performance metrics
#         st.markdown("---")
#         st.markdown("### 📊 Efficiency Benchmarks")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Utilization gauge
#             util_gauge = render_utilization_gauge(efficiency_metrics['utilization_rate'])
#             st.plotly_chart(util_gauge, use_container_width=True)
        
#         with col2:
#             # Performance radar chart
#             radar_chart = render_performance_radar_chart(equipment_data)
#             st.plotly_chart(radar_chart, use_container_width=True)
        
#         # Efficiency recommendations
#         st.markdown("#### 💡 Efficiency Recommendations")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.success("**Optimization Opportunities:**")
#             st.write("• Redistribute idle equipment from Site B to Site A")
#             st.write("• Schedule maintenance during low-demand periods")
#             st.write("• Consider selling underperforming assets")
#             st.write("• Implement predictive maintenance program")
        
#         with col2:
#             st.info("**Performance Targets:**")
#             st.write(f"• Current Utilization: {efficiency_metrics['utilization_rate']:.1f}% | Target: 85%")
#             st.write(f"• Average Efficiency: {efficiency_metrics['avg_efficiency']:.1f}% | Target: 90%")
#             st.write(f"• Idle Equipment: {efficiency_metrics['high_idle_count']} | Target: <5")
#             st.write("• Monthly Revenue Growth: Target +15%")
    
#     with tab3:
#         render_location_analysis(equipment_data)
        
#         # Location-specific insights
#         st.markdown("---")
#         st.markdown("### 🗺️ Location Insights")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("#### Site Performance Ranking")
            
#             location_performance = equipment_data.groupby('Location').agg({
#                 'Engine Hours': 'sum',
#                 'Total Hours': 'sum',
#                 'Equipment ID': 'count'
#             })
            
#             location_performance['Efficiency'] = (
#                 location_performance['Engine Hours'] / location_performance['Total Hours'] * 100
#             ).round(1)
            
#             location_performance = location_performance.sort_values('Efficiency', ascending=False)
            
#             for idx, (location, data) in enumerate(location_performance.iterrows(), 1):
#                 color = '#28a745' if idx <= 2 else '#ffc107' if idx <= 3 else '#dc3545'
#                 st.markdown(f"""
#                 <div style="border-left: 4px solid {color}; padding: 0.8rem; margin: 0.5rem 0; 
#                            background: white; border-radius: 8px;">
#                     <strong>#{idx} {location}</strong><br>
#                     <small>Efficiency: {data['Efficiency']:.1f}% | Equipment: {data['Equipment ID']} units</small>
#                 </div>
#                 """, unsafe_allow_html=True)
        
#         with col2:
#             st.markdown("#### Location Recommendations")
#             st.warning("**Site B - Industrial:** High idle time detected. Consider equipment reallocation.")
#             st.info("**Site A - Downtown:** Peak performance. Consider expanding operations.")
#             st.success("**Site C - Airport:** Optimal utilization. Maintain current strategy.")
#             st.error("**Warehouse:** Low activity. Review storage and deployment strategy.")
    
#     with tab4:
#         render_financial_analysis(equipment_data, analytics_data)
        
#         # Financial projections
#         st.markdown("---")
#         st.markdown("### 📈 Financial Projections")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Monthly revenue projection
#             months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
#             projected_revenue = [120000, 125000, 135000, 142000, 148000, 155000]
            
#             projection_df = pd.DataFrame({
#                 'Month': months,
#                 'Projected Revenue': projected_revenue
#             })
            
#             fig_projection = px.line(projection_df, x='Month', y='Projected Revenue',
#                                    title="6-Month Revenue Projection",
#                                    markers=True, color_discrete_sequence=['#2ca02c'])
#             fig_projection.update_layout(showlegend=False, height=400)
#             st.plotly_chart(fig_projection, use_container_width=True)
        
#         with col2:
#             # Cost breakdown
#             costs = {
#                 'Maintenance': 25000,
#                 'Fuel': 18000,
#                 'Insurance': 12000,
#                 'Storage': 8000,
#                 'Labor': 35000
#             }
            
#             cost_df = pd.DataFrame(list(costs.items()), columns=['Category', 'Amount'])
            
#             fig_costs = px.pie(cost_df, values='Amount', names='Category',
#                               title="Monthly Cost Breakdown")
#             st.plotly_chart(fig_costs, use_container_width=True)
        
#         # Profitability analysis
#         st.markdown("#### 💼 Profitability Analysis")
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             gross_revenue = 155000
#             st.metric("Gross Revenue", format_currency(gross_revenue), "+12%")
        
#         with col2:
#             total_costs = sum(costs.values())
#             st.metric("Operating Costs", format_currency(total_costs), "+5%")
        
#         with col3:
#             net_profit = gross_revenue - total_costs
#             st.metric("Net Profit", format_currency(net_profit), "+18%")
        
#         with col4:
#             profit_margin = (net_profit / gross_revenue) * 100
#             st.metric("Profit Margin", f"{profit_margin:.1f}%", "+2.5%")
    
#     with tab5:
#         st.markdown("### 📋 Executive Summary Report")
        
#         # Key findings section
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("#### 🎯 Key Findings")
            
#             st.success("**Strengths:**")
#             st.write(f"• Fleet utilization at {efficiency_metrics['utilization_rate']:.1f}% - above industry average")
#             st.write("• Strong revenue growth trend (+15.3% month-over-month)")
#             st.write("• High-performing equipment generating consistent returns")
#             st.write("• Effective maintenance scheduling reducing downtime")
            
#             st.warning("**Areas for Improvement:**")
#             st.write(f"• {efficiency_metrics['high_idle_count']} equipment units with high idle time")
#             st.write("• Uneven utilization across locations")
#             st.write("• Opportunity to optimize fuel consumption")
#             st.write("• Need for better demand forecasting")
        
#         with col2:
#             st.markdown("#### 📈 Performance Summary")
            
#             # Create performance summary metrics
#             summary_metrics = {
#                 'Total Equipment': len(equipment_data),
#                 'Active Rentals': len(equipment_data[equipment_data['Status'] == 'Rented']),
#                 'Utilization Rate': f"{efficiency_metrics['utilization_rate']:.1f}%",
#                 'Monthly Revenue': format_currency(efficiency_metrics['monthly_projection']),
#                 'Average Engine Hours': f"{efficiency_metrics['avg_engine_hours']:.0f}",
#                 'Equipment Efficiency': f"{efficiency_metrics['avg_efficiency']:.1f}%"
#             }
            
#             for metric, value in summary_metrics.items():
#                 st.markdown(f"**{metric}:** {value}")
        
#         # Recommendations section
#         st.markdown("---")
#         st.markdown("#### 💡 Strategic Recommendations")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             st.markdown("**Short-term (1-3 months):**")
#             st.write("• Relocate idle equipment from low-demand sites")
#             st.write("• Implement dynamic pricing based on demand")
#             st.write("• Enhance equipment tracking accuracy") 
#             st.write("• Optimize maintenance schedules")
        
#         with col2:
#             st.markdown("**Medium-term (3-12 months):**")
#             st.write("• Invest in predictive analytics platform")
#             st.write("• Expand fleet in high-demand locations")
#             st.write("• Implement IoT sensors for real-time monitoring")
#             st.write("• Develop customer loyalty programs")
        
#         with col3:
#             st.markdown("**Long-term (1+ years):**")
#             st.write("• Consider fleet electrification initiatives")
#             st.write("• Expand into new geographical markets")
#             st.write("• Develop autonomous equipment capabilities")
#             st.write("• Build strategic partnerships")
        
#         # Export report option
#         st.markdown("---")
#         col1, col2, col3 = st.columns([1, 1, 1])
        
#         with col2:
#             if st.button("📄 Export Detailed Report", use_container_width=True, type="primary"):
#                 # Create comprehensive report data
#                 report_data = {
#                     'Equipment Summary': equipment_data.describe(),
#                     'Usage Analytics': analytics_data.describe(),
#                     'Performance Metrics': pd.Series(efficiency_metrics)
#                 }
                
#                 st.success("📧 Detailed analytics report has been generated and will be sent to your email.")
#                 st.info("💾 Report saved to: /reports/usage_analytics_" + datetime.now().strftime('%Y%m%d') + ".pdf")

# if __name__ == "__main__":
#     main()



import streamlit as st
import pandas as pd
from lib.state import is_authenticated, get_current_user, logout_user, get_token
from lib.api import api_client
from lib.components import render_metric_card
from lib.styles import apply_custom_css

st.set_page_config(page_title="Usage Analytics", page_icon="📊", layout="wide")
apply_custom_css()

if not is_authenticated():
    st.error("🔒 Please login first"); st.stop()

def fetch_equipment():
    token = get_token()
    data = api_client.get_equipment_list(token)
    return data if isinstance(data, list) else []

def main():
    user = get_current_user()
    token = get_token()

    c1, c2 = st.columns([3,1])
    with c1:
        st.markdown("""
        <div class="dashboard-header">
          <h1>📊 Usage Analytics</h1>
          <p>Summaries computed from your live equipment data</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout_user(); st.rerun()
    st.markdown("---")

    items = fetch_equipment()
    if not items:
        st.info("No equipment yet. Import some first."); return

    # Make a DF for charts
    df = pd.DataFrame(items)
    df["status"] = df["status"].astype(str)
    df["type"] = df["type"].astype(str)

    total = len(df)
    in_use = (df["status"].str.lower()=="in_use").sum()
    available = (df["status"].str.lower()=="available").sum()
    maint = (df["status"].str.lower()=="maintenance").sum()
    avg_hours = float(df.get("hours_used", pd.Series([0])).mean() or 0)

    m1,m2,m3,m4 = st.columns(4)
    with m1: render_metric_card("Total", str(total), "", "🏗️", "#1f77b4")
    with m2: render_metric_card("In Use", str(in_use), "", "📋", "#ff7f0e")
    with m3: render_metric_card("Available", str(available), "", "✅", "#2ca02c")
    with m4: render_metric_card("Avg Hours Used", f"{avg_hours:.1f}", "", "⏱️", "#9467bd")

    st.markdown("### Status Distribution")
    st.bar_chart(df["status"].value_counts())

    st.markdown("### By Type")
    st.bar_chart(df["type"].value_counts())

    if "hours_used" in df.columns:
        st.markdown("### Hours Used (by Equipment)")
        plot_df = df[["id","hours_used"]].set_index("id")
        st.line_chart(plot_df)

    st.markdown("### Raw Data")
    show_cols = [c for c in ["id","name","type","status","current_location","hours_used","rental_rate_per_day","updated_at"] if c in df.columns]
    st.dataframe(df[show_cols], use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()

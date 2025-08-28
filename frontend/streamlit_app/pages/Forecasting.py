# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import numpy as np
# from lib.state import is_authenticated, get_current_user, logout_user
# from lib.data import get_sample_equipment_data, get_demand_forecast_data, get_usage_analytics_data
# from lib.components import render_metric_card, render_demand_forecast_chart
# from lib.styles import apply_custom_css, format_currency

# st.set_page_config(
#     page_title="Demand Forecasting",
#     page_icon="🔮",
#     layout="wide"
# )

# # Apply custom CSS
# apply_custom_css()

# # Check authentication
# if not is_authenticated():
#     st.error("🔒 Please login first")
#     st.stop()

# def generate_demand_insights(forecast_data, equipment_data):
#     """Generate AI-powered demand insights"""
    
#     insights = {}
    
#     # Calculate demand trends by equipment type
#     type_trends = forecast_data.groupby('Equipment Type')['Predicted Demand'].agg(['mean', 'max', 'min']).round(1)
    
#     # Identify peak demand periods
#     daily_demand = forecast_data.groupby('Date')['Predicted Demand'].sum()
#     peak_demand_date = daily_demand.idxmax()
#     peak_demand_value = daily_demand.max()
    
#     # Current vs predicted demand comparison
#     current_rented = len(equipment_data[equipment_data['Status'] == 'Rented'])
#     avg_predicted = forecast_data['Predicted Demand'].mean()
    
#     insights.update({
#         'peak_demand_date': peak_demand_date,
#         'peak_demand_value': peak_demand_value,
#         'current_vs_predicted': avg_predicted - current_rented,
#         'high_demand_equipment': type_trends['mean'].idxmax(),
#         'demand_variance': forecast_data.groupby('Equipment Type')['Predicted Demand'].std().round(2)
#     })
    
#     return insights

# def render_demand_forecast_overview(forecast_data):
#     """Render demand forecasting overview"""
    
#     st.markdown("### 🔮 Demand Forecast Overview")
    
#     # Time horizon selector
#     col1, col2 = st.columns([1, 3])
#     with col1:
#         forecast_horizon = st.selectbox("Forecast Horizon", 
#                                        ["Next 7 days", "Next 14 days", "Next 30 days"])
    
#     # Main forecast chart
#     fig_forecast = render_demand_forecast_chart(forecast_data)
#     st.plotly_chart(fig_forecast, use_container_width=True)
    
#     # Demand summary by equipment type
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Average demand by type
#         avg_demand = forecast_data.groupby('Equipment Type')['Predicted Demand'].mean().sort_values(ascending=False)
        
#         fig_avg_demand = px.bar(x=avg_demand.values, y=avg_demand.index,
#                                orientation='h', title="Average Predicted Demand by Type",
#                                color=avg_demand.values, color_continuous_scale='Blues')
#         fig_avg_demand.update_layout(showlegend=False, height=400)
#         st.plotly_chart(fig_avg_demand, use_container_width=True)
    
#     with col2:
#         # Demand confidence levels
#         confidence_data = forecast_data.groupby('Equipment Type')['Confidence'].mean()
        
#         fig_confidence = px.bar(x=confidence_data.index, y=confidence_data.values,
#                                title="Forecast Confidence by Equipment Type",
#                                color=confidence_data.values, color_continuous_scale='Greens')
#         fig_confidence.update_layout(showlegend=False, height=400)
#         st.plotly_chart(fig_confidence, use_container_width=True)

# def render_supply_demand_analysis(forecast_data, equipment_data):
#     """Render supply vs demand analysis"""
    
#     st.markdown("### ⚖️ Supply vs Demand Analysis")
    
#     # Calculate supply vs demand by equipment type
#     supply_data = equipment_data.groupby('Type').size().reset_index(name='Total_Supply')
#     available_supply = equipment_data[equipment_data['Status'] == 'Available'].groupby('Type').size().reset_index(name='Available_Supply')
#     avg_demand = forecast_data.groupby('Equipment Type')['Predicted Demand'].mean().reset_index()
#     avg_demand.columns = ['Type', 'Avg_Demand']
    
#     # Merge data
#     supply_demand = supply_data.merge(available_supply, on='Type', how='left').fillna(0)
#     supply_demand = supply_demand.merge(avg_demand, left_on='Type', right_on='Type', how='left').fillna(0)
    
#     supply_demand['Demand_Gap'] = supply_demand['Avg_Demand'] - supply_demand['Available_Supply']
#     supply_demand['Utilization_Forecast'] = (supply_demand['Avg_Demand'] / supply_demand['Total_Supply'] * 100).round(1)
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Supply vs Demand chart
#         fig_supply_demand = go.Figure()
        
#         fig_supply_demand.add_trace(go.Bar(
#             x=supply_demand['Type'],
#             y=supply_demand['Available_Supply'],
#             name='Available Supply',
#             marker_color='lightblue'
#         ))
        
#         fig_supply_demand.add_trace(go.Bar(
#             x=supply_demand['Type'],
#             y=supply_demand['Avg_Demand'],
#             name='Predicted Demand',
#             marker_color='orange'
#         ))
        
#         fig_supply_demand.update_layout(
#             title="Supply vs Predicted Demand",
#             barmode='group',
#             height=400
#         )
        
#         st.plotly_chart(fig_supply_demand, use_container_width=True)
    
#     with col2:
#         # Utilization forecast
#         fig_utilization = px.bar(supply_demand, x='Type', y='Utilization_Forecast',
#                                 title="Forecasted Utilization Rate (%)",
#                                 color='Utilization_Forecast',
#                                 color_continuous_scale='RdYlGn')
#         fig_utilization.update_layout(showlegend=False, height=400)
#         st.plotly_chart(fig_utilization, use_container_width=True)
    
#     # Supply-demand gap analysis
#     st.markdown("#### 📊 Supply-Demand Gap Analysis")
    
#     # Color code based on gap
#     supply_demand['Gap_Status'] = supply_demand['Demand_Gap'].apply(
#         lambda x: 'Surplus' if x < -2 else 'Shortage' if x > 2 else 'Balanced'
#     )
    
#     for _, row in supply_demand.iterrows():
#         gap = row['Demand_Gap']
#         status = row['Gap_Status']
        
#         if status == 'Shortage':
#             st.error(f"**{row['Type']}:** Predicted shortage of {gap:.0f} units. Consider acquiring more equipment or optimizing current fleet.")
#         elif status == 'Surplus':
#             st.success(f"**{row['Type']}:** Surplus of {abs(gap):.0f} units available. Good capacity for unexpected demand.")
#         else:
#             st.info(f"**{row['Type']}:** Well balanced supply and demand.")

# def render_seasonal_trends(forecast_data):
#     """Render seasonal trends analysis"""
    
#     st.markdown("### 📅 Seasonal Trends & Patterns")
    
#     # Add seasonal components to forecast data
#     forecast_data['Month'] = forecast_data['Date'].dt.month
#     forecast_data['WeekOfYear'] = forecast_data['Date'].dt.isocalendar().week
#     forecast_data['DayOfWeek'] = forecast_data['Date'].dt.day_name()
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Monthly trends
#         monthly_demand = forecast_data.groupby(['Month', 'Equipment Type'])['Predicted Demand'].mean().reset_index()
        
#         fig_monthly = px.line(monthly_demand, x='Month', y='Predicted Demand', 
#                              color='Equipment Type',
#                              title="Seasonal Demand Patterns by Month")
#         fig_monthly.update_layout(height=400)
#         st.plotly_chart(fig_monthly, use_container_width=True)
    
#     with col2:
#         # Day of week patterns
#         dow_demand = forecast_data.groupby(['DayOfWeek', 'Equipment Type'])['Predicted Demand'].mean().reset_index()
        
#         # Reorder days
#         day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#         dow_demand['DayOfWeek'] = pd.Categorical(dow_demand['DayOfWeek'], categories=day_order, ordered=True)
#         dow_demand = dow_demand.sort_values('DayOfWeek')
        
#         fig_dow = px.bar(dow_demand, x='DayOfWeek', y='Predicted Demand',
#                         color='Equipment Type',
#                         title="Weekly Demand Patterns")
#         fig_dow.update_layout(height=400)
#         st.plotly_chart(fig_dow, use_container_width=True)
    
#     # Seasonal insights
#     st.markdown("#### 🔍 Seasonal Insights")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.info("**Spring (Mar-May)**\n• High demand for excavators\n• Construction season begins\n• 25% increase in overall demand")
    
#     with col2:
#         st.warning("**Summer (Jun-Aug)**\n• Peak demand period\n• All equipment types in high demand\n• Plan for capacity increases")
    
#     with col3:
#         st.success("**Fall/Winter (Sep-Feb)**\n• Lower demand period\n• Ideal for maintenance\n• Focus on indoor projects")

# def render_market_intelligence(forecast_data, equipment_data):
#     """Render market intelligence and competitive insights"""
    
#     st.markdown("### 🎯 Market Intelligence")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("#### 📈 Market Opportunities")
        
#         # Identify high-growth segments
#         growth_opportunities = [
#             {"segment": "Excavator Rentals", "growth": "+18%", "reason": "Infrastructure projects increasing"},
#             {"segment": "Crane Services", "growth": "+15%", "reason": "High-rise construction boom"},
#             {"segment": "Compact Equipment", "growth": "+12%", "reason": "Urban development focus"},
#             {"segment": "Green Equipment", "growth": "+25%", "reason": "Environmental regulations"}
#         ]
        
#         for opp in growth_opportunities:
#             st.success(f"**{opp['segment']}:** {opp['growth']} growth\n{opp['reason']}")
    
#     with col2:
#         st.markdown("#### ⚠️ Market Risks")
        
#         market_risks = [
#             {"risk": "Economic Downturn", "impact": "High", "mitigation": "Diversify customer base"},
#             {"risk": "Fuel Price Volatility", "impact": "Medium", "mitigation": "Fuel surcharge policies"},
#             {"risk": "Equipment Shortage", "impact": "Medium", "mitigation": "Strategic partnerships"},
#             {"risk": "Regulatory Changes", "impact": "Low", "mitigation": "Compliance monitoring"}
#         ]
        
#         for risk in market_risks:
#             if risk['impact'] == 'High':
#                 st.error(f"**{risk['risk']}** ({risk['impact']} Impact)\n{risk['mitigation']}")
#             elif risk['impact'] == 'Medium':
#                 st.warning(f"**{risk['risk']}** ({risk['impact']} Impact)\n{risk['mitigation']}")
#             else:
#                 st.info(f"**{risk['risk']}** ({risk['impact']} Impact)\n{risk['mitigation']}")
    
#     # Market positioning analysis
#     st.markdown("#### 🏆 Competitive Position")
    
#     positioning_data = {
#         'Metric': ['Market Share', 'Fleet Size', 'Service Quality', 'Pricing', 'Technology'],
#         'Our Position': [12, 85, 92, 78, 88],
#         'Industry Average': [8, 65, 75, 80, 70],
#         'Market Leader': [25, 95, 95, 85, 95]
#     }
    
#     positioning_df = pd.DataFrame(positioning_data)
    
#     fig_position = go.Figure()
    
#     fig_position.add_trace(go.Bar(x=positioning_df['Metric'], y=positioning_df['Our Position'],
#                                  name='Our Position', marker_color='lightblue'))
#     fig_position.add_trace(go.Bar(x=positioning_df['Metric'], y=positioning_df['Industry Average'],
#                                  name='Industry Average', marker_color='orange'))
#     fig_position.add_trace(go.Bar(x=positioning_df['Metric'], y=positioning_df['Market Leader'],
#                                  name='Market Leader', marker_color='lightgreen'))
    
#     fig_position.update_layout(
#         title="Competitive Positioning Analysis",
#         barmode='group',
#         height=400
#     )
    
#     st.plotly_chart(fig_position, use_container_width=True)

# def render_actionable_recommendations(insights, forecast_data, equipment_data):
#     """Render AI-powered actionable recommendations"""
    
#     st.markdown("### 💡 AI-Powered Recommendations")
    
#     # Strategic recommendations based on forecast
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("#### 🎯 Strategic Actions")
        
#         recommendations = [
#             {
#                 "priority": "High",
#                 "action": "Increase Excavator Fleet",
#                 "reason": f"Peak demand expected on {insights['peak_demand_date'].strftime('%B %d')}",
#                 "impact": "+$45K monthly revenue"
#             },
#             {
#                 "priority": "High", 
#                 "action": "Optimize Site B Allocation",
#                 "reason": "Low utilization detected in demand forecast",
#                 "impact": "+15% efficiency gain"
#             },
#             {
#                 "priority": "Medium",
#                 "action": "Implement Dynamic Pricing",
#                 "reason": "Demand volatility presents pricing opportunities",
#                 "impact": "+8% profit margin"
#             },
#             {
#                 "priority": "Medium",
#                 "action": "Expand Crane Services",
#                 "reason": "Consistent high demand with good margins",
#                 "impact": "+$28K monthly revenue"
#             }
#         ]
        
#         for rec in recommendations:
#             if rec['priority'] == 'High':
#                 st.error(f"**🔥 {rec['action']}** (High Priority)\n{rec['reason']}\n💰 {rec['impact']}")
#             else:
#                 st.warning(f"**⚡ {rec['action']}** (Medium Priority)\n{rec['reason']}\n💰 {rec['impact']}")
    
#     with col2:
#         st.markdown("#### 🛠️ Operational Optimizations")
        
#         optimizations = [
#             {
#                 "area": "Maintenance Scheduling",
#                 "suggestion": "Schedule during low-demand periods (Jan-Feb)",
#                 "benefit": "Minimize revenue loss"
#             },
#             {
#                 "area": "Equipment Positioning",
#                 "suggestion": "Pre-position equipment based on demand forecast",
#                 "benefit": "Reduce transportation costs by 20%"
#             },
#             {
#                 "area": "Inventory Management",
#                 "suggestion": "Maintain 15% buffer for peak demand periods",
#                 "benefit": "Capture surge opportunities"
#             },
#             {
#                 "area": "Customer Relationships",
#                 "suggestion": "Offer long-term contracts with volume discounts",
#                 "benefit": "Stabilize demand and improve cash flow"
#             }
#         ]
        
#         for opt in optimizations:
#             st.info(f"**{opt['area']}**\n{opt['suggestion']}\n✅ {opt['benefit']}")
    
#     # Implementation timeline
#     st.markdown("#### 📅 Implementation Timeline")
    
#     timeline_data = [
#         {"Phase": "Immediate (0-2 weeks)", "Actions": "• Redistribute idle equipment\n• Implement dynamic pricing\n• Update demand tracking", "Impact": "Quick wins"},
#         {"Phase": "Short-term (1-3 months)", "Actions": "• Acquire additional excavators\n• Optimize maintenance schedules\n• Enhance forecasting models", "Impact": "Revenue growth"},
#         {"Phase": "Medium-term (3-12 months)", "Actions": "• Expand to new locations\n• Implement IoT monitoring\n• Build strategic partnerships", "Impact": "Market expansion"},
#         {"Phase": "Long-term (12+ months)", "Actions": "• Fleet modernization\n• Advanced AI integration\n• Market leadership position", "Impact": "Industry leadership"}
#     ]
    
#     for phase in timeline_data:
#         with st.expander(f"📋 {phase['Phase']} - {phase['Impact']}"):
#             st.markdown(phase['Actions'])

# def main():
#     user = get_current_user()
    
#     # Header
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.markdown("""
#         <div class="dashboard-header">
#             <h1>🔮 Demand Forecasting & Market Intelligence</h1>
#             <p>AI-powered demand prediction and strategic insights</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         if st.button("🚪 Logout", type="secondary", use_container_width=True):
#             logout_user()
#             st.rerun()
    
#     st.markdown("---")
    
#     # Load data
#     equipment_data = get_sample_equipment_data()
#     forecast_data = get_demand_forecast_data()
#     insights = generate_demand_insights(forecast_data, equipment_data)
    
#     # Key forecast metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     total_predicted = forecast_data['Predicted Demand'].sum()
#     peak_day_demand = forecast_data.groupby('Date')['Predicted Demand'].sum().max()
#     avg_confidence = forecast_data['Confidence'].mean() * 100
#     high_demand_equipment = insights['high_demand_equipment']
    
#     with col1:
#         render_metric_card("Total Predicted Demand", f"{total_predicted:.0f}", "+12%", "🔮", "#1f77b4")
    
#     with col2:
#         render_metric_card("Peak Day Demand", f"{peak_day_demand:.0f}", f"{insights['peak_demand_date'].strftime('%b %d')}", "📈", "#ff7f0e")
    
#     with col3:
#         render_metric_card("Forecast Confidence", f"{avg_confidence:.1f}%", "+2.3%", "🎯", "#2ca02c")
    
#     with col4:
#         render_metric_card("Top Demand Type", high_demand_equipment, "Leading category", "🏗️", "#9467bd")
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # AI Insights Alert
#     if insights['current_vs_predicted'] > 5:
#         st.warning(f"🚨 **Demand Alert:** Predicted demand exceeds current capacity by {insights['current_vs_predicted']:.0f} units. Consider fleet expansion or strategic partnerships.")
#     elif insights['current_vs_predicted'] < -10:
#         st.info(f"💡 **Optimization Opportunity:** Current capacity exceeds predicted demand. Consider optimizing fleet allocation or exploring new markets.")
#     else:
#         st.success("✅ **Optimal Balance:** Current fleet capacity aligns well with predicted demand.")
    
#     # Main forecasting tabs
#     tab1, tab2, tab3, tab4, tab5 = st.tabs([
#         "🔮 Demand Forecast", "⚖️ Supply vs Demand", "📅 Seasonal Analysis", 
#         "🎯 Market Intelligence", "💡 Recommendations"
#     ])
    
#     with tab1:
#         render_demand_forecast_overview(forecast_data)
        
#         # Detailed forecast table
#         st.markdown("---")
#         st.markdown("### 📊 Detailed Forecast Data")
        
#         # Allow filtering by equipment type
#         equipment_types = forecast_data['Equipment Type'].unique().tolist()
#         selected_types = st.multiselect("Filter Equipment Types", equipment_types, default=equipment_types[:3])
        
#         if selected_types:
#             filtered_forecast = forecast_data[forecast_data['Equipment Type'].isin(selected_types)]
            
#             # Summary statistics
#             forecast_summary = filtered_forecast.groupby('Equipment Type').agg({
#                 'Predicted Demand': ['mean', 'max', 'min'],
#                 'Confidence': 'mean',
#                 'Current Available': 'mean'
#             }).round(2)
            
#             forecast_summary.columns = ['Avg Demand', 'Max Demand', 'Min Demand', 'Avg Confidence', 'Current Available']
#             st.dataframe(forecast_summary, use_container_width=True)
            
#             # Export forecast data
#             if st.button("📥 Export Forecast Data"):
#                 csv = filtered_forecast.to_csv(index=False)
#                 st.download_button(
#                     label="⬇️ Download CSV",
#                     data=csv,
#                     file_name=f"demand_forecast_{datetime.now().strftime('%Y%m%d')}.csv",
#                     mime="text/csv"
#                 )
    
#     with tab2:
#         render_supply_demand_analysis(forecast_data, equipment_data)
        
#         # Gap mitigation strategies
#         st.markdown("---")
#         st.markdown("### 🛠️ Gap Mitigation Strategies")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("#### For Equipment Shortages:")
#             st.write("• **Partner with other dealers** for equipment sharing")
#             st.write("• **Implement waitlist system** with priority booking")
#             st.write("• **Offer alternative equipment** with equivalent capabilities")
#             st.write("• **Adjust pricing** to manage demand during peak periods")
#             st.write("• **Extend operating hours** to maximize utilization")
        
#         with col2:
#             st.markdown("#### For Equipment Surplus:")
#             st.write("• **Expand marketing efforts** in underserved areas")
#             st.write("• **Offer promotional pricing** to stimulate demand")
#             st.write("• **Target new customer segments** (small contractors, DIY)")
#             st.write("• **Consider equipment relocation** to high-demand areas")
#             st.write("• **Evaluate fleet rightsizing** opportunities")
    
#     with tab3:
#         render_seasonal_trends(forecast_data)
        
#         # Seasonal preparation recommendations
#         st.markdown("---")
#         st.markdown("### 🎯 Seasonal Preparation Strategy")
        
#         current_month = datetime.now().month
#         season_recommendations = {
#             (12, 1, 2): {
#                 "season": "Winter",
#                 "focus": "Maintenance & Planning",
#                 "actions": ["Schedule major maintenance", "Plan fleet expansion", "Review year performance", "Prepare for spring demand"]
#             },
#             (3, 4, 5): {
#                 "season": "Spring", 
#                 "focus": "Ramp Up Operations",
#                 "actions": ["Increase marketing efforts", "Prepare equipment for peak season", "Staff up for higher demand", "Monitor weather patterns"]
#             },
#             (6, 7, 8): {
#                 "season": "Summer",
#                 "focus": "Peak Operations",
#                 "actions": ["Maximize fleet utilization", "Monitor equipment health", "Implement surge pricing", "Focus on customer satisfaction"]
#             },
#             (9, 10, 11): {
#                 "season": "Fall",
#                 "focus": "Optimization & Planning", 
#                 "actions": ["Optimize fleet allocation", "Plan maintenance schedules", "Evaluate performance", "Prepare for winter slowdown"]
#             }
#         }
        
#         # Find current season
#         current_season = None
#         for months, season_info in season_recommendations.items():
#             if current_month in months:
#                 current_season = season_info
#                 break
        
#         if current_season:
#             st.info(f"**Current Season: {current_season['season']}** - Focus: {current_season['focus']}")
#             for action in current_season['actions']:
#                 st.write(f"• {action}")
    
#     with tab4:
#         render_market_intelligence(forecast_data, equipment_data)
        
#         # Competitive analysis
#         st.markdown("---")
#         st.markdown("### 🏆 Competitive Landscape")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("#### Market Share Analysis")
            
#             market_share_data = {
#                 'Company': ['ABC Equipment (You)', 'MegaRent Corp', 'CityWide Rentals', 'BuildMax Equipment', 'Others'],
#                 'Market Share': [12, 25, 18, 15, 30],
#                 'Growth Rate': [15, 8, 12, 5, 7]
#             }
            
#             market_df = pd.DataFrame(market_share_data)
            
#             fig_market = px.pie(market_df, values='Market Share', names='Company',
#                                title="Local Market Share Distribution")
#             st.plotly_chart(fig_market, use_container_width=True)
        
#         with col2:
#             st.markdown("#### Growth Rate Comparison")
            
#             fig_growth = px.bar(market_df, x='Company', y='Growth Rate',
#                                title="Annual Growth Rate Comparison (%)",
#                                color='Growth Rate', color_continuous_scale='Greens')
#             fig_growth.update_layout(showlegend=False)
#             st.plotly_chart(fig_growth, use_container_width=True)
    
#     with tab5:
#         render_actionable_recommendations(insights, forecast_data, equipment_data)
        
#         # ROI Calculator
#         st.markdown("---")
#         st.markdown("### 💰 Investment ROI Calculator")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             investment_amount = st.number_input("Investment Amount ($)", min_value=0, value=250000, step=10000)
#             expected_revenue = st.number_input("Expected Annual Revenue ($)", min_value=0, value=450000, step=10000)
        
#         with col2:
#             operating_costs = st.number_input("Annual Operating Costs ($)", min_value=0, value=180000, step=5000)
#             payback_period = st.number_input("Desired Payback Period (years)", min_value=1, value=3, step=1)
        
#         with col3:
#             # Calculate ROI metrics
#             annual_profit = expected_revenue - operating_costs
#             roi_percentage = (annual_profit / investment_amount) * 100
#             actual_payback = investment_amount / annual_profit if annual_profit > 0 else float('inf')
            
#             st.metric("Annual Profit", format_currency(annual_profit))
#             st.metric("ROI Percentage", f"{roi_percentage:.1f}%")
#             st.metric("Payback Period", f"{actual_payback:.1f} years")
            
#             if actual_payback <= payback_period:
#                 st.success("✅ Investment meets payback criteria")
#             else:
#                 st.warning("⚠️ Investment exceeds desired payback period")
        
#         # Investment recommendations
#         st.markdown("#### 📋 Investment Priority Matrix")
        
#         investment_options = [
#             {"Equipment": "2x New Excavators", "Cost": "$180K", "Revenue Impact": "$65K/year", "ROI": "36%", "Priority": "High"},
#             {"Equipment": "Fleet Management Software", "Cost": "$25K", "Revenue Impact": "$15K/year", "ROI": "60%", "Priority": "High"},
#             {"Equipment": "1x Tower Crane", "Cost": "$350K", "Revenue Impact": "$95K/year", "ROI": "27%", "Priority": "Medium"},
#             {"Equipment": "GPS Tracking System", "Cost": "$45K", "Revenue Impact": "$22K/year", "ROI": "49%", "Priority": "Medium"},
#             {"Equipment": "Maintenance Facility", "Cost": "$500K", "Revenue Impact": "$80K/year", "ROI": "16%", "Priority": "Low"}
#         ]
        
#         investment_df = pd.DataFrame(investment_options)
        
#         # Color code by priority
#         def color_priority(val):
#             if val == 'High':
#                 return 'background-color: #d4edda'
#             elif val == 'Medium':
#                 return 'background-color: #fff3cd'
#             else:
#                 return 'background-color: #f8d7da'
        
#         styled_df = investment_df.style.applymap(color_priority, subset=['Priority'])
#         st.dataframe(styled_df, use_container_width=True, hide_index=True)

# if __name__ == "__main__":
#     main()


import streamlit as st
import pandas as pd
from lib.state import is_authenticated, get_current_user, logout_user, get_token
from lib.api import api_client
from lib.components import render_metric_card
from lib.styles import apply_custom_css

st.set_page_config(page_title="Demand Forecasting", page_icon="🔮", layout="wide")
apply_custom_css()

if not is_authenticated():
    st.error("🔒 Please login first"); st.stop()

def flatten_forecast(api_data):
    # api_data: {"forecast":[{date, day_of_week, season, equipment_forecasts:[...]}], ...}
    rows = []
    for day in api_data.get("forecast", []):
        for e in day.get("equipment_forecasts", []):
            rows.append({
                "Date": day["date"],
                "Day": day["day_of_week"],
                "Season": day["season"],
                "Equipment ID": e["equipment_id"],
                "Name": e.get("equipment_name"),
                "Type": e.get("equipment_type"),
                "Predicted Utilization %": e.get("predicted_utilization"),
                "Potential Revenue": e.get("potential_revenue"),
                "Recommendation": e.get("recommendation"),
            })
    return pd.DataFrame(rows)

def main():
    user = get_current_user()
    token = get_token()

    c1, c2 = st.columns([3,1])
    with c1:
        st.markdown("""
        <div class="dashboard-header">
          <h1>🔮 Utilization Forecast</h1>
          <p>Predicted utilization & revenue (live from backend)</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout_user(); st.rerun()
    st.markdown("---")

    days = st.slider("Days ahead", 7, 60, 30)
    if st.button("Generate Forecast", type="primary"):
        data = api_client.get_equipment_utilization_forecast(token, days)
        if not data or not data.get("forecast"):
            st.info("No forecast (maybe no equipment in your account)."); return
        df = flatten_forecast(data)

        avg_util = df["Predicted Utilization %"].mean()
        total_days = data.get("forecast_period_days", days)
        total_equipment = data.get("total_equipment", 0)

        m1, m2, m3 = st.columns(3)
        with m1: render_metric_card("Avg Predicted Utilization", f"{avg_util:.1f}%", "", "📈", "#1f77b4")
        with m2: render_metric_card("Days Forecasted", f"{total_days}", "", "📅", "#2ca02c")
        with m3: render_metric_card("Equipment Count", f"{total_equipment}", "", "🏗️", "#ff7f0e")

        st.markdown("### Forecast Table")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("### By Equipment Type (Avg Utilization)")
        by_type = df.groupby("Type")["Predicted Utilization %"].mean().sort_values(ascending=False)
        st.bar_chart(by_type)

if __name__ == "__main__":
    main()

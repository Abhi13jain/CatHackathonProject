import streamlit as st

def apply_custom_css():
    """Apply custom CSS styles for better UI/UX"""
    
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding-top: 2rem;
    }
    
    /* Custom font for the entire app */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .hero-content h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .hero-description {
        font-size: 1rem;
        opacity: 0.8;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-card h3 {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 0.8rem;
        font-size: 1.2rem;
    }
    
    .feature-card p {
        color: #7f8c8d;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    
    /* Login Section */
    .login-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-section h2 {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Dashboard Header */
    .dashboard-header {
        margin-bottom: 1rem;
    }
    
    .dashboard-header h1 {
        color: #2c3e50;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-header p {
        color: #7f8c8d;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.12);
    }
    
    .metric-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .metric-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .metric-title {
        font-weight: 500;
        color: #7f8c8d;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Equipment Cards */
    .equipment-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
        border-left: 4px solid #3498db;
    }
    
    .equipment-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .equipment-header h4 {
        color: #2c3e50;
        font-weight: 600;
        margin: 0;
    }
    
    .equipment-status {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .equipment-details p {
        margin: 0.3rem 0;
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    /* Alert Cards */
    .alert-card {
        background: white;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 0.8rem;
    }
    
    .alert-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .alert-icon {
        font-size: 1.2rem;
    }
    
    .alert-title {
        font-weight: 600;
        color: #2c3e50;
        flex-grow: 1;
    }
    
    .alert-priority {
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        color: white;
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    .alert-message {
        color: #7f8c8d;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f8f9fa;
        border-radius: 8px;
        color: #7f8c8d;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Data Table Styling */
    .stDataFrame {
        border: 1px solid #e9ecef;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Plotly Chart Container */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Info/Warning/Error Messages */
    .stAlert {
        border-radius: 8px;
        border-left-width: 4px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Custom spacing */
    .metric-row {
        margin: 2rem 0;
    }
    
    .content-section {
        margin: 1.5rem 0;
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .hero-content h1 {
            font-size: 2rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
    }
    
    /* Animation for loading states */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-card, .equipment-card, .alert-card {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
    }
    
    /* Success/Warning indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-available { background-color: #28a745; }
    .status-rented { background-color: #ffc107; }
    .status-maintenance { background-color: #dc3545; }
    .status-reserved { background-color: #6f42c1; }
    
    /* Loading spinner */
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

def get_status_color(status):
    """Get color for equipment status"""
    colors = {
        'Available': '#28a745',
        'Rented': '#ffc107',
        'Maintenance': '#dc3545', 
        'Reserved': '#6f42c1'
    }
    return colors.get(status, '#6c757d')

def format_currency(amount):
    """Format currency values"""
    if amount >= 1000000:
        return f"${amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"${amount/1000:.1f}K"
    else:
        return f"${amount:.0f}"

def format_hours(hours):
    """Format hours display"""
    if hours >= 1000:
        return f"{hours/1000:.1f}K hrs"
    else:
        return f"{hours} hrs"

def get_priority_color(priority):
    """Get color for alert priority"""
    colors = {
        'High': '#dc3545',
        'Medium': '#ffc107',
        'Low': '#28a745'
    }
    return colors.get(priority, '#6c757d')
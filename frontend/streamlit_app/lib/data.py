import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def get_sample_equipment_data():
    """Generate sample equipment data matching the problem statement requirements"""
    
    equipment_types = ['Excavator', 'Crane', 'Bulldozer', 'Grader', 'Loader', 'Compactor', 'Forklift']
    statuses = ['Available', 'Rented', 'Maintenance', 'Reserved']
    locations = ['Site A - Downtown', 'Site B - Industrial', 'Site C - Airport', 'Warehouse', 'Site D - Highway']
    
    # Generate equipment IDs based on the pattern from the image
    equipment_data = []
    
    for i in range(1, 157):  # 156 total equipment
        equip_type = random.choice(equipment_types)
        
        # Create equipment ID with type prefix
        type_codes = {
            'Excavator': 'EX',
            'Crane': 'CR', 
            'Bulldozer': 'BD',
            'Grader': 'GR',
            'Loader': 'LD',
            'Compactor': 'CP',
            'Forklift': 'FK'
        }
        
        equipment_id = f"{type_codes[equip_type]}{str(i).zfill(4)}"
        
        # Generate realistic data - Fixed probabilities that sum to 1.0
        status = np.random.choice(statuses, p=[0.43, 0.47, 0.05, 0.05])  # More rented equipment
        location = random.choice(locations)
        
        # Generate dates
        check_out_date = datetime.now() - timedelta(days=random.randint(1, 45))
        if status == 'Rented':
            due_date = check_out_date + timedelta(days=random.randint(7, 30))
        else:
            due_date = None
            
        # Generate usage hours
        engine_hours = random.randint(1200, 8500)
        total_hours = engine_hours + random.randint(50, 500)
        idle_hours = random.randint(0, 200) if status != 'Rented' else random.randint(0, 50)
        
        # Generate operational days
        operational_days = random.randint(1, 30)
        
        equipment_data.append({
            'Equipment ID': equipment_id,
            'Type': equip_type,
            'Status': status,
            'Location': location,
            'Check Out Date': check_out_date.strftime('%Y-%m-%d') if status == 'Rented' else None,
            'Due Date': due_date.strftime('%Y-%m-%d') if due_date else None,
            'Engine Hours': engine_hours,
            'Total Hours': total_hours,
            'Idle Hours': idle_hours,
            'Operational Days': operational_days,
            'Last Update': (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime('%Y-%m-%d %H:%M'),
            'Fuel Level': random.randint(20, 100) if status == 'Rented' else random.randint(50, 100),
            'Next Maintenance': (datetime.now() + timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(equipment_data)

def get_usage_analytics_data():
    """Generate usage analytics data for charts"""
    
    # Generate 30 days of data
    dates = pd.date_range(start=datetime.now() - timedelta(days=29), end=datetime.now(), freq='D')
    
    analytics_data = []
    
    for date in dates:
        # Generate realistic usage patterns (higher on weekdays, lower on weekends)
        is_weekend = date.weekday() >= 5
        base_usage = 1200 if not is_weekend else 800
        
        usage_hours = base_usage + random.randint(-200, 300)
        revenue = usage_hours * random.uniform(2.5, 4.2)  # $2.5-4.2 per hour
        
        analytics_data.append({
            'Date': date,
            'Usage Hours': usage_hours,
            'Revenue': round(revenue, 2),
            'Active Equipment': random.randint(75, 95),
            'New Rentals': random.randint(5, 15),
            'Returns': random.randint(3, 12),
            'Utilization Rate': random.randint(75, 95)
        })
    
    return pd.DataFrame(analytics_data)

def get_overdue_equipment():
    """Get equipment that is overdue for return"""
    
    equipment_data = get_sample_equipment_data()
    
    # Filter for rented equipment with due dates in the past
    overdue = []
    current_date = datetime.now()
    
    for _, row in equipment_data.iterrows():
        if row['Status'] == 'Rented' and row['Due Date']:
            due_date = datetime.strptime(row['Due Date'], '%Y-%m-%d')
            if due_date < current_date:
                days_overdue = (current_date - due_date).days
                overdue.append({
                    'Equipment ID': row['Equipment ID'],
                    'Type': row['Type'],
                    'Location': row['Location'],
                    'Days Overdue': days_overdue,
                    'Due Date': row['Due Date']
                })
    
    return overdue[:10]  # Return top 10 overdue items

def get_maintenance_due():
    """Get equipment due for maintenance"""
    
    equipment_data = get_sample_equipment_data()
    current_date = datetime.now()
    
    maintenance_due = []
    
    for _, row in equipment_data.iterrows():
        next_maintenance = datetime.strptime(row['Next Maintenance'], '%Y-%m-%d')
        days_until_maintenance = (next_maintenance - current_date).days
        
        if days_until_maintenance <= 7:  # Due within a week
            maintenance_due.append({
                'Equipment ID': row['Equipment ID'],
                'Type': row['Type'],
                'Location': row['Location'],
                'Days Until Maintenance': days_until_maintenance,
                'Engine Hours': row['Engine Hours']
            })
    
    return sorted(maintenance_due, key=lambda x: x['Days Until Maintenance'])[:10]

def get_demand_forecast_data():
    """Generate demand forecasting data"""
    
    # Generate 30 days future forecast
    future_dates = pd.date_range(start=datetime.now() + timedelta(days=1), 
                                end=datetime.now() + timedelta(days=30), freq='D')
    
    equipment_types = ['Excavator', 'Crane', 'Bulldozer', 'Grader', 'Loader']
    
    forecast_data = []
    
    for date in future_dates:
        for equip_type in equipment_types:
            # Simulate seasonal patterns and trends
            base_demand = {
                'Excavator': 25,
                'Crane': 18,
                'Bulldozer': 15,
                'Grader': 10,
                'Loader': 20
            }[equip_type]
            
            # Add some randomness and trends
            seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365)
            trend_factor = 1 + 0.02 * (date.timetuple().tm_yday / 365)
            random_factor = random.uniform(0.8, 1.3)
            
            predicted_demand = int(base_demand * seasonal_factor * trend_factor * random_factor)
            
            forecast_data.append({
                'Date': date,
                'Equipment Type': equip_type,
                'Predicted Demand': predicted_demand,
                'Confidence': random.uniform(0.75, 0.95),
                'Current Available': base_demand + random.randint(-5, 10)
            })
    
    return pd.DataFrame(forecast_data)

def get_fleet_summary():
    """Get fleet summary statistics"""
    
    equipment_data = get_sample_equipment_data()
    
    summary = {
        'total_equipment': len(equipment_data),
        'rented': len(equipment_data[equipment_data['Status'] == 'Rented']),
        'available': len(equipment_data[equipment_data['Status'] == 'Available']),
        'maintenance': len(equipment_data[equipment_data['Status'] == 'Maintenance']),
        'utilization_rate': len(equipment_data[equipment_data['Status'] == 'Rented']) / len(equipment_data) * 100,
        'total_revenue': sum([random.randint(100, 500) for _ in range(len(equipment_data[equipment_data['Status'] == 'Rented']))]),
        'avg_engine_hours': equipment_data['Engine Hours'].mean(),
        'total_operational_days': equipment_data['Operational Days'].sum()
    }
    
    return summary

def get_location_summary():
    """Get equipment summary by location"""
    
    equipment_data = get_sample_equipment_data()
    
    location_summary = equipment_data.groupby(['Location', 'Status']).size().unstack(fill_value=0)
    location_summary['Total'] = location_summary.sum(axis=1)
    
    return location_summary.reset_index()

def get_anomaly_detections():
    """Get anomaly detection alerts"""
    
    anomalies = [
        {
            'Equipment ID': 'EX1045',
            'Type': 'Excavator',
            'Anomaly': 'Unusual idle time',
            'Description': 'Equipment idle for 72 hours at Site B',
            'Severity': 'Medium',
            'Detected': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')
        },
        {
            'Equipment ID': 'CR2023',
            'Type': 'Crane',
            'Anomaly': 'Location mismatch',
            'Description': 'GPS shows different location than reported',
            'Severity': 'High',
            'Detected': (datetime.now() - timedelta(minutes=45)).strftime('%Y-%m-%d %H:%M')
        },
        {
            'Equipment ID': 'BD3012',
            'Type': 'Bulldozer', 
            'Anomaly': 'High fuel consumption',
            'Description': 'Fuel usage 40% above normal for similar operations',
            'Severity': 'Medium',
            'Detected': (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M')
        }
    ]
    
    return anomalies
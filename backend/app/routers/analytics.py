from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import numpy as np

from app.services.firebase import firebase_service
from app.deps import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/equipment/utilization")
async def get_equipment_utilization_forecast(
    current_user: Dict = Depends(get_current_user),
    days_ahead: int = Query(30, description="Number of days to forecast")
):
    """Get equipment utilization forecast using predictive analytics"""
    try:
        db = firebase_service.db
        
        # Get user's equipment
        equipment_docs = db.collection('equipment').where('owner_id', '==', current_user['uid']).stream()
        equipment_list = []
        
        for doc in equipment_docs:
            equipment = doc.to_dict()
            equipment['id'] = doc.id
            equipment_list.append(equipment)
        
        if not equipment_list:
            return {"message": "No equipment found", "forecast": []}
        
        # Generate forecast for next N days
        forecast_data = []
        current_date = datetime.utcnow()
        
        for day in range(days_ahead):
            forecast_date = current_date + timedelta(days=day)
            season = (forecast_date.month % 12 + 3) // 3  # 1=Spring, 2=Summer, 3=Fall, 4=Winter
            day_of_week = forecast_date.weekday()
            
            daily_forecast = {
                "date": forecast_date.strftime("%Y-%m-%d"),
                "day_of_week": forecast_date.strftime("%A"),
                "season": ["Spring", "Summer", "Fall", "Winter"][season - 1],
                "equipment_forecasts": []
            }
            
            for equipment in equipment_list:
                # Predict utilization based on season, day, and equipment type
                base_utilization = 0.5
                
                # Seasonal adjustments
                if season == 2:  # Summer
                    base_utilization += 0.2
                elif season == 3:  # Fall
                    base_utilization += 0.1
                elif season == 1:  # Spring
                    base_utilization += 0.15
                
                # Day of week adjustments
                if day_of_week < 5:  # Weekdays
                    base_utilization += 0.1
                
                # Equipment type adjustments
                equipment_type = equipment.get('type', 'excavator')
                if equipment_type in ['excavator', 'crane']:
                    base_utilization += 0.1
                elif equipment_type in ['bulldozer', 'loader']:
                    base_utilization += 0.05
                
                # Add some randomness
                utilization = np.clip(base_utilization + np.random.normal(0, 0.1), 0, 1)
                
                # Calculate potential revenue
                daily_rate = equipment.get('rental_rate_per_day', 500)
                potential_revenue = daily_rate * utilization
                
                equipment_forecast = {
                    "equipment_id": equipment['id'],
                    "equipment_name": equipment.get('name', 'Unknown'),
                    "equipment_type": equipment_type,
                    "predicted_utilization": round(utilization * 100, 2),
                    "potential_revenue": round(potential_revenue, 2),
                    "recommendation": get_utilization_recommendation(utilization)
                }
                
                daily_forecast["equipment_forecasts"].append(equipment_forecast)
            
            forecast_data.append(daily_forecast)
        
        return {
            "total_equipment": len(equipment_list),
            "forecast_period_days": days_ahead,
            "forecast": forecast_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating utilization forecast: {str(e)}")

def get_utilization_recommendation(utilization_rate: float) -> str:
    """Get recommendation based on utilization rate"""
    if utilization_rate >= 0.8:
        return "Excellent utilization - consider expanding fleet"
    elif utilization_rate >= 0.6:
        return "Good utilization - maintain current operations"
    elif utilization_rate >= 0.4:
        return "Moderate utilization - look for additional projects"
    elif utilization_rate >= 0.2:
        return "Low utilization - consider sharing or marketing"
    else:
        return "Very low utilization - urgent action needed"

@router.get("/sharing/opportunities")
async def get_sharing_opportunities(
    current_user: Dict = Depends(get_current_user),
    max_distance_km: float = Query(10.0, description="Maximum distance for sharing")
):
    """Analyze sharing opportunities based on location and demand patterns"""
    try:
        db = firebase_service.db
        
        # Get nearby sharing requests
        sharing_requests = db.collection('sharing_requests').where('status', '==', 'active').stream()
        
        opportunities = []
        for doc in sharing_requests:
            request = doc.to_dict()
            request['id'] = doc.id
            
            # Calculate opportunity score
            opportunity_score = calculate_opportunity_score(request)
            
            opportunity = {
                "request_id": request['id'],
                "requester_name": request.get('requester_name', 'Unknown'),
                "equipment_type": request.get('equipment_type', 'Unknown'),
                "project_description": request.get('project_description', ''),
                "opportunity_score": round(opportunity_score, 2),
                "potential_revenue": estimate_potential_revenue(request),
                "recommendation": get_opportunity_recommendation(opportunity_score)
            }
            
            opportunities.append(opportunity)
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return {
            "max_distance_km": max_distance_km,
            "total_opportunities": len(opportunities),
            "opportunities": opportunities[:10]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sharing opportunities: {str(e)}")

def calculate_opportunity_score(request: Dict) -> float:
    """Calculate opportunity score based on various factors"""
    score = 0.0
    
    # Project duration factor (longer projects are better)
    duration = request.get('project_duration_days', 1)
    duration_score = min(1, duration / 7)  # 7+ days is optimal
    score += duration_score * 0.3
    
    # Equipment type demand factor
    equipment_demand = {
        'excavator': 0.9, 'crane': 0.8, 'bulldozer': 0.7,
        'grader': 0.6, 'loader': 0.8, 'compactor': 0.5,
        'forklift': 0.7, 'concrete_mixer': 0.6
    }
    equipment_type = request.get('equipment_type', 'excavator')
    demand_score = equipment_demand.get(equipment_type, 0.5)
    score += demand_score * 0.4
    
    # Cost split factor (50-50 is optimal)
    cost_split = request.get('preferred_cost_split', '50-50')
    if cost_split == '50-50':
        cost_score = 1.0
    elif '60-40' in cost_split:
        cost_score = 0.8
    else:
        cost_score = 0.6
    score += cost_score * 0.3
    
    return score

def estimate_potential_revenue(request: Dict) -> float:
    """Estimate potential revenue from sharing opportunity"""
    base_rates = {
        'excavator': 800, 'crane': 1200, 'bulldozer': 600,
        'grader': 500, 'loader': 400, 'compactor': 300,
        'forklift': 200, 'concrete_mixer': 400
    }
    
    equipment_type = request.get('equipment_type', 'excavator')
    base_rate = base_rates.get(equipment_type, 500)
    
    duration = request.get('project_duration_days', 1)
    utilization = 0.8  # 80% for shared equipment
    
    return base_rate * duration * utilization

def get_opportunity_recommendation(score: float) -> str:
    """Get recommendation based on opportunity score"""
    if score >= 0.8:
        return "High priority - excellent opportunity"
    elif score >= 0.6:
        return "Good opportunity - worth pursuing"
    elif score >= 0.4:
        return "Moderate opportunity - consider if available"
    else:
        return "Low priority - focus on better opportunities"

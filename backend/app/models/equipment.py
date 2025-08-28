# from pydantic import BaseModel, Field
# from typing import Optional, List, Dict, Any
# from datetime import datetime
# from enum import Enum

# class EquipmentStatus(str, Enum):
#     AVAILABLE = "available"
#     IN_USE = "in_use"
#     MAINTENANCE = "maintenance"
#     OUT_OF_SERVICE = "out_of_service"

# class EquipmentType(str, Enum):
#     EXCAVATOR = "excavator"
#     CRANE = "crane"
#     BULLDOZER = "bulldozer"
#     GRADER = "grader"
#     LOADER = "loader"
#     COMPACTOR = "compactor"
#     FORKLIFT = "forklift"
#     CONCRETE_MIXER = "concrete_mixer"
#     GENERATOR = "generator"
#     AIR_COMPRESSOR = "air_compressor"

# class FuelType(str, Enum):
#     DIESEL = "diesel"
#     GASOLINE = "gasoline"
#     ELECTRIC = "electric"
#     HYBRID = "hybrid"

# class Equipment(BaseModel):
#     id: str = Field(..., description="Unique equipment identifier")
#     name: str = Field(..., description="Equipment name/model")
#     type: EquipmentType = Field(..., description="Type of equipment")
#     status: EquipmentStatus = Field(default=EquipmentStatus.AVAILABLE)
    
#     # Technical specifications
#     capacity: Optional[str] = Field(None, description="Equipment capacity (e.g., '20 ton', '1.2 cu yd')")
#     fuel_type: Optional[FuelType] = Field(None, description="Fuel type")
#     year_manufactured: Optional[int] = Field(None, description="Year of manufacture")
#     hours_used: Optional[int] = Field(0, description="Total hours of operation")
    
#     # Location and availability
#     current_location: str = Field(..., description="Current location coordinates or address")
#     latitude: Optional[float] = Field(None, description="Latitude coordinate")
#     longitude: Optional[float] = Field(None, description="Longitude coordinate")
    
#     # Financial information
#     rental_rate_per_hour: Optional[float] = Field(None, description="Hourly rental rate")
#     rental_rate_per_day: Optional[float] = Field(None, description="Daily rental rate")
#     maintenance_cost_per_hour: Optional[float] = Field(None, description="Maintenance cost per hour")
    
#     # Owner information
#     owner_id: str = Field(..., description="ID of the equipment owner")
#     owner_name: str = Field(..., description="Name of the equipment owner")
    
#     # Metadata
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)
#     description: Optional[str] = Field(None, description="Additional description")
#     images: Optional[List[str]] = Field(None, description="List of image URLs")
    
#     class Config:
#         json_encoders = {
#             datetime: lambda v: v.isoformat()
#         }

# class EquipmentUsage(BaseModel):
#     id: str = Field(..., description="Unique usage record identifier")
#     equipment_id: str = Field(..., description="Equipment being used")
#     user_id: str = Field(..., description="User using the equipment")
#     project_name: str = Field(..., description="Name of the project")
    
#     # Usage details
#     start_time: datetime = Field(..., description="Start time of usage")
#     end_time: Optional[datetime] = Field(None, description="End time of usage")
#     hours_used: Optional[float] = Field(None, description="Total hours used")
    
#     # Location
#     usage_location: str = Field(..., description="Location where equipment was used")
#     usage_latitude: Optional[float] = Field(None, description="Latitude of usage location")
#     usage_longitude: Optional[float] = Field(None, description="Longitude of usage location")
    
#     # Financial
#     total_cost: Optional[float] = Field(None, description="Total cost of usage")
#     fuel_consumed: Optional[float] = Field(None, description="Fuel consumed in liters")
    
#     # Status
#     status: str = Field(default="active", description="Usage status")
#     notes: Optional[str] = Field(None, description="Additional notes")
    
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)

# class SharingRequest(BaseModel):
#     id: str = Field(..., description="Unique sharing request identifier")
#     requester_id: str = Field(..., description="ID of the user requesting sharing")
#     requester_name: str = Field(..., description="Name of the requesting company")
    
#     # Equipment requirements
#     equipment_type: EquipmentType = Field(..., description="Type of equipment needed")
#     equipment_specifications: Optional[Dict[str, Any]] = Field(None, description="Specific equipment requirements")
    
#     # Project details
#     project_name: str = Field(..., description="Name of the project")
#     project_description: str = Field(..., description="Description of the project")
#     project_duration_days: int = Field(..., description="Duration of the project in days")
    
#     # Location and timing
#     project_location: str = Field(..., description="Project location")
#     latitude: float = Field(..., description="Project latitude")
#     longitude: float = Field(..., description="Project longitude")
#     start_date: datetime = Field(..., description="Project start date")
#     end_date: datetime = Field(..., description="Project end date")
    
#     # Sharing preferences
#     max_distance_km: float = Field(..., description="Maximum distance willing to travel")
#     preferred_cost_split: str = Field(..., description="Preferred cost sharing arrangement")
#     contact_preferences: Optional[Dict[str, Any]] = Field(None, description="Contact preferences")
    
#     # Status and matching
#     status: str = Field(default="active", description="Request status")
#     matched_equipment_id: Optional[str] = Field(None, description="ID of matched equipment")
#     matched_owner_id: Optional[str] = Field(None, description="ID of equipment owner")
    
#     # Timestamps
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     expires_at: datetime = Field(..., description="When the request expires")
#     updated_at: datetime = Field(default_factory=datetime.utcnow)

# class SharingMatch(BaseModel):
#     id: str = Field(..., description="Unique sharing match identifier")
#     request_id: str = Field(..., description="ID of the sharing request")
#     equipment_id: str = Field(..., description="ID of the matched equipment")
    
#     # Parties involved
#     requester_id: str = Field(..., description="ID of the requesting user")
#     owner_id: str = Field(..., description="ID of the equipment owner")
    
#     # Agreement details
#     cost_split: str = Field(..., description="Agreed cost sharing arrangement")
#     total_cost: float = Field(..., description="Total cost of the sharing arrangement")
#     requester_share: float = Field(..., description="Cost share for requester")
#     owner_share: float = Field(..., description="Cost share for owner")
    
#     # Timing
#     start_date: datetime = Field(..., description="Start date of sharing")
#     end_date: datetime = Field(..., description="End date of sharing")
    
#     # Status
#     status: str = Field(default="pending", description="Match status")
#     notes: Optional[str] = Field(None, description="Additional notes")
    
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)

# class User(BaseModel):
#     id: str = Field(..., description="Unique user identifier")
#     email: str = Field(..., description="User email address")
#     name: str = Field(..., description="User/company name")
#     company_type: Optional[str] = Field(None, description="Type of construction company")
    
#     # Location
#     primary_location: str = Field(..., description="Primary business location")
#     latitude: Optional[float] = Field(None, description="Business latitude")
#     longitude: Optional[float] = Field(None, description="Business longitude")
    
#     # Contact information
#     phone: Optional[str] = Field(None, description="Contact phone number")
#     website: Optional[str] = Field(None, description="Company website")
    
#     # Business details
#     business_license: Optional[str] = Field(None, description="Business license number")
#     insurance_info: Optional[Dict[str, Any]] = Field(None, description="Insurance information")
    
#     # Rating and reputation
#     rating: Optional[float] = Field(None, description="User rating (1-5)")
#     total_reviews: Optional[int] = Field(0, description="Total number of reviews")
    
#     # Metadata
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)
#     is_verified: bool = Field(default=False, description="Whether the user is verified")
#     is_active: bool = Field(default=True, description="Whether the user account is active")


from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class EquipmentStatus(str, Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"

class EquipmentType(str, Enum):
    EXCAVATOR = "excavator"
    CRANE = "crane"
    BULLDOZER = "bulldozer"
    GRADER = "grader"
    LOADER = "loader"
    COMPACTOR = "compactor"
    FORKLIFT = "forklift"
    CONCRETE_MIXER = "concrete_mixer"
    GENERATOR = "generator"
    AIR_COMPRESSOR = "air_compressor"

class FuelType(str, Enum):
    DIESEL = "diesel"
    GASOLINE = "gasoline"
    ELECTRIC = "electric"
    HYBRID = "hybrid"

class Equipment(BaseModel):
    # Make server-set fields optional so client/CSV can omit them
    id: Optional[str] = Field(None, description="Unique equipment identifier")
    owner_id: Optional[str] = Field(None, description="ID of the equipment owner")
    owner_name: Optional[str] = Field(None, description="Name of the equipment owner")

    name: str = Field(..., description="Equipment name/model")
    type: EquipmentType = Field(..., description="Type of equipment")
    status: EquipmentStatus = Field(default=EquipmentStatus.AVAILABLE)

    # Technical specifications
    capacity: Optional[str] = Field(None, description="Equipment capacity (e.g., '20 ton', '1.2 cu yd')")
    fuel_type: Optional[FuelType] = Field(None, description="Fuel type")
    year_manufactured: Optional[int] = Field(None, description="Year of manufacture")
    hours_used: Optional[int] = Field(0, description="Total hours of operation")

    # Location and availability
    current_location: str = Field(..., description="Current location name/address")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")

    # Financial information
    rental_rate_per_hour: Optional[float] = Field(None, description="Hourly rental rate")
    rental_rate_per_day: Optional[float] = Field(None, description="Daily rental rate")
    maintenance_cost_per_hour: Optional[float] = Field(None, description="Maintenance cost per hour")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = Field(None, description="Additional description")
    images: Optional[List[str]] = Field(None, description="List of image URLs")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

class EquipmentUsage(BaseModel):
    id: str = Field(..., description="Unique usage record identifier")
    equipment_id: str = Field(..., description="Equipment being used")
    user_id: str = Field(..., description="User using the equipment")
    project_name: str = Field(..., description="Project")
    start_time: datetime = Field(..., description="Start time")
    end_time: Optional[datetime] = Field(None, description="End time")
    hours_used: Optional[float] = Field(None, description="Total hours")
    usage_location: str = Field(..., description="Location")
    usage_latitude: Optional[float] = Field(None)
    usage_longitude: Optional[float] = Field(None)
    total_cost: Optional[float] = Field(None)
    fuel_consumed: Optional[float] = Field(None)
    status: str = Field(default="active")
    notes: Optional[str] = Field(None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SharingRequest(BaseModel):
    id: str
    requester_id: str
    requester_name: str
    equipment_type: EquipmentType
    equipment_specifications: Optional[Dict[str, Any]] = None
    project_name: str
    project_description: str
    project_duration_days: int
    project_location: str
    latitude: float
    longitude: float
    start_date: datetime
    end_date: datetime
    max_distance_km: float
    preferred_cost_split: str
    contact_preferences: Optional[Dict[str, Any]] = None
    status: str = "active"
    matched_equipment_id: Optional[str] = None
    matched_owner_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SharingMatch(BaseModel):
    id: str
    request_id: str
    equipment_id: str
    requester_id: str
    owner_id: str
    cost_split: str
    total_cost: float
    requester_share: float
    owner_share: float
    start_date: datetime
    end_date: datetime
    status: str = "pending"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    id: str
    email: str
    name: str
    company_type: Optional[str] = None
    primary_location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    business_license: Optional[str] = None
    insurance_info: Optional[Dict[str, Any]] = None
    rating: Optional[float] = None
    total_reviews: Optional[int] = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_verified: bool = False
    is_active: bool = True

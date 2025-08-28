# from fastapi import APIRouter, Depends, HTTPException, Query
# from typing import List, Optional, Dict, Any
# from datetime import datetime, timedelta
# import uuid
# from math import radians, cos, sin, asin, sqrt

# from app.models.equipment import (
#     Equipment, EquipmentUsage, SharingRequest, SharingMatch, User,
#     EquipmentStatus, EquipmentType
# )
# from app.services.firebase import firebase_service
# from app.deps import get_current_user

# router = APIRouter(prefix="/equipment", tags=["equipment"])

# def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
#     """Calculate distance between two points using Haversine formula"""
#     lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
#     dlng = lng2 - lng1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
#     c = 2 * asin(sqrt(a))
#     r = 6371  # Radius of earth in kilometers
#     return c * r

# @router.get("/", response_model=List[Equipment])
# async def get_equipment_list(
#     current_user: Dict = Depends(get_current_user),
#     equipment_type: Optional[EquipmentType] = Query(None),
#     status: Optional[EquipmentStatus] = Query(None),
#     max_distance: Optional[float] = Query(None)
# ):
#     """Get list of available equipment with optional filters"""
#     try:
#         db = firebase_service.db
        
#         # Build query
#         query = db.collection('equipment')
        
#         if equipment_type:
#             query = query.where('type', '==', equipment_type.value)
#         if status:
#             query = query.where('status', '==', status.value)
        
#         # Get equipment
#         equipment_docs = query.stream()
#         equipment_list = []
        
#         for doc in equipment_docs:
#             equipment_data = doc.to_dict()
#             equipment_data['id'] = doc.id
#             equipment_list.append(equipment_data)
        
#         return equipment_list
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching equipment: {str(e)}")

# @router.post("/", response_model=Equipment)
# async def add_equipment(
#     equipment_data: Equipment,
#     current_user: Dict = Depends(get_current_user)
# ):
#     """Add new equipment to the fleet"""
#     try:
#         db = firebase_service.db
        
#         # Generate unique ID
#         equipment_id = str(uuid.uuid4())
#         equipment_data.id = equipment_id
#         equipment_data.owner_id = current_user['uid']
#         equipment_data.owner_name = current_user.get('name', 'Unknown')
#         equipment_data.created_at = datetime.utcnow()
#         equipment_data.updated_at = datetime.utcnow()
        
#         # Convert to dict and store in Firebase
#         equipment_dict = equipment_data.dict()
#         db.collection('equipment').document(equipment_id).set(equipment_dict)
        
#         return equipment_data
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error adding equipment: {str(e)}")

# @router.get("/sharing/requests", response_model=List[SharingRequest])
# async def get_sharing_requests(
#     current_user: Dict = Depends(get_current_user),
#     status: Optional[str] = Query(None)
# ):
#     """Get sharing requests with optional filters"""
#     try:
#         db = firebase_service.db
        
#         query = db.collection('sharing_requests')
        
#         if status:
#             query = query.where('status', '==', status)
        
#         # Filter out expired requests
#         query = query.where('expires_at', '>', datetime.utcnow())
        
#         requests_docs = query.stream()
#         requests_list = []
        
#         for doc in requests_docs:
#             request_data = doc.to_dict()
#             request_data['id'] = doc.id
#             requests_list.append(request_data)
        
#         return requests_list
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching sharing requests: {str(e)}")

# @router.post("/sharing/requests", response_model=SharingRequest)
# async def create_sharing_request(
#     request_data: SharingRequest,
#     current_user: Dict = Depends(get_current_user)
# ):
#     """Create a new sharing request"""
#     try:
#         db = firebase_service.db
        
#         # Generate unique ID
#         request_id = str(uuid.uuid4())
#         request_data.id = request_id
#         request_data.requester_id = current_user['uid']
#         request_data.requester_name = current_user.get('name', 'Unknown')
#         request_data.created_at = datetime.utcnow()
#         request_data.updated_at = datetime.utcnow()
        
#         # Set expiration (24 hours from now)
#         request_data.expires_at = datetime.utcnow() + timedelta(hours=24)
        
#         # Convert to dict and store in Firebase
#         request_dict = request_data.dict()
#         db.collection('sharing_requests').document(request_id).set(request_dict)
        
#         return request_data
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error creating sharing request: {str(e)}")


from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid, csv, io
from math import radians, cos, sin, asin, sqrt
from pydantic import ValidationError

from app.models.equipment import (
    Equipment, EquipmentUsage, SharingRequest, SharingMatch, User,
    EquipmentStatus, EquipmentType, FuelType
)
from app.services.firebase import firebase_service
from app.deps import get_current_user

router = APIRouter(prefix="/equipment", tags=["equipment"])

# ---------- helpers ----------
def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def _chunk(iterable, size=450):
    buf = []
    for x in iterable:
        buf.append(x)
        if len(buf) == size:
            yield buf
            buf = []
    if buf:
        yield buf

def _norm_enum(v: Optional[str]) -> Optional[str]:
    return v.lower().strip() if isinstance(v, str) else v

# ---------- list ----------
@router.get("/", response_model=List[Equipment])
async def get_equipment_list(
    current_user: Dict = Depends(get_current_user),
    equipment_type: Optional[EquipmentType] = Query(None),
    status: Optional[EquipmentStatus] = Query(None),
    max_distance: Optional[float] = Query(None)
):
    try:
        db = firebase_service.db
        query = db.collection('equipment')

        if equipment_type:
            query = query.where('type', '==', equipment_type.value)
        if status:
            query = query.where('status', '==', status.value)

        equipment_docs = query.stream()
        equipment_list = []
        for doc in equipment_docs:
            data = doc.to_dict()
            data['id'] = doc.id
            equipment_list.append(data)
        return equipment_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching equipment: {str(e)}")

# ---------- create single ----------
@router.post("/", response_model=Equipment)
async def add_equipment(equipment_data: Equipment, current_user: Dict = Depends(get_current_user)):
    try:
        db = firebase_service.db
        equipment_id = equipment_data.id or str(uuid.uuid4())

        # server-side fields
        equipment_data.id = equipment_id
        equipment_data.owner_id = current_user['uid']
        equipment_data.owner_name = current_user.get('name', 'Unknown')
        equipment_data.created_at = datetime.utcnow()
        equipment_data.updated_at = datetime.utcnow()

        # coerce enums when provided as strings
        if isinstance(equipment_data.type, str):
            equipment_data.type = EquipmentType(_norm_enum(equipment_data.type))
        if isinstance(equipment_data.status, str):
            equipment_data.status = EquipmentStatus(_norm_enum(equipment_data.status))
        if isinstance(equipment_data.fuel_type, str):
            equipment_data.fuel_type = FuelType(_norm_enum(equipment_data.fuel_type))

        db.collection('equipment').document(equipment_id).set(equipment_data.dict())
        return equipment_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding equipment: {str(e)}")

# ---------- bulk create (JSON array) ----------
@router.post("/bulk", response_model=List[Equipment])
async def bulk_add_equipment(items: List[Equipment], current_user: Dict = Depends(get_current_user)):
    try:
        db = firebase_service.db
        saved: List[Equipment] = []
        for it in items:
            it.id = it.id or str(uuid.uuid4())
            it.owner_id = current_user["uid"]
            it.owner_name = current_user.get("name", "Unknown")
            it.created_at = datetime.utcnow()
            it.updated_at = datetime.utcnow()
            it.type = EquipmentType(_norm_enum(it.type)) if isinstance(it.type, str) else it.type
            it.status = EquipmentStatus(_norm_enum(it.status)) if isinstance(it.status, str) else it.status
            it.fuel_type = FuelType(_norm_enum(it.fuel_type)) if isinstance(it.fuel_type, str) else it.fuel_type
            saved.append(it)

        for chunk in _chunk(saved, 450):  # Firestore batch limit is 500
            batch = db.batch()
            for it in chunk:
                batch.set(db.collection("equipment").document(it.id), it.dict())
            batch.commit()
        return saved
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in bulk insert: {str(e)}")

# ---------- CSV import ----------
@router.post("/import-csv", response_model=Dict[str, Any])
async def import_equipment_csv(file: UploadFile = File(...), current_user: Dict = Depends(get_current_user)):
    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Please upload a CSV file")

        content = (await file.read()).decode("utf-8", errors="ignore")
        reader = csv.DictReader(io.StringIO(content))
        headers = [h.strip() for h in (reader.fieldnames or [])]

        to_save: List[Equipment] = []
        errors: List[Dict[str, Any]] = []

        # Two formats supported:
        # A) Generic columns (name,type,status,current_location,latitude,longitude,year_manufactured,hours_used,rental_rate_per_day,description,capacity,fuel_type)
        # B) Hackathon sample table columns (Equipment ID, Type, Site ID, Check-Out Date, Check-In Date, Engine Hours/Day, Idle Hours/Day, Operating Days, Last Operator ID)
        sample_format = "Equipment ID" in headers and "Type" in headers

        for idx, row in enumerate(reader, start=2):
            try:
                if sample_format:
                    # Map hackathon sample into Equipment
                    eq_id = (row.get("Equipment ID") or f"EQ-{idx}").strip()
                    eq_type = _norm_enum(row.get("Type") or "excavator")
                    site = (row.get("Site ID") or "Unknown").strip()

                    # Derive hours_used = engine_hours/day * operating_days
                    eng_per_day = float(row.get("Engine Hours/Day") or 0)
                    op_days = int(float(row.get("Operating Days") or 0))
                    hours_used = int(eng_per_day * op_days)

                    payload = {
                        "id": str(uuid.uuid4()),
                        "name": eq_id,
                        "type": eq_type,
                        "status": "available",
                        "current_location": site,
                        "hours_used": hours_used,
                        "description": f"Imported from sample CSV (last operator: {row.get('Last Operator ID','N/A')})",
                        "owner_id": current_user["uid"],
                        "owner_name": current_user.get("name", "Unknown"),
                    }
                else:
                    payload = {
                        "id": str(uuid.uuid4()),
                        "name": row.get("name") or row.get("equipment_name") or f"Item-{idx}",
                        "type": _norm_enum(row.get("type") or "excavator"),
                        "status": _norm_enum(row.get("status") or "available"),
                        "capacity": row.get("capacity"),
                        "fuel_type": _norm_enum(row.get("fuel_type") or None),
                        "year_manufactured": int(row["year_manufactured"]) if row.get("year_manufactured") else None,
                        "hours_used": int(float(row["hours_used"])) if row.get("hours_used") else 0,
                        "current_location": row.get("current_location") or "Unknown",
                        "latitude": float(row["latitude"]) if row.get("latitude") else None,
                        "longitude": float(row["longitude"]) if row.get("longitude") else None,
                        "rental_rate_per_day": float(row["rental_rate_per_day"]) if row.get("rental_rate_per_day") else None,
                        "description": row.get("description"),
                        "owner_id": current_user["uid"],
                        "owner_name": current_user.get("name", "Unknown"),
                    }

                item = Equipment(**payload)
                # Normalize enums
                item.type = EquipmentType(item.type)
                item.status = EquipmentStatus(item.status)
                if item.fuel_type:
                    item.fuel_type = FuelType(item.fuel_type)
                to_save.append(item)

            except (ValueError, ValidationError) as e:
                errors.append({"line": idx, "error": str(e), "row": row})

        db = firebase_service.db
        for chunk in _chunk(to_save, 450):
            batch = db.batch()
            for it in chunk:
                batch.set(db.collection("equipment").document(it.id), it.dict())
            batch.commit()

        return {"inserted": len(to_save), "failed": len(errors), "errors": errors}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing CSV: {str(e)}")

# ---------- sharing requests (unchanged from your file) ----------
@router.get("/sharing/requests", response_model=List[SharingRequest])
async def get_sharing_requests(current_user: Dict = Depends(get_current_user), status: Optional[str] = Query(None)):
    try:
        db = firebase_service.db
        query = db.collection('sharing_requests')
        if status:
            query = query.where('status', '==', status)
        query = query.where('expires_at', '>', datetime.utcnow())
        requests_docs = query.stream()
        requests_list = []
        for doc in requests_docs:
            data = doc.to_dict()
            data['id'] = doc.id
            requests_list.append(data)
        return requests_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sharing requests: {str(e)}")

@router.post("/sharing/requests", response_model=SharingRequest)
async def create_sharing_request(request_data: SharingRequest, current_user: Dict = Depends(get_current_user)):
    try:
        db = firebase_service.db
        request_id = str(uuid.uuid4())
        request_data.id = request_id
        request_data.requester_id = current_user['uid']
        request_data.requester_name = current_user.get('name', 'Unknown')
        request_data.created_at = datetime.utcnow()
        request_data.updated_at = datetime.utcnow()
        # default expiry: +24h if not already set
        if not request_data.expires_at or request_data.expires_at <= request_data.created_at:
            request_data.expires_at = datetime.utcnow() + timedelta(hours=24)
        db.collection('sharing_requests').document(request_id).set(request_data.dict())
        return request_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating sharing request: {str(e)}")

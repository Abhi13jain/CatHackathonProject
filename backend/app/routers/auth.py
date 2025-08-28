from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.models.auth import Token
from app.utils.security import create_access_token
from app.services.firebase import firebase_service
from app.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

class FirebaseTokenRequest(BaseModel):
    id_token: str

@router.get("/firebase-config")
async def get_firebase_config():
    """Get Firebase configuration for frontend"""
    return firebase_service.get_firebase_config()

@router.post("/firebase-login", response_model=Token)
async def firebase_login(token_request: FirebaseTokenRequest):
    """Verify Firebase ID token and return JWT"""
    
    user_data = await firebase_service.verify_firebase_token(token_request.id_token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
    
    # Create JWT token
    jwt_token_data = {
        "sub": user_data["uid"],
        "email": user_data["email"],
        "name": user_data["name"]
    }
    access_token = create_access_token(jwt_token_data)
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user"""
    return {"message": "Successfully logged out"}
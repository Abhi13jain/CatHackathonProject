from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import verify_token
from app.models.auth import TokenData

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current authenticated user from JWT token"""
    
    # Verify token
    token_data: TokenData = verify_token(credentials.credentials)
    
    # Return user data from token
    return {
        "uid": token_data.user_id,
        "email": token_data.email,
        "name": token_data.user_id  # Will be updated with actual name from token
    }
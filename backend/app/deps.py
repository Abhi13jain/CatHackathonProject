# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from app.utils.security import verify_token
# from app.models.auth import TokenData

# security = HTTPBearer()

# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
#     """Get current authenticated user from JWT token"""
    
#     # Verify token
#     token_data: TokenData = verify_token(credentials.credentials)
    
#     # Return user data from token
#     return {
#         "uid": token_data.user_id,
#         "email": token_data.email,
#         "name": token_data.user_id  # Will be updated with actual name from token
#     }

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import verify_token
from app.models.auth import TokenData
from app.config import settings

security = HTTPBearer(auto_error=not settings.DEV_BYPASS_AUTH)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Returns current user from JWT.
    If DEV_BYPASS_AUTH=true, returns a fixed dev user and ignores Authorization.
    """
    if settings.DEV_BYPASS_AUTH:
        return {"uid": "dev-user-123", "email": "dev@example.com", "name": "Dev User"}

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing credentials"
        )

    token_data: TokenData = verify_token(credentials.credentials)
    return {
        "uid": token_data.user_id,
        "email": token_data.email,
        "name": token_data.user_id
    }

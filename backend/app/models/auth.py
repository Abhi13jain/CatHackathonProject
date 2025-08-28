from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class GoogleUser(BaseModel):
    email: str
    name: str
    picture: Optional[str] = None
    sub: str  # Google user ID

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
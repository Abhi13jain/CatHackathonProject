from fastapi import APIRouter
from datetime import datetime, timezone

# This router is mounted at /api/v1 in main.py
router = APIRouter(prefix="/api/v1", tags=["system"])

@router.get("/health", include_in_schema=False)
async def health():
    """Simple probe for the frontend / ops checks."""
    return {
        "status": "ok",
        "service": "backend",
        "time": datetime.now(timezone.utc).isoformat(),
    }

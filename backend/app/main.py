from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, equipment, analytics

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(equipment.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Smart Rental Tracker API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Smart Rental Tracker API is running"}
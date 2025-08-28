# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     # JWT Settings
#     SECRET_KEY: str = "your-secret-key-change-in-production"
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
#     # Firebase Settings
#     FIREBASE_PROJECT_ID: str
#     FIREBASE_PRIVATE_KEY_ID: str
#     FIREBASE_PRIVATE_KEY: str
#     FIREBASE_CLIENT_EMAIL: str
#     FIREBASE_CLIENT_ID: str
    
#     # Firebase Web App Config (for frontend)
#     FIREBASE_WEB_API_KEY: str
#     FIREBASE_AUTH_DOMAIN: str
#     FIREBASE_STORAGE_BUCKET: str
#     FIREBASE_MESSAGING_SENDER_ID: str
#     FIREBASE_APP_ID: str
#     FIREBASE_MEASUREMENT_ID: str
    
#     # API Settings
#     API_V1_STR: str = "/api/v1"
#     PROJECT_NAME: str = "Smart Rental Tracker API"
    
#     class Config:
#         env_file = ".env"

# settings = Settings()


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Firebase Admin
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: str

    # Firebase Web
    FIREBASE_WEB_API_KEY: str
    FIREBASE_AUTH_DOMAIN: str
    FIREBASE_STORAGE_BUCKET: str
    FIREBASE_MESSAGING_SENDER_ID: str
    FIREBASE_APP_ID: str
    FIREBASE_MEASUREMENT_ID: str

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Smart Rental Tracker API"

    # Dev helper
    DEV_BYPASS_AUTH: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

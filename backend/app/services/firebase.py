import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.config import settings
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class FirebaseService:
    def __init__(self):
        if not firebase_admin._apps:
            # Create credentials from environment variables
            cred_dict = {
                "type": "service_account",
                "project_id": settings.FIREBASE_PROJECT_ID,
                "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
                "private_key": settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
                "client_email": settings.FIREBASE_CLIENT_EMAIL,
                "client_id": settings.FIREBASE_CLIENT_ID,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    async def verify_firebase_token(self, id_token: str) -> Optional[Dict]:
        """Verify Firebase ID token and return user info"""
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            
            # Get user info
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            name = decoded_token.get('name', '')
            picture = decoded_token.get('picture', '')
            
            # Store/update user in Firestore
            user_data = {
                'uid': uid,
                'email': email,
                'name': name,
                'picture': picture,
                'last_login': firestore.SERVER_TIMESTAMP,
                'provider': 'google'
            }
            
            # Update user document
            self.db.collection('users').document(uid).set(user_data, merge=True)
            
            return {
                'uid': uid,
                'email': email,
                'name': name,
                'picture': picture
            }
            
        except Exception as e:
            logger.error(f"Error verifying Firebase token: {e}")
            return None
    
    def get_firebase_config(self) -> Dict:
        """Return Firebase config for frontend from environment variables"""
        return {
            "apiKey": settings.FIREBASE_WEB_API_KEY,
            "authDomain": settings.FIREBASE_AUTH_DOMAIN,
            "projectId": settings.FIREBASE_PROJECT_ID,
            "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
            "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
            "appId": settings.FIREBASE_APP_ID,
            "measurementId": settings.FIREBASE_MEASUREMENT_ID
        }

firebase_service = FirebaseService()
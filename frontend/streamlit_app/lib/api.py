import httpx
import streamlit as st

API_BASE_URL = "http://localhost:8000/api/v1"

class APIClient:
    def __init__(self):
        self.client = httpx.Client(base_url=API_BASE_URL)
    
    def get_firebase_config(self):
        """Get Firebase configuration"""
        try:
            response = self.client.get("/auth/firebase-config")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Error getting Firebase config: {e}")
            return None
    
    def firebase_login(self, id_token: str):
        """Login with Firebase ID token"""
        try:
            response = self.client.post("/auth/firebase-login", json={"id_token": id_token})
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Error with Firebase login: {e}")
            return None
    
    def get_profile(self, token: str):
        """Get user profile"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = self.client.get("/auth/profile", headers=headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Error getting profile: {e}")
            return None

api_client = APIClient()
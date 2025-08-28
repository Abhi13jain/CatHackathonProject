# # # # # import httpx
# # # # # import streamlit as st
# # # # # from typing import Optional, Dict, Any
# # # # # import json

# # # # # API_BASE_URL = "http://localhost:8000/api/v1"

# # # # # class APIClient:
# # # # #     def __init__(self):
# # # # #         self.client = httpx.Client(base_url=API_BASE_URL, timeout=30.0)
    
# # # # #     def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
# # # # #         """Get headers with optional authorization token"""
# # # # #         headers = {"Content-Type": "application/json"}
# # # # #         if token:
# # # # #             headers["Authorization"] = f"Bearer {token}"
# # # # #         return headers
    
# # # # #     def _handle_response(self, response: httpx.Response) -> Optional[Dict[str, Any]]:
# # # # #         """Handle API response and return data or None on error"""
# # # # #         try:
# # # # #             if response.status_code == 200:
# # # # #                 return response.json()
# # # # #             elif response.status_code == 401:
# # # # #                 st.error("🔒 Authentication failed. Please login again.")
# # # # #                 return None
# # # # #             elif response.status_code >= 400:
# # # # #                 st.error(f"❌ API Error ({response.status_code}): {response.text}")
# # # # #                 return None
# # # # #         except Exception as e:
# # # # #             st.error(f"❌ Request failed: {str(e)}")
# # # # #             return None
        
# # # # #         return None
    
# # # # #     # Authentication endpoints
# # # # #     def get_firebase_config(self) -> Optional[Dict[str, Any]]:
# # # # #         """Get Firebase configuration"""
# # # # #         try:
# # # # #             response = self.client.get("/auth/firebase-config")
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error getting Firebase config: {e}")
# # # # #             return None
    
# # # # #     def firebase_login(self, id_token: str) -> Optional[Dict[str, Any]]:
# # # # #         """Login with Firebase ID token"""
# # # # #         try:
# # # # #             response = self.client.post("/auth/firebase-login", json={"id_token": id_token})
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error with Firebase login: {e}")
# # # # #             return None
    
# # # # #     def get_profile(self, token: str) -> Optional[Dict[str, Any]]:
# # # # #         """Get user profile"""
# # # # #         try:
# # # # #             headers = self._get_headers(token)
# # # # #             response = self.client.get("/auth/profile", headers=headers)
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error getting profile: {e}")
# # # # #             return None
    
# # # # #     def logout(self, token: str) -> bool:
# # # # #         """Logout user"""
# # # # #         try:
# # # # #             headers = self._get_headers(token)
# # # # #             response = self.client.post("/auth/logout", headers=headers)
# # # # #             return response.status_code == 200
# # # # #         except Exception as e:
# # # # #             st.error(f"Error during logout: {e}")
# # # # #             return False
    
# # # # #     # Equipment management endpoints
# # # # #     def get_equipment_list(self, token: str, filters: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
# # # # #         """Get list of equipment with optional filters"""
# # # # #         try:
# # # # #             headers = self._get_headers(token)
# # # # #             params = filters or {}
# # # # #             response = self.client.get("/equipment", headers=headers, params=params)
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error fetching equipment list: {e}")
# # # # #             return None
    
# # # # #     def add_equipment(self, token: str, equipment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
# # # # #         """Add new equipment to the fleet"""
# # # # #         try:
# # # # #             headers = self._get_headers(token)
# # # # #             response = self.client.post("/equipment", headers=headers, json=equipment_data)
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error adding equipment: {e}")
# # # # #             return None
    
# # # # #     # Sharing endpoints
# # # # #     def get_sharing_requests(self, token: str, status: Optional[str] = None) -> Optional[Dict[str, Any]]:
# # # # #         """Get sharing requests with optional filters"""
# # # # #         try:
# # # # #             headers = self._get_headers(token)
# # # # #             params = {"status": status} if status else {}
# # # # #             response = self.client.get("/equipment/sharing/requests", headers=headers, params=params)
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error fetching sharing requests: {e}")
# # # # #             return None
    
# # # # #     def create_sharing_request(self, token: str, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
# # # # #         """Create a new sharing request"""
# # # # #         try:
# # # # #             headers = self._get_headers(token)
# # # # #             response = self.client.post("/equipment/sharing/requests", headers=headers, json=request_data)
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error creating sharing request: {e}")
# # # # #             return None
    
# # # # #     # Analytics endpoints
# # # # #     def get_equipment_utilization_forecast(self, token: str, days_ahead: int = 30) -> Optional[Dict[str, Any]]:
# # # # #         """Get equipment utilization forecast"""
# # # # #         try:
# # # # #             headers = self._get_headers(token)
# # # # #             params = {"days_ahead": days_ahead}
# # # # #             response = self.client.get("/analytics/equipment/utilization", headers=headers, params=params)
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error fetching utilization forecast: {e}")
# # # # #             return None
    
# # # # #     def get_sharing_opportunities(self, token: str, max_distance_km: float = 10.0) -> Optional[Dict[str, Any]]:
# # # # #         """Get sharing opportunities analysis"""
# # # # #         try:
# # # # #             headers = self._get_headers(token)
# # # # #             params = {"max_distance_km": max_distance_km}
# # # # #             response = self.client.get("/analytics/sharing/opportunities", headers=headers, params=params)
# # # # #             return self._handle_response(response)
# # # # #         except Exception as e:
# # # # #             st.error(f"Error fetching sharing opportunities: {e}")
# # # # #             return None
    
# # # # #     # Health check
# # # # #     def health_check(self) -> bool:
# # # # #         """Check if API is healthy"""
# # # # #         try:
# # # # #             response = self.client.get("/health")
# # # # #             return response.status_code == 200
# # # # #         except Exception:
# # # # #             return False
    
# # # # #     def __del__(self):
# # # # #         """Clean up HTTP client"""
# # # # #         if hasattr(self, 'client'):
# # # # #             self.client.close()

# # # # # # Global API client instance
# # # # # api_client = APIClient()


# # # # import httpx
# # # # import streamlit as st
# # # # from typing import Optional, Dict, Any, Union

# # # # # ---- Change this if your backend runs elsewhere ----
# # # # API_BASE_URL = "http://localhost:8000/api/v1"

# # # # # ---- DEV NOTE ----
# # # # # If your backend requires JWT, set SEND_AUTH = True.
# # # # # If you added a backend dev-bypass (no auth), keep this False.
# # # # SEND_AUTH = False

# # # # class APIClient:
# # # #     def __init__(self):
# # # #         self.client = httpx.Client(base_url=API_BASE_URL, timeout=60.0)

# # # #     def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
# # # #         headers = {"Content-Type": "application/json"}
# # # #         if SEND_AUTH and token:
# # # #             headers["Authorization"] = f"Bearer {token}"
# # # #         return headers

# # # #     def _handle_response(self, response: httpx.Response) -> Union[Dict[str, Any], list, None]:
# # # #         try:
# # # #             if 200 <= response.status_code < 300:
# # # #                 if response.headers.get("content-type","").startswith("application/json"):
# # # #                     return response.json()
# # # #                 return {}
# # # #             elif response.status_code == 401:
# # # #                 st.error("🔒 Authentication failed. Please login again.")
# # # #                 return None
# # # #             else:
# # # #                 st.error(f"❌ API Error ({response.status_code}): {response.text}")
# # # #                 return None
# # # #         except Exception as e:
# # # #             st.error(f"❌ Request failed: {str(e)}")
# # # #             return None

# # # #     # ----- AUTH -----
# # # #     def get_firebase_config(self):
# # # #         try:
# # # #             res = self.client.get("/auth/firebase-config")
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error getting Firebase config: {e}")
# # # #             return None

# # # #     def firebase_login(self, id_token: str):
# # # #         try:
# # # #             res = self.client.post("/auth/firebase-login", json={"id_token": id_token})
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error with Firebase login: {e}")
# # # #             return None

# # # #     def get_profile(self, token: Optional[str]):
# # # #         try:
# # # #             res = self.client.get("/auth/profile", headers=self._get_headers(token))
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error getting profile: {e}")
# # # #             return None

# # # #     # ----- EQUIPMENT -----
# # # #     def get_equipment_list(self, token: Optional[str], filters: Optional[Dict] = None):
# # # #         try:
# # # #             res = self.client.get("/equipment", headers=self._get_headers(token), params=filters or {})
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error fetching equipment list: {e}")
# # # #             return None

# # # #     def add_equipment(self, token: Optional[str], equipment_data: Dict[str, Any]):
# # # #         try:
# # # #             res = self.client.post("/equipment", headers=self._get_headers(token), json=equipment_data)
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error adding equipment: {e}")
# # # #             return None

# # # #     # ----- SHARING -----
# # # #     def get_sharing_requests(self, token: Optional[str], status: Optional[str] = None):
# # # #         try:
# # # #             params = {"status": status} if status else {}
# # # #             res = self.client.get("/equipment/sharing/requests", headers=self._get_headers(token), params=params)
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error fetching sharing requests: {e}")
# # # #             return None

# # # #     def create_sharing_request(self, token: Optional[str], request_data: Dict[str, Any]):
# # # #         try:
# # # #             res = self.client.post("/equipment/sharing/requests", headers=self._get_headers(token), json=request_data)
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error creating sharing request: {e}")
# # # #             return None

# # # #     # ----- ANALYTICS -----
# # # #     def get_equipment_utilization_forecast(self, token: Optional[str], days_ahead: int = 30):
# # # #         try:
# # # #             res = self.client.get("/analytics/equipment/utilization",
# # # #                                   headers=self._get_headers(token),
# # # #                                   params={"days_ahead": days_ahead})
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error fetching utilization forecast: {e}")
# # # #             return None

# # # #     def get_sharing_opportunities(self, token: Optional[str], max_distance_km: float = 10.0):
# # # #         try:
# # # #             res = self.client.get("/analytics/sharing/opportunities",
# # # #                                   headers=self._get_headers(token),
# # # #                                   params={"max_distance_km": max_distance_km})
# # # #             return self._handle_response(res)
# # # #         except Exception as e:
# # # #             st.error(f"Error fetching sharing opportunities: {e}")
# # # #             return None

# # # #     # ----- HEALTH -----
# # # #     def health_check(self) -> bool:
# # # #         try:
# # # #             res = self.client.get("/health")
# # # #             return res.status_code == 200
# # # #         except Exception:
# # # #             return False

# # # #     def __del__(self):
# # # #         if hasattr(self, 'client'):
# # # #             self.client.close()

# # # # api_client = APIClient()


# # # import httpx
# # # import streamlit as st
# # # from typing import Optional, Dict, Any

# # # API_BASE_URL = "http://localhost:8000/api/v1"

# # # class APIClient:
# # #     def __init__(self):
# # #         # follow_redirects fixes the 307 issue from trailing slashes
# # #         self.client = httpx.Client(
# # #             base_url=API_BASE_URL,
# # #             timeout=30.0,
# # #             follow_redirects=True
# # #         )

# # #     def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
# # #         headers = {"Content-Type": "application/json"}
# # #         if token:
# # #             headers["Authorization"] = f"Bearer {token}"
# # #         return headers

# # #     def _handle_response(self, response: httpx.Response) -> Optional[Dict[str, Any]]:
# # #         try:
# # #             if response.status_code in (200, 201):
# # #                 # Many FastAPI handlers return 200; some might return 201 on create
# # #                 # If body is empty, return True-ish result
# # #                 if response.headers.get("content-type", "").startswith("application/json"):
# # #                     return response.json()
# # #                 return {}
# # #             elif response.status_code == 204:
# # #                 return {}
# # #             elif response.status_code == 401:
# # #                 st.error("🔒 Authentication failed. Please login again.")
# # #                 return None
# # #             else:
# # #                 st.error(f"❌ API Error ({response.status_code}): {response.text}")
# # #                 return None
# # #         except Exception as e:
# # #             st.error(f"❌ Request failed: {str(e)}")
# # #             return None

# # #     # ---------------- Authentication ----------------
# # #     def get_firebase_config(self) -> Optional[Dict[str, Any]]:
# # #         try:
# # #             resp = self.client.get("/auth/firebase-config")
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error getting Firebase config: {e}")
# # #             return None

# # #     def firebase_login(self, id_token: str) -> Optional[Dict[str, Any]]:
# # #         try:
# # #             resp = self.client.post("/auth/firebase-login", json={"id_token": id_token})
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error with Firebase login: {e}")
# # #             return None

# # #     def get_profile(self, token: str) -> Optional[Dict[str, Any]]:
# # #         try:
# # #             headers = self._get_headers(token)
# # #             resp = self.client.get("/auth/profile", headers=headers)
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error getting profile: {e}")
# # #             return None

# # #     def logout(self, token: str) -> bool:
# # #         try:
# # #             headers = self._get_headers(token)
# # #             resp = self.client.post("/auth/logout", headers=headers)
# # #             return resp.status_code in (200, 204)
# # #         except Exception as e:
# # #             st.error(f"Error during logout: {e}")
# # #             return False

# # #     # ---------------- Equipment ----------------
# # #     def get_equipment_list(self, token: str, filters: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
# # #         """Backend route is @router.get('/') → '/equipment/' (note trailing slash)"""
# # #         try:
# # #             headers = self._get_headers(token)
# # #             params = filters or {}
# # #             resp = self.client.get("/equipment/", headers=headers, params=params)  # <-- slash
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error fetching equipment list: {e}")
# # #             return None

# # #     def add_equipment(self, token: str, equipment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
# # #         """Backend route is @router.post('/') → '/equipment/' (note trailing slash)"""
# # #         try:
# # #             headers = self._get_headers(token)
# # #             resp = self.client.post("/equipment/", headers=headers, json=equipment_data)  # <-- slash
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error adding equipment: {e}")
# # #             return None

# # #     # ---------------- Sharing ----------------
# # #     def get_sharing_requests(self, token: str, status: Optional[str] = None) -> Optional[Dict[str, Any]]:
# # #         """Backend route: '/equipment/sharing/requests' (no trailing slash defined)"""
# # #         try:
# # #             headers = self._get_headers(token)
# # #             params = {"status": status} if status else {}
# # #             resp = self.client.get("/equipment/sharing/requests", headers=headers, params=params)
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error fetching sharing requests: {e}")
# # #             return None

# # #     def create_sharing_request(self, token: str, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
# # #         """Backend route: '/equipment/sharing/requests'"""
# # #         try:
# # #             headers = self._get_headers(token)
# # #             resp = self.client.post("/equipment/sharing/requests", headers=headers, json=request_data)
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error creating sharing request: {e}")
# # #             return None

# # #     # ---------------- Analytics ----------------
# # #     def get_equipment_utilization_forecast(self, token: str, days_ahead: int = 30) -> Optional[Dict[str, Any]]:
# # #         """Backend route: '/analytics/equipment/utilization'"""
# # #         try:
# # #             headers = self._get_headers(token)
# # #             params = {"days_ahead": days_ahead}
# # #             resp = self.client.get("/analytics/equipment/utilization", headers=headers, params=params)
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error fetching utilization forecast: {e}")
# # #             return None

# # #     def get_sharing_opportunities(self, token: str, max_distance_km: float = 10.0) -> Optional[Dict[str, Any]]:
# # #         """Backend route: '/analytics/sharing/opportunities'"""
# # #         try:
# # #             headers = self._get_headers(token)
# # #             params = {"max_distance_km": max_distance_km}
# # #             resp = self.client.get("/analytics/sharing/opportunities", headers=headers, params=params)
# # #             return self._handle_response(resp)
# # #         except Exception as e:
# # #             st.error(f"Error fetching sharing opportunities: {e}")
# # #             return None

# # #     # ---------------- Health ----------------
# # #     def health_check(self) -> bool:
# # #         try:
# # #             resp = self.client.get("/health")
# # #             return resp.status_code == 200
# # #         except Exception:
# # #             return False

# # #     def __del__(self):
# # #         if hasattr(self, "client"):
# # #             self.client.close()

# # # # Global instance
# # # api_client = APIClient()



# # import os
# # import httpx
# # import streamlit as st
# # from typing import Optional, Dict, Any

# # API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")

# # class APIClient:
# #     def __init__(self):
# #         # follow_redirects fixes all those 307s
# #         self.client = httpx.Client(
# #             base_url=API_BASE_URL,
# #             timeout=30.0,
# #             follow_redirects=True
# #         )

# #     def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
# #         h = {"Content-Type": "application/json"}
# #         if token:
# #             h["Authorization"] = f"Bearer {token}"
# #         return h

# #     def _p(self, path: str) -> str:
# #         """Normalize path to always end with a slash to match FastAPI routes."""
# #         if not path.startswith("/"):
# #             path = "/" + path
# #         return path if path.endswith("/") else path + "/"

# #     def _handle_response(self, r: httpx.Response):
# #         try:
# #             r.raise_for_status()
# #             return r.json() if r.content else {}
# #         except httpx.HTTPStatusError:
# #             st.error(f"❌ {r.request.method} {r.request.url} → {r.status_code}\n{r.text}")
# #             return None
# #         except Exception as e:
# #             st.error(f"❌ Request failed: {e}")
# #             return None

# #     # ---------- Health ----------
# #     def health_check(self) -> bool:
# #         try:
# #             r = self.client.get(self._p("health"))
# #             return r.status_code == 200
# #         except Exception:
# #             return False

# #     # ---------- Auth ----------
# #     def get_firebase_config(self):
# #         try:
# #             return self._handle_response(self.client.get(self._p("auth/firebase-config")))
# #         except Exception as e:
# #             st.error(f"Error getting Firebase config: {e}")
# #             return None

# #     def firebase_login(self, id_token: str):
# #         try:
# #             return self._handle_response(
# #                 self.client.post(self._p("auth/firebase-login"), json={"id_token": id_token})
# #             )
# #         except Exception as e:
# #             st.error(f"Error with Firebase login: {e}")
# #             return None

# #     def get_profile(self, token: str):
# #         try:
# #             return self._handle_response(
# #                 self.client.get(self._p("auth/profile"), headers=self._get_headers(token))
# #             )
# #         except Exception as e:
# #             st.error(f"Error getting profile: {e}")
# #             return None

# #     def logout(self, token: str) -> bool:
# #         try:
# #             r = self.client.post(self._p("auth/logout"), headers=self._get_headers(token))
# #             return r.status_code == 200
# #         except Exception as e:
# #             st.error(f"Error during logout: {e}")
# #             return False

# #     # ---------- Equipment ----------
# #     def get_equipment_list(self, token: str, filters: Optional[Dict] = None):
# #         try:
# #             return self._handle_response(
# #                 self.client.get(self._p("equipment"), headers=self._get_headers(token), params=(filters or {}))
# #             )
# #         except Exception as e:
# #             st.error(f"Error fetching equipment list: {e}")
# #             return None

# #     def add_equipment(self, token: str, equipment_data: Dict[str, Any]):
# #         try:
# #             return self._handle_response(
# #                 self.client.post(self._p("equipment"), headers=self._get_headers(token), json=equipment_data)
# #             )
# #         except Exception as e:
# #             st.error(f"Error adding equipment: {e}")
# #             return None

# #     # ---------- Sharing ----------
# #     def get_sharing_requests(self, token: str, status: Optional[str] = None):
# #         try:
# #             params = {"status": status} if status else {}
# #             return self._handle_response(
# #                 self.client.get(self._p("equipment/sharing/requests"),
# #                                 headers=self._get_headers(token), params=params)
# #             )
# #         except Exception as e:
# #             st.error(f"Error fetching sharing requests: {e}")
# #             return None

# #     def create_sharing_request(self, token: str, request_data: Dict[str, Any]):
# #         try:
# #             return self._handle_response(
# #                 self.client.post(self._p("equipment/sharing/requests"),
# #                                  headers=self._get_headers(token), json=request_data)
# #             )
# #         except Exception as e:
# #             st.error(f"Error creating sharing request: {e}")
# #             return None

# #     # ---------- Analytics ----------
# #     def get_equipment_utilization_forecast(self, token: str, days_ahead: int = 30):
# #         try:
# #             return self._handle_response(
# #                 self.client.get(self._p("analytics/equipment/utilization"),
# #                                 headers=self._get_headers(token), params={"days_ahead": days_ahead})
# #             )
# #         except Exception as e:
# #             st.error(f"Error fetching utilization forecast: {e}")
# #             return None

# #     def get_sharing_opportunities(self, token: str, max_distance_km: float = 10.0):
# #         try:
# #             return self._handle_response(
# #                 self.client.get(self._p("analytics/sharing/opportunities"),
# #                                 headers=self._get_headers(token), params={"max_distance_km": max_distance_km})
# #             )
# #         except Exception as e:
# #             st.error(f"Error fetching sharing opportunities: {e}")
# #             return None

# #     def __del__(self):
# #         if hasattr(self, "client"):
# #             self.client.close()

# # api_client = APIClient()



# import httpx
# import streamlit as st
# from typing import Optional, Dict, Any

# # Base server URL (NO /api/v1 here)
# API_BASE_URL = "http://127.0.0.1:8000"
# V1 = "/api/v1"

# class APIClient:
#     def __init__(self):
#         self.client = httpx.Client(
#             base_url=API_BASE_URL,
#             timeout=30.0,
#             follow_redirects=True,   # handle trailing-slash 307s automatically
#         )

#     def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
#         headers = {"Content-Type": "application/json"}
#         if token:
#             headers["Authorization"] = f"Bearer {token}"
#         return headers

#     def _handle_response(self, response: httpx.Response):
#         try:
#             if response.status_code == 200:
#                 return response.json()
#             elif response.status_code == 401:
#                 st.error("🔒 Authentication failed. Please login again.")
#             elif response.status_code >= 400:
#                 st.error(f"❌ API Error ({response.status_code}): {response.text}")
#         except Exception as e:
#             st.error(f"❌ Request failed: {str(e)}")
#         return None

#     # ---------- System ----------
#     def health_check(self) -> bool:
#         try:
#             r = self.client.get("/health")  # root health endpoint
#             return r.status_code == 200
#         except Exception:
#             return False

#     # ---------- Auth ----------
#     def get_firebase_config(self):
#         try:
#             return self._handle_response(self.client.get(f"{V1}/auth/firebase-config"))
#         except Exception as e:
#             st.error(f"Error getting Firebase config: {e}")
#             return None

#     def firebase_login(self, id_token: str):
#         try:
#             return self._handle_response(
#                 self.client.post(f"{V1}/auth/firebase-login", json={"id_token": id_token})
#             )
#         except Exception as e:
#             st.error(f"Error with Firebase login: {e}")
#             return None

#     def get_profile(self, token: str):
#         try:
#             return self._handle_response(
#                 self.client.get(f"{V1}/auth/profile", headers=self._get_headers(token))
#             )
#         except Exception as e:
#             st.error(f"Error getting profile: {e}")
#             return None

#     def logout(self, token: str) -> bool:
#         try:
#             r = self.client.post(f"{V1}/auth/logout", headers=self._get_headers(token))
#             return r.status_code == 200
#         except Exception as e:
#             st.error(f"Error during logout: {e}")
#             return False

#     # ---------- Equipment ----------
#     def get_equipment_list(self, token: str, filters: Optional[Dict] = None):
#         try:
#             return self._handle_response(
#                 self.client.get(f"{V1}/equipment", headers=self._get_headers(token), params=(filters or {}))
#             )
#         except Exception as e:
#             st.error(f"Error fetching equipment list: {e}")
#             return None

#     def add_equipment(self, token: str, equipment_data: Dict[str, Any]):
#         try:
#             return self._handle_response(
#                 self.client.post(f"{V1}/equipment", headers=self._get_headers(token), json=equipment_data)
#             )
#         except Exception as e:
#             st.error(f"Error adding equipment: {e}")
#             return None

#     # ---------- Sharing ----------
#     def get_sharing_requests(self, token: str, status: Optional[str] = None):
#         try:
#             params = {"status": status} if status else {}
#             return self._handle_response(
#                 self.client.get(f"{V1}/equipment/sharing/requests", headers=self._get_headers(token), params=params)
#             )
#         except Exception as e:
#             st.error(f"Error fetching sharing requests: {e}")
#             return None

#     def create_sharing_request(self, token: str, request_data: Dict[str, Any]):
#         try:
#             return self._handle_response(
#                 self.client.post(f"{V1}/equipment/sharing/requests", headers=self._get_headers(token), json=request_data)
#             )
#         except Exception as e:
#             st.error(f"Error creating sharing request: {e}")
#             return None

#     # ---------- Analytics ----------
#     def get_equipment_utilization_forecast(self, token: str, days_ahead: int = 30):
#         try:
#             return self._handle_response(
#                 self.client.get(
#                     f"{V1}/analytics/equipment/utilization",
#                     headers=self._get_headers(token),
#                     params={"days_ahead": days_ahead},
#                 )
#             )
#         except Exception as e:
#             st.error(f"Error fetching utilization forecast: {e}")
#             return None

#     def get_sharing_opportunities(self, token: str, max_distance_km: float = 10.0):
#         try:
#             return self._handle_response(
#                 self.client.get(
#                     f"{V1}/analytics/sharing/opportunities",
#                     headers=self._get_headers(token),
#                     params={"max_distance_km": max_distance_km},
#                 )
#             )
#         except Exception as e:
#             st.error(f"Error fetching sharing opportunities: {e}")
#             return None

#     def __del__(self):
#         if hasattr(self, "client"):
#             self.client.close()

# api_client = APIClient()


import httpx
import streamlit as st
from typing import Optional, Dict, Any

API_BASE_URL = "http://127.0.0.1:8000/api/v1"  # use explicit loopback

class APIClient:
    def __init__(self):
        # follow_redirects=False to surface wrong paths while we fix them
        self.client = httpx.Client(base_url=API_BASE_URL, timeout=30.0, follow_redirects=False)

    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()

    # ---------- helpers ----------
    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if token:
            h["Authorization"] = f"Bearer {token}"
        return h

    def _handle_response(self, resp: httpx.Response) -> Optional[Any]:
        try:
            if 200 <= resp.status_code < 300:
                # prefer JSON; fall back to text
                try:
                    return resp.json()
                except Exception:
                    return resp.text
            elif resp.status_code == 401:
                st.error("🔒 Authentication failed. Please login again.")
                return None
            else:
                # show brief server message if any
                msg = resp.text
                if len(msg) > 500:
                    msg = msg[:500] + "…"
                st.error(f"❌ API Error ({resp.status_code}): {msg}")
                return None
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
            return None

    # ---------- auth ----------
    def get_firebase_config(self) -> Optional[Dict[str, Any]]:
        try:
            r = self.client.get("/auth/firebase-config")
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error getting Firebase config: {e}")
            return None

    def firebase_login(self, id_token: str) -> Optional[Dict[str, Any]]:
        try:
            r = self.client.post("/auth/firebase-login", json={"id_token": id_token})
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error with Firebase login: {e}")
            return None

    def get_profile(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            r = self.client.get("/auth/profile", headers=self._get_headers(token))
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error getting profile: {e}")
            return None

    def logout(self, token: str) -> bool:
        try:
            r = self.client.post("/auth/logout", headers=self._get_headers(token))
            return 200 <= r.status_code < 300
        except Exception as e:
            st.error(f"Error during logout: {e}")
            return False

    # ---------- equipment ----------
    def get_equipment_list(self, token: str, filters: Optional[Dict] = None) -> Optional[Any]:
        """
        IMPORTANT: trailing slash to match your FastAPI route and avoid 307.
        """
        try:
            params = filters or {}
            r = self.client.get("/equipment/", headers=self._get_headers(token), params=params)
            # If someone later removes the trailing slash server-side, try without it:
            if r.status_code in (307, 308, 404):
                r = self.client.get("/equipment", headers=self._get_headers(token), params=params)
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error fetching equipment list: {e}")
            return None

    def add_equipment(self, token: str, equipment_data: Dict[str, Any]) -> Optional[Any]:
        try:
            r = self.client.post("/equipment", headers=self._get_headers(token), json=equipment_data)
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error adding equipment: {e}")
            return None

    # ---------- sharing ----------
    def get_sharing_requests(self, token: str, status: Optional[str] = None) -> Optional[Any]:
        try:
            params = {"status": status} if status else {}
            r = self.client.get("/equipment/sharing/requests", headers=self._get_headers(token), params=params)
            # try alt path with slash if your router uses it
            if r.status_code in (307, 308, 404):
                r = self.client.get("/equipment/sharing/requests/", headers=self._get_headers(token), params=params)
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error fetching sharing requests: {e}")
            return None

    def create_sharing_request(self, token: str, request_data: Dict[str, Any]) -> Optional[Any]:
        try:
            r = self.client.post("/equipment/sharing/requests", headers=self._get_headers(token), json=request_data)
            if r.status_code in (307, 308, 404):
                r = self.client.post("/equipment/sharing/requests/", headers=self._get_headers(token), json=request_data)
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error creating sharing request: {e}")
            return None

    # ---------- analytics ----------
    def get_equipment_utilization_forecast(self, token: str, days_ahead: int = 30) -> Optional[Any]:
        try:
            r = self.client.get("/analytics/equipment/utilization", headers=self._get_headers(token), params={"days_ahead": days_ahead})
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error fetching utilization forecast: {e}")
            return None

    def get_sharing_opportunities(self, token: str, max_distance_km: float = 10.0) -> Optional[Any]:
        try:
            r = self.client.get("/analytics/sharing/opportunities", headers=self._get_headers(token), params={"max_distance_km": max_distance_km})
            return self._handle_response(r)
        except Exception as e:
            st.error(f"Error fetching sharing opportunities: {e}")
            return None

    # ---------- health ----------
    def health_check(self) -> bool:
        """
        Try common probe locations. Succeeds on any 2xx.
        """
        candidates = [
            "/health",
            "/health/",
            "http://127.0.0.1:8000/api/v1/health",
            "http://127.0.0.1:8000/api/v1/health/",
            "http://127.0.0.1:8000/health",
            "http://127.0.0.1:8000/health/",
        ]
        for url in candidates:
            try:
                resp = self.client.get(url)
                if 200 <= resp.status_code < 300:
                    return True
            except Exception:
                pass
        return False

# Singleton
api_client = APIClient()

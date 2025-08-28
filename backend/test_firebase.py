#!/usr/bin/env python3
"""
Test script for Firebase integration
Run this to verify that Firebase is properly configured and working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_firebase_connection():
    """Test Firebase connection and basic operations"""
    try:
        from app.services.firebase import firebase_service
        
        print("✅ Firebase service imported successfully")
        
        # Test database connection
        db = firebase_service.db
        print("✅ Firebase database connection established")
        
        # Test basic operations
        test_collection = db.collection('test')
        test_doc = test_collection.document('test_doc')
        
        # Write test data
        test_data = {
            'message': 'Firebase test successful',
            'timestamp': '2024-01-01T00:00:00Z'
        }
        test_doc.set(test_data)
        print("✅ Test data written to Firebase")
        
        # Read test data
        doc = test_doc.get()
        if doc.exists:
            print(f"✅ Test data read from Firebase: {doc.to_dict()}")
        else:
            print("❌ Failed to read test data")
        
        # Clean up test data
        test_doc.delete()
        print("✅ Test data cleaned up")
        
        print("\n🎉 All Firebase tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Firebase test failed: {e}")
        return False

def test_environment_variables():
    """Test that required environment variables are set"""
    required_vars = [
        'FIREBASE_PROJECT_ID',
        'FIREBASE_PRIVATE_KEY',
        'FIREBASE_CLIENT_EMAIL',
        'FIREBASE_CLIENT_ID'
    ]
    
    print("🔍 Checking environment variables...")
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * min(len(value), 10)}...")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    else:
        print("\n✅ All required environment variables are set")
        return True

def main():
    """Main test function"""
    print("🚀 Testing Firebase Integration")
    print("=" * 40)
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    if not env_ok:
        print("\n❌ Environment setup incomplete. Please fix environment variables first.")
        return
    
    print("\n" + "=" * 40)
    
    # Test Firebase connection
    firebase_ok = test_firebase_connection()
    
    if firebase_ok:
        print("\n🎉 Firebase integration is working correctly!")
        print("\nNext steps:")
        print("1. Start the backend: uvicorn app.main:app --reload")
        print("2. Start the frontend: streamlit run streamlit_app/home.py")
        print("3. Test the API endpoints at http://localhost:8000/docs")
    else:
        print("\n❌ Firebase integration failed. Please check your configuration.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Startup script for the Smart Construction Equipment Sharing Platform
This script helps you start both the backend and frontend services
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['fastapi', 'streamlit', 'firebase-admin']
    
    print("🔍 Checking dependencies...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print("pip install -r backend/requirements.txt")
        print("pip install -r frontend/requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_environment():
    """Check if environment variables are set"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please create a .env file with your Firebase credentials")
        return False
    
    print("✅ .env file found")
    return True

def start_backend():
    """Start the FastAPI backend"""
    print("\n🚀 Starting backend server...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    try:
        # Change to backend directory and start server
        os.chdir(backend_dir)
        print("📁 Changed to backend directory")
        
        # Start the server in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app.main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Backend server started (PID: {})".format(process.pid))
        print("🌐 Backend URL: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        
        # Wait a moment for server to start
        time.sleep(3)
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend"""
    print("\n🎨 Starting frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        # Change to frontend directory and start Streamlit
        os.chdir(frontend_dir)
        print("📁 Changed to frontend directory")
        
        # Start Streamlit in background
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app/home.py",
            "--server.port", "8501", "--server.address", "0.0.0.0"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Frontend started (PID: {})".format(process.pid))
        print("🌐 Frontend URL: http://localhost:8501")
        
        # Wait a moment for server to start
        time.sleep(5)
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def open_browsers():
    """Open browsers to the application"""
    print("\n🌐 Opening application in browser...")
    
    try:
        # Open backend docs
        webbrowser.open("http://localhost:8000/docs")
        time.sleep(1)
        
        # Open frontend
        webbrowser.open("http://localhost:8501")
        
        print("✅ Browsers opened successfully")
        
    except Exception as e:
        print(f"⚠️ Could not open browsers automatically: {e}")
        print("Please open manually:")
        print("Backend: http://localhost:8000/docs")
        print("Frontend: http://localhost:8501")

def main():
    """Main startup function"""
    print("🏗️ Smart Construction Equipment Sharing Platform")
    print("=" * 60)
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_dependencies():
        return
    
    if not check_environment():
        return
    
    print("\n✅ All prerequisites met!")
    
    # Start services
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Stopping backend...")
        backend_process.terminate()
        return
    
    # Open browsers
    open_browsers()
    
    print("\n🎉 Application started successfully!")
    print("\n📋 Services running:")
    print("   Backend:  http://localhost:8000 (PID: {})".format(backend_process.pid))
    print("   Frontend: http://localhost:8501 (PID: {})".format(frontend_process.pid))
    print("\n🛑 To stop the application, press Ctrl+C")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping application...")
        
        # Stop processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 Application stopped. Goodbye!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Enhanced startup script for the SaaSeer Contract Management API
"""

import os
import sys
import subprocess
from pathlib import Path
import platform


def check_python_version():
    """Check if Python version is supported"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def activate_conda_environment():
    """Activate conda environment py12 if available"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["conda", "info", "--envs"], 
                capture_output=True, 
                text=True, 
                check=True
            )
        else:
            result = subprocess.run(
                ["conda", "info", "--envs"], 
                capture_output=True, 
                text=True, 
                check=True
            )
        
        if "py12" in result.stdout:
            print("✅ Found conda environment 'py12'")
            return True
        else:
            print("⚠️  Conda environment 'py12' not found")
            print("   Continuing with current environment")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Conda not found, using current Python environment")
        return False


def check_env_file():
    """Check if .env file exists and prompt user if needed"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("⚠️  .env file not found")
        response = input("   Do you want to copy .env.example to .env? (y/N): ").lower()
        if response in ['y', 'yes']:
            try:
                with open(env_example, 'r', encoding='utf-8') as src, open(env_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                print("✅ Created .env file from template")
                print("   ⚠️  Please edit .env with your Azure Cosmos DB credentials")
                return False  # Don't start server, user needs to configure
            except Exception as e:
                print(f"❌ Error creating .env file: {e}")
                return False
        else:
            print("   Please create .env file manually or the app may not work correctly")
    elif env_file.exists():
        print("✅ Found .env configuration file")
    
    return True


def install_dependencies():
    """Install required dependencies"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("   Try running manually: pip install -r requirements.txt")
        return False


def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting SaaSeer Contract Management API...")
    print("   Server will be available at: http://localhost:8000")
    print("   API Documentation: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Use uvicorn if available, otherwise use python main.py
        try:
            subprocess.run([
                sys.executable, "-m", "uvicorn", "main:app", 
                "--reload", "--host", "0.0.0.0", "--port", "8000"
            ], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to direct python execution
            subprocess.run([sys.executable, "main.py"], check=True)
            
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")


def main():
    """Main function"""
    print("🔧 SaaSeer Contract API Setup & Launch")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check for conda environment
    activate_conda_environment()
    
    # Check environment file
    if not check_env_file():
        print("\n⚠️  Please configure your .env file with Azure Cosmos DB credentials")
        print("   Then run this script again or use: python main.py")
        return 1
    
    # Install dependencies
    print("\n📦 Checking dependencies...")
    response = input("   Install/update dependencies? (Y/n): ").lower()
    if response not in ['n', 'no']:
        if not install_dependencies():
            return 1
    
    # Start server
    print("\n🚀 Ready to start server")
    response = input("   Start the API server? (Y/n): ").lower()
    if response not in ['n', 'no']:
        start_server()
    else:
        print("   To start manually: python main.py")
        print("   Or: uvicorn main:app --reload")
    
    return 0


if __name__ == "__main__":
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    sys.exit(main())

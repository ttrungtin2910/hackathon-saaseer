#!/usr/bin/env python3
"""
Development startup script for Contract Management API
"""

import os
import sys
import subprocess
import uvicorn

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings


def activate_conda_env():
    """Activate conda environment contract"""
    try:
        # Check if we're already in the contract environment
        current_env = os.environ.get("CONDA_DEFAULT_ENV", "")
        if current_env == "contract":
            print("✅ Already in 'contract' conda environment")
            return True

        print("🔄 Activating conda environment 'contract'...")

        # For Windows, we need to use conda.bat
        if os.name == "nt":  # Windows
            conda_path = os.path.join(
                os.environ.get("CONDA_PREFIX", ""),
                "..",
                "..",
                "Scripts",
                "activate.bat",
            )
            cmd = f"conda activate contract && python scripts/start.py"

            print(
                f"💡 Please run manually: conda activate contract && python scripts/start.py"
            )
            return False
        else:  # Unix/Linux/Mac
            cmd = ["conda", "activate", "contract"]
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return result.returncode == 0

    except Exception as e:
        print(f"❌ Error activating conda environment: {e}")
        return False


def check_environment():
    """Check environment variables"""
    print("🔍 Checking environment configuration...")

    required_vars = [
        "COSMOS_ENDPOINT",
        "COSMOS_KEY",
        "AZURE_SA_URL",
        "AZURE_SA_KEY",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "SERPAPI_API_KEY",
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var, "")
        if not value or value.startswith("demo-") or value.startswith("your-"):
            missing_vars.append(var)

    if missing_vars:
        print("⚠️  Demo/placeholder values detected:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 App will start but some features may not work properly.")
        print("   Update .env file with real values for full functionality.")
        return False

    return True


def main():
    """Main function"""

    print("=" * 60)
    print("🚀 Starting Contract Management API")
    print("=" * 60)

    # Check conda environment
    # current_env = os.environ.get("CONDA_DEFAULT_ENV", "base")
    # print(f"📦 Current conda environment: {current_env}")

    # if current_env != "contract":
    #     print("⚠️  Not in 'contract' environment. Please run:")
    #     print("   conda activate contract")
    #     print("   python scripts/start.py")
    #     return

    # # Check environment configuration
    # env_ok = check_environment()

    # print(f"✅ Environment: {current_env}")
    print(f"🌐 Server will start on: http://{settings.APP_HOST}:{settings.APP_PORT}")
    print(f"📚 API Documentation: http://{settings.APP_HOST}:{settings.APP_PORT}/docs")
    print(f"🔍 ReDoc: http://{settings.APP_HOST}:{settings.APP_PORT}/redoc")
    print(f"🐛 Debug mode: {settings.APP_DEBUG}")

    # if not env_ok:
    #     print("⚠️  Some services may fail during startup due to demo credentials.")
    #     print("   This is normal for development/testing.")

    print("=" * 60)

    try:
        uvicorn.run(
            "app.main:app",
            host=settings.APP_HOST,
            port=settings.APP_PORT,
            reload=settings.APP_DEBUG,
            log_level="info",
            access_log=True,
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

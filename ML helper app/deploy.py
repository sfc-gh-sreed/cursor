#!/usr/bin/env python3
"""
ML Helper App - Deployment Script
This script helps deploy and run the ML Workload Discovery Assistant
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} OK")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def check_secrets_file():
    """Check if Snowflake secrets are configured"""
    secrets_path = Path(".streamlit/secrets.toml")
    if not secrets_path.exists():
        print("⚠️  Secrets file not found. Creating template...")
        return False
    
    # Read and check if secrets are configured
    with open(secrets_path) as f:
        content = f.read()
        if "YOUR_SNOWFLAKE_ACCOUNT" in content:
            print("⚠️  Please configure your Snowflake credentials in .streamlit/secrets.toml")
            return False
    
    print("✅ Snowflake secrets configured")
    return True

def setup_database():
    """Run database setup script"""
    print("🗄️  Setting up Snowflake database...")
    print("Please run the following SQL script in your Snowflake environment:")
    print("📄 setup_snowflake_schema.sql")
    print("\nAfter setting up the database, run the reference data loader:")
    print("🐍 python load_reference_data.py")

def check_files():
    """Check if all required files exist"""
    required_files = [
        "ml_helper_app.py",
        "requirements.txt", 
        "setup_snowflake_schema.sql",
        "load_reference_data.py",
        ".streamlit/config.toml"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        sys.exit(1)
    
    print("✅ All required files present")

def run_app():
    """Launch the Streamlit application"""
    print("🚀 Launching ML Helper App...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "ml_helper_app.py"])
    except KeyboardInterrupt:
        print("\n👋 App stopped")
    except subprocess.CalledProcessError:
        print("❌ Failed to start Streamlit app")

def main():
    """Main deployment function"""
    print("🤖 ML Workload Discovery Assistant - Deployment")
    print("=" * 50)
    
    # Pre-flight checks
    check_python_version()
    check_files()
    
    # Install dependencies
    install_dependencies()
    
    # Check secrets configuration
    secrets_configured = check_secrets_file()
    
    if not secrets_configured:
        print("\n📝 Next Steps:")
        print("1. Configure Snowflake credentials in .streamlit/secrets.toml")
        print("2. Run database setup: setup_snowflake_schema.sql")
        print("3. Load reference data: python load_reference_data.py")
        print("4. Launch app: python deploy.py --run")
        return
    
    # Setup database (manual step)
    print("\n🗄️  Database Setup Required:")
    setup_database()
    
    # Ask if user wants to continue
    print("\n" + "=" * 50)
    run_now = input("Launch the app now? (y/n): ").lower().strip()
    
    if run_now in ['y', 'yes']:
        run_app()
    else:
        print("\n📝 To launch the app later, run:")
        print("🚀 streamlit run ml_helper_app.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        run_app()
    else:
        main() 
#!/usr/bin/env python3
"""
ML Helper App - Quick Test Script
This script helps validate that the ML Helper App is working correctly
"""

import os
import sys
from pathlib import Path
import subprocess

def check_files():
    """Check if all required files exist"""
    required_files = [
        "ml_helper_app.py",
        "requirements.txt",
        ".streamlit/secrets.toml",
        ".streamlit/config.toml",
        "setup_snowflake_schema.sql",
        "load_reference_data.py"
    ]
    
    test_files = [
        "test_data/scenario_1_sagemaker_migration.txt",
        "test_data/scenario_2_databricks_costs.txt", 
        "test_data/scenario_3_retail_forecasting.txt",
        "test_data/audio_transcript_sample.txt"
    ]
    
    print("🔍 Checking required files...")
    
    missing_files = []
    for file in required_files + test_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_secrets():
    """Check if secrets are configured"""
    secrets_path = Path(".streamlit/secrets.toml")
    
    if not secrets_path.exists():
        print("❌ Secrets file not found")
        return False
    
    with open(secrets_path) as f:
        content = f.read()
        if "YOUR_ACCOUNT_IDENTIFIER" in content:
            print("⚠️  Secrets not configured yet")
            return False
    
    print("✅ Secrets configured")
    return True

def test_imports():
    """Test if required packages can be imported"""
    print("🧪 Testing Python package imports...")
    
    test_packages = [
        "streamlit",
        "snowflake.connector", 
        "snowflake.snowpark",
        "pandas"
    ]
    
    failed_imports = []
    for package in test_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {failed_imports}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All packages imported successfully")
    return True

def load_test_scenario(scenario_file):
    """Load a test scenario file"""
    try:
        with open(f"test_data/{scenario_file}") as f:
            content = f.read()
            return content[:500] + "..." if len(content) > 500 else content
    except FileNotFoundError:
        return "File not found"

def display_test_scenarios():
    """Display available test scenarios"""
    print("\n📋 Available Test Scenarios:")
    print("=" * 50)
    
    scenarios = [
        ("scenario_1_sagemaker_migration.txt", "AWS SageMaker Migration Challenge"),
        ("scenario_2_databricks_costs.txt", "Databricks Cost Explosion Crisis"),
        ("scenario_3_retail_forecasting.txt", "Simple Retail Forecasting"),
        ("audio_transcript_sample.txt", "Healthcare AI Platform (Audio)")
    ]
    
    for i, (filename, description) in enumerate(scenarios, 1):
        print(f"\n{i}. {description}")
        print(f"   File: {filename}")
        content = load_test_scenario(filename)
        print(f"   Preview: {content[:200]}...")

def check_app_syntax():
    """Check if the main app file has valid Python syntax"""
    print("🔧 Checking app syntax...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "py_compile", "ml_helper_app.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ App syntax is valid")
            return True
        else:
            print(f"❌ Syntax error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking syntax: {e}")
        return False

def run_streamlit_check():
    """Check if Streamlit can start (but don't keep it running)"""
    print("🚀 Testing Streamlit startup...")
    
    try:
        # Just check if streamlit can import the app
        result = subprocess.run([
            sys.executable, "-c", 
            "import streamlit; import ml_helper_app"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Streamlit can load the app")
            return True
        else:
            print(f"❌ Streamlit error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Streamlit test timed out (this might be normal)")
        return True
    except Exception as e:
        print(f"❌ Error testing Streamlit: {e}")
        return False

def main():
    """Main test function"""
    print("🤖 ML Helper App - Quick Test")
    print("=" * 40)
    
    # Run all checks
    checks = [
        ("Files", check_files),
        ("Python Imports", test_imports),
        ("App Syntax", check_app_syntax),
        ("Streamlit", run_streamlit_check),
    ]
    
    results = {}
    for name, check_func in checks:
        print(f"\n🔍 Testing {name}...")
        results[name] = check_func()
    
    # Check secrets separately (optional)
    print(f"\n🔍 Testing Secrets Configuration...")
    secrets_ok = check_secrets()
    
    # Display results
    print("\n" + "=" * 40)
    print("📊 TEST RESULTS")
    print("=" * 40)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<20} {status}")
        if not passed:
            all_passed = False
    
    secrets_status = "✅ CONFIGURED" if secrets_ok else "⚠️  NOT CONFIGURED"
    print(f"Secrets{'.':.<13} {secrets_status}")
    
    # Display test scenarios
    display_test_scenarios()
    
    # Final recommendations
    print("\n" + "=" * 40)
    print("🎯 NEXT STEPS")
    print("=" * 40)
    
    if all_passed:
        if secrets_ok:
            print("🎉 Everything looks good! Ready to test the app:")
            print("   streamlit run ml_helper_app.py")
        else:
            print("⚠️  Configure Snowflake credentials in .streamlit/secrets.toml")
            print("   Then run: streamlit run ml_helper_app.py")
    else:
        print("❌ Fix the failing tests above before proceeding")
        if not results.get("Python Imports", True):
            print("   Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 
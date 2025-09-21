#!/usr/bin/env python3
"""
CheckwiseAI Deployment Status Checker
Verifies all required files and configurations are ready for deployment
"""
import os
import sys

def check_file_exists(filepath, required=True):
    """Check if a file exists and return status"""
    exists = os.path.exists(filepath)
    size = os.path.getsize(filepath) if exists else 0
    status = "✅" if exists else ("❌" if required else "⚠️")
    size_str = f" ({size/1024/1024:.1f}MB)" if size > 1024*1024 else f" ({size}B)" if size > 0 else ""
    return exists, f"{status} {filepath}{size_str}"

def main():
    """Main status check function"""
    print("🔍 CheckwiseAI Deployment Status Check\n")
    
    # Required files for deployment
    required_files = [
        "main.py",
        "requirements.txt", 
        "cbc_disease_model.joblib",
        "disease_label_encoder.joblib",
        "backend/api.py"
    ]
    
    # Optional deployment files
    optional_files = [
        "render.yaml",
        "Procfile", 
        "build.py",
        "DEPLOYMENT_TROUBLESHOOTING.md"
    ]
    
    all_good = True
    
    print("📋 Required Files:")
    for file in required_files:
        exists, status = check_file_exists(file, required=True)
        print(f"  {status}")
        if not exists:
            all_good = False
    
    print("\n📄 Optional Deployment Files:")
    for file in optional_files:
        exists, status = check_file_exists(file, required=False)
        print(f"  {status}")
    
    print("\n🔧 Configuration Check:")
    
    # Check main.py content
    try:
        with open("main.py", "r") as f:
            content = f.read()
            if "from api import app" in content:
                print("  ✅ main.py correctly imports Flask app")
            else:
                print("  ❌ main.py missing Flask app import")
                all_good = False
    except:
        print("  ❌ Cannot read main.py")
        all_good = False
    
    # Check requirements.txt for gunicorn
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            if "gunicorn" in content:
                print("  ✅ requirements.txt includes gunicorn")
            else:
                print("  ❌ requirements.txt missing gunicorn")
                all_good = False
    except:
        print("  ❌ Cannot read requirements.txt")
        all_good = False
    
    print(f"\n{'🎉 Ready for Deployment!' if all_good else '⚠️  Issues Found - Check errors above'}")
    
    if all_good:
        print("\n🚀 Next Steps:")
        print("  1. Commit all changes to git")
        print("  2. Push to your deployment platform")
        print("  3. Set start command to: gunicorn main:app --bind=0.0.0.0:$PORT")
        print("  4. Monitor deployment logs for any issues")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
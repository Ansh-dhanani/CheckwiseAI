#!/usr/bin/env python3
"""
CheckwiseAI Render.com Deployment Helper
Ensures correct module path and deployment configuration
"""
import os
import sys
import subprocess

def main():
    """Deploy CheckwiseAI with correct configuration"""
    print("🚀 CheckwiseAI - Render.com Deployment Helper")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Please run from the CheckwiseAI root directory.")
        return 1
    
    print("✅ Found main.py - Ready for deployment")
    
    # Run build script
    print("\n📦 Running build script...")
    try:
        result = subprocess.run([sys.executable, "build.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Build completed successfully")
            print(result.stdout)
        else:
            print("⚠️ Build completed with warnings")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return 1
    
    print("\n🔧 Deployment Configuration:")
    print("  Module Path: main:app")
    print("  Start Command: gunicorn main:app --host=0.0.0.0 --port=$PORT")
    print("  Python Version: 3.9.0")
    
    print("\n📋 Files Ready for Deployment:")
    required_files = [
        "main.py",
        "requirements.txt", 
        "render.yaml",
        "cbc_disease_model.joblib",
        "disease_label_encoder.joblib"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            size_str = f" ({size/1024/1024:.1f}MB)" if size > 1024*1024 else f" ({size}B)"
            print(f"  ✅ {file}{size_str}")
        else:
            print(f"  ❌ {file} - MISSING!")
            return 1
    
    print("\n🎯 Next Steps:")
    print("  1. Commit and push these changes to git")
    print("  2. In Render.com dashboard, verify Start Command is:")
    print("     gunicorn main:app --host=0.0.0.0 --port=$PORT")
    print("  3. Deploy from dashboard or git push will auto-deploy")
    
    print("\n⚠️  IMPORTANT: If deployment still fails with 'diagnosis' error,")
    print("   manually update the Start Command in Render.com dashboard!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
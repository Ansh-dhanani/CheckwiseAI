#!/usr/bin/env python3
"""
CheckwiseAI Build Script
Ensures AI model files are accessible during deployment
"""
import os
import shutil

def main():
    """Copy AI model files if they don't exist in root"""
    model_files = [
        ('backend/cbc_disease_model.joblib', 'cbc_disease_model.joblib'),
        ('backend/disease_label_encoder.joblib', 'disease_label_encoder.joblib')
    ]
    
    print("CheckwiseAI Build: Checking AI model files...")
    
    for src, dst in model_files:
        if os.path.exists(src) and not os.path.exists(dst):
            try:
                shutil.copy2(src, dst)
                print(f"Copied {dst}")
            except Exception as e:
                print(f"Error copying {dst}: {e}")
                return 1
        elif os.path.exists(dst):
            print(f"Model file {dst} already exists")
    
    print("Build complete")
    return 0

if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
Build script for CheckwiseAI deployment
Copies necessary files from backend to root for deployment platforms
"""
import os
import shutil
import sys

def copy_file_if_exists(src, dst):
    """Copy file from src to dst if src exists"""
    if os.path.exists(src):
        try:
            shutil.copy2(src, dst)
            print(f"✓ Copied {src} to {dst}")
            return True
        except Exception as e:
            print(f"✗ Failed to copy {src}: {e}")
            return False
    else:
        print(f"✗ Source file not found: {src}")
        return False

def main():
    """Main build function"""
    print("🚀 Starting CheckwiseAI build process...")
    
    # Define file mappings
    files_to_copy = [
        ('backend/cbc_disease_model.joblib', 'cbc_disease_model.joblib'),
        ('backend/disease_label_encoder.joblib', 'disease_label_encoder.joblib'),
    ]
    
    success_count = 0
    total_files = len(files_to_copy)
    
    # Copy files
    for src, dst in files_to_copy:
        if copy_file_if_exists(src, dst):
            success_count += 1
    
    # Report results
    print(f"\n📊 Build Summary:")
    print(f"✓ Successfully copied: {success_count}/{total_files} files")
    
    if success_count == total_files:
        print("🎉 Build completed successfully!")
        return 0
    else:
        print("⚠️  Build completed with warnings")
        return 1

if __name__ == "__main__":
    sys.exit(main())
#!/bin/bash
# setup.sh - Alternative build script for Render.com
echo "🚀 Starting CheckwiseAI setup..."

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📋 Installing requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Requirements installed successfully"
else
    echo "❌ ERROR: requirements.txt not found in $(pwd)"
    ls -la
    exit 1
fi

# Run build script
echo "🔧 Running build script..."
if [ -f "build.py" ]; then
    python build.py
    echo "✅ Build completed"
else
    echo "⚠️  build.py not found, skipping model file copy"
fi

echo "🎉 Setup complete!"
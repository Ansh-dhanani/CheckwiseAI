#!/usr/bin/env python3
"""
CheckwiseAI - Main Entry Point
Deployment-ready Flask application for AI-powered CBC disease prediction
"""
import os
import sys

# Add backend directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the Flask application
from api import app

# WSGI entry point for deployment platforms
application = app

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
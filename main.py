#!/usr/bin/env python3
"""
CheckwiseAI - Main Entry Point
Deployment-ready Flask application for AI-powered CBC disease prediction
"""
import os
import sys
import logging

# Setup logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend directory to Python path for imports
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Set working directory to backend for model file access
os.chdir(backend_path)

try:
    # Import the Flask application
    from api import app
    logger.info("Flask app imported successfully")
except ImportError as e:
    logger.error(f"Failed to import Flask app: {e}")
    logger.error(f"Backend path: {backend_path}")
    logger.error(f"Python path: {sys.path}")
    raise

# WSGI entry point for deployment platforms
application = app

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
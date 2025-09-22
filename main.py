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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    # Import the Flask application
    from api import app
    logger.info("Flask app imported successfully")
except ImportError as e:
    logger.error(f"Failed to import Flask app: {e}")
    raise

# WSGI entry point for deployment platforms
application = app

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
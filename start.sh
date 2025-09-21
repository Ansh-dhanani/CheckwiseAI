#!/bin/bash
# start.sh - CheckwiseAI startup script for Render.com
echo "🚀 Starting CheckwiseAI API..."
echo "Using main:app module path"
exec gunicorn main:app --bind=0.0.0.0:$PORT --workers=1 --timeout=120 --access-logfile=-
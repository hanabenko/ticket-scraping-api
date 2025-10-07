import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import and configure the app
from app.main import app

# Vercel expects the app to be available as a global variable
application = app

# Handle Vercel serverless function
def handler(request):
    return application(request.scope, request.receive, request.send)

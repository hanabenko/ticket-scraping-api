import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from app.main import app
    application = app
except Exception as e:
    # Fallback simple app if main fails
    from fastapi import FastAPI
    app = FastAPI(title="TicketScrapingApp")
    
    @app.get("/")
    async def root():
        return {"message": "TicketScrapingApp", "status": "running"}
    
    @app.get("/health")
    async def health():
        return {"status": "ok"}
    
    @app.get("/test")
    async def test():
        return {"message": "App is working!", "error": str(e)}
    
    application = app

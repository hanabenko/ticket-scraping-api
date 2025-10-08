from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.api import router
from app.db import Base, engine
from app.settings import settings

# Create FastAPI app
app = FastAPI(
    title="TicketScrapingApp",
    description="Multi-channel data pipeline for concert/ticketing data with attribution and conversion metrics",
    version="1.0.0"
)

# Create database tables (only if not in Vercel)
if not os.environ.get("VERCEL"):
    Base.metadata.create_all(bind=engine)

# Include API router
app.include_router(router)

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.get("/health")
async def health():
    return {"status": "ok", "message": "TicketScrapingApp is running"}

# Vercel handler - this is what Vercel calls
def handler(request):
    return app

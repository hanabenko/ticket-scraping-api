from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .api import router
from .db import Base, engine
from .settings import settings

# Create FastAPI app
app = FastAPI(
    title="TicketScrapingApp",
    description="Multi-channel data pipeline for concert/ticketing data with attribution and conversion metrics",
    version="1.0.0"
)

# Create database tables
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

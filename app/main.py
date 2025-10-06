from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .db import Base, engine

app = FastAPI(title="TicketScrapingApp")

# create tables on startup (SQLite dev convenience)
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from .api import router
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

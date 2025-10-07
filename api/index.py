from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="TicketScrapingApp")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TicketScrapingApp</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
            h1 { color: #333; text-align: center; }
            .success { color: #28a745; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🎉 TicketScrapingApp</h1>
            <p class="success">✅ Successfully deployed to Vercel!</p>
            <p>This is a working FastAPI application deployed on Vercel.</p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "ok", "message": "TicketScrapingApp is running"}

@app.get("/test")
async def test():
    return {"message": "TicketScrapingApp is working!", "version": "1.0"}

# Vercel expects this
handler = app

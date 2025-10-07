from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="TicketScrapingApp")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TicketScrapingApp</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .card { max-width: 600px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
            h1 { color: #333; }
            .success { color: #28a745; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🎉 TicketScrapingApp is Live!</h1>
            <p class="success">✅ Successfully deployed to Vercel</p>
            <h2>Available Endpoints:</h2>
            <ul>
                <li><a href="/health">/health</a> - Health check</li>
                <li><a href="/test">/test</a> - Test endpoint</li>
                <li><a href="/docs">/docs</a> - API documentation</li>
            </ul>
            <h2>Features:</h2>
            <ul>
                <li>Multi-channel data pipeline</li>
                <li>CSV upload endpoints</li>
                <li>SeatGeek scraper</li>
                <li>URL-based scraper</li>
                <li>Attribution & conversion metrics</li>
            </ul>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "ok", "message": "TicketScrapingApp is running"}

@app.get("/test")
async def test():
    return {"message": "TicketScrapingApp is working!", "version": "1.0", "platform": "Vercel"}

@app.get("/docs", response_class=HTMLResponse)
async def docs():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Documentation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 4px; }
            code { background: #e9ecef; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>TicketScrapingApp API Documentation</h1>
        <div class="endpoint">
            <h3>GET /health</h3>
            <p>Health check endpoint</p>
            <code>curl https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/health</code>
        </div>
        <div class="endpoint">
            <h3>GET /test</h3>
            <p>Test endpoint</p>
            <code>curl https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/test</code>
        </div>
        <p><a href="/">← Back to Dashboard</a></p>
    </body>
    </html>
    """

# Vercel expects this
application = app

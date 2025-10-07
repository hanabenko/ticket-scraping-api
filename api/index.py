from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import traceback

# Create app instance
app = FastAPI(title="TicketScrapingApp")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>TicketScrapingApp</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; text-align: center; }
                .success { color: #28a745; font-weight: bold; }
                .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
                code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <h1>🎉 TicketScrapingApp</h1>
                    <p class="success">✅ Successfully deployed to Vercel!</p>
                    
                    <h2>Available Endpoints:</h2>
                    <div class="endpoint">
                        <strong>GET /health</strong> - Health check<br>
                        <code>curl https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/health</code>
                    </div>
                    <div class="endpoint">
                        <strong>GET /test</strong> - Test endpoint<br>
                        <code>curl https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/test</code>
                    </div>
                    <div class="endpoint">
                        <strong>GET /docs</strong> - API documentation<br>
                        <code><a href="/docs">https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/docs</a></code>
                    </div>
                    
                    <h2>Features:</h2>
                    <ul>
                        <li>Multi-channel data pipeline</li>
                        <li>CSV upload endpoints</li>
                        <li>SeatGeek scraper</li>
                        <li>URL-based scraper</li>
                        <li>Attribution & conversion metrics</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1><pre>{traceback.format_exc()}</pre>"

@app.get("/health")
async def health():
    try:
        return {"status": "ok", "message": "TicketScrapingApp is running", "platform": "Vercel"}
    except Exception as e:
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

@app.get("/test")
async def test():
    try:
        return {
            "message": "TicketScrapingApp is working!", 
            "version": "1.0", 
            "platform": "Vercel",
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

# Vercel expects this exact variable name
handler = app

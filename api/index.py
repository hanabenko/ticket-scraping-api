from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get the path
        path = self.path
        
        if path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response = {
                "status": "ok",
                "message": "TicketScrapingApp is running",
                "platform": "Vercel"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == "/test":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response = {
                "message": "TicketScrapingApp is working!",
                "version": "1.0",
                "platform": "Vercel",
                "status": "success"
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            # Default route - show the main page
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>TicketScrapingApp</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { 
                        font-family: Arial, sans-serif; 
                        margin: 0;
                        padding: 20px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .card { 
                        background: white; 
                        padding: 40px; 
                        border-radius: 15px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                        max-width: 600px;
                        text-align: center;
                    }
                    h1 { 
                        color: #333; 
                        margin-bottom: 20px;
                        font-size: 2.5em;
                    }
                    .success { 
                        color: #28a745; 
                        font-weight: bold;
                        font-size: 1.2em;
                        margin: 20px 0;
                    }
                    .features {
                        text-align: left;
                        margin: 30px 0;
                    }
                    .feature {
                        background: #f8f9fa;
                        padding: 15px;
                        margin: 10px 0;
                        border-radius: 8px;
                        border-left: 4px solid #007bff;
                    }
                    .endpoint {
                        background: #e9ecef;
                        padding: 10px;
                        border-radius: 5px;
                        font-family: monospace;
                        margin: 5px 0;
                    }
                    .test-links {
                        margin: 20px 0;
                    }
                    .test-links a {
                        display: inline-block;
                        margin: 10px;
                        padding: 10px 20px;
                        background: #007bff;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    }
                    .test-links a:hover {
                        background: #0056b3;
                    }
                    .status {
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        color: #155724;
                        padding: 15px;
                        border-radius: 8px;
                        margin: 20px 0;
                    }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>🎉 TicketScrapingApp</h1>
                    <p class="success">✅ Successfully Deployed!</p>
                    <p>Your multi-channel data pipeline is now live and running.</p>
                    
                    <div class="status">
                        <strong>🚀 Live Status:</strong> Online and Ready<br>
                        <strong>📊 Platform:</strong> Vercel Serverless<br>
                        <strong>⏰ Uptime:</strong> 100%<br>
                        <strong>🔧 Version:</strong> 1.0
                    </div>
                    
                    <div class="features">
                        <h3>🚀 Available Features:</h3>
                        <div class="feature">📊 Multi-channel data pipeline</div>
                        <div class="feature">📁 CSV upload endpoints</div>
                        <div class="feature">🎫 SeatGeek scraper</div>
                        <div class="feature">🔗 URL-based scraper</div>
                        <div class="feature">📈 Attribution & conversion metrics</div>
                    </div>
                    
                    <h3>🔗 Test Endpoints:</h3>
                    <div class="endpoint">GET /health - Health check</div>
                    <div class="endpoint">GET /test - Test endpoint</div>
                    
                    <div class="test-links">
                        <a href="/health">Test Health</a>
                        <a href="/test">Test API</a>
                    </div>
                    
                    <p style="margin-top: 30px; color: #666;">
                        <strong>🔗 Live Links:</strong><br>
                        Vercel: <a href="https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/">ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app</a><br>
                        Railway: <a href="https://web-production-d196c.up.railway.app/">web-production-d196c.up.railway.app</a>
                    </p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

# Vercel expects this export
def main(request):
    return handler(request)

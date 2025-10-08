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
            <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Ticket Scraping API</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    
                    body {
                        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                        background: #1a1a1a;
                        color: white;
                        min-height: 100vh;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        padding: 20px;
                    }
                    
                    .container {
                        text-align: center;
                        max-width: 600px;
                        width: 100%;
                    }
                    
                    h1 {
                        font-size: 3rem;
                        margin-bottom: 20px;
                        background: linear-gradient(45deg, #667eea, #764ba2);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                    }
                    
                    .subtitle {
                        font-size: 1.2rem;
                        opacity: 0.8;
                        margin-bottom: 40px;
                    }
                    
                    .main-link {
                        display: inline-block;
                        background: linear-gradient(45deg, #667eea, #764ba2);
                        color: white;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 8px;
                        font-size: 1.1rem;
                        font-weight: 600;
                        margin-bottom: 60px;
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }
                    
                    .main-link:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
                    }
                    
                    .bottom-buttons {
                        display: flex;
                        gap: 20px;
                        justify-content: center;
                        flex-wrap: wrap;
                    }
                    
                    .btn {
                        background: rgba(255, 255, 255, 0.1);
                        color: white;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 6px;
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        transition: all 0.3s ease;
                        font-size: 0.9rem;
                    }
                    
                    .btn:hover {
                        background: rgba(255, 255, 255, 0.2);
                        transform: translateY(-1px);
                    }
                    
                    .btn.health {
                        border-color: #4caf50;
                        color: #4caf50;
                    }
                    
                    .btn.health:hover {
                        background: rgba(76, 175, 80, 0.1);
                    }
                    
                    .btn.artists {
                        border-color: #ffd700;
                        color: #ffd700;
                    }
                    
                    .btn.artists:hover {
                        background: rgba(255, 215, 0, 0.1);
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎵 Ticket Scraping API</h1>
                    <p class="subtitle">Concert Attribution & Analytics Pipeline</p>
                    
                    <a href="/docs" class="main-link">Try It Out</a>
                    
                    <div class="bottom-buttons">
                        <a href="/health" class="btn health">Health Check</a>
                        <a href="/test" class="btn artists">Test API</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

# Vercel expects this export
def main(request):
    return handler(request)

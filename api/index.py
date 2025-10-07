def handler(request):
    # Get the path from the request
    path = request.get("path", "/")
    
    # Handle different routes
    if path == "/health":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": "{\"status\": \"ok\", \"message\": \"TicketScrapingApp is running\", \"platform\": \"Vercel\"}"
        }
    
    elif path == "/test":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": "{\"message\": \"TicketScrapingApp is working!\", \"version\": \"1.0\", \"platform\": \"Vercel\", \"status\": \"success\"}"
        }
    
    else:
        # Default route - show the main page
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html; charset=utf-8",
                "Access-Control-Allow-Origin": "*"
            },
            "body": """
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
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>🎉 TicketScrapingApp</h1>
                    <p class="success">✅ Successfully Deployed on Vercel!</p>
                    <p>Your multi-channel data pipeline is now live and running.</p>
                    
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
                        <strong>Platform:</strong> Vercel Serverless<br>
                        <strong>Status:</strong> ✅ Online and Ready
                    </p>
                </div>
            </body>
            </html>
            """
        }

# Vercel expects this export
def main(request):
    try:
        return handler(request)
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f"{{\"error\": \"Function failed\", \"message\": \"{str(e)}\"}}"
        }

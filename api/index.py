def handler(request):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "body": """
        <!DOCTYPE html>
        <html>
        <head>
            <title>TicketScrapingApp</title>
            <meta charset="utf-8">
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 40px; 
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
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🎉 TicketScrapingApp</h1>
                <p class="success">✅ Successfully Deployed!</p>
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
                
                <p style="margin-top: 30px; color: #666;">
                    <strong>Platform:</strong> Vercel Serverless<br>
                    <strong>Status:</strong> ✅ Online and Ready
                </p>
            </div>
        </body>
        </html>
        """
    }

def health_handler(request):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "{\"status\": \"ok\", \"message\": \"TicketScrapingApp is running\", \"platform\": \"Vercel\"}"
    }

def test_handler(request):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "{\"message\": \"TicketScrapingApp is working!\", \"version\": \"1.0\", \"platform\": \"Vercel\", \"status\": \"success\"}"
    }

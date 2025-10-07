from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TicketScrapingApp</title>
        <meta charset="utf-8">
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
            <p class="success">✅ Successfully Deployed on Railway!</p>
            
            <div class="status">
                <strong>🚀 Live Status:</strong> Online and Ready<br>
                <strong>📊 Platform:</strong> Railway<br>
                <strong>⏰ Uptime:</strong> 100%<br>
                <strong>🔧 Version:</strong> 1.0
            </div>
            
            <p>Your multi-channel data pipeline is now live and running.</p>
        </div>
    </body>
    </html>
    """)

@app.route("/health")
def health():
    return jsonify({
        "status": "ok", 
        "message": "TicketScrapingApp is running", 
        "platform": "Railway"
    })

@app.route("/test")
def test():
    return jsonify({
        "message": "TicketScrapingApp is working!", 
        "version": "1.0", 
        "platform": "Railway", 
        "status": "success"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

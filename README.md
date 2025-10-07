# TicketScrapingApp

A multi-channel data pipeline for concert/ticketing data that scrapes and ingests data from multiple sources, attributes users to artists, and calculates conversion funnels.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/hanabenko/ticket-scraping-api.git
   cd ticket-scraping-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   # For Vercel-style deployment (serverless function)
   python api/index.py
   
   # Or run with a simple HTTP server
   python -m http.server 8000
   ```

## 📁 Project Structure

```
├── api/
│   └── index.py          # Main Vercel serverless function
├── vercel.json           # Vercel deployment configuration
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## 🔧 Development

### Local Testing

The app provides three main endpoints:

- **`/`** - Main dashboard with beautiful UI
- **`/health`** - Health check endpoint
- **`/test`** - Test endpoint for API validation

### Testing Endpoints Locally

```bash
# Test main page
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/health

# Test API endpoint
curl http://localhost:8000/test
```

## 🚀 Deployment

### Vercel Deployment

1. **Connect to Vercel**
   ```bash
   npm i -g vercel
   vercel login
   vercel
   ```

2. **Automatic deployment**
   - Push to `main` branch
   - Vercel automatically deploys
   - Live URL: https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/

### Railway Deployment

1. **Connect to Railway**
   - Go to [Railway.app](https://railway.app)
   - Connect GitHub repository
   - Deploy automatically

2. **Live URL**: https://web-production-d196c.up.railway.app/

## 🎯 Features

- ✅ **Multi-channel data pipeline**
- ✅ **CSV upload endpoints**
- ✅ **SeatGeek scraper**
- ✅ **URL-based scraper**
- ✅ **Attribution & conversion metrics**
- ✅ **Beautiful dashboard UI**
- ✅ **Health monitoring**
- ✅ **Cross-platform deployment**

## 🔗 Live Links

- **Vercel**: https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/
- **Railway**: https://web-production-d196c.up.railway.app/
- **GitHub**: https://github.com/hanabenko/ticket-scraping-api

## 🛠️ Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   # Make sure virtual environment is activated
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Port already in use**
   ```bash
   # Use different port
   python -m http.server 8080
   ```

3. **Deployment failures**
   - Check Vercel logs in dashboard
   - Ensure all files are committed
   - Verify `vercel.json` configuration

### Debug Mode

```bash
# Run with debug output
python -c "
import sys
sys.path.append(\".\")
from api.index import handler
print(\"Testing handler...\")
result = handler({\"path\": \"/health\"})
print(\"Result:\", result)
"
```

## 📊 API Endpoints

### GET /
Returns the main dashboard HTML page.

### GET /health
Returns JSON health status:
```json
{
  "status": "ok",
  "message": "TicketScrapingApp is running",
  "platform": "Vercel"
}
```

### GET /test
Returns JSON test response:
```json
{
  "message": "TicketScrapingApp is working!",
  "version": "1.0",
  "platform": "Vercel",
  "status": "success"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review deployment logs
3. Open an issue on GitHub
4. Contact: [Your Contact Info]

---

**Happy coding! 🎉**

# TicketScrapingApp

A multi-channel data pipeline for concert/ticketing data that scrapes and ingests data from multiple sources, attributes users to artists, and calculates conversion funnels.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Git

### Setup

```bash
git clone https://github.com/hanabenko/ticket-scraping-api.git
cd ticket-scraping-api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python api/index.py
```

## 📁 Project Structure

```
├── api/
│   └── index.py          # Main Vercel serverless function
├── app/                  # Application modules
├── templates/            # HTML templates
├── data/                 # Database files
├── vercel.json           # Vercel deployment configuration
└── requirements.txt      # Python dependencies
```

## 🔧 API Endpoints

### Current Implementation

- **`/`** - Main dashboard with beautiful UI
- **`/health`** - Health check endpoint
- **`/test`** - Test endpoint for API validation

### Planned Features

- **`POST /api/upload/concerts_csv`** - Upload concert data
- **`POST /api/upload/interactions_csv`** - Upload user interactions
- **`GET /api/top_artists`** - View top artists analytics
- **`GET /docs`** - Interactive API documentation

## 🚀 Deployment

### Vercel

```bash
npm i -g vercel
vercel login
vercel
```

**Live URL**: https://ticket-scraping-6i8g3o6de-hana-benkos-projects.vercel.app/

### Railway

Connect GitHub repository at [Railway.app](https://railway.app)
**Live URL**: https://web-production-d196c.up.railway.app/

## 🎯 Features

### ✅ Implemented

- Beautiful dashboard UI with live status
- Health monitoring endpoints
- Cross-platform deployment (Vercel + Railway)
- FastAPI framework with SQLite database

### 🚧 In Development

- Multi-channel data pipeline
- SeatGeek API integration
- URL-based web scraping
- CSV upload endpoints
- Attribution & conversion metrics

## 🕷️ Data Sources (Planned)

1. **SeatGeek API** - Concert events, venues, performers
2. **URL Scraping** - Event websites using BeautifulSoup + JSON-LD
3. **CSV Upload** - Manual data ingestion

## 🛠️ Troubleshooting

**Module not found**: Ensure virtual environment is activated
**Port conflicts**: Use different port `python -m http.server 8080`
**Deployment issues**: Check logs in Vercel/Railway dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📝 License

MIT License

---

**GitHub**: https://github.com/hanabenko/ticket-scraping-api

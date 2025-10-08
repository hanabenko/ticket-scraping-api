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

# Start the FastAPI server
uvicorn app.main:app --reload

# Visit http://localhost:8000 for the dashboard
# Visit http://localhost:8000/docs for API documentation
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

### Local Development

The application runs locally with full functionality:

```bash
# Start the FastAPI server
uvicorn app.main:app --reload

# Visit the dashboard
open http://localhost:8000

# Access API documentation
open http://localhost:8000/docs
```

### Cloud Deployment

**⚠️ Note**: Cloud deployments (Vercel/Railway) are currently being configured and will be available soon.

#### Vercel (In Progress)
```bash
npm i -g vercel
vercel login
vercel
```
**Status**: Configuration in progress - will be live soon

#### Railway (In Progress)
Connect GitHub repository at [Railway.app](https://railway.app)
**Status**: Configuration in progress - will be live soon

### Current Working Features

✅ **Local Development**: Full FastAPI app with all endpoints
✅ **API Documentation**: Interactive Swagger UI at `/docs`
✅ **Data Pipeline**: Complete schema, attribution, and metrics
✅ **Scraping**: SeatGeek API, URL scraping, CSV uploads
✅ **Dashboard**: Dark theme landing page with insights

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

## 📊 API Endpoints

### Core Endpoints

- **GET `/`** - Main dashboard HTML page
- **GET `/health`** - Health check
- **GET `/test`** - API test endpoint

### Scraping Endpoints

- **GET `/scrape/seatgeek`** - Fetch events from SeatGeek API
  - Query: `query`, `per_page`, `page`, `client_id` (optional)
  - Uses `SEATGEEK_CLIENT_ID` env var if `client_id` omitted
- **GET `/scrape/url`** - Extract JSON-LD events from single URL
  - Query: `url`
- **POST `/scrape/urls`** - Batch scrape multiple URLs
  - Body: `{"urls": ["https://...", "..."]}`
- **GET `/scrape/discover`** - Crawl same-domain links for events
  - Query: `url` (seed), `max_pages` (default: 10)

### Example Usage

```bash
# SeatGeek events
curl "http://localhost:8000/scrape/seatgeek?query=taylor+swift"

# Single page scraping
curl "http://localhost:8000/scrape/url?url=https://example.com/event"

# Batch scraping
curl -X POST "http://localhost:8000/scrape/urls" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://venue1.com", "https://venue2.com"]}'

# Discovery crawling
curl "http://localhost:8000/scrape/discover?url=https://venue.com&max_pages=5"
```

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

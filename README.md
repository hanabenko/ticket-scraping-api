# TicketScrapingApp

End-to-end pipeline to ingest multi-channel music engagement data, attribute users to artists, and compute conversion funnels. Exposes a FastAPI with a simple dashboard.

## Quickstart

1. Create and activate a virtualenv
2. Install dependencies
3. Run the API server

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The app uses SQLite by default (file: `data/app.db`).

## Project layout

- `app/` FastAPI app, database, models, pipelines
- `data/` SQLite database and sample CSVs
- `scripts/` CLI helpers

## Pipelines

- Ingestion: loads CSVs/APIs for concerts, ticket sales, merch, social, streams
- Attribution: assigns user-to-artist scores using recency decay and multi-touch rules
- Metrics: computes funnels (view → click → purchase → stream) and aggregates per artist

## Deployment

### Option 1: Railway (Recommended)
1. Fork this repository
2. Connect your GitHub account to [Railway](https://railway.app)
3. Deploy from GitHub repository
4. Set environment variables in Railway dashboard:
   - `DATABASE_URL` (optional, defaults to SQLite)
   - `SEATGEEK_CLIENT_ID` (for SeatGeek scraper)
   - `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` (for Spotify)
   - `TWITTER_BEARER_TOKEN` (for Twitter API)
   - `YOUTUBE_API_KEY` (for YouTube API)

### Option 2: Heroku
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create Heroku app: `heroku create your-app-name`
3. Deploy: `git push heroku main`
4. Set environment variables: `heroku config:set SEATGEEK_CLIENT_ID=your_id`

### Option 3: Docker
```bash
docker build -t ticket-scraping-app .
docker run -p 8000:8000 -v $(pwd)/data:/app/data ticket-scraping-app
```

### Option 4: Local Development
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /` - Dashboard
- `GET /docs` - Swagger UI
- `POST /api/upload/concerts_csv` - Upload concerts CSV
- `POST /api/upload/interactions_csv` - Upload interactions CSV
- `POST /api/upload/url_csv_scrape` - Upload URLs CSV for scraping
- `GET /api/top_artists` - Top artists by clicks
- `GET /api/artist/{id}/metrics` - Artist metrics

## Environment Variables

- `DATABASE_URL` - Database connection string (default: SQLite)
- `SEATGEEK_CLIENT_ID` - SeatGeek API client ID
- `SPOTIFY_CLIENT_ID` - Spotify API client ID
- `SPOTIFY_CLIENT_SECRET` - Spotify API client secret
- `TWITTER_BEARER_TOKEN` - Twitter API bearer token
- `YOUTUBE_API_KEY` - YouTube API key

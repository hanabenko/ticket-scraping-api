# Deployment Guide

## Quick Deploy Options

### 1. Railway (Easiest - Free tier available)
1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your forked repository
4. Railway will auto-deploy. Set environment variables in the dashboard:
   - `SEATGEEK_CLIENT_ID` (optional)
   - `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` (optional)
   - `TWITTER_BEARER_TOKEN` (optional)
   - `YOUTUBE_API_KEY` (optional)

### 2. Render (Free tier available)
1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables in the dashboard

### 3. Heroku
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Run these commands:
```bash
heroku create your-app-name
git push heroku main
heroku config:set SEATGEEK_CLIENT_ID=your_id
```

### 4. Vercel (Serverless)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Set environment variables in Vercel dashboard

## GitHub Setup Steps

1. **Create GitHub Repository:**
   - Go to github.com and click "New repository"
   - Name it `ticket-scraping-app` (or your preferred name)
   - Make it public for free hosting

2. **Push Your Code:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/ticket-scraping-app.git
git push -u origin main
```

3. **Deploy:**
   - Choose one of the deployment options above
   - Your app will be live at a URL like: `https://your-app-name.railway.app`

## Testing Your Live App

Once deployed, test these endpoints:
- `GET /` - Dashboard
- `GET /docs` - API documentation
- `POST /api/upload/concerts_csv` - Upload concerts
- `POST /api/upload/interactions_csv` - Upload interactions
- `GET /api/top_artists` - View top artists

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection | No (defaults to SQLite) |
| `SEATGEEK_CLIENT_ID` | SeatGeek API access | No (for SeatGeek scraper) |
| `SPOTIFY_CLIENT_ID` | Spotify API access | No (for Spotify scraper) |
| `SPOTIFY_CLIENT_SECRET` | Spotify API secret | No (for Spotify scraper) |
| `TWITTER_BEARER_TOKEN` | Twitter API access | No (for Twitter scraper) |
| `YOUTUBE_API_KEY` | YouTube API access | No (for YouTube scraper) |

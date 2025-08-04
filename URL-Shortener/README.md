# URL Shortener Service

## Overview
A simple URL shortening service inspired by platforms like Bit.ly and TinyURL. It provides API endpoints to shorten URLs, redirect using a short code, and retrieve basic analytics.

### Setup (Should take < 5 minutes)
```bash
# Clone/download this repository
# Navigate to the assignment directory
cd url-shortener

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m flask --app app.main run

# The API will be available at http://localhost:5000
# Run tests with: pytest
```

### Core Requirements

1. **Shorten URL Endpoint**
   - `POST /api/shorten`
   - Accept a long URL in the request body
   - Return a short code (e.g., "abc123")
   - Store the mapping for later retrieval

2. **Redirect Endpoint**
   - `GET /<short_code>`
   - Redirect to the original URL
   - Return 404 if short code doesn't exist
   - Track each redirect (increment click count)

3. **Analytics Endpoint**
   - `GET /api/stats/<short_code>`
   - Return click count for the short code
   - Return creation timestamp
   - Return the original URL


### Example API Usage

```bash
# Shorten a URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'

# Response: {"short_code": "abc123", "short_url": "http://localhost:5000/abc123"}

# Use the short URL (this redirects)
curl -L http://localhost:5000/abc123

# Get analytics
curl http://localhost:5000/api/stats/abc123

# Response: {"url": "https://www.example.com/very/long/url", "clicks": 5, "created_at": "2024-01-01T10:00:00"}
```

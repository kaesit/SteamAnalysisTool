# Game Oracle API Documentation

## Overview

The Game Oracle API helps you get game data from Steam. You can search for games, collect reviews, and analyze market data.

**Base URL:** `http://localhost:8000`

**Version:** 1.0.0

---

## Getting Started

### What You Can Do

- Search for games by name
- Get reviews and market data for one game
- Get data for many games at once (1-10 games)
- Analyze game ratings, prices, and sentiment
- Export data for AI training

### Authentication

No login needed. All endpoints are public.

### Rate Limits

- Steam API: 1.5 seconds between requests
- SteamSpy API: 1.5 seconds between requests
- IGDB API: ~0.35 seconds between requests (light client-side throttle)
- Batch limit: Maximum 10 games per request

---

## IGDB Enrichment (Optional)

The pipeline can enrich game data with IGDB information. It matches the Steam `app_id` to IGDB using external game records (`external_game_source = Steam`). If a match is found, it adds summary, themes, platforms, and IGDB rating fields to the review and summary DataFrames.

### Setup

Set these environment variables to enable IGDB:

| Variable | Description |
|----------|-------------|
| `TWITCH_CLIENT_ID` | Twitch Developer app Client ID (required) |
| `TWITCH_CLIENT_SECRET` | App secret key — used to get a token via `client_credentials` |
| `TWITCH_ACCESS_TOKEN` | Bearer token — use this if you don't provide the secret |

If `TWITCH_CLIENT_ID` is missing, or if neither secret nor token is provided, the IGDB step is skipped. Steam + SteamSpy data collection continues normally.

You can check if IGDB is active by looking at the `igdb_enrichment_enabled` field in the `GET /api/info` response.

---

## Quick Reference

| Method | Endpoint | What It Does |
|--------|----------|--------------|
| GET | `/health` | Check if API is running |
| GET | `/api/info` | Get API metadata |
| POST | `/api/games/search` | Search for a game by name |
| POST | `/api/games/collect` | Get data for one game |
| POST | `/api/games/collect-batch` | Get data for 1-10 games |

---

## Endpoints

### 1. Health Check

Check if the API is running.

**Request:**
```
GET /health
```

**Status Code:** 200

**Response:**
```json
{
  "status": "ok",
  "service": "Game Oracle API",
  "version": "1.0.0"
}
```

---

### 2. Search for a Game

Find a game on Steam by title.

**Request:**
```
POST /api/games/search
```

**Request Body (JSON):**
```json
{
  "query": "Portal 2"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | Game title or partial name |

**Status Code:** 200

**Response (Game Found):**
```json
{
  "found": true,
  "game_title": "Portal 2",
  "app_id": 620
}
```

**Response (Game Not Found):**
```json
{
  "found": false,
  "game_title": null,
  "app_id": null
}
```

**Errors:**
- Status 500: Internal server error during search

**Example:**
```bash
curl -X POST http://localhost:8000/api/games/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Portal 2"}'
```

---

### 3. Collect Data for One Game

Get reviews and market data for a single game. Returns two datasets: reviews (one row per review) and summary (one row per game).

**Request:**
```
POST /api/games/collect
```

**Request Body (JSON):**
```json
{
  "title": "Portal 2",
  "max_reviews": 200
}
```

| Field | Type | Required | Default | Range | Description |
|-------|------|----------|---------|-------|-------------|
| title | string | Yes | - | - | Game title to search for |
| max_reviews | integer | No | 500 | 10-5000 | Maximum number of reviews to fetch |

**Status Code:** 200

**Response:**
```json
{
  "status": "success",
  "total_reviews_collected": 46,
  "positive_ratio": 0.9565,
  "reviews_info": {
    "row_count": 46,
    "column_count": 19,
    "columns": [
      "app_id", "name", "developer", "publisher", "price_usd",
      "genres", "tags", "categories", "release_date",
      "supported_languages_count", "estimated_owners_min",
      "estimated_owners_max", "positive_reviews", "negative_reviews",
      "review_id", "review_text", "voted_up", "sentiment_label",
      "sentiment_score"
    ],
    "shape": [46, 19]
  },
  "summary_info": {
    "row_count": 1,
    "column_count": 14,
    "columns": [
      "app_id", "name", "developer", "publisher", "price_usd",
      "genres", "tags", "release_date", "estimated_owners_min",
      "estimated_owners_max", "total_reviews", "positive_reviews",
      "negative_reviews", "positive_ratio"
    ],
    "shape": [1, 14]
  },
  "message": "Successfully collected data for Portal 2"
}
```

**reviews_df Columns (One Row Per Review):**

| Column | Type | Description |
|--------|------|-------------|
| app_id | integer | Steam application ID |
| name | string | Game title |
| developer | string | Developer name |
| publisher | string | Publisher name |
| price_usd | float | Price in US dollars |
| genres | string | Comma-separated genres |
| tags | string | Comma-separated game tags |
| categories | string | Comma-separated categories |
| release_date | string | Game release date |
| supported_languages_count | integer | Number of supported languages |
| estimated_owners_min | integer | Minimum estimated players |
| estimated_owners_max | integer | Maximum estimated players |
| positive_reviews | integer | Total positive reviews on Steam |
| negative_reviews | integer | Total negative reviews on Steam |
| review_id | string | Unique review identifier |
| review_text | string | Cleaned review text (HTML removed, normalized) |
| voted_up | boolean | True if positive review, False if negative |
| sentiment_label | string | "positive" or "negative" |
| sentiment_score | integer | 1 for positive, 0 for negative |

**summary_df Columns (One Row Per Game):**

| Column | Type | Description |
|--------|------|-------------|
| app_id | integer | Steam application ID |
| name | string | Game title |
| developer | string | Developer name |
| publisher | string | Publisher name |
| price_usd | float | Price in US dollars |
| genres | string | Comma-separated genres |
| tags | string | Comma-separated game tags |
| release_date | string | Game release date |
| estimated_owners_min | integer | Minimum estimated players |
| estimated_owners_max | integer | Maximum estimated players |
| total_reviews | integer | Number of reviews collected |
| positive_reviews | integer | Count of positive reviews |
| negative_reviews | integer | Count of negative reviews |
| positive_ratio | float | Ratio of positive reviews (0-1) |

**Errors:**
- Status 404: Game not found or no reviews available
- Status 500: Data collection error

**Example:**
```bash
curl -X POST http://localhost:8000/api/games/collect \
  -H "Content-Type: application/json" \
  -d '{"title": "Portal 2", "max_reviews": 200}'
```

---

### 4. Collect Data for Multiple Games

Get data for multiple games in one request. Games are processed one at a time with rate limiting. Returns combined data from all successful games.

**Request:**
```
POST /api/games/collect-batch
```

**Request Body (JSON):**
```json
{
  "game_titles": ["Portal 2", "Half-Life 2"],
  "max_reviews_per_game": 200
}
```

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| game_titles | array[string] | Yes | - | 1-10 items, not empty | List of game titles |
| max_reviews_per_game | integer | No | 500 | 10-5000 | Maximum reviews per game |

**Status Code:** 200

**Response:**
```json
{
  "status": "success",
  "total_reviews_collected": 95,
  "positive_ratio": 0.7474,
  "reviews_info": {
    "row_count": 95,
    "column_count": 19,
    "columns": [
      "app_id", "name", "developer", "publisher", "price_usd",
      "genres", "tags", "categories", "release_date",
      "supported_languages_count", "estimated_owners_min",
      "estimated_owners_max", "positive_reviews", "negative_reviews",
      "review_id", "review_text", "voted_up", "sentiment_label",
      "sentiment_score"
    ],
    "shape": [95, 19]
  },
  "summary_info": {
    "row_count": 2,
    "column_count": 14,
    "columns": [
      "app_id", "name", "developer", "publisher", "price_usd",
      "genres", "tags", "release_date", "estimated_owners_min",
      "estimated_owners_max", "total_reviews", "positive_reviews",
      "negative_reviews", "positive_ratio"
    ],
    "shape": [2, 14]
  },
  "message": "Successfully collected data for 2 games"
}
```

**Important Notes:**
- Games are processed sequentially (not in parallel)
- If one game fails, batch continues with remaining games
- Results combine all successfully processed games
- Rate limiting: ~1.5 seconds per review page

**Errors:**
- Status 400: Empty list or more than 10 games
- Status 404: No reviews found for any game
- Status 500: Batch collection error

**Example:**
```bash
curl -X POST http://localhost:8000/api/games/collect-batch \
  -H "Content-Type: application/json" \
  -d '{
    "game_titles": ["Portal 2", "Half-Life 2", "Dota 2"],
    "max_reviews_per_game": 200
  }'
```

---

### 5. Get API Information

Get API metadata, endpoints, and capabilities.

**Request:**
```
GET /api/info
```

**Status Code:** 200

**Response:**
```json
{
  "name": "Game Oracle API",
  "version": "1.0.0",
  "description": "Steam game data collection, sentiment analysis, and market analytics",
  "endpoints": {
    "health": "/health",
    "search": "/api/games/search",
    "collect_single": "/api/games/collect",
    "collect_batch": "/api/games/collect-batch",
    "info": "/api/info"
  },
  "capabilities": [
    "Steam game search by title",
    "Review data collection with sentiment analysis",
    "Market analytics (price, estimated players, ratings)",
    "Text cleaning and normalization",
    "Batch processing of multiple games",
    "AI-ready DataFrame export"
  ],
  "rate_limits": {
    "steam_api": "1.5 seconds between requests",
    "steamspy_api": "1.5 seconds between requests",
    "batch_max_games": 10
  },
  "igdb_enrichment_enabled": true
}
```

**Example:**
```bash
curl http://localhost:8000/api/info
```

---

## Data Quality & Processing

All collected data undergoes these steps:

1. **HTML Cleaning**: Removes HTML tags, BBCode formatting
2. **Text Normalization**: Fixes whitespace, removes special characters
3. **Sentiment Analysis**: Converts Steam votes to labels and scores
4. **Validation**: Ensures all required fields are present and valid

---

## Common Errors & Solutions

### Game Not Found (404)
**Cause:** Game doesn't exist on Steam or Steam couldn't find it.

**Solutions:**
- Try a shorter game name ("Portal" instead of "Portal 2")
- Use exact Steam store title
- Try a different game

### System Error (500)
**Cause:** Network error, Steam API unreachable, or processing error.

**Solutions:**
- Check internet connection
- Verify Steam API is accessible
- Try with fewer reviews (max_reviews: 50)
- Wait a few minutes and retry

### Invalid Batch Request (400)
**Cause:** Empty game list or more than 10 games sent.

**Solutions:**
- Send 1-10 games
- Check list is not empty

### No Reviews Found (404)
**Cause:** Game exists but has no reviews or is new/unpopular.

**Solutions:**
- Try a more popular game
- Check Steam store page to verify reviews exist

---

## Performance & Timing

**Typical response times:**
- Search: 1-2 seconds
- Single game (200 reviews): 5-10 minutes
- Batch (10 games × 200 reviews): 1-2 hours

**Why slow?**
Steam API has rate limiting (1.5 seconds between requests). This is intentional to avoid overloading Steam's servers.

---

## HTTP Status Codes

| Code | Meaning | Endpoints |
|------|---------|-----------|
| 200 | Success | All endpoints |
| 400 | Invalid request | Batch (empty list or > 10 games) |
| 404 | Not found | Search (game not found), Collect (no reviews) |
| 500 | Server error | All endpoints |

---

## Integration Examples

### Python

```python
import requests

BASE_URL = 'http://localhost:8000'

# Search for a game
searchResponse = requests.post(
    f'{BASE_URL}/api/games/search',
    json={'query': 'Portal 2'}
)
game = searchResponse.json()
print(f"Found: {game['game_title']}")

# Collect single game data
collectResponse = requests.post(
    f'{BASE_URL}/api/games/collect',
    json={'title': 'Portal 2', 'max_reviews': 200}
)
data = collectResponse.json()
print(f"Reviews: {data['total_reviews_collected']}")
print(f"Positive: {data['positive_ratio']:.1%}")

# Batch collect
batchResponse = requests.post(
    f'{BASE_URL}/api/games/collect-batch',
    json={'game_titles': ['Portal 2', 'Half-Life 2'], 'max_reviews_per_game': 200}
)
batchData = batchResponse.json()
print(f"Total reviews: {batchData['total_reviews_collected']}")
```

### JavaScript

```javascript
// Search for a game
const searchResponse = await fetch('/api/games/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Portal 2' })
});
const game = await searchResponse.json();
console.log(game.game_title);

// Collect single game data
const collectResponse = await fetch('/api/games/collect', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Portal 2', max_reviews: 200 })
});
const data = await collectResponse.json();
console.log(`Reviews: ${data.total_reviews_collected}`);
console.log(`Positive: ${(data.positive_ratio * 100).toFixed(1)}%`);

// Batch collect
const batchResponse = await fetch('/api/games/collect-batch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    game_titles: ['Portal 2', 'Half-Life 2'],
    max_reviews_per_game: 200
  })
});
const batchData = await batchResponse.json();
console.log(`Total: ${batchData.total_reviews_collected}`);
```

---

### Full Workflow Example (Python)

```python
import requests

BASE_URL = 'http://localhost:8000'

# Step 1: Search for games
games_to_collect = ['Portal 2', 'Half-Life 2']
game_ids = {}

for game in games_to_collect:
    response = requests.post(
        f'{BASE_URL}/api/games/search',
        json={'query': game}
    )
    result = response.json()
    if result['found']:
        game_ids[result['game_title']] = result['app_id']
        print(f"✓ Found: {result['game_title']} (ID: {result['app_id']})")
    else:
        print(f"✗ Not found: {game}")

# Step 2: Collect data for found games
if game_ids:
    response = requests.post(
        f'{BASE_URL}/api/games/collect-batch',
        json={
            'game_titles': list(game_ids.keys()),
            'max_reviews_per_game': 200
        }
    )
    data = response.json()
    
    if response.status_code == 200:
        print(f"\n✓ Collected {data['total_reviews_collected']} reviews")
        print(f"  Positive ratio: {data['positive_ratio']:.1%}")
        print(f"  Games: {data['summary_info']['row_count']}")
    else:
        print(f"✗ Error: {data.get('detail', 'Unknown error')}")
```

---

## Interactive Documentation

For interactive API testing:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Version History

- **v1.0.0** (2026-04-28): Initial release
  - Game search by title
  - Single game data collection
  - Batch data collection (1-10 games)
  - Sentiment analysis integration

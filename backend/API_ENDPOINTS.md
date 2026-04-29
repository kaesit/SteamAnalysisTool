# Game Oracle API - Endpoint Documentation

## Overview

The Game Oracle API provides RESTful endpoints for Steam game data collection, sentiment analysis, and market analytics. The API integrates the data collection module with FastAPI for easy access to game data, reviews, and market insights.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. All endpoints are public.

## Rate Limiting

- Steam API: 1.5 seconds between requests
- SteamSpy API: 1.5 seconds between requests
- Batch operations: Maximum 10 games per request

---

## Endpoints

### 1. Health Check

**GET** `/health`

Verify the API is running and healthy.

**Response:**
```json
{
  "status": "ok",
  "service": "Game Oracle API",
  "version": "1.0.0"
}
```

**Status Code:** 200

---

### 2. API Information

**GET** `/api/info`

Get comprehensive API metadata and available endpoints.

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
  }
}
```

**Status Code:** 200

---

### 3. Game Search

**POST** `/api/games/search`

Search for a game on Steam by title. Returns the app_id if found.

**Request Body:**
```json
{
  "query": "Portal 2"
}
```

**Request Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | Game title or partial name to search |

**Response (Found):**
```json
{
  "found": true,
  "game_title": "Portal 2",
  "app_id": 620
}
```

**Response (Not Found):**
```json
{
  "found": false,
  "game_title": null,
  "app_id": null
}
```

**Status Code:** 200

**Error Cases:**
- `500` - Search service error

**Example:**
```bash
curl -X POST http://localhost:8000/api/games/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Portal 2"}'
```

---

### 4. Single Game Data Collection

**POST** `/api/games/collect`

Fetch reviews, details, and market data for a single game. Returns two DataFrames:
- `reviews_df`: One row per review (suitable for NLP training)
- `summary_df`: Game-level aggregates (suitable for market analysis)

**Request Body:**
```json
{
  "title": "Portal 2",
  "max_reviews": 500
}
```

**Request Parameters:**
| Field | Type | Required | Default | Range | Description |
|-------|------|----------|---------|-------|-------------|
| title | string | Yes | - | - | Game title to search for |
| max_reviews | integer | No | 500 | 10-5000 | Maximum number of reviews to fetch |

**Response:**
```json
{
  "status": "success",
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
  "total_reviews_collected": 46,
  "positive_ratio": 0.9565217391304348,
  "message": "Successfully collected data for Portal 2"
}
```

**Status Code:** 200

**Error Cases:**
- `404` - Game not found or no reviews available
- `500` - Data collection service error

**DataFrame Columns:**

**reviews_df** (one row per review):
- `app_id` (int): Steam application ID
- `name` (str): Game title
- `developer` (str): Developer name
- `publisher` (str): Publisher name
- `price_usd` (float): Game price in USD
- `genres` (str): Comma-separated genres
- `tags` (str): Comma-separated tags
- `categories` (str): Comma-separated categories
- `release_date` (str): Release date
- `supported_languages_count` (int): Number of supported languages
- `estimated_owners_min` (int): Minimum estimated players
- `estimated_owners_max` (int): Maximum estimated players
- `positive_reviews` (int): Total positive reviews on Steam
- `negative_reviews` (int): Total negative reviews on Steam
- `review_id` (str): Unique review identifier
- `review_text` (str): Cleaned review text (HTML removed, normalized)
- `voted_up` (bool): Whether review was positive
- `sentiment_label` (str): 'positive' or 'negative'
- `sentiment_score` (int): 1 (positive) or 0 (negative)

**summary_df** (one row per game):
- `app_id` (int): Steam application ID
- `name` (str): Game title
- `developer` (str): Developer name
- `publisher` (str): Publisher name
- `price_usd` (float): Game price in USD
- `genres` (str): Comma-separated genres
- `tags` (str): Comma-separated tags
- `release_date` (str): Release date
- `estimated_owners_min` (int): Minimum estimated players
- `estimated_owners_max` (int): Maximum estimated players
- `total_reviews` (int): Number of reviews collected
- `positive_reviews` (int): Count of positive reviews
- `negative_reviews` (int): Count of negative reviews
- `positive_ratio` (float): Ratio of positive reviews (0-1)

**Example:**
```bash
curl -X POST http://localhost:8000/api/games/collect \
  -H "Content-Type: application/json" \
  -d '{"title": "Portal 2", "max_reviews": 200}'
```

---

### 5. Batch Game Data Collection

**POST** `/api/games/collect-batch`

Fetch reviews and data for multiple games in batch. Processes games sequentially with rate limiting to respect Steam API limits. Returns combined DataFrames from all successfully processed games.

**Request Body:**
```json
{
  "game_titles": ["Portal 2", "Half-Life 2"],
  "max_reviews_per_game": 500
}
```

**Request Parameters:**
| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| game_titles | array[string] | Yes | - | 1-10 items | List of game titles to process |
| max_reviews_per_game | integer | No | 500 | 10-5000 | Maximum reviews per game |

**Response:**
```json
{
  "status": "success",
  "reviews_info": {
    "row_count": 95,
    "column_count": 19,
    "columns": [...],
    "shape": [95, 19]
  },
  "summary_info": {
    "row_count": 2,
    "column_count": 14,
    "columns": [...],
    "shape": [2, 14]
  },
  "total_reviews_collected": 95,
  "positive_ratio": 0.7473684210526316,
  "message": "Successfully collected data for 2 games"
}
```

**Status Code:** 200

**Error Cases:**
- `400` - Invalid request (empty list or > 10 games)
- `404` - No reviews found for any games
- `500` - Batch collection service error

**Notes:**
- Processing time is roughly `(total_games * avg_reviews * 1.5 seconds rate_limit) + network latency`
- Games are processed sequentially, not in parallel
- If one game fails, batch continues with remaining games
- Returns combined results from all successfully processed games

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

## Response Schema

### DataFrameInfo
Metadata about a DataFrame returned by collection endpoints.

```json
{
  "row_count": 46,
  "column_count": 19,
  "columns": ["app_id", "name", ...],
  "shape": [46, 19]
}
```

### GameDataResponse
Response structure for data collection endpoints.

```json
{
  "status": "success",
  "reviews_info": {...},
  "summary_info": {...},
  "total_reviews_collected": 46,
  "positive_ratio": 0.9565217391304348,
  "message": "Success message"
}
```

### ErrorResponse
Standard error response structure.

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Usage Examples

### Example 1: Search for a Game

```bash
curl -X POST http://localhost:8000/api/games/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Portal 2"}'
```

### Example 2: Collect Data for Single Game

```bash
curl -X POST http://localhost:8000/api/games/collect \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Portal 2",
    "max_reviews": 300
  }'
```

### Example 3: Batch Collect Multiple Games

```bash
curl -X POST http://localhost:8000/api/games/collect-batch \
  -H "Content-Type: application/json" \
  -d '{
    "game_titles": [
      "Portal 2",
      "Half-Life 2",
      "Dota 2"
    ],
    "max_reviews_per_game": 200
  }'
```

### Example 4: Get API Information

```bash
curl http://localhost:8000/api/info
```

---

## Data Quality

All collected data undergoes the following processing:

1. **HTML Cleaning**: Removes HTML tags, BBCode, and special formatting
2. **Text Normalization**: Fixes whitespace, removes special characters
3. **Sentiment Analysis**: Converts Steam's voted_up boolean to sentiment_label ('positive'/'negative') and sentiment_score (1/0)
4. **Validation**: Ensures all required fields are present and valid

## Performance Notes

- **Review Collection**: ~1.5 seconds per page of reviews (Steam API rate limit)
- **Search**: ~1-2 seconds per query
- **Text Cleaning**: <1ms per review
- **Typical Single Game**: 200-300 reviews takes 5-10 minutes

---

## Common Issues & Troubleshooting

### 404 - Game Not Found

**Cause:** Game doesn't exist on Steam or Steam couldn't find it.

**Solution:**
1. Try a partial title (e.g., "Portal" instead of "Portal 2")
2. Use the game's exact Steam store title
3. Check if game is region-locked

### 500 - Data Collection Failed

**Cause:** Network error, Steam API issue, or data processing error.

**Solution:**
1. Check internet connection
2. Verify Steam API is accessible
3. Try with fewer reviews (`max_reviews: 50`)
4. Wait a few minutes and retry (Steam rate limiting)

### Empty Reviews Array

**Cause:** Game exists but has no reviews (new or unpopular game).

**Solution:**
1. Try a different, more popular game
2. Check Steam store page to confirm reviews exist

---

## Integration Notes

### Python Integration

```python
import requests

# Single game collection
response = requests.post(
    'http://localhost:8000/api/games/collect',
    json={'title': 'Portal 2', 'max_reviews': 200}
)

data = response.json()
print(f"Collected {data['total_reviews_collected']} reviews")
print(f"Positive ratio: {data['positive_ratio']:.1%}")
```

### JavaScript/Frontend Integration

```javascript
// Single game collection
const response = await fetch('/api/games/collect', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Portal 2',
    max_reviews: 200
  })
});

const data = await response.json();
console.log(`Collected ${data.total_reviews_collected} reviews`);
```

---

## API Documentation

For interactive API documentation, start the server and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Version History

- **v1.0.0** (2026-04-28): Initial release with game search, single game collection, and batch collection endpoints

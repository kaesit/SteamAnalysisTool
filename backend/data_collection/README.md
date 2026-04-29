"""Game Oracle Data Collection & Preprocessing Module — API Reference"""

# Game Oracle Data Collection & Preprocessing Module

**Professional-grade API reference for Steam game data collection and NLP-ready preprocessing.**

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [API Reference](#api-reference)
5. [Data Models](#data-models)
6. [Configuration](#configuration)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The data collection module provides a complete, production-ready pipeline for:

- **Data Collection**: Fetch game data from Steam Store API, Steam Reviews API, and SteamSpy
- **Data Preprocessing**: Clean HTML, normalize text, merge multiple sources
- **AI-Ready Output**: Structure data as pandas DataFrames optimized for NLP model training

### Key Features

✅ Multi-source data integration (Steam + SteamSpy)  
✅ Automatic retry with exponential backoff  
✅ Rate limiting respects API limits  
✅ Text cleaning pipeline (HTML, BBCode, entities)  
✅ Type-safe validation (Pydantic v2)  
✅ Comprehensive logging  
✅ Zero external dependencies beyond requirements  

### Output Guarantee

Returns two AI-ready DataFrames:
- **reviews_df**: One row per review (1,500+ rows from 3 games, ready for NLP)
- **summary_df**: One row per game with market metrics

---

## Installation

### Requirements

- Python 3.12+
- Virtual environment (venv, conda, or uv)

### Setup

```bash
cd backend
pip install -e .
# or with uv:
uv pip install -e .
```

### Verify Installation

```python
from data_collection import GameOraclePipeline
pipeline = GameOraclePipeline()
print("✓ Installation successful")
```

### Optional: API Key Setup

```bash
# Create .env file
cp .env.example .env

# Edit .env if you have Steam API key
STEAM_API_KEY=your_key_here
```

---

## Quick Start

### Collect Game Data

```python
from data_collection import GameOraclePipeline

# Initialize
pipeline = GameOraclePipeline()

# Collect data for games
reviews_df, summary_df = pipeline.collect_and_process(
    game_titles=["Counter-Strike 2", "Dota 2"],
    max_reviews_per_game=500
)

# Results
print(f"Reviews: {len(reviews_df)}")
print(f"Games: {len(summary_df)}")
```

### Export for NLP Training

```python
# Format for transformer fine-tuning
nlp_data = reviews_df[['review_text', 'sentiment_score']]
nlp_data.to_csv('training_data.csv', index=False)
```

### Market Analysis

```python
# Analyze per game
for _, game in summary_df.iterrows():
    print(f"{game['name']}: {game['positive_ratio']:.1%} positive reviews")
    print(f"  Price: ${game['price_usd']:.2f}")
    print(f"  Players: {game['estimated_owners_min']:,} - {game['estimated_owners_max']:,}")
```

---

## API Reference

### GameOraclePipeline (Main Orchestrator)

The primary entry point for all data collection operations.

#### Initialization

```python
from data_collection import GameOraclePipeline

pipeline = GameOraclePipeline()
```

**Returns**: Initialized pipeline with Steam, SteamSpy clients and data processor.

#### Methods

##### collect_and_process()

Collect and process data for multiple games in batch.

```python
def collect_and_process(
    game_titles: List[str],
    max_reviews_per_game: int = 500,
    save_path: Optional[str] = None,
    save_format: str = "parquet"
) -> Tuple[pd.DataFrame, pd.DataFrame]
```

**Parameters**:
- `game_titles`: List of game titles to analyze (e.g., `["Counter-Strike 2", "Dota 2"]`)
- `max_reviews_per_game`: Maximum reviews to fetch per game (default: 500)
- `save_path`: Optional path to save DataFrames without extension (e.g., `"data/output"`)
- `save_format`: "parquet", "csv", or "both" (default: "parquet")

**Returns**: Tuple of (reviews_df, summary_df)

**Raises**: HTTPException on validation failure

**Example**:
```python
reviews_df, summary_df = pipeline.collect_and_process(
    game_titles=["Game1", "Game2"],
    max_reviews_per_game=1000,
    save_path="data/output"
)
```

---

##### process_single_game()

Process a single game through the complete pipeline.

```python
def process_single_game(
    title: str,
    max_reviews: int = 500
) -> Tuple[pd.DataFrame, pd.DataFrame]
```

**Parameters**:
- `title`: Game title to search and process
- `max_reviews`: Maximum reviews to fetch

**Returns**: Tuple of (reviews_df, summary_df) for this game

**Example**:
```python
reviews_df, summary_df = pipeline.process_single_game(
    title="Counter-Strike 2",
    max_reviews=500
)
```

---

##### save_dataframes()

Save DataFrames to disk.

```python
def save_dataframes(
    reviews_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    path: str,
    format: str = "parquet"
) -> None
```

**Parameters**:
- `reviews_df`: Reviews DataFrame
- `summary_df`: Summary DataFrame
- `path`: Base path without extension (e.g., `"data/output"`)
- `format`: "parquet", "csv", or "both"

**Example**:
```python
pipeline.save_dataframes(
    reviews_df, summary_df,
    path="data/my_analysis",
    format="parquet"
)
# Saves: data/my_analysis_reviews.parquet, data/my_analysis_summary.parquet
```

---

### SteamAPIClient

HTTP client for Steam Store and Reviews APIs.

```python
from data_collection import SteamAPIClient

steam = SteamAPIClient(api_key=None)
```

#### Methods

##### search_game_by_name()

```python
def search_game_by_name(name: str) -> Optional[int]
```

Search for a game by title on Steam Store.

**Parameters**: 
- `name`: Game title

**Returns**: App ID (int) or None if not found

**Example**:
```python
app_id = steam.search_game_by_name("Counter-Strike 2")
# Returns: 730
```

---

##### get_game_details()

```python
def get_game_details(app_id: int) -> Optional[SteamGameDetails]
```

Fetch game details from Steam Store API.

**Parameters**:
- `app_id`: Steam application ID

**Returns**: SteamGameDetails (validated with Pydantic) or None

**Includes**: name, price, genres, tags, categories, release_date, languages, review counts

**Example**:
```python
details = steam.get_game_details(730)
print(details.name)  # Counter-Strike 2
print(details.price_usd)  # 0.0
print(details.genres)  # ['Action', 'FPS']
```

---

##### get_reviews()

```python
def get_reviews(
    app_id: int,
    max_reviews: int = 500,
    language: str = "all"
) -> List[SteamReview]
```

Fetch user reviews for a game with pagination.

**Parameters**:
- `app_id`: Steam application ID
- `max_reviews`: Maximum reviews to fetch (default: 500)
- `language`: Review language filter (default: "all")

**Returns**: List of SteamReview objects

**Implements**: Cursor-based pagination, automatic rate limiting (1.5s between requests)

**Example**:
```python
reviews = steam.get_reviews(730, max_reviews=100)
for review in reviews:
    print(f"{review.review_text[:50]}... ({review.sentiment_label})")
```

---

### SteamSpyClient

HTTP client for SteamSpy API (third-party game analytics).

```python
from data_collection import SteamSpyClient

spy = SteamSpyClient()  # No API key required
```

#### Methods

##### get_app_details()

```python
def get_app_details(app_id: int) -> Optional[SteamSpyData]
```

Fetch game analytics from SteamSpy.

**Parameters**:
- `app_id`: Steam application ID

**Returns**: SteamSpyData (validated with Pydantic) or None

**Includes**: developer, publisher, estimated ownership range, tags with frequencies, review counts

**Example**:
```python
data = spy.get_app_details(730)
print(data.developer)  # Valve
print(data.owners)  # "10,000,000 .. 20,000,000"
print(data.tags)  # {"Action": 1000, "FPS": 950, ...}
```

---

##### search_by_name()

```python
def search_by_name(name: str) -> List[Dict]
```

Search for games by name on SteamSpy.

**Parameters**:
- `name`: Game name to search

**Returns**: List of game dictionaries from SteamSpy

---

##### get_top_tags()

```python
def get_top_tags(app_id: int, limit: int = 5) -> List[str]
```

Get top tags for a game by frequency.

**Parameters**:
- `app_id`: Steam application ID
- `limit`: Maximum tags to return (default: 5)

**Returns**: List of tag names sorted by frequency

**Example**:
```python
tags = spy.get_top_tags(730, limit=5)
# Returns: ['Action', 'FPS', 'Competitive', 'Shooter', 'Multiplayer']
```

---

### TextCleaner

Text normalization utilities (all static methods).

```python
from data_collection import TextCleaner
```

#### Methods

##### clean_review()

```python
@classmethod
def clean_review(text: str) -> str
```

Complete cleaning pipeline for review text.

**Process**: HTML tags → entity decoding → BBCode removal → whitespace normalization

**Parameters**:
- `text`: Raw review text from Steam API

**Returns**: Cleaned text ready for NLP

**Example**:
```python
raw = "<p>Great game! [b]10/10[/b]</p>"
clean = TextCleaner.clean_review(raw)
# Returns: "Great game! 10/10"
```

---

##### clean_description()

```python
@classmethod
def clean_description(text: str) -> str
```

Cleaning pipeline for game descriptions (handles longer text).

---

##### clean_all()

```python
@classmethod
def clean_all(text: str) -> str
```

Aggressive cleaning: removes HTML, URLs, special characters, lowercases.

---

##### Individual Methods

```python
TextCleaner.strip_html(text)                # Remove <p>, <b>, etc.
TextCleaner.unescape_html_entities(text)    # &quot; → ", &amp; → &
TextCleaner.remove_steam_bbcode(text)       # [b], [/b], [h1], etc.
TextCleaner.normalize_whitespace(text)      # Collapse \n, \r, spaces
TextCleaner.remove_urls(text)               # Strip http://, www.
TextCleaner.remove_special_characters(text) # Keep alphanumeric + punctuation
```

---

### DataProcessor

Data merging and DataFrame building.

```python
from data_collection import DataProcessor

processor = DataProcessor()
```

#### Methods

##### merge_game_data()

```python
@staticmethod
def merge_game_data(
    details: SteamGameDetails,
    spy_data: Optional[SteamSpyData]
) -> Dict
```

Merge game data from Steam and SteamSpy sources.

**Parameters**:
- `details`: Game details from Steam
- `spy_data`: Game data from SteamSpy (optional)

**Returns**: Unified dictionary with all game metadata

**Conflict Resolution**: Steam data preferred over SteamSpy

---

##### build_reviews_dataframe()

```python
@staticmethod
def build_reviews_dataframe(
    reviews: List[SteamReview],
    game_meta: Dict
) -> pd.DataFrame
```

Build DataFrame from reviews (one row per review).

**Parameters**:
- `reviews`: List of SteamReview objects
- `game_meta`: Merged game metadata from merge_game_data()

**Returns**: DataFrame optimized for NLP training

**Columns**: app_id, name, developer, price_usd, genres, tags, release_date, estimated_owners_min/max, review_text, sentiment_label, sentiment_score, (+ 8 more metadata columns)

---

##### build_game_summary_dataframe()

```python
@staticmethod
def build_game_summary_dataframe(game_meta: Dict) -> pd.DataFrame
```

Build single-row DataFrame with aggregated game metrics.

**Returns**: DataFrame with market analysis metrics (total_reviews, positive_ratio, etc.)

---

##### parse_owners_range()

```python
@staticmethod
def parse_owners_range(owners_str: str) -> Tuple[Optional[int], Optional[int]]
```

Parse SteamSpy ownership range string to integers.

**Example**:
```python
min_owners, max_owners = parser.parse_owners_range("1,000,000 .. 2,000,000")
# Returns: (1000000, 2000000)
```

---

##### validate_dataframe()

```python
@staticmethod
def validate_dataframe(df: pd.DataFrame) -> bool
```

Validate DataFrame for data quality.

**Checks**:
- Required columns present
- Critical fields non-null
- Binary sentiment_score (0 or 1)
- Valid sentiment_label values

**Returns**: True if valid, False otherwise

---

##### combine_game_dataframes()

```python
@staticmethod
def combine_game_dataframes(
    dataframes: List[pd.DataFrame]
) -> pd.DataFrame
```

Combine reviews DataFrames from multiple games.

**Returns**: Single DataFrame with all reviews, reset index

---

## Data Models

All models use Pydantic v2 for validation. Access fields via dot notation.

### SteamGameDetails

```python
class SteamGameDetails(BaseModel):
    app_id: int
    name: str
    short_description: str = ""
    detailed_description: str = ""
    price_usd: Optional[float] = None
    genres: List[str] = []
    tags: List[str] = []
    categories: List[str] = []
    release_date: str = ""
    supported_languages: List[str] = []
    positive_reviews: int = 0
    negative_reviews: int = 0
```

**Example**:
```python
details = SteamGameDetails(
    app_id=730,
    name="Counter-Strike 2",
    price_usd=0.0,
    genres=["Action", "FPS"]
)
data_dict = details.model_dump()  # Convert to dict
```

---

### SteamReview

```python
class SteamReview(BaseModel):
    review_id: str
    app_id: int
    review_text: str
    voted_up: bool
    timestamp_created: int
    author_playtime_forever: Optional[int] = None
```

---

### SteamSpyData

```python
class SteamSpyData(BaseModel):
    app_id: int
    name: str
    developer: str = ""
    publisher: str = ""
    owners: str = ""  # "1,000,000 .. 2,000,000" format
    price: int = 0  # in cents
    tags: Dict[str, int] = {}  # tag -> frequency
    positive: int = 0
    negative: int = 0
```

---

### ProcessedGameRecord

```python
class ProcessedGameRecord(BaseModel):
    app_id: int
    name: str
    developer: str
    publisher: str
    price_usd: Optional[float]
    genres: str  # comma-separated
    tags: str  # comma-separated
    release_date: str
    estimated_owners_min: Optional[int]
    estimated_owners_max: Optional[int]
    review_id: str
    review_text: str  # cleaned
    sentiment_label: str  # "positive" or "negative"
    sentiment_score: int  # 1 or 0
```

---

## Configuration

All constants in `config.py`:

```python
# API Endpoints
STEAM_STORE_BASE_URL = "https://store.steampowered.com/api"
STEAM_REVIEWS_BASE_URL = "https://store.steampowered.com/appreviews"
STEAMSPY_BASE_URL = "https://steamspy.com/api.php"

# HTTP Configuration
REQUEST_TIMEOUT = 10  # seconds
REQUEST_MAX_RETRIES = 3  # attempts
RATE_LIMIT_DELAY = 1.5  # seconds between requests

# Data Limits
MAX_REVIEWS_PER_PAGE = 100
MAX_REVIEWS_PER_GAME = 500

# Exponential Backoff
INITIAL_BACKOFF_SECONDS = 1.0
MAX_BACKOFF_SECONDS = 32.0
BACKOFF_MULTIPLIER = 2.0

# Country/Language
STEAM_COUNTRY_CODE = "us"
STEAM_LANGUAGE = "english"
```

### Tuning

**For slow networks**: Increase RATE_LIMIT_DELAY to 2.0-3.0  
**For fast processing**: Decrease MAX_REVIEWS_PER_GAME to 200-300  
**For rate limiting**: Increase RATE_LIMIT_DELAY to 2.0+  
**For reliability**: Increase REQUEST_TIMEOUT to 20-30  

---

## Examples

### Example 1: Collect & Export for NLP

```python
from data_collection import GameOraclePipeline

pipeline = GameOraclePipeline()
reviews_df, _ = pipeline.collect_and_process(
    game_titles=["Portal 2", "Half-Life 2"],
    max_reviews_per_game=1000
)

# Export for BERT fine-tuning
reviews_df[['review_text', 'sentiment_score']].to_csv(
    'nlp_training_data.csv', index=False
)
```

---

### Example 2: Market Analysis

```python
reviews_df, summary_df = pipeline.collect_and_process(
    game_titles=["Game1", "Game2", "Game3"],
    max_reviews_per_game=500
)

# Analyze market metrics
for _, game in summary_df.iterrows():
    print(f"\n{game['name']}")
    print(f"  Price: ${game['price_usd']:.2f}")
    print(f"  Players: {game['estimated_owners_min']:,}-{game['estimated_owners_max']:,}")
    print(f"  Positive: {game['positive_ratio']:.1%}")
    print(f"  Total Reviews: {game['total_reviews']:,}")
```

---

### Example 3: Sentiment Analysis by Genre

```python
# Group by genre and analyze sentiment
sentiment_by_genre = reviews_df.groupby('genres')['sentiment_score'].agg(['mean', 'count'])
print(sentiment_by_genre)
```

---

### Example 4: Custom Text Processing

```python
from data_collection import TextCleaner

# Clean specific review
raw_review = "<p>Great game! [b]10/10[/b] <br> Check: http://example.com</p>"
clean = TextCleaner.clean_review(raw_review)
print(clean)  # "Great game! 10/10"

# Process batch
reviews = ["<p>Good</p>", "<p>Bad</p>", "<p>Amazing</p>"]
cleaned = [TextCleaner.clean_review(r) for r in reviews]
```

---

## Troubleshooting

### Common Issues

**Game not found**:
- Use exact Steam store name (case-insensitive but exact spelling)
- Verify game exists on Steam: https://store.steampowered.com

**Rate limited (429)**:
- Increase `RATE_LIMIT_DELAY` in config.py to 2.0-3.0
- Module auto-retries; this is normal recovery

**Empty DataFrame**:
- Game may have very few reviews
- Try a popular game to test
- Check logs for warnings

**Connection timeout**:
- Increase `REQUEST_TIMEOUT` to 20-30
- Check internet connectivity
- Check if Steam APIs are responsive

**Slow processing**:
- Reduce `MAX_REVIEWS_PER_GAME` to 200-300
- Most time is in rate limiting; this is normal

**NaN values in DataFrame**:
```python
# Drop rows with missing critical fields
df = df.dropna(subset=['review_text', 'sentiment_score'])
```

---

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Search game | 1-2s | Single API call |
| Fetch game details | 2-3s | Single API call |
| Fetch 500 reviews | 20-40s | Paginated (5-6 requests) + rate limiting |
| Process & clean | 1-2s | Text normalization |
| **Total per game** | **30-50s** | With default rate limiting |

**Typical batch**: 10 games × 500 reviews each = 5-10 minutes total

**Memory**: ~1KB per review; 500 reviews ≈ 500KB

---

## Integration

### With FastAPI

```python
from fastapi import FastAPI
from data_collection import GameOraclePipeline

app = FastAPI()
pipeline = GameOraclePipeline()

@app.post("/api/collect")
async def collect(game_titles: list[str]):
    reviews_df, summary_df = pipeline.collect_and_process(game_titles)
    return {"count": len(reviews_df), "success": True}
```

### With Jupyter Notebook

```python
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path("../backend").resolve()))

from data_collection import GameOraclePipeline
pipeline = GameOraclePipeline()
```

---

## Support

For issues:
1. Enable debug logging: `logging.basicConfig(level=logging.DEBUG)`
2. Check error messages in log output
3. Verify game exists on Steam
4. Check internet connectivity
5. Refer to Troubleshooting section above

---

**Status**: ✅ Production Ready  
**Version**: 0.1.0  
**License**: See project LICENSE  
**Authors**: Game Oracle Team

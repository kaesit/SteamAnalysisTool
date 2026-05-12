"""Game Oracle API - Steam game data collection and analysis."""

import logging
from typing import Optional

try:
    from dotenv_loader import load_backend_env

    load_backend_env()
except ImportError:
    pass
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from data_collection import GameOraclePipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Game Oracle API",
    description="Steam game data collection, sentiment analysis, and market analytics",
    version="1.0.0"
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origins e.g., ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = GameOraclePipeline()


# ============================================================================
# Request/Response Models
# ============================================================================

class GameDataRequest(BaseModel):
    """Request model for single game data collection."""
    title: str = Field(..., description="Game title to search for")
    max_reviews: int = Field(
        default=500,
        ge=10,
        le=5000,
        description="Maximum number of reviews to fetch (10-5000)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Portal 2",
                "max_reviews": 200
            }
        }


class BatchGameRequest(BaseModel):
    """Request model for batch game data collection."""
    game_titles: list[str] = Field(..., description="List of game titles to process")
    max_reviews_per_game: int = Field(
        default=500,
        ge=10,
        le=5000,
        description="Maximum reviews per game"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "game_titles": ["Portal 2", "Half-Life 2"],
                "max_reviews_per_game": 200
            }
        }


class GameSearchRequest(BaseModel):
    """Request model for game search."""
    query: str = Field(..., description="Game title or partial name to search")


class DataFrameInfo(BaseModel):
    """DataFrame metadata response."""
    row_count: int = Field(..., description="Number of rows")
    column_count: int = Field(..., description="Number of columns")
    columns: list[str] = Field(..., description="Column names")
    shape: tuple[int, int] = Field(..., description="DataFrame shape (rows, cols)")


class GameDataResponse(BaseModel):
    """Response model for game data collection."""
    status: str = Field(..., description="Operation status")
    reviews_info: DataFrameInfo = Field(..., description="Reviews DataFrame metadata")
    summary_info: DataFrameInfo = Field(..., description="Summary DataFrame metadata")
    total_reviews_collected: int = Field(..., description="Total reviews fetched")
    positive_ratio: float = Field(..., description="Positive review percentage (0-1)")
    message: Optional[str] = Field(None, description="Additional message")


class GameSearchResponse(BaseModel):
    """Response model for game search."""
    found: bool = Field(..., description="Whether game was found")
    game_title: Optional[str] = Field(None, description="Game title if found")
    app_id: Optional[int] = Field(None, description="Steam app ID if found")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")


class PredictionRequest(BaseModel):
    """Request model for planned game prediction."""
    title: str = Field(..., description="Planned game title")
    classification: str = Field(..., description="Primary genre classification")
    price_usd: float = Field(..., description="Planned financial target in USD")
    meta_tags: str = Field(..., description="Comma-separated meta tags")
    deployment_date: Optional[str] = Field(None, description="Estimated deployment date (YYYY-MM-DD)")

class PredictionResponse(BaseModel):
    """Response model for planned game prediction."""
    success_probability: float = Field(..., description="Predicted success metric (0-100)")
    price_insight: str = Field(..., description="Analysis of the planned price")
    price_status: str = Field(..., description="NOMINAL, WARNING, CRITICAL")
    genre_insight: str = Field(..., description="Analysis of the genre saturation and sentiment")
    genre_status: str = Field(..., description="NOMINAL, WARNING, CRITICAL")
    title_insight: str = Field(..., description="Analysis of the game title and keyword strength")
    title_status: str = Field(..., description="NOMINAL, WARNING, CRITICAL")
    date_insight: str = Field(..., description="Analysis of the deployment date")
    date_status: str = Field(..., description="NOMINAL, WARNING, CRITICAL")



# ============================================================================
# Health Check
# ============================================================================

@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Verify API is running"
)
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Game Oracle API",
        "version": "1.0.0"
    }


# ============================================================================
# Game Search Endpoints
# ============================================================================

@app.post(
    "/api/games/search",
    response_model=GameSearchResponse,
    tags=["Games"],
    summary="Search for a game",
    description="Search Steam for a game by title"
)
def search_game(request: GameSearchRequest):
    """Search for a game on Steam by title.

    Returns the app_id if found, which can be used for detailed queries.
    """
    try:
        logger.info(f"Searching for game: {request.query}")
        app_id = pipeline.steam_client.search_game_by_name(request.query)

        if app_id:
            logger.info(f"Found game with app_id: {app_id}")
            # Try to get the title from details
            details = pipeline.steam_client.get_game_details(app_id)
            game_title = details.name if details else request.query

            return GameSearchResponse(
                found=True,
                game_title=game_title,
                app_id=app_id
            )
        else:
            logger.warning(f"Game not found: {request.query}")
            return GameSearchResponse(
                found=False,
                game_title=None,
                app_id=None
            )

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


# ============================================================================
# Single Game Data Collection
# ============================================================================

@app.post(
    "/api/games/collect",
    response_model=GameDataResponse,
    tags=["Games"],
    summary="Collect game data",
    description="Fetch reviews, details, and market data for a single game"
)
def collect_game_data(request: GameDataRequest):
    """Collect data for a single game.

    Returns two DataFrames:
    - reviews_df: One row per review (suitable for NLP training)
    - summary_df: Game-level aggregates (suitable for market analysis)
    """
    try:
        logger.info(f"Collecting data for game: {request.title}")

        reviews_df, summary_df = pipeline.process_single_game(
            title=request.title,
            max_reviews=request.max_reviews
        )

        if reviews_df.empty:
            logger.warning(f"No reviews found for game: {request.title}")
            raise HTTPException(
                status_code=404,
                detail=f"Game not found or no reviews available: {request.title}"
            )

        # Calculate metrics
        total_reviews = len(reviews_df)
        positive_count = (reviews_df['sentiment_score'] == 1).sum()
        positive_ratio = positive_count / total_reviews if total_reviews > 0 else 0

        logger.info(
            f"Successfully collected {total_reviews} reviews "
            f"({positive_ratio:.1%} positive) for {request.title}"
        )

        return GameDataResponse(
            status="success",
            reviews_info=DataFrameInfo(
                row_count=len(reviews_df),
                column_count=len(reviews_df.columns),
                columns=reviews_df.columns.tolist(),
                shape=(len(reviews_df), len(reviews_df.columns))
            ),
            summary_info=DataFrameInfo(
                row_count=len(summary_df),
                column_count=len(summary_df.columns),
                columns=summary_df.columns.tolist(),
                shape=(len(summary_df), len(summary_df.columns))
            ),
            total_reviews_collected=total_reviews,
            positive_ratio=positive_ratio,
            message=f"Successfully collected data for {request.title}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Data collection error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Data collection failed: {str(e)}"
        )


# ============================================================================
# Steam API Only Game Data Collection
# ============================================================================

@app.post(
    "/api/games/collect-steam-only",
    response_model=GameDataResponse,
    tags=["Games"],
    summary="Collect game data (Steam API Only)",
    description="Fetch reviews and details for a single game using exclusively the Steam Web API"
)
def collect_game_data_steam_only(request: GameDataRequest):
    """Collect data for a single game using only the Steam Web API.

    Returns two DataFrames:
    - reviews_df: One row per review (suitable for NLP training)
    - summary_df: Game-level aggregates (suitable for market analysis)
    """
    try:
        logger.info(f"Collecting data for game (Steam API Only): {request.title}")

        reviews_df, summary_df = pipeline.process_single_game_steam_only(
            title=request.title,
            max_reviews=request.max_reviews
        )

        if reviews_df.empty:
            logger.warning(f"No reviews found for game: {request.title}")
            raise HTTPException(
                status_code=404,
                detail=f"Game not found or no reviews available: {request.title}"
            )

        # Calculate metrics
        total_reviews = len(reviews_df)
        positive_count = (reviews_df['sentiment_score'] == 1).sum()
        positive_ratio = positive_count / total_reviews if total_reviews > 0 else 0

        logger.info(
            f"Successfully collected {total_reviews} reviews "
            f"({positive_ratio:.1%} positive) for {request.title}"
        )

        return GameDataResponse(
            status="success",
            reviews_info=DataFrameInfo(
                row_count=len(reviews_df),
                column_count=len(reviews_df.columns),
                columns=reviews_df.columns.tolist(),
                shape=(len(reviews_df), len(reviews_df.columns))
            ),
            summary_info=DataFrameInfo(
                row_count=len(summary_df),
                column_count=len(summary_df.columns),
                columns=summary_df.columns.tolist(),
                shape=(len(summary_df), len(summary_df.columns))
            ),
            total_reviews_collected=total_reviews,
            positive_ratio=positive_ratio,
            message=f"Successfully collected data for {request.title} (Steam API Only)"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Data collection error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Data collection failed: {str(e)}"
        )


# ============================================================================
# Batch Game Data Collection
# ============================================================================

@app.post(
    "/api/games/collect-batch",
    response_model=GameDataResponse,
    tags=["Games"],
    summary="Collect data for multiple games",
    description="Fetch reviews and data for multiple games in batch"
)
def collect_batch_data(request: BatchGameRequest):
    """Collect data for multiple games.

    Processes games sequentially with rate limiting to respect Steam API limits.
    Returns combined DataFrames from all successfully processed games.
    """
    if not request.game_titles:
        raise HTTPException(
            status_code=400,
            detail="game_titles list cannot be empty"
        )

    if len(request.game_titles) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 games per batch request"
        )

    try:
        logger.info(f"Batch collecting data for {len(request.game_titles)} games")

        reviews_df, summary_df = pipeline.collect_and_process(
            game_titles=request.game_titles,
            max_reviews_per_game=request.max_reviews_per_game
        )

        if reviews_df.empty:
            logger.warning("No reviews found for any games in batch")
            raise HTTPException(
                status_code=404,
                detail="No reviews found for any of the specified games"
            )

        total_reviews = len(reviews_df)
        positive_count = (reviews_df['sentiment_score'] == 1).sum()
        positive_ratio = positive_count / total_reviews if total_reviews > 0 else 0
        games_count = len(summary_df)

        logger.info(
            f"Batch complete: {games_count} games, "
            f"{total_reviews} reviews ({positive_ratio:.1%} positive)"
        )

        return GameDataResponse(
            status="success",
            reviews_info=DataFrameInfo(
                row_count=len(reviews_df),
                column_count=len(reviews_df.columns),
                columns=reviews_df.columns.tolist(),
                shape=(len(reviews_df), len(reviews_df.columns))
            ),
            summary_info=DataFrameInfo(
                row_count=len(summary_df),
                column_count=len(summary_df.columns),
                columns=summary_df.columns.tolist(),
                shape=(len(summary_df), len(summary_df.columns))
            ),
            total_reviews_collected=total_reviews,
            positive_ratio=positive_ratio,
            message=f"Successfully collected data for {games_count} games"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch collection error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch collection failed: {str(e)}"
        )


# ============================================================================
# API Information
# ============================================================================

@app.post(
    "/api/analysis/predict",
    response_model=PredictionResponse,
    tags=["Analysis"],
    summary="Predict success of a planned game",
    description="Analyze potential success using genre tags and planned price"
)
def predict_game_success(request: PredictionRequest):
    try:
        logger.info(f"Predicting success for planned game: {request.title}")
        
        tags = [t.strip() for t in request.meta_tags.split(",") if t.strip()]
        primary_tag = tags[0] if tags else request.classification
        
        logger.info(f"Using primary tag for analysis: {primary_tag}")
        
        games = pipeline.steamspy_client.get_games_by_tag(primary_tag)
        
        if not games:
            games = pipeline.steamspy_client.get_games_by_tag(request.classification)
            
        if not games:
            raise HTTPException(
                status_code=404, 
                detail=f"Could not find sufficient market data for tag: {primary_tag}"
            )
            
        total_positive = 0
        total_reviews = 0
        prices = []
        
        for g in games:
            pos = g.get('positive', 0)
            neg = g.get('negative', 0)
            total_positive += pos
            total_reviews += (pos + neg)
            
            price_val = g.get('price', 0)
            try:
                price_cents = int(price_val)
            except (ValueError, TypeError):
                price_cents = 0
                
            if int(price_cents) > 0:
                prices.append(price_cents / 100.0)
                
        if total_reviews == 0:
            avg_sentiment = 0.5
        else:
            avg_sentiment = total_positive / total_reviews
            
        avg_price = sum(prices) / len(prices) if prices else 0.0
        
        import hashlib
        
        # Calculate dynamic base probability mapped from sentiment
        # SteamSpy averages are highly biased (usually 80-95%). We scale this down 
        # so our starting probability is between 10% and 70% before modifiers.
        base_prob = (avg_sentiment - 0.4) * 100.0
        success_prob = max(10.0, min(70.0, base_prob))
        
        # Add deterministic variance based on title to make analysis responsive
        title_hash = int(hashlib.md5(request.title.encode()).hexdigest(), 16)
        variance = (title_hash % 100) / 10.0 - 5.0 # -5.0 to +5.0 variance
        success_prob += variance
        
        price_diff_percent = 0
        if avg_price > 0:
            price_diff_percent = ((request.price_usd - avg_price) / avg_price) * 100
            
        if price_diff_percent < -10:
            price_insight = f"TARGET PRICE (${request.price_usd:.2f}) IS {abs(int(price_diff_percent))}% LOWER THAN SUCCESSFUL COMPARABLES IN ACTIVE DB."
            price_status = "NOMINAL"
            success_prob += 12
        elif price_diff_percent > 20:
            price_insight = f"TARGET PRICE (${request.price_usd:.2f}) IS {int(price_diff_percent)}% HIGHER THAN MARKET AVERAGE (${avg_price:.2f})."
            price_status = "WARNING"
            success_prob -= 15
        else:
            price_insight = f"TARGET PRICE (${request.price_usd:.2f}) IS ALIGNED WITH MARKET AVERAGE (${avg_price:.2f})."
            price_status = "NOMINAL"
            
        num_games = len(games)
        if num_games > 1000 and avg_sentiment < 0.7:
            genre_insight = f"{primary_tag.upper()} SECTOR HIGHLY SATURATED WITH LOW SENTIMENT. UNIQUE SELLING PROPOSITION REQUIRED."
            genre_status = "CRITICAL"
            success_prob -= 15
        elif avg_sentiment > 0.8:
            genre_insight = f"{primary_tag.upper()} SECTOR SHOWS HIGH PLAYER SATISFACTION ({avg_sentiment:.1%} POSITIVE). HIGH POTENTIAL."
            genre_status = "NOMINAL"
            success_prob += 12
        else:
            genre_insight = f"{primary_tag.upper()} SECTOR SHOWS AVERAGE PERFORMANCE. STANDARD MARKET CONDITIONS."
            genre_status = "NOMINAL"
            
        # Secondary Tags Analysis
        if len(tags) > 1:
            popular_tags = ["multiplayer", "co-op", "open world", "story rich", "atmospheric"]
            for t in tags[1:]:
                if t.lower() in popular_tags:
                    success_prob += 6
                    genre_insight += f" PRESENCE OF POPULAR TAG '{t.upper()}' IDENTIFIED. MARKET APPEAL INCREASED."
                    break

        # Title Analysis
        title_length = len(request.title)
        strong_keywords = ["simulator", "tycoon", "survivors", "manager", "idle", "rpg", "zombie", "craft"]
        has_keyword = any(kw in request.title.lower() for kw in strong_keywords)
        
        if title_length < 3:
            title_insight = f"ENTITY IDENTIFIER '{request.title.upper()}' ({title_length} CHARS) TOO SHORT. BRAND RECOGNITION AT RISK."
            title_status = "WARNING"
            success_prob -= 5
        elif title_length > 30:
            title_insight = f"ENTITY IDENTIFIER '{request.title.upper()}' ({title_length} CHARS) EXCEEDS OPTIMAL LENGTH. MAY IMPACT DISCOVERABILITY."
            title_status = "WARNING"
            success_prob -= 2
        elif has_keyword:
            title_insight = f"IDENTIFIER '{request.title.upper()}' CONTAINS HIGH-PERFORMING ALGORITHMIC KEYWORDS. SEARCH VISIBILITY OPTIMIZED."
            title_status = "NOMINAL"
            success_prob += 10
        else:
            title_insight = f"ENTITY IDENTIFIER '{request.title.upper()}' LENGTH ({title_length} CHARS) AND STRUCTURE WITHIN ACCEPTABLE PARAMETERS."
            title_status = "NOMINAL"
            success_prob += 2
            
        # Date Analysis
        date_insight = "DEPLOYMENT WINDOW NOT SPECIFIED. DEFAULT PROJECTIONS APPLIED."
        date_status = "WARNING"
        if request.deployment_date:
            try:
                # Expecting YYYY-MM-DD
                parts = request.deployment_date.split("-")
                if len(parts) == 3:
                    month = int(parts[1])
                    if month in [10, 11, 12]:
                        date_insight = "HOLIDAY WINDOW DETECTED (Q4). HIGH CONVERSION POTENTIAL BUT INCREASED COMPETITIVE NOISE."
                        date_status = "WARNING"
                        success_prob += 8
                    elif month in [6, 7, 8]:
                        date_insight = "SUMMER WINDOW DETECTED. LOWER COMPETITION EXPECTED."
                        date_status = "NOMINAL"
                        success_prob += 5
                    else:
                        date_insight = "STANDARD DEPLOYMENT WINDOW. NO SEASONAL ANOMALIES DETECTED."
                        date_status = "NOMINAL"
            except Exception:
                pass
            
        success_prob = max(1.0, min(99.9, success_prob))
            
        return PredictionResponse(
            success_probability=round(success_prob, 1),
            price_insight=price_insight,
            price_status=price_status,
            genre_insight=genre_insight,
            genre_status=genre_status,
            title_insight=title_insight,
            title_status=title_status,
            date_insight=date_insight,
            date_status=date_status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


# ============================================================================
# API Information
# ============================================================================

@app.get(
    "/api/info",
    tags=["Info"],
    summary="API information",
    description="Get API metadata and available endpoints"
)
def api_info():
    """Get API information and capabilities."""
    return {
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
            "Optional IGDB metadata enrichment when TWITCH_* credentials are set",
            "Text cleaning and normalization",
            "Batch processing of multiple games",
            "AI-ready DataFrame export"
        ],
        "igdb_enrichment_enabled": pipeline.igdb_client.is_configured(),
        "rate_limits": {
            "steam_api": "1.5 seconds between requests",
            "steamspy_api": "1.5 seconds between requests",
            "igdb_api": "~0.35 seconds between requests (client-side throttle)",
            "batch_max_games": 10
        }
    }


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get(
    "/",
    tags=["Root"],
    summary="API root",
    description="Welcome endpoint"
)
def read_root():
    """API root endpoint."""
    return {
        "message": "Welcome to Game Oracle API",
        "docs": "/docs",
        "api_info": "/api/info"
    }
"""Game Oracle API - Steam game data collection and analysis."""

import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
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
"""Pydantic data models for Steam and SteamSpy API responses.

Models defined here validate raw API responses and provide type-safe
data structures for downstream processing.
"""

from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class SteamGameDetails(BaseModel):
    """Validated game details from Steam Store API.

    Attributes:
        app_id: Unique Steam application ID.
        name: Game title.
        short_description: Short description of the game.
        detailed_description: Full HTML description of the game.
        price_usd: Price in USD (None if free).
        genres: List of genre tags (e.g., ['Action', 'RPG']).
        tags: List of Steam tags describing the game.
        categories: List of game categories (e.g., ['Single-player', 'Online PvP']).
        release_date: Release date string (format varies).
        supported_languages: List of supported language codes.
        positive_reviews: Count of positive reviews.
        negative_reviews: Count of negative reviews.
    """

    app_id: int
    name: str
    short_description: str = ""
    detailed_description: str = ""
    price_usd: Optional[float] = None
    genres: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    release_date: str = ""
    supported_languages: List[str] = Field(default_factory=list)
    positive_reviews: int = 0
    negative_reviews: int = 0

    model_config = {"extra": "ignore"}


class SteamReview(BaseModel):
    """Single review from Steam Reviews API.

    Attributes:
        review_id: Unique identifier for the review.
        app_id: Steam application ID this review is for.
        review_text: The review text content.
        voted_up: Whether the review is positive (True) or negative (False).
        timestamp_created: Unix timestamp when review was created.
        author_playtime_forever: Total playtime of reviewer in minutes.
    """

    review_id: str
    app_id: int
    review_text: str
    voted_up: bool
    timestamp_created: int
    author_playtime_forever: Optional[int] = None

    model_config = {"extra": "ignore"}


class SteamSpyData(BaseModel):
    """Validated game data from SteamSpy API.

    SteamSpy provides additional market analysis metrics not available
    directly from Steam's official API, including estimated ownership
    ranges and refined tag scoring.

    Attributes:
        app_id: Unique Steam application ID.
        name: Game title.
        developer: Developer company name.
        publisher: Publisher company name.
        owners: Estimated ownership range as string (e.g., "1,000,000 .. 2,000,000").
        price: Price in cents (multiply by 0.01 to get USD).
        tags: Dictionary of tags with their frequency scores.
        positive: Count of positive reviews.
        negative: Count of negative reviews.
    """

    app_id: int
    name: str
    developer: str = ""
    publisher: str = ""
    owners: str = ""
    price: int = 0
    tags: Dict[str, int] = Field(default_factory=dict)
    positive: int = 0
    negative: int = 0

    model_config = {"extra": "ignore"}


class ProcessedGameRecord(BaseModel):
    """Merged, processed game data ready for analysis.

    This model represents the final output of data collection and preprocessing,
    with all fields normalized and enriched for downstream NLP and market analysis.

    Attributes:
        app_id: Unique Steam application ID.
        name: Game title.
        developer: Developer name.
        publisher: Publisher name.
        price_usd: Price in USD.
        genres: Comma-separated list of genres.
        tags: Comma-separated list of tags (top scoring from SteamSpy).
        categories: Comma-separated list of categories.
        release_date: Release date string.
        supported_languages_count: Number of supported languages.
        estimated_owners_min: Minimum estimated owners from SteamSpy.
        estimated_owners_max: Maximum estimated owners from SteamSpy.
        positive_reviews: Count of positive reviews.
        negative_reviews: Count of negative reviews.
        review_id: Unique review identifier.
        review_text: Cleaned review text.
        voted_up: Raw binary label (True=positive, False=negative).
        sentiment_label: String label ('positive' or 'negative').
        sentiment_score: Binary score (1=positive, 0=negative).
    """

    app_id: int
    name: str
    developer: str = ""
    publisher: str = ""
    price_usd: Optional[float] = None
    genres: str = ""
    tags: str = ""
    categories: str = ""
    release_date: str = ""
    supported_languages_count: int = 0
    estimated_owners_min: Optional[int] = None
    estimated_owners_max: Optional[int] = None
    positive_reviews: int = 0
    negative_reviews: int = 0
    review_id: str = ""
    review_text: str = ""
    voted_up: bool = False
    sentiment_label: str = ""
    sentiment_score: int = 0

    model_config = {"extra": "allow"}

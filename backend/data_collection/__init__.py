"""Game Oracle Data Collection and Preprocessing Module.

This module provides a complete data collection pipeline for Steam game analysis,
fetching data from Steam Web API and SteamSpy, then processing it into
AI-ready DataFrames for NLP fine-tuning and market analysis.

Main Components:
    - GameOraclePipeline: Main orchestrator for complete workflow
    - SteamAPIClient: Steam Store API and Reviews API client
    - SteamSpyClient: SteamSpy API client
    - TextCleaner: Text normalization utilities
    - DataProcessor: Data merging and DataFrame building

Example Usage:
    >>> from data_collection import GameOraclePipeline
    >>>
    >>> pipeline = GameOraclePipeline()
    >>> reviews_df, summary_df = pipeline.collect_and_process(
    ...     game_titles=["Zula", "Wolfteam"],
    ...     max_reviews_per_game=500,
    ...     save_path="data/output"
    ... )
    >>>
    >>> print(f"Collected {len(reviews_df)} reviews")
    >>> print(reviews_df.head())
"""

from .pipeline import GameOraclePipeline
from .clients import SteamAPIClient, SteamSpyClient
from .processors import TextCleaner, DataProcessor
from .models import (
    SteamGameDetails,
    SteamReview,
    SteamSpyData,
    ProcessedGameRecord,
)

__version__ = "0.1.0"
__author__ = "Game Oracle Team"

__all__ = [
    "GameOraclePipeline",
    "SteamAPIClient",
    "SteamSpyClient",
    "TextCleaner",
    "DataProcessor",
    "SteamGameDetails",
    "SteamReview",
    "SteamSpyData",
    "ProcessedGameRecord",
]

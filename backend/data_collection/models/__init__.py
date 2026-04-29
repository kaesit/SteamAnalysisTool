"""Data models for Game Oracle steam data collection.

This package contains Pydantic models for validating and representing
Steam API and SteamSpy API responses, as well as the merged processed game data.
"""

from .game_data import (
    SteamGameDetails,
    SteamReview,
    SteamSpyData,
    ProcessedGameRecord,
)

__all__ = [
    "SteamGameDetails",
    "SteamReview",
    "SteamSpyData",
    "ProcessedGameRecord",
]

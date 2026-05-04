"""Configuration constants for Steam API and SteamSpy API clients.

This module defines all configuration constants required by the data collection
module, including API endpoints, timeouts, and rate limiting parameters.
"""

# Steam Store API Configuration
STEAM_STORE_BASE_URL: str = "https://store.steampowered.com/api"
STEAM_REVIEWS_BASE_URL: str = "https://store.steampowered.com/appreviews"
STEAM_SEARCH_URL: str = "https://store.steampowered.com/api/storesearch"

# SteamSpy API Configuration
STEAMSPY_BASE_URL: str = "https://steamspy.com/api.php"

# IGDB API v4 (Twitch kimlik bilgileri ile; https://api-docs.igdb.com/)
IGDB_API_BASE_URL: str = "https://api.igdb.com/v4"
TWITCH_OAUTH_TOKEN_URL: str = "https://id.twitch.tv/oauth2/token"
# IGDB: Steam mağazası dış kaynağı (`category` yerine `external_game_source` kullanılır)
IGDB_EXTERNAL_GAME_SOURCE_STEAM: int = 1

# HTTP Request Configuration
REQUEST_TIMEOUT: int = 10
REQUEST_MAX_RETRIES: int = 3
RATE_LIMIT_DELAY: float = 1.5
# IGDB kota/rate limit için istekler arası bekleme (saniye)
IGDB_RATE_LIMIT_DELAY: float = 0.35

# Review Fetching Configuration
MAX_REVIEWS_PER_PAGE: int = 100
MAX_REVIEWS_PER_GAME: int = 500

# Country Code for Steam Store API (US for standard pricing)
STEAM_COUNTRY_CODE: str = "us"
STEAM_LANGUAGE: str = "english"

# Retry and Backoff Configuration
INITIAL_BACKOFF_SECONDS: float = 1.0
MAX_BACKOFF_SECONDS: float = 32.0
BACKOFF_MULTIPLIER: float = 2.0

"""Steam Store API and Steam Reviews API client.

This module provides a client for fetching game details, reviews, and search
functionality from Steam's public APIs.
"""

import logging
import os
import time
from typing import Optional, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import (
    STEAM_STORE_BASE_URL,
    STEAM_REVIEWS_BASE_URL,
    STEAM_SEARCH_URL,
    REQUEST_TIMEOUT,
    REQUEST_MAX_RETRIES,
    RATE_LIMIT_DELAY,
    MAX_REVIEWS_PER_PAGE,
    STEAM_COUNTRY_CODE,
    STEAM_LANGUAGE,
    INITIAL_BACKOFF_SECONDS,
    MAX_BACKOFF_SECONDS,
    BACKOFF_MULTIPLIER,
)
from ..models.game_data import SteamGameDetails, SteamReview

logger = logging.getLogger(__name__)


class SteamAPIClient:
    """Client for Steam Store API and Steam Reviews API.

    This client handles all communication with Steam's public APIs, including
    searching for games, fetching game details, and retrieving user reviews.
    Implements rate limiting and retry logic with exponential backoff.

    Attributes:
        api_key: Optional Steam Web API key (currently unused for public endpoints).
        session: Requests session with retry strategy.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize Steam API client.

        Args:
            api_key: Optional Steam Web API key. If not provided, attempts to load
                     from STEAM_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("STEAM_API_KEY")
        self.session = self._create_session_with_retries()
        logger.info("SteamAPIClient initialized")

    def _create_session_with_retries(self) -> requests.Session:
        """Create requests session with exponential backoff retry strategy.

        Returns:
            Configured requests.Session with retry adapter.
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=REQUEST_MAX_RETRIES,
            backoff_factor=BACKOFF_MULTIPLIER,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _request(
        self,
        url: str,
        params: Optional[dict] = None,
        max_retries: Optional[int] = None,
    ) -> Optional[dict]:
        """Execute HTTP GET request with retry and rate limiting.

        Implements exponential backoff for failures and respects rate limits.
        Logs all request attempts and failures.

        Args:
            url: Full URL to request.
            params: Query parameters dictionary.
            max_retries: Number of retry attempts (default from config).

        Returns:
            JSON response as dictionary, or None if request fails after retries.
        """
        if max_retries is None:
            max_retries = REQUEST_MAX_RETRIES

        backoff = INITIAL_BACKOFF_SECONDS

        for attempt in range(max_retries + 1):
            try:
                time.sleep(RATE_LIMIT_DELAY)
                response = self.session.get(
                    url, params=params, timeout=REQUEST_TIMEOUT
                )
                response.raise_for_status()

                logger.debug(f"Request successful: {url} (attempt {attempt + 1})")
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    logger.warning(
                        f"Rate limited (429) on {url}. Backing off {backoff}s"
                    )
                    time.sleep(backoff)
                    backoff = min(backoff * BACKOFF_MULTIPLIER, MAX_BACKOFF_SECONDS)
                    continue
                else:
                    logger.error(
                        f"HTTP error {response.status_code} on {url}: {e}"
                    )

            except requests.exceptions.Timeout:
                logger.error(f"Request timeout on {url} (attempt {attempt + 1})")

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed on {url}: {e}")

            except ValueError as e:
                logger.error(f"Invalid JSON response from {url}: {e}")
                return None

            if attempt < max_retries:
                time.sleep(backoff)
                backoff = min(backoff * BACKOFF_MULTIPLIER, MAX_BACKOFF_SECONDS)

        logger.error(f"All retries exhausted for {url}")
        return None

    def search_game_by_name(self, name: str) -> Optional[int]:
        """Search for a game by title and return its app ID.

        Args:
            name: Game title to search for.

        Returns:
            App ID (int) of first matching game, or None if not found.
        """
        logger.info(f"Searching for game: {name}")

        params = {"term": name, "cc": STEAM_COUNTRY_CODE, "l": STEAM_LANGUAGE}
        response = self._request(STEAM_SEARCH_URL, params)

        if not response or "items" not in response:
            logger.warning(f"No results found for game: {name}")
            return None

        items = response.get("items", [])
        if not items:
            logger.warning(f"Search returned empty items list for: {name}")
            return None

        app_id = items[0].get("id")
        logger.info(f"Found game '{name}' with app_id: {app_id}")
        return app_id

    def get_game_details(self, app_id: int) -> Optional[SteamGameDetails]:
        """Fetch game details from Steam Store API.

        Args:
            app_id: Steam application ID.

        Returns:
            SteamGameDetails object, or None if request fails.
        """
        logger.info(f"Fetching game details for app_id: {app_id}")

        url = f"{STEAM_STORE_BASE_URL}/appdetails"
        params = {"appids": app_id, "cc": STEAM_COUNTRY_CODE, "l": STEAM_LANGUAGE}

        response = self._request(url, params)
        if not response or str(app_id) not in response:
            logger.warning(f"Failed to fetch details for app_id: {app_id}")
            return None

        app_data = response[str(app_id)]
        if not app_data.get("success"):
            logger.warning(f"API returned success=false for app_id: {app_id}")
            return None

        data = app_data.get("data", {})

        try:
            details = SteamGameDetails(
                app_id=app_id,
                name=data.get("name", ""),
                short_description=data.get("short_description", ""),
                detailed_description=data.get("detailed_description", ""),
                price_usd=(
                    data.get("price_overview", {}).get("final_price", 0) / 100
                    if data.get("price_overview")
                    else None
                ),
                genres=[g.get("description") for g in data.get("genres", [])],
                tags=data.get("tags", []),
                categories=[
                    c.get("description") for c in data.get("categories", [])
                ],
                release_date=data.get("release_date", {}).get("date", ""),
                supported_languages=self._parse_languages(
                    data.get("supported_languages", "")
                ),
                positive_reviews=0,
                negative_reviews=0,
            )

            logger.info(f"Successfully parsed game details for: {details.name}")
            return details

        except Exception as e:
            logger.error(f"Error parsing game details for app_id {app_id}: {e}")
            return None

    def get_reviews(
        self,
        app_id: int,
        max_reviews: int = 500,
        language: str = "all",
    ) -> List[SteamReview]:
        """Fetch user reviews for a game.

        Implements cursor-based pagination to fetch multiple pages of reviews.
        Respects rate limiting between paginated requests.

        Args:
            app_id: Steam application ID.
            max_reviews: Maximum number of reviews to fetch.
            language: Review language filter ('all', 'english', etc.).

        Returns:
            List of SteamReview objects.
        """
        logger.info(f"Fetching reviews for app_id: {app_id} (max: {max_reviews})")

        reviews = []
        cursor = "*"
        cursor_count = 0

        while len(reviews) < max_reviews:
            url = f"{STEAM_REVIEWS_BASE_URL}/{app_id}"
            params = {
                "json": 1,
                "filter": "recent",
                "language": language,
                "num_per_page": MAX_REVIEWS_PER_PAGE,
                "cursor": cursor,
            }

            response = self._request(url, params)
            if not response:
                logger.warning(f"Failed to fetch reviews page for app_id: {app_id}")
                break

            review_items = response.get("reviews", [])
            if not review_items:
                logger.info(f"No more reviews found for app_id: {app_id}")
                break

            for review_data in review_items:
                if len(reviews) >= max_reviews:
                    break

                try:
                    review = SteamReview(
                        review_id=str(review_data.get("recommendationid", "")),
                        app_id=app_id,
                        review_text=review_data.get("review", ""),
                        voted_up=review_data.get("voted_up", False),
                        timestamp_created=review_data.get("timestamp_created", 0),
                        author_playtime_forever=review_data.get(
                            "author", {}
                        ).get("playtime_forever"),
                    )
                    reviews.append(review)

                except Exception as e:
                    logger.warning(f"Error parsing review for app_id {app_id}: {e}")
                    continue

            cursor = response.get("cursor", "")
            cursor_count += 1

            if not cursor:
                logger.info(f"Reached end of reviews for app_id: {app_id}")
                break

            if cursor_count > 100:
                logger.warning(
                    f"Exceeded 100 review pages for app_id {app_id}, stopping"
                )
                break

        logger.info(f"Fetched {len(reviews)} reviews for app_id: {app_id}")
        return reviews

    @staticmethod
    def _parse_languages(languages_html: str) -> List[str]:
        """Parse supported languages from HTML string.

        Args:
            languages_html: HTML string containing language information.

        Returns:
            List of language names.
        """
        if not languages_html:
            return []

        languages = []
        parts = languages_html.split("<br>")
        for part in parts:
            part = part.strip()
            if part and part not in ["<strong>*</strong> languages with full audio/video"]:
                part = part.replace("<strong>", "").replace("</strong>", "").strip()
                if part and part != "*":
                    languages.append(part)

        return languages

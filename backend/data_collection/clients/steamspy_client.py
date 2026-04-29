"""SteamSpy API client for game analytics and market data.

SteamSpy provides additional game analytics not available from official Steam API,
including estimated ownership figures, playtime data, and refined tag analytics.
"""

import logging
import time
from typing import Optional, List, Dict

import requests

from ..config import (
    STEAMSPY_BASE_URL,
    REQUEST_TIMEOUT,
    REQUEST_MAX_RETRIES,
    RATE_LIMIT_DELAY,
    INITIAL_BACKOFF_SECONDS,
    MAX_BACKOFF_SECONDS,
    BACKOFF_MULTIPLIER,
)
from ..models.game_data import SteamSpyData

logger = logging.getLogger(__name__)


class SteamSpyClient:
    """Client for SteamSpy API.

    SteamSpy is a third-party service providing game analytics based on Steam data.
    No API key required. Implements rate limiting and retry logic.
    """

    def __init__(self) -> None:
        """Initialize SteamSpy client."""
        logger.info("SteamSpyClient initialized")

    def _request(
        self,
        params: dict,
        max_retries: Optional[int] = None,
    ) -> Optional[dict]:
        """Execute HTTP GET request to SteamSpy API.

        Implements exponential backoff and rate limiting.

        Args:
            params: Query parameters dictionary.
            max_retries: Number of retry attempts (default from config).

        Returns:
            JSON response as dictionary, or None if request fails.
        """
        if max_retries is None:
            max_retries = REQUEST_MAX_RETRIES

        backoff = INITIAL_BACKOFF_SECONDS

        for attempt in range(max_retries + 1):
            try:
                time.sleep(RATE_LIMIT_DELAY)
                response = requests.get(
                    STEAMSPY_BASE_URL,
                    params=params,
                    timeout=REQUEST_TIMEOUT,
                )
                response.raise_for_status()

                logger.debug(
                    f"SteamSpy request successful for params {params} "
                    f"(attempt {attempt + 1})"
                )
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    logger.warning(
                        f"Rate limited (429) by SteamSpy. Backing off {backoff}s"
                    )
                    time.sleep(backoff)
                    backoff = min(backoff * BACKOFF_MULTIPLIER, MAX_BACKOFF_SECONDS)
                    continue
                else:
                    logger.error(f"HTTP error {response.status_code}: {e}")

            except requests.exceptions.Timeout:
                logger.error(
                    f"SteamSpy request timeout (attempt {attempt + 1})"
                )

            except requests.exceptions.RequestException as e:
                logger.error(f"SteamSpy request failed: {e}")

            except ValueError as e:
                logger.error(f"Invalid JSON response from SteamSpy: {e}")
                return None

            if attempt < max_retries:
                time.sleep(backoff)
                backoff = min(backoff * BACKOFF_MULTIPLIER, MAX_BACKOFF_SECONDS)

        logger.error(f"All retries exhausted for SteamSpy request with params {params}")
        return None

    def get_app_details(self, app_id: int) -> Optional[SteamSpyData]:
        """Fetch game details from SteamSpy.

        Args:
            app_id: Steam application ID.

        Returns:
            SteamSpyData object, or None if request fails.
        """
        logger.info(f"Fetching SteamSpy data for app_id: {app_id}")

        params = {"request": "appdetails", "appid": app_id}
        response = self._request(params)

        if not response:
            logger.warning(f"Failed to fetch SteamSpy data for app_id: {app_id}")
            return None

        if "appid" not in response:
            logger.warning(
                f"SteamSpy returned invalid response for app_id: {app_id}"
            )
            return None

        try:
            data = SteamSpyData(
                app_id=response.get("appid", app_id),
                name=response.get("name", ""),
                developer=response.get("developer", ""),
                publisher=response.get("publisher", ""),
                owners=response.get("owners", ""),
                price=response.get("price", 0),
                tags=response.get("tags", {}),
                positive=response.get("positive", 0),
                negative=response.get("negative", 0),
            )

            logger.info(f"Successfully parsed SteamSpy data for: {data.name}")
            return data

        except Exception as e:
            logger.error(f"Error parsing SteamSpy data for app_id {app_id}: {e}")
            return None

    def search_by_name(self, name: str) -> List[Dict]:
        """Search for games by name on SteamSpy.

        Args:
            name: Game name to search for.

        Returns:
            List of matching game dictionaries from SteamSpy.
        """
        logger.info(f"Searching SteamSpy for game: {name}")

        params = {"request": "search", "term": name}
        response = self._request(params)

        if not response:
            logger.warning(f"SteamSpy search returned no results for: {name}")
            return []

        results = response if isinstance(response, list) else []
        logger.info(f"Found {len(results)} results for '{name}' on SteamSpy")
        return results

    def get_top_tags(self, app_id: int, limit: int = 5) -> List[str]:
        """Get top tags for a game from SteamSpy data.

        Args:
            app_id: Steam application ID.
            limit: Maximum number of tags to return.

        Returns:
            List of top tag names, sorted by frequency.
        """
        data = self.get_app_details(app_id)
        if not data:
            return []

        sorted_tags = sorted(
            data.tags.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return [tag for tag, _ in sorted_tags[:limit]]

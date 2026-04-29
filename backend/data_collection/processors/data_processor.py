"""Data processing and merging utilities for collected game data.

This module handles merging data from multiple API sources, parsing complex
fields, and structuring data into AI-ready pandas DataFrames.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd

from ..models.game_data import (
    SteamGameDetails,
    SteamReview,
    SteamSpyData,
    ProcessedGameRecord,
)
from .text_cleaner import TextCleaner

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processor for merging and transforming collected game data.

    Merges Steam API and SteamSpy data, normalizes fields, cleans text,
    and structures everything into AI-ready DataFrames.
    """

    @staticmethod
    def merge_game_data(
        details: SteamGameDetails,
        spy_data: Optional[SteamSpyData],
    ) -> Dict:
        """Merge game details from Steam and SteamSpy sources.

        Resolves conflicts by preferring Steam data (as primary source),
        fills missing fields from SteamSpy, and normalizes prices.

        Args:
            details: Game details from Steam Store API.
            spy_data: Game data from SteamSpy API (optional).

        Returns:
            Merged game metadata dictionary.
        """
        logger.debug(f"Merging data for game: {details.name}")

        merged = {
            "app_id": details.app_id,
            "name": details.name,
            "developer": spy_data.developer if spy_data else "",
            "publisher": spy_data.publisher if spy_data else "",
            "price_usd": details.price_usd,
            "genres": ", ".join(details.genres) if details.genres else "",
            "tags": DataProcessor._get_top_tags(spy_data)
            if spy_data
            else ", ".join(details.tags[:5]),
            "categories": ", ".join(details.categories) if details.categories else "",
            "release_date": details.release_date,
            "supported_languages_count": len(details.supported_languages),
            "positive_reviews": details.positive_reviews
            or (spy_data.positive if spy_data else 0),
            "negative_reviews": details.negative_reviews
            or (spy_data.negative if spy_data else 0),
        }

        if spy_data:
            min_owners, max_owners = DataProcessor.parse_owners_range(spy_data.owners)
            merged["estimated_owners_min"] = min_owners
            merged["estimated_owners_max"] = max_owners
        else:
            merged["estimated_owners_min"] = None
            merged["estimated_owners_max"] = None

        return merged

    @staticmethod
    def build_reviews_dataframe(
        reviews: List[SteamReview],
        game_meta: Dict,
    ) -> pd.DataFrame:
        """Build DataFrame from reviews with game metadata.

        Creates one row per review, with game metadata repeated. Structure is
        optimized for NLP fine-tuning with text input and sentiment labels.

        Args:
            reviews: List of review objects.
            game_meta: Merged game metadata dictionary.

        Returns:
            DataFrame with one row per review.
        """
        logger.info(f"Building reviews DataFrame for {game_meta['name']} "
                    f"({len(reviews)} reviews)")

        records = []

        for review in reviews:
            cleaned_text = TextCleaner.clean_review(review.review_text)

            if not cleaned_text or len(cleaned_text.strip()) < 3:
                logger.debug(f"Skipping review {review.review_id} (empty after cleaning)")
                continue

            sentiment_score = 1 if review.voted_up else 0
            sentiment_label = "positive" if review.voted_up else "negative"

            record = ProcessedGameRecord(
                app_id=game_meta["app_id"],
                name=game_meta["name"],
                developer=game_meta["developer"],
                publisher=game_meta["publisher"],
                price_usd=game_meta["price_usd"],
                genres=game_meta["genres"],
                tags=game_meta["tags"],
                categories=game_meta["categories"],
                release_date=game_meta["release_date"],
                supported_languages_count=game_meta["supported_languages_count"],
                estimated_owners_min=game_meta["estimated_owners_min"],
                estimated_owners_max=game_meta["estimated_owners_max"],
                positive_reviews=game_meta["positive_reviews"],
                negative_reviews=game_meta["negative_reviews"],
                review_id=review.review_id,
                review_text=cleaned_text,
                voted_up=review.voted_up,
                sentiment_label=sentiment_label,
                sentiment_score=sentiment_score,
            )

            records.append(record.model_dump())

        if not records:
            logger.warning(f"No valid reviews for {game_meta['name']}")
            return pd.DataFrame()

        df = pd.DataFrame(records)
        logger.info(f"Created DataFrame with {len(df)} rows for {game_meta['name']}")
        return df

    @staticmethod
    def build_game_summary_dataframe(game_meta: Dict) -> pd.DataFrame:
        """Build single-row DataFrame with aggregated game metrics.

        Creates one row per game with summary statistics for market analysis.

        Args:
            game_meta: Merged game metadata dictionary.

        Returns:
            Single-row DataFrame with game summary metrics.
        """
        logger.info(f"Building summary DataFrame for: {game_meta['name']}")

        total_reviews = (
            game_meta["positive_reviews"] + game_meta["negative_reviews"]
        )

        if total_reviews > 0:
            positive_ratio = (
                game_meta["positive_reviews"] / total_reviews
            )
        else:
            positive_ratio = 0.0

        record = {
            "app_id": game_meta["app_id"],
            "name": game_meta["name"],
            "developer": game_meta["developer"],
            "publisher": game_meta["publisher"],
            "price_usd": game_meta["price_usd"],
            "genres": game_meta["genres"],
            "tags": game_meta["tags"],
            "release_date": game_meta["release_date"],
            "estimated_owners_min": game_meta["estimated_owners_min"],
            "estimated_owners_max": game_meta["estimated_owners_max"],
            "total_reviews": total_reviews,
            "positive_reviews": game_meta["positive_reviews"],
            "negative_reviews": game_meta["negative_reviews"],
            "positive_ratio": positive_ratio,
        }

        return pd.DataFrame([record])

    @staticmethod
    def parse_owners_range(owners_str: str) -> Tuple[Optional[int], Optional[int]]:
        """Parse SteamSpy owners range string to min/max integers.

        SteamSpy returns ownership as a string like "1,000,000 .. 2,000,000".
        This method extracts the numeric bounds.

        Args:
            owners_str: Ownership range string from SteamSpy.

        Returns:
            Tuple of (min_owners, max_owners) as integers, or (None, None).
        """
        if not owners_str:
            return None, None

        try:
            parts = owners_str.split("..")
            if len(parts) != 2:
                return None, None

            min_str = parts[0].strip().replace(",", "")
            max_str = parts[1].strip().replace(",", "")

            min_owners = int(min_str) if min_str else None
            max_owners = int(max_str) if max_str else None

            return min_owners, max_owners

        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse owners range '{owners_str}': {e}")
            return None, None

    @staticmethod
    def _get_top_tags(spy_data: SteamSpyData, limit: int = 5) -> str:
        """Extract top tags from SteamSpy data.

        Args:
            spy_data: SteamSpy game data with tags dictionary.
            limit: Maximum number of tags to include.

        Returns:
            Comma-separated string of top tags.
        """
        if not spy_data.tags:
            return ""

        sorted_tags = sorted(
            spy_data.tags.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        top_tags = [tag for tag, _ in sorted_tags[:limit]]
        return ", ".join(top_tags)

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> bool:
        """Validate DataFrame for required columns and data quality.

        Checks for required columns, non-null values in critical fields,
        and expected data types.

        Args:
            df: DataFrame to validate.

        Returns:
            True if DataFrame passes validation, False otherwise.
        """
        if df.empty:
            logger.warning("DataFrame is empty")
            return False

        required_columns = [
            "app_id",
            "name",
            "review_text",
            "sentiment_label",
            "sentiment_score",
        ]

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            logger.error(f"Missing required columns: {missing}")
            return False

        if df["review_text"].isna().any():
            logger.warning("DataFrame contains NaN in review_text")
            null_count = df["review_text"].isna().sum()
            logger.warning(f"Dropping {null_count} rows with null review_text")
            df = df.dropna(subset=["review_text"])

        if not all(df["sentiment_score"].isin([0, 1])):
            logger.error("sentiment_score contains non-binary values")
            return False

        if not all(df["sentiment_label"].isin(["positive", "negative"])):
            logger.error("sentiment_label contains unexpected values")
            return False

        logger.info(f"DataFrame validation passed: {len(df)} rows")
        return True

    @staticmethod
    def combine_game_dataframes(
        dataframes: List[pd.DataFrame],
    ) -> pd.DataFrame:
        """Combine reviews DataFrames from multiple games.

        Args:
            dataframes: List of individual game review DataFrames.

        Returns:
            Combined DataFrame with all reviews, reset index.
        """
        if not dataframes:
            logger.warning("No dataframes to combine")
            return pd.DataFrame()

        valid_dfs = [df for df in dataframes if not df.empty]

        if not valid_dfs:
            logger.warning("All input DataFrames are empty")
            return pd.DataFrame()

        combined = pd.concat(valid_dfs, ignore_index=True)
        logger.info(f"Combined {len(valid_dfs)} DataFrames into "
                    f"{len(combined)} total rows")
        return combined

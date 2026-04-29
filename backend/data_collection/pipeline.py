"""Game Oracle Data Collection and Preprocessing Pipeline.

Main orchestrator that coordinates API clients, data processing, and output
formatting. This is the primary entry point for collecting and processing
game data from Steam and SteamSpy.
"""

import logging
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd

from .clients.steam_client import SteamAPIClient
from .clients.steamspy_client import SteamSpyClient
from .processors.data_processor import DataProcessor
from .models.game_data import SteamGameDetails, SteamSpyData

logger = logging.getLogger(__name__)


class GameOraclePipeline:
    """Main data collection and preprocessing pipeline.

    Orchestrates the complete workflow: search → fetch details → fetch reviews →
    fetch SteamSpy data → merge → clean → structure into DataFrames.

    The pipeline is designed to be:
    - Batch-processable (multiple games in one call)
    - Recoverable (failures on one game don't stop the pipeline)
    - Logging-rich (full visibility into what's happening)
    - AI-ready (output is structured for NLP fine-tuning)
    """

    def __init__(self) -> None:
        """Initialize pipeline with API clients and processors."""
        self.steam_client = SteamAPIClient()
        self.steamspy_client = SteamSpyClient()
        self.data_processor = DataProcessor()
        logger.info("GameOraclePipeline initialized")

    def collect_and_process(
        self,
        game_titles: List[str],
        max_reviews_per_game: int = 500,
        save_path: Optional[str] = None,
        save_format: str = "parquet",
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Collect and process data for multiple games.

        Main entry point. Fetches data from Steam and SteamSpy for each game,
        merges and cleans the data, and returns AI-ready DataFrames.

        Args:
            game_titles: List of game titles to analyze.
            max_reviews_per_game: Maximum reviews to fetch per game (default 500).
            save_path: Optional path to save output DataFrames (without extension).
            save_format: 'parquet', 'csv', or 'both' (default 'parquet').

        Returns:
            Tuple of (reviews_df, summary_df):
                - reviews_df: One row per review (NLP training data)
                - summary_df: One row per game (market analysis data)

        Examples:
            >>> pipeline = GameOraclePipeline()
            >>> reviews, summary = pipeline.collect_and_process(
            ...     ["Zula", "Wolfteam"],
            ...     max_reviews_per_game=1000
            ... )
            >>> print(f"Collected {len(reviews)} reviews")
        """
        logger.info(f"Starting pipeline for {len(game_titles)} games")

        all_reviews_dfs = []
        all_summary_dfs = []
        failed_games = []

        for title in game_titles:
            try:
                logger.info(f"Processing game: {title}")

                reviews_df, summary_df = self.process_single_game(
                    title=title,
                    max_reviews=max_reviews_per_game,
                )

                if not reviews_df.empty:
                    all_reviews_dfs.append(reviews_df)
                    all_summary_dfs.append(summary_df)
                else:
                    logger.warning(f"No valid data for game: {title}")
                    failed_games.append(title)

            except Exception as e:
                logger.error(f"Failed to process game '{title}': {e}")
                failed_games.append(title)
                continue

        # Combine all DataFrames
        combined_reviews = self.data_processor.combine_game_dataframes(
            all_reviews_dfs
        )
        combined_summary = pd.concat(
            all_summary_dfs, ignore_index=True
        ) if all_summary_dfs else pd.DataFrame()

        logger.info(f"Pipeline complete. Processed {len(game_titles) - len(failed_games)} games")
        if failed_games:
            logger.warning(f"Failed games: {', '.join(failed_games)}")

        # Validate output
        if not combined_reviews.empty:
            self.data_processor.validate_dataframe(combined_reviews)

        # Save if requested
        if save_path:
            self.save_dataframes(
                combined_reviews,
                combined_summary,
                save_path,
                save_format,
            )

        return combined_reviews, combined_summary

    def process_single_game(
        self,
        title: str,
        max_reviews: int = 500,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Process a single game through the complete pipeline.

        Args:
            title: Game title to search and process.
            max_reviews: Maximum reviews to fetch.

        Returns:
            Tuple of (reviews_df, summary_df) for this game.
        """
        logger.info(f"Processing single game: {title}")

        # Step 1: Search for game
        app_id = self.steam_client.search_game_by_name(title)
        if not app_id:
            logger.error(f"Could not find app_id for game: {title}")
            return pd.DataFrame(), pd.DataFrame()

        # Step 2: Fetch game details from Steam
        steam_details = self.steam_client.get_game_details(app_id)
        if not steam_details:
            logger.error(f"Failed to fetch Steam details for app_id: {app_id}")
            return pd.DataFrame(), pd.DataFrame()

        # Step 3: Fetch SteamSpy data
        spy_data = self.steamspy_client.get_app_details(app_id)
        if not spy_data:
            logger.warning(f"SteamSpy data unavailable for app_id: {app_id}")

        # Step 4: Merge data
        game_meta = self.data_processor.merge_game_data(steam_details, spy_data)

        # Step 5: Fetch reviews
        reviews = self.steam_client.get_reviews(app_id, max_reviews=max_reviews)
        if not reviews:
            logger.warning(f"No reviews found for game: {title}")
            return pd.DataFrame(), pd.DataFrame()

        logger.info(f"Fetched {len(reviews)} reviews for: {title}")

        # Step 6: Build DataFrames
        reviews_df = self.data_processor.build_reviews_dataframe(reviews, game_meta)
        summary_df = self.data_processor.build_game_summary_dataframe(game_meta)

        return reviews_df, summary_df

    def save_dataframes(
        self,
        reviews_df: pd.DataFrame,
        summary_df: pd.DataFrame,
        path: str,
        format: str = "parquet",
    ) -> None:
        """Save DataFrames to disk.

        Supports parquet (recommended) and CSV formats.

        Args:
            reviews_df: Reviews DataFrame.
            summary_df: Summary DataFrame.
            path: Base path (without extension).
            format: 'parquet', 'csv', or 'both'.
        """
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        if format in ["parquet", "both"]:
            reviews_path = f"{path}_reviews.parquet"
            summary_path = f"{path}_summary.parquet"

            try:
                reviews_df.to_parquet(reviews_path, index=False)
                summary_df.to_parquet(summary_path, index=False)
                logger.info(f"Saved parquet files: {path}_*.parquet")
            except Exception as e:
                logger.error(f"Failed to save parquet files: {e}")

        if format in ["csv", "both"]:
            reviews_path = f"{path}_reviews.csv"
            summary_path = f"{path}_summary.csv"

            try:
                reviews_df.to_csv(reviews_path, index=False)
                summary_df.to_csv(summary_path, index=False)
                logger.info(f"Saved CSV files: {path}_*.csv")
            except Exception as e:
                logger.error(f"Failed to save CSV files: {e}")

    def get_dataframe_info(self, df: pd.DataFrame) -> None:
        """Log information about a DataFrame.

        Args:
            df: DataFrame to analyze.
        """
        if df.empty:
            logger.info("DataFrame is empty")
            return

        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"Columns: {', '.join(df.columns)}")
        logger.info(f"Data types:\n{df.dtypes}")
        logger.info(f"Missing values:\n{df.isna().sum()}")

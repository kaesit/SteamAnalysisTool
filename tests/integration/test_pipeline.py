"""Integration tests for data collection pipeline."""

import pytest
from data_collection import GameOraclePipeline


@pytest.fixture
def pipeline():
    """Create a GameOraclePipeline instance."""
    return GameOraclePipeline()


class TestGameOraclePipeline:
    """Test suite for GameOraclePipeline."""

    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initializes with all clients."""
        assert pipeline.steam_client is not None
        assert pipeline.steamspy_client is not None
        assert pipeline.data_processor is not None

    def test_search_game_by_name(self, pipeline):
        """Test searching for a game by name."""
        app_id = pipeline.steam_client.search_game_by_name("Counter-Strike 2")
        assert app_id is not None
        assert isinstance(app_id, int)

    def test_search_nonexistent_game(self, pipeline):
        """Test searching for a game that doesn't exist."""
        app_id = pipeline.steam_client.search_game_by_name("Nonexistent Game XYZ 12345")
        assert app_id is None

    def test_process_single_game(self, pipeline):
        """Test processing a single game."""
        reviews_df, summary_df = pipeline.process_single_game(
            title="Portal 2",
            max_reviews=30
        )

        # Check reviews DataFrame
        assert not reviews_df.empty
        assert len(reviews_df) > 0
        assert "review_text" in reviews_df.columns
        assert "sentiment_score" in reviews_df.columns
        assert "sentiment_label" in reviews_df.columns

        # Check summary DataFrame
        assert not summary_df.empty
        assert len(summary_df) == 1
        assert "total_reviews" in summary_df.columns
        assert "positive_ratio" in summary_df.columns

    def test_process_single_game_sentiment_distribution(self, pipeline):
        """Test that sentiment scores are binary (0 or 1)."""
        reviews_df, _ = pipeline.process_single_game(
            title="Portal 2",
            max_reviews=30
        )

        # Check sentiment scores are binary
        valid_scores = reviews_df["sentiment_score"].isin([0, 1]).all()
        assert valid_scores

        # Check sentiment labels are valid
        valid_labels = reviews_df["sentiment_label"].isin(["positive", "negative"]).all()
        assert valid_labels

    def test_process_single_game_no_null_required_fields(self, pipeline):
        """Test that required fields have no null values."""
        reviews_df, summary_df = pipeline.process_single_game(
            title="Portal 2",
            max_reviews=20
        )

        # Check reviews DataFrame
        required_cols = ["review_text", "sentiment_score", "sentiment_label"]
        for col in required_cols:
            assert reviews_df[col].notna().all()

        # Check summary DataFrame
        summary_cols = ["app_id", "name", "total_reviews"]
        for col in summary_cols:
            assert summary_df[col].notna().all()

    def test_collect_and_process_multiple_games(self, pipeline):
        """Test collecting and processing multiple games."""
        reviews_df, summary_df = pipeline.collect_and_process(
            game_titles=["Portal 2", "Half-Life 2"],
            max_reviews_per_game=25
        )

        # Check reviews DataFrame
        assert len(reviews_df) > 0
        assert len(summary_df) >= 1

        # Check that data contains both games (or at least one if other fails)
        games_collected = set(reviews_df["name"].unique())
        assert len(games_collected) >= 1

    def test_collect_single_nonexistent_game(self, pipeline):
        """Test collecting data for non-existent game raises appropriate error."""
        with pytest.raises(Exception):
            pipeline.process_single_game(
                title="Nonexistent Game XYZ 12345",
                max_reviews=50
            )

    def test_collect_and_process_partial_success(self, pipeline):
        """Test batch processing continues even if one game fails."""
        # Mix valid and invalid game titles
        reviews_df, summary_df = pipeline.collect_and_process(
            game_titles=["Portal 2", "Nonexistent Game XYZ"],
            max_reviews_per_game=20
        )

        # Should still collect data from valid games
        assert len(reviews_df) > 0
        assert len(summary_df) >= 1


class TestDataQuality:
    """Test data quality checks on collected data."""

    def test_no_duplicate_reviews(self, pipeline):
        """Test that there are no duplicate reviews."""
        reviews_df, _ = pipeline.process_single_game(
            title="Portal 2",
            max_reviews=30
        )

        # Check for duplicate review IDs
        unique_reviews = reviews_df["review_id"].nunique()
        assert unique_reviews == len(reviews_df)

    def test_game_metadata_consistency(self, pipeline):
        """Test that game metadata is consistent across rows."""
        reviews_df, summary_df = pipeline.process_single_game(
            title="Portal 2",
            max_reviews=30
        )

        # All rows should have the same app_id, name, etc.
        unique_names = reviews_df["name"].nunique()
        assert unique_names == 1

        unique_app_ids = reviews_df["app_id"].nunique()
        assert unique_app_ids == 1

    def test_positive_ratio_calculation(self, pipeline):
        """Test that positive ratio is correctly calculated."""
        reviews_df, summary_df = pipeline.process_single_game(
            title="Portal 2",
            max_reviews=20
        )

        # Calculate expected positive ratio
        positive_count = (reviews_df["sentiment_score"] == 1).sum()
        expected_ratio = positive_count / len(reviews_df)

        # Compare with summary DataFrame
        actual_ratio = summary_df.iloc[0]["positive_ratio"]
        assert abs(expected_ratio - actual_ratio) < 0.0001

    def test_text_cleaning_applied(self, pipeline):
        """Test that text cleaning is applied to reviews."""
        reviews_df, _ = pipeline.process_single_game(
            title="Portal 2",
            max_reviews=20
        )

        # Check that HTML tags are removed
        for review_text in reviews_df["review_text"]:
            assert "<" not in review_text
            assert ">" not in review_text
            assert "[" not in review_text  # BBCode
            assert "]" not in review_text

    def test_review_text_not_empty(self, pipeline):
        """Test that review texts are not empty."""
        reviews_df, _ = pipeline.process_single_game(
            title="Portal 2",
            max_reviews=20
        )

        # All review texts should have content
        assert reviews_df["review_text"].str.len().min() > 0

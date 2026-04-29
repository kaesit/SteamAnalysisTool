"""Unit tests for data processing."""

import pandas as pd
import pytest
from data_collection.processors.data_processor import DataProcessor
from data_collection.models.game_data import SteamGameDetails, SteamSpyData, SteamReview


class TestDataProcessor:
    """Test suite for DataProcessor class."""

    @pytest.fixture
    def processor(self):
        """Create a DataProcessor instance."""
        return DataProcessor()

    @pytest.fixture
    def sample_game_details(self):
        """Create sample game details."""
        return SteamGameDetails(
            app_id=730,
            name="Counter-Strike 2",
            short_description="FPS Game",
            detailed_description="A competitive FPS",
            price_usd=None,
            genres=["Action", "Multiplayer"],
            tags=["FPS", "Competitive"],
            categories=["Multiplayer"],
            release_date="2023-09-01",
            supported_languages=["English", "Spanish"],
            positive_reviews=50000,
            negative_reviews=5000,
        )

    @pytest.fixture
    def sample_steamspy_data(self):
        """Create sample SteamSpy data."""
        return SteamSpyData(
            app_id=730,
            name="Counter-Strike 2",
            developer="Valve",
            publisher="Valve",
            owners="10,000,000 .. 20,000,000",
            price=0,
            tags={"FPS": 50000, "Multiplayer": 45000},
            positive=80000,
            negative=5000,
        )

    def test_parse_owners_range_valid(self, processor):
        """Test parsing valid owner range string."""
        min_val, max_val = processor.parse_owners_range("10,000,000 .. 20,000,000")
        assert min_val == 10_000_000
        assert max_val == 20_000_000

    def test_parse_owners_range_invalid(self, processor):
        """Test parsing invalid owner range string."""
        min_val, max_val = processor.parse_owners_range("invalid")
        assert min_val is None
        assert max_val is None

    def test_parse_owners_range_empty(self, processor):
        """Test parsing empty owner range string."""
        min_val, max_val = processor.parse_owners_range("")
        assert min_val is None
        assert max_val is None

    def test_merge_game_data(self, processor, sample_game_details, sample_steamspy_data):
        """Test merging game data from two sources."""
        merged = processor.merge_game_data(sample_game_details, sample_steamspy_data)

        assert merged["app_id"] == 730
        assert merged["name"] == "Counter-Strike 2"
        assert merged["developer"] == "Valve"
        assert merged["price_usd"] is None
        assert merged["estimated_owners_min"] == 10_000_000
        assert merged["estimated_owners_max"] == 20_000_000

    def test_merge_game_data_without_steamspy(self, processor, sample_game_details):
        """Test merging game data without SteamSpy data."""
        merged = processor.merge_game_data(sample_game_details, None)

        assert merged["app_id"] == 730
        assert merged["name"] == "Counter-Strike 2"
        assert merged["estimated_owners_min"] is None
        assert merged["estimated_owners_max"] is None

    def test_build_reviews_dataframe(self, processor, sample_game_details):
        """Test building reviews DataFrame."""
        reviews = [
            SteamReview(
                review_id="1",
                app_id=730,
                review_text="Great game!",
                voted_up=True,
                timestamp_created=1609459200,
                author_playtime_forever=1000,
            ),
            SteamReview(
                review_id="2",
                app_id=730,
                review_text="Not for me",
                voted_up=False,
                timestamp_created=1609459201,
                author_playtime_forever=100,
            ),
        ]

        game_meta = {
            "app_id": 730,
            "name": "Counter-Strike 2",
            "developer": "Valve",
            "publisher": "Valve",
            "price_usd": None,
            "genres": "Action,Multiplayer",
            "tags": "FPS,Competitive",
            "categories": "Multiplayer",
            "release_date": "2023-09-01",
            "supported_languages_count": 2,
            "estimated_owners_min": 10_000_000,
            "estimated_owners_max": 20_000_000,
            "positive_reviews": 50000,
            "negative_reviews": 5000,
        }

        df = processor.build_reviews_dataframe(reviews, game_meta)

        assert len(df) == 2
        assert "review_text" in df.columns
        assert "sentiment_label" in df.columns
        assert "sentiment_score" in df.columns
        assert df.iloc[0]["voted_up"]  # Use truthy check for numpy types
        assert not df.iloc[1]["voted_up"]

    def test_build_game_summary_dataframe(self, processor):
        """Test building game summary DataFrame."""
        game_meta = {
            "app_id": 730,
            "name": "Counter-Strike 2",
            "developer": "Valve",
            "publisher": "Valve",
            "price_usd": None,
            "genres": "Action,Multiplayer",
            "tags": "FPS,Competitive",
            "release_date": "2023-09-01",
            "estimated_owners_min": 10_000_000,
            "estimated_owners_max": 20_000_000,
            "total_reviews": 100,
            "positive_reviews": 80,
            "negative_reviews": 20,
        }

        df = processor.build_game_summary_dataframe(game_meta)

        assert len(df) == 1
        assert df.iloc[0]["app_id"] == 730
        assert df.iloc[0]["name"] == "Counter-Strike 2"
        assert df.iloc[0]["total_reviews"] == 100

    def test_validate_dataframe_valid(self, processor):
        """Test validating a valid DataFrame."""
        df = pd.DataFrame({
            "app_id": [730, 620],
            "name": ["CS2", "Portal 2"],
            "review_text": ["Good", "Bad"],
            "sentiment_score": [1, 0],
            "sentiment_label": ["positive", "negative"],
        })

        assert processor.validate_dataframe(df) is True

    def test_validate_dataframe_missing_column(self, processor):
        """Test validating DataFrame with missing column."""
        df = pd.DataFrame({
            "app_id": [730, 620],
            "review_text": ["Good", "Bad"],
            # Missing sentiment_score
        })

        assert processor.validate_dataframe(df) is False

    def test_validate_dataframe_invalid_sentiment(self, processor):
        """Test validating DataFrame with invalid sentiment score."""
        df = pd.DataFrame({
            "app_id": [730, 620],
            "review_text": ["Good", "Bad"],
            "sentiment_score": [1, 2],  # Invalid: should be 0 or 1
            "sentiment_label": ["positive", "negative"],
        })

        assert processor.validate_dataframe(df) is False

    def test_combine_game_dataframes(self, processor):
        """Test combining multiple game DataFrames."""
        df1 = pd.DataFrame({
            "app_id": [730],
            "name": ["Counter-Strike 2"],
            "sentiment_score": [1],
        })

        df2 = pd.DataFrame({
            "app_id": [620],
            "name": ["Portal 2"],
            "sentiment_score": [1],
        })

        combined = processor.combine_game_dataframes([df1, df2])

        assert len(combined) == 2
        assert combined.iloc[0]["app_id"] == 730
        assert combined.iloc[1]["app_id"] == 620

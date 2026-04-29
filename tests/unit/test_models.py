"""Unit tests for data models."""

from data_collection.models.game_data import (
    SteamGameDetails,
    SteamReview,
    SteamSpyData,
)


class TestSteamGameDetails:
    """Test suite for SteamGameDetails model."""

    def test_valid_game_details(self):
        """Test creating valid game details."""
        details = SteamGameDetails(
            app_id=730,
            name="Counter-Strike 2",
            short_description="The ultimate team game",
            detailed_description="A long description",
            price_usd=None,
            genres=["Action", "Multiplayer"],
            tags=["FPS", "Competitive"],
            categories=["Multiplayer", "PvP"],
            release_date="2023-09-01",
            supported_languages=["English", "Spanish"],
            positive_reviews=50000,
            negative_reviews=5000,
        )

        assert details.app_id == 730
        assert details.name == "Counter-Strike 2"
        assert details.price_usd is None
        assert len(details.genres) == 2
        assert details.positive_reviews == 50000

    def test_game_details_with_price(self):
        """Test game details with price."""
        details = SteamGameDetails(
            app_id=620,
            name="Portal 2",
            short_description="Puzzle platformer",
            detailed_description="A long description",
            price_usd=9.99,
            genres=["Puzzle"],
            tags=["Physics", "Comedy"],
            categories=["Singleplayer"],
            release_date="2011-04-19",
            supported_languages=["English"],
            positive_reviews=100000,
            negative_reviews=1000,
        )

        assert details.app_id == 620
        assert details.price_usd == 9.99
        assert details.name == "Portal 2"

    def test_game_details_validation(self):
        """Test that game details properly validates app_id type."""
        details = SteamGameDetails(
            app_id=730,
            name="Test Game",
            short_description="Short",
            detailed_description="Long",
            price_usd=None,
            genres=["Action"],
            tags=["Test"],
            categories=["Multiplayer"],
            release_date="2023-01-01",
            supported_languages=["English"],
            positive_reviews=100,
            negative_reviews=10,
        )

        assert isinstance(details.app_id, int)
        assert details.app_id == 730


class TestSteamReview:
    """Test suite for SteamReview model."""

    def test_valid_positive_review(self):
        """Test creating a positive review."""
        review = SteamReview(
            review_id="123456",
            app_id=730,
            review_text="Amazing game!",
            voted_up=True,
            timestamp_created=1609459200,
            author_playtime_forever=10000,
        )

        assert review.review_id == "123456"
        assert review.app_id == 730
        assert review.voted_up is True
        assert review.review_text == "Amazing game!"

    def test_valid_negative_review(self):
        """Test creating a negative review."""
        review = SteamReview(
            review_id="789012",
            app_id=730,
            review_text="Not my cup of tea",
            voted_up=False,
            timestamp_created=1609459200,
            author_playtime_forever=100,
        )

        assert review.review_id == "789012"
        assert review.voted_up is False
        assert review.author_playtime_forever == 100

    def test_review_with_none_playtime(self):
        """Test review with None playtime."""
        review = SteamReview(
            review_id="345678",
            app_id=620,
            review_text="Good game",
            voted_up=True,
            timestamp_created=1609459200,
            author_playtime_forever=None,
        )

        assert review.author_playtime_forever is None
        assert review.voted_up is True


class TestSteamSpyData:
    """Test suite for SteamSpyData model."""

    def test_valid_steamspy_data(self):
        """Test creating valid SteamSpy data."""
        data = SteamSpyData(
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

        assert data.app_id == 730
        assert data.name == "Counter-Strike 2"
        assert data.owners == "10,000,000 .. 20,000,000"
        assert data.price == 0
        assert data.positive == 80000

    def test_steamspy_data_with_price(self):
        """Test SteamSpy data with price."""
        data = SteamSpyData(
            app_id=620,
            name="Portal 2",
            developer="Valve",
            publisher="Valve",
            owners="5,000,000 .. 10,000,000",
            price=999,
            tags={"Puzzle": 30000, "Physics": 25000},
            positive=100000,
            negative=2000,
        )

        assert data.app_id == 620
        assert data.price == 999
        assert data.owners == "5,000,000 .. 10,000,000"

    def test_empty_tags(self):
        """Test SteamSpy data with empty tags."""
        data = SteamSpyData(
            app_id=999,
            name="Unknown Game",
            developer="Dev",
            publisher="Pub",
            owners="100,000 .. 500,000",
            price=1999,
            tags={},
            positive=500,
            negative=50,
        )

        assert data.tags == {}
        assert data.positive == 500

"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check_returns_ok(self, client):
        """Test health endpoint returns OK status."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "Game Oracle API"
        assert "version" in data


class TestAPIInfoEndpoint:
    """Test API info endpoint."""

    def test_api_info_returns_metadata(self, client):
        """Test API info endpoint returns metadata."""
        response = client.get("/api/info")
        assert response.status_code == 200

        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data
        assert "capabilities" in data
        assert "rate_limits" in data

    def test_api_info_contains_all_endpoints(self, client):
        """Test API info contains all endpoints."""
        response = client.get("/api/info")
        data = response.json()

        endpoints = data["endpoints"]
        assert "health" in endpoints
        assert "search" in endpoints
        assert "collect_single" in endpoints
        assert "collect_batch" in endpoints


class TestGameSearchEndpoint:
    """Test game search endpoint."""

    def test_search_finds_existing_game(self, client):
        """Test searching for an existing game."""
        response = client.post(
            "/api/games/search",
            json={"query": "Counter-Strike 2"}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["found"] is True
        assert data["app_id"] is not None
        assert "game_title" in data

    def test_search_returns_not_found_for_invalid_game(self, client):
        """Test searching for non-existent game."""
        response = client.post(
            "/api/games/search",
            json={"query": "Nonexistent Game XYZ 12345"}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["found"] is False
        assert data["app_id"] is None

    def test_search_missing_query(self, client):
        """Test search endpoint with missing query."""
        response = client.post(
            "/api/games/search",
            json={}
        )
        assert response.status_code == 422  # Validation error


class TestCollectGameDataEndpoint:
    """Test single game data collection endpoint."""

    def test_collect_single_game_success(self, client):
        """Test collecting data for a single game."""
        response = client.post(
            "/api/games/collect",
            json={"title": "Portal 2", "max_reviews": 30}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["total_reviews_collected"] > 0
        assert 0 <= data["positive_ratio"] <= 1
        assert "reviews_info" in data
        assert "summary_info" in data

    def test_collect_dataframe_structure(self, client):
        """Test that collected DataFrames have correct structure."""
        response = client.post(
            "/api/games/collect",
            json={"title": "Portal 2", "max_reviews": 20}
        )
        data = response.json()

        # Check reviews DataFrame info
        reviews_info = data["reviews_info"]
        assert reviews_info["row_count"] > 0
        assert reviews_info["column_count"] > 0
        assert "review_text" in reviews_info["columns"]
        assert "sentiment_score" in reviews_info["columns"]
        assert "sentiment_label" in reviews_info["columns"]

        # Check summary DataFrame info
        summary_info = data["summary_info"]
        assert summary_info["row_count"] == 1
        assert "positive_ratio" in summary_info["columns"]
        assert "total_reviews" in summary_info["columns"]

    def test_collect_game_not_found(self, client):
        """Test collecting data for non-existent game."""
        response = client.post(
            "/api/games/collect",
            json={"title": "Nonexistent Game XYZ 12345", "max_reviews": 50}
        )
        assert response.status_code == 404

    def test_collect_max_reviews_validation(self, client):
        """Test max_reviews validation."""
        # Test too high
        response = client.post(
            "/api/games/collect",
            json={"title": "Portal 2", "max_reviews": 9999}
        )
        assert response.status_code == 422

        # Test too low
        response = client.post(
            "/api/games/collect",
            json={"title": "Portal 2", "max_reviews": 5}
        )
        assert response.status_code == 422

    def test_collect_missing_title(self, client):
        """Test collect endpoint with missing title."""
        response = client.post(
            "/api/games/collect",
            json={"max_reviews": 50}
        )
        assert response.status_code == 422


class TestBatchCollectEndpoint:
    """Test batch game data collection endpoint."""

    def test_batch_collect_multiple_games(self, client):
        """Test collecting data for multiple games."""
        response = client.post(
            "/api/games/collect-batch",
            json={
                "game_titles": ["Portal 2", "Half-Life 2"],
                "max_reviews_per_game": 30
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["total_reviews_collected"] > 0
        assert data["summary_info"]["row_count"] >= 1

    def test_batch_collect_empty_list_validation(self, client):
        """Test batch collect with empty game list."""
        response = client.post(
            "/api/games/collect-batch",
            json={
                "game_titles": [],
                "max_reviews_per_game": 50
            }
        )
        assert response.status_code == 400

    def test_batch_collect_too_many_games(self, client):
        """Test batch collect with too many games."""
        games = [f"Game {i}" for i in range(15)]
        response = client.post(
            "/api/games/collect-batch",
            json={
                "game_titles": games,
                "max_reviews_per_game": 50
            }
        )
        assert response.status_code == 400

    def test_batch_collect_max_reviews_validation(self, client):
        """Test batch collect max_reviews validation."""
        response = client.post(
            "/api/games/collect-batch",
            json={
                "game_titles": ["Portal 2"],
                "max_reviews_per_game": 9999
            }
        )
        assert response.status_code == 422

    def test_batch_collect_missing_games(self, client):
        """Test batch collect with missing game_titles."""
        response = client.post(
            "/api/games/collect-batch",
            json={"max_reviews_per_game": 50}
        )
        assert response.status_code == 422


class TestRootEndpoint:
    """Test root endpoint."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "docs" in data

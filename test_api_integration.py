#!/usr/bin/env python
"""Test API integration - verify FastAPI endpoints work with data collection module."""

import subprocess
import time
import requests
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path("backend").resolve()))

BASE_URL = "http://localhost:8000"
SERVER_PROCESS = None


def start_server():
    """Start the FastAPI development server."""
    global SERVER_PROCESS
    print("\n" + "="*70)
    print("STARTING API SERVER")
    print("="*70 + "\n")

    try:
        SERVER_PROCESS = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(3)  # Wait for server to start
        print("OK: Server started on port 8000\n")
        return True
    except Exception as e:
        print(f"ERROR: Failed to start server: {e}\n")
        return False


def stop_server():
    """Stop the FastAPI development server."""
    global SERVER_PROCESS
    if SERVER_PROCESS:
        print("\n" + "="*70)
        print("STOPPING API SERVER")
        print("="*70 + "\n")
        SERVER_PROCESS.terminate()
        SERVER_PROCESS.wait(timeout=5)
        print("OK: Server stopped\n")


def test_health():
    """Test health check endpoint."""
    print("="*70)
    print("1. HEALTH CHECK TEST")
    print("="*70 + "\n")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "Game Oracle API"

        print(f"OK: Health check passed")
        print(f"  Status: {data['status']}")
        print(f"  Service: {data['service']}")
        print(f"  Version: {data['version']}\n")
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}\n")
        return False


def test_api_info():
    """Test API info endpoint."""
    print("="*70)
    print("2. API INFO TEST")
    print("="*70 + "\n")

    try:
        response = requests.get(f"{BASE_URL}/api/info", timeout=10)
        assert response.status_code == 200

        data = response.json()
        assert "endpoints" in data
        assert "capabilities" in data

        print(f"OK: API info retrieved")
        print(f"  Endpoints: {len(data['endpoints'])}")
        print(f"  Capabilities: {len(data['capabilities'])}")
        print(f"  Rate limits configured: Yes\n")
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}\n")
        return False


def test_game_search():
    """Test game search endpoint."""
    print("="*70)
    print("3. GAME SEARCH TEST")
    print("="*70 + "\n")

    try:
        payload = {"query": "Counter-Strike 2"}
        response = requests.post(
            f"{BASE_URL}/api/games/search",
            json=payload,
            timeout=30
        )
        assert response.status_code == 200

        data = response.json()
        assert data["found"] is True
        assert data["app_id"] is not None

        print(f"OK: Game search successful")
        print(f"  Query: {payload['query']}")
        print(f"  Found: {data['found']}")
        print(f"  Game: {data['game_title']}")
        print(f"  App ID: {data['app_id']}\n")
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}\n")
        return False


def test_single_game_collection():
    """Test single game data collection endpoint."""
    print("="*70)
    print("4. SINGLE GAME COLLECTION TEST")
    print("="*70 + "\n")

    try:
        payload = {
            "title": "Portal 2",
            "max_reviews": 50
        }
        print(f"Collecting data for: {payload['title']}")
        print(f"Max reviews: {payload['max_reviews']}\n")

        response = requests.post(
            f"{BASE_URL}/api/games/collect",
            json=payload,
            timeout=60
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["total_reviews_collected"] > 0

        print(f"OK: Single game collection successful")
        print(f"  Total reviews: {data['total_reviews_collected']}")
        print(f"  Positive ratio: {data['positive_ratio']:.1%}")
        print(f"  Reviews DataFrame:")
        print(f"    - Rows: {data['reviews_info']['row_count']}")
        print(f"    - Columns: {data['reviews_info']['column_count']}")
        print(f"    - Required columns present: {all(col in data['reviews_info']['columns'] for col in ['review_text', 'sentiment_score', 'sentiment_label'])}")
        print(f"  Summary DataFrame:")
        print(f"    - Rows: {data['summary_info']['row_count']}")
        print(f"    - Columns: {data['summary_info']['column_count']}\n")
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}\n")
        return False


def test_batch_collection():
    """Test batch game data collection endpoint."""
    print("="*70)
    print("5. BATCH GAME COLLECTION TEST")
    print("="*70 + "\n")

    try:
        payload = {
            "game_titles": ["Half-Life 2", "Dota 2"],
            "max_reviews_per_game": 50
        }
        print(f"Collecting data for {len(payload['game_titles'])} games:")
        for game in payload['game_titles']:
            print(f"  - {game}")
        print(f"Max reviews per game: {payload['max_reviews_per_game']}\n")

        response = requests.post(
            f"{BASE_URL}/api/games/collect-batch",
            json=payload,
            timeout=120
        )
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["total_reviews_collected"] > 0

        print(f"OK: Batch collection successful")
        print(f"  Games processed: {data['summary_info']['row_count']}")
        print(f"  Total reviews: {data['total_reviews_collected']}")
        print(f"  Positive ratio: {data['positive_ratio']:.1%}")
        print(f"  Reviews DataFrame:")
        print(f"    - Rows: {data['reviews_info']['row_count']}")
        print(f"    - Columns: {data['reviews_info']['column_count']}")
        print(f"  Summary DataFrame:")
        print(f"    - Rows: {data['summary_info']['row_count']}")
        print(f"    - Columns: {data['summary_info']['column_count']}\n")
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}\n")
        return False


def test_validation():
    """Test input validation."""
    print("="*70)
    print("6. INPUT VALIDATION TEST")
    print("="*70 + "\n")

    tests_passed = 0
    tests_total = 0

    # Test empty batch
    tests_total += 1
    try:
        payload = {"game_titles": [], "max_reviews_per_game": 50}
        response = requests.post(
            f"{BASE_URL}/api/games/collect-batch",
            json=payload,
            timeout=10
        )
        assert response.status_code == 400
        print("OK: Empty batch correctly rejected\n")
        tests_passed += 1
    except Exception as e:
        print(f"ERROR: Empty batch validation failed: {e}\n")

    # Test too many games
    tests_total += 1
    try:
        payload = {
            "game_titles": [f"Game {i}" for i in range(15)],
            "max_reviews_per_game": 50
        }
        response = requests.post(
            f"{BASE_URL}/api/games/collect-batch",
            json=payload,
            timeout=10
        )
        assert response.status_code == 400
        print("OK: Too many games correctly rejected\n")
        tests_passed += 1
    except Exception as e:
        print(f"ERROR: Too many games validation failed: {e}\n")

    # Test max_reviews bounds
    tests_total += 1
    try:
        payload = {
            "title": "Portal 2",
            "max_reviews": 9999  # Out of bounds
        }
        response = requests.post(
            f"{BASE_URL}/api/games/collect",
            json=payload,
            timeout=10
        )
        assert response.status_code == 422  # Validation error
        print("OK: Out of bounds max_reviews correctly rejected\n")
        tests_passed += 1
    except Exception as e:
        print(f"ERROR: Bounds validation failed: {e}\n")

    print(f"Validation tests: {tests_passed}/{tests_total} passed\n")
    return tests_passed == tests_total


def main():
    """Run all API integration tests."""
    print("\n" + "="*70)
    print("GAME ORACLE - API INTEGRATION TEST SUITE")
    print("="*70 + "\n")

    # Start server
    if not start_server():
        print("\nFAILED: Could not start API server")
        sys.exit(1)

    try:
        # Run tests
        results = {
            "Health Check": test_health(),
            "API Info": test_api_info(),
            "Game Search": test_game_search(),
            "Single Game Collection": test_single_game_collection(),
            "Batch Collection": test_batch_collection(),
            "Input Validation": test_validation(),
        }

        # Summary
        print("="*70)
        print("TEST SUMMARY")
        print("="*70 + "\n")

        passed = sum(1 for v in results.values() if v)
        total = len(results)

        for test_name, result in results.items():
            status = "PASS" if result else "FAIL"
            print(f"  {test_name:30} {status}")

        print(f"\nTotal: {passed}/{total} tests passed\n")

        if passed == total:
            print("="*70)
            print("ALL TESTS PASSED!")
            print("="*70 + "\n")
            print("API is ready for use. Access documentation:")
            print("  - Swagger UI: http://localhost:8000/docs")
            print("  - ReDoc: http://localhost:8000/redoc")
            print("  - API Info: http://localhost:8000/api/info\n")
            return 0
        else:
            print("="*70)
            print("SOME TESTS FAILED!")
            print("="*70 + "\n")
            return 1

    finally:
        stop_server()


if __name__ == "__main__":
    sys.exit(main())

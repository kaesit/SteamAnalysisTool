"""Test script for Game Oracle data collection module.

Tests the module components without requiring heavy API calls.
Designed to verify basic functionality and data structures.
"""

import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from data_collection import (
    TextCleaner,
    SteamAPIClient,
    SteamSpyClient,
    DataProcessor,
    GameOraclePipeline,
)
from data_collection.models import SteamGameDetails, SteamReview, SteamSpyData

logger = logging.getLogger(__name__)


def test_text_cleaner() -> bool:
    """Test TextCleaner functionality."""
    logger.info("=" * 60)
    logger.info("TEST 1: TextCleaner")
    logger.info("=" * 60)

    test_cases = [
        (
            "<p>Great game!</p>",
            "Great game!",
            "HTML tag removal",
        ),
        (
            "Line1\nLine2\r\nLine3",
            "Line1 Line2 Line3",
            "Newline normalization",
        ),
        (
            "Multiple   spaces",
            "Multiple spaces",
            "Whitespace collapse",
        ),
        (
            "[b]Bold[/b] text",
            "Bold text",
            "BBCode removal",
        ),
        (
            "&quot;Hello&quot; &amp; goodbye",
            '"Hello" & goodbye',
            "HTML entity decoding",
        ),
    ]

    cleaner = TextCleaner()
    all_passed = True

    for input_text, expected, description in test_cases:
        cleaned = cleaner.clean_review(input_text)
        passed = cleaned == expected
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status}: {description}")
        if not passed:
            logger.info(f"  Input:    {input_text}")
            logger.info(f"  Expected: {expected}")
            logger.info(f"  Got:      {cleaned}")
            all_passed = False

    return all_passed


def test_data_models() -> bool:
    """Test Pydantic data models."""
    logger.info("=" * 60)
    logger.info("TEST 2: Data Models")
    logger.info("=" * 60)

    try:
        # Test SteamGameDetails
        details = SteamGameDetails(
            app_id=730,
            name="Counter-Strike 2",
            price_usd=0.0,
            genres=["Action", "FPS"],
            positive_reviews=100000,
            negative_reviews=5000,
        )
        logger.info(f"✓ PASS: SteamGameDetails created: {details.name}")

        # Test SteamReview
        review = SteamReview(
            review_id="123",
            app_id=730,
            review_text="Great game!",
            voted_up=True,
            timestamp_created=1234567890,
        )
        logger.info(f"✓ PASS: SteamReview created: {review.review_id}")

        # Test SteamSpyData
        spy_data = SteamSpyData(
            app_id=730,
            name="Counter-Strike 2",
            developer="Valve",
            owners="10,000,000 .. 20,000,000",
            positive=100000,
            negative=5000,
        )
        logger.info(f"✓ PASS: SteamSpyData created: {spy_data.name}")

        return True

    except Exception as e:
        logger.error(f"✗ FAIL: Error creating data models: {e}")
        return False


def test_data_processor() -> bool:
    """Test DataProcessor functionality."""
    logger.info("=" * 60)
    logger.info("TEST 3: DataProcessor")
    logger.info("=" * 60)

    try:
        processor = DataProcessor()

        # Test parsing owners range
        min_owners, max_owners = processor.parse_owners_range(
            "1,000,000 .. 2,000,000"
        )
        assert min_owners == 1000000, f"Expected 1000000, got {min_owners}"
        assert max_owners == 2000000, f"Expected 2000000, got {max_owners}"
        logger.info("✓ PASS: Owners range parsing")

        # Test merging game data
        details = SteamGameDetails(
            app_id=730,
            name="Counter-Strike 2",
            price_usd=0.0,
            genres=["Action"],
        )
        spy_data = SteamSpyData(
            app_id=730,
            name="CS2",
            developer="Valve",
            owner="10,000,000 .. 20,000,000",
        )

        merged = processor.merge_game_data(details, spy_data)
        assert merged["name"] == "Counter-Strike 2", "Name mismatch"
        assert merged["developer"] == "Valve", "Developer mismatch"
        logger.info("✓ PASS: Game data merging")

        return True

    except Exception as e:
        logger.error(f"✗ FAIL: DataProcessor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_clients() -> bool:
    """Test API client initialization."""
    logger.info("=" * 60)
    logger.info("TEST 4: API Clients")
    logger.info("=" * 60)

    try:
        steam_client = SteamAPIClient()
        logger.info("✓ PASS: SteamAPIClient initialized")

        steamspy_client = SteamSpyClient()
        logger.info("✓ PASS: SteamSpyClient initialized")

        return True

    except Exception as e:
        logger.error(f"✗ FAIL: API client initialization failed: {e}")
        return False


def test_pipeline_initialization() -> bool:
    """Test GameOraclePipeline initialization."""
    logger.info("=" * 60)
    logger.info("TEST 5: Pipeline Initialization")
    logger.info("=" * 60)

    try:
        pipeline = GameOraclePipeline()
        logger.info("✓ PASS: GameOraclePipeline initialized")
        logger.info(f"  - Steam client: {pipeline.steam_client.__class__.__name__}")
        logger.info(f"  - SteamSpy client: {pipeline.steamspy_client.__class__.__name__}")
        logger.info(f"  - Data processor: {pipeline.data_processor.__class__.__name__}")

        return True

    except Exception as e:
        logger.error(f"✗ FAIL: Pipeline initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main() -> None:
    """Run all tests."""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 58 + "║")
    logger.info("║" + "  GAME ORACLE - DATA COLLECTION MODULE TESTS".center(58) + "║")
    logger.info("║" + " " * 58 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    logger.info("\n")

    results = []

    results.append(("TextCleaner", test_text_cleaner()))
    results.append(("Data Models", test_data_models()))
    results.append(("DataProcessor", test_data_processor()))
    results.append(("API Clients", test_api_clients()))
    results.append(("Pipeline", test_pipeline_initialization()))

    logger.info("\n")
    logger.info("=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status}: {test_name}")

    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)

    logger.info(f"\nTotal: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        logger.info("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        logger.error("\n❌ Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

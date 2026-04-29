#!/usr/bin/env python
"""Demo script to test the data collection module with real Steam API data."""

import sys
import logging
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path("backend").resolve()))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from data_collection import GameOraclePipeline, TextCleaner

print("\n" + "="*70)
print("GAME ORACLE - DATA COLLECTION DEMO")
print("="*70 + "\n")

# Test 1: Text Cleaner
print("TEST 1: Text Cleaning")
print("-" * 70)

raw_review = "<p>Great game! [b]Highly recommended[/b]</p>\nCheck: http://example.com"
clean_review = TextCleaner.clean_review(raw_review)

print(f"Raw text:    {raw_review}")
print(f"Cleaned:     {clean_review}")
print()

# Test 2: Real API call - Search for game
print("TEST 2: Search Game on Steam")
print("-" * 70)

pipeline = GameOraclePipeline()
game_name = "Counter-Strike 2"
print(f"Searching for: {game_name}")

app_id = pipeline.steam_client.search_game_by_name(game_name)

if app_id:
    print(f"Found! App ID: {app_id}")
else:
    print(f"Not found on Steam")
    sys.exit(1)

print()

# Test 3: Fetch game details
print("TEST 3: Fetch Game Details")
print("-" * 70)

details = pipeline.steam_client.get_game_details(app_id)

if details:
    price_str = f"${details.price_usd:.2f}" if details.price_usd else "Free"
    print(f"Name:              {details.name}")
    print(f"Price:             {price_str}")
    print(f"Genres:            {', '.join(details.genres)}")
    print(f"Release Date:      {details.release_date}")
    print(f"Positive Reviews:  {details.positive_reviews:,}")
    print(f"Negative Reviews:  {details.negative_reviews:,}")
else:
    print("Failed to fetch game details")
    sys.exit(1)

print()

# Test 4: Fetch reviews (small batch for demo)
print("TEST 4: Fetch Reviews from Steam")
print("-" * 70)

print(f"Fetching 20 reviews from {game_name}... (this takes ~15-30 seconds)")
reviews = pipeline.steam_client.get_reviews(app_id, max_reviews=20)

if reviews:
    print(f"Fetched: {len(reviews)} reviews")
    print()

    # Show first review
    first = reviews[0]
    print("First Review:")
    print(f"  Text: {first.review_text[:100]}...")
    print(f"  Sentiment: {'Positive' if first.voted_up else 'Negative'}")
    print(f"  Playtime: {first.author_playtime_forever} minutes")
else:
    print("No reviews found")
    sys.exit(1)

print()

# Test 5: Full pipeline
print("TEST 5: Complete Pipeline (Search -> Details -> Reviews -> Process)")
print("-" * 70)

print(f"Processing game: {game_name}")
reviews_df, summary_df = pipeline.process_single_game(game_name, max_reviews=50)

print()
print(f"RESULTS:")
print(f"  Reviews collected:    {len(reviews_df)}")
print(f"  Positive reviews:     {(reviews_df['sentiment_score'] == 1).sum()}")
print(f"  Negative reviews:     {(reviews_df['sentiment_score'] == 0).sum()}")
print()

if len(reviews_df) > 0:
    print("DataFrame Info:")
    print(f"  Columns: {list(reviews_df.columns)}")
    print(f"  Shape: {reviews_df.shape}")
    print()

    print("Sample Reviews:")
    for idx, (_, row) in enumerate(reviews_df.head(3).iterrows(), 1):
        sentiment = "POSITIVE" if row['sentiment_score'] == 1 else "NEGATIVE"
        print(f"\n  Review {idx} [{sentiment}]:")
        print(f"    Has text: Yes ({len(row['review_text'])} characters)")

print()
print("="*70)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("="*70)
print("\nYour data collection module is working!")
print("\nNext steps:")
print("  1. Read: backend/data_collection/README.md")
print("  2. Explore: notebooks/01_data_collection_example.ipynb")
print("  3. Use: from data_collection import GameOraclePipeline")
print()

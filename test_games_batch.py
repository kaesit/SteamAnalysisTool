#!/usr/bin/env python
"""Test with different games including popular ones."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("backend").resolve()))

import logging
logging.basicConfig(level=logging.WARNING)

from data_collection import GameOraclePipeline
import pandas as pd

pipeline = GameOraclePipeline()

# Populer oyunlar
games_to_test = [
    "Portal 2",
    "Half-Life 2",
    "The Elder Scrolls V: Skyrim",
]

print("\n" + "="*70)
print("TEST SUITE: POPULAR GAMES")
print("="*70 + "\n")

all_data = []

for i, game_name in enumerate(games_to_test, 1):
    print(f"[{i}/{len(games_to_test)}] Testing: {game_name}")

    try:
        # Search
        app_id = pipeline.steam_client.search_game_by_name(game_name)
        if not app_id:
            print(f"     ERROR: Game not found\n")
            continue

        # Get details
        details = pipeline.steam_client.get_game_details(app_id)
        if not details:
            print(f"     ERROR: Could not fetch details\n")
            continue

        # Get reviews
        reviews = pipeline.steam_client.get_reviews(app_id, max_reviews=100)
        if not reviews:
            print(f"     WARNING: No reviews found\n")
            continue

        # Collect info
        all_data.append({
            'game': game_name,
            'app_id': app_id,
            'reviews_count': len(reviews),
            'positive': sum(1 for r in reviews if r.voted_up),
            'negative': sum(1 for r in reviews if not r.voted_up),
        })

        pos = sum(1 for r in reviews if r.voted_up)
        neg = sum(1 for r in reviews if not r.voted_up)
        pos_ratio = pos / len(reviews) * 100

        print(f"     OK: {len(reviews)} reviews | {pos_ratio:.1f}% positive")
        print(f"        App ID: {app_id}\n")

    except Exception as e:
        print(f"     ERROR: {str(e)[:60]}\n")

if all_data:
    print("="*70)
    print("SUMMARY TABLE")
    print("="*70 + "\n")

    df = pd.DataFrame(all_data)
    df['positive_ratio'] = df['positive'] / df['reviews_count'] * 100

    for idx, row in df.iterrows():
        print(f"{idx+1}. {row['game']:40}")
        print(f"   App ID: {row['app_id']:6} | Reviews: {row['reviews_count']:3} | "
              f"Positive: {row['positive_ratio']:5.1f}%")

    print("\n" + "="*70)
    print("AGGREGATE STATS")
    print("="*70 + "\n")

    total_reviews = df['reviews_count'].sum()
    total_positive = df['positive'].sum()
    overall_positive = total_positive / total_reviews * 100

    print(f"Games tested:       {len(df)}")
    print(f"Total reviews:      {total_reviews}")
    print(f"Overall positive:   {overall_positive:.1f}%")
    print(f"Avg reviews/game:   {total_reviews / len(df):.0f}")

    print("\n" + "="*70)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*70 + "\n")
else:
    print("\nNo games were successfully processed.")

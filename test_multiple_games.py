#!/usr/bin/env python
"""Test script to run data collection on multiple games."""

import sys
import logging
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path("backend").resolve()))

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)

from data_collection import GameOraclePipeline

print("\n" + "="*70)
print("GAME ORACLE - MULTIPLE GAMES TEST")
print("="*70 + "\n")

pipeline = GameOraclePipeline()

# Test with different games
test_games = [
    "Dota 2",
    "PUBG: Battlegrounds",
    "Valorant"
]

print(f"Testing {len(test_games)} games:\n")
for game in test_games:
    print(f"  - {game}")

print("\n" + "-"*70)
print("FETCHING DATA (this will take 2-3 minutes)...\n")

all_reviews = []
all_summaries = []

for i, game_title in enumerate(test_games, 1):
    print(f"[{i}/{len(test_games)}] Processing: {game_title}")

    try:
        reviews_df, summary_df = pipeline.process_single_game(
            title=game_title,
            max_reviews=100  # 100 per game for speed
        )

        if not reviews_df.empty:
            all_reviews.append(reviews_df)
            all_summaries.append(summary_df)

            positive = (reviews_df['sentiment_score'] == 1).sum()
            negative = (reviews_df['sentiment_score'] == 0).sum()

            print(f"  OK: Success! {len(reviews_df)} reviews ({positive} pos, {negative} neg)")
        else:
            print(f"  WARN: No reviews found")

    except Exception as e:
        print(f"  ERROR: Failed: {str(e)[:50]}")

print("\n" + "="*70)
print("RESULTS SUMMARY")
print("="*70 + "\n")

if all_reviews:
    combined_reviews = pd.concat(all_reviews, ignore_index=True)
    combined_summary = pd.concat(all_summaries, ignore_index=True)

    print(f"Total Reviews Collected: {len(combined_reviews)}")
    print(f"Games Processed: {len(combined_summary)}\n")

    # By game statistics
    print("By Game:")
    print("-" * 70)
    for idx, game in combined_summary.iterrows():
        name = game['name'][:30]
        total = game['total_reviews']
        pos_ratio = game['positive_ratio']
        price = game['price_usd'] if game['price_usd'] else 'Free'

        print(f"  {name:30} | Reviews: {total:6} | Positive: {pos_ratio:5.1%} | Price: ${price}")

    print("\n" + "-" * 70)
    print("Overall Statistics:")
    print(f"  Total Reviews:      {len(combined_reviews)}")
    print(f"  Total Games:        {len(combined_summary)}")
    print(f"  Avg Reviews/Game:   {len(combined_reviews) / len(combined_summary):.0f}")
    print(f"  Positive Ratio:     {(combined_reviews['sentiment_score'] == 1).sum() / len(combined_reviews):.1%}")

    # DataFrame columns
    print("\nDataFrame Schema:")
    print(f"  Columns: {len(combined_reviews.columns)}")
    print(f"  Shape: {combined_reviews.shape}")

    print("\nColumns available:")
    for col in combined_reviews.columns:
        dtype = combined_reviews[col].dtype
        print(f"  • {col:30} ({dtype})")

    # Export example
    print("\n" + "="*70)
    print("EXPORT EXAMPLES")
    print("="*70 + "\n")

    # Export for NLP
    nlp_data = combined_reviews[['review_text', 'sentiment_score']].copy()
    print(f"1. NLP Training Format ({len(nlp_data)} rows):")
    print(f"   - review_text (input)")
    print(f"   - sentiment_score (label: 0 or 1)")
    print(f"   Ready to train on any transformer model!\n")

    # Export for market analysis
    market_data = combined_summary[[
        'name', 'price_usd', 'positive_ratio', 'total_reviews',
        'estimated_owners_min', 'estimated_owners_max'
    ]].copy()

    print(f"2. Market Analysis Format ({len(market_data)} games):")
    for col in market_data.columns:
        print(f"   - {col}")
    print()

    # Top reviewed games
    print(f"3. Most Reviewed Games:")
    top_games = combined_summary.nlargest(3, 'total_reviews')[['name', 'total_reviews', 'positive_ratio']]
    for idx, game in top_games.iterrows():
        print(f"   • {game['name']}: {game['total_reviews']} reviews ({game['positive_ratio']:.1%} positive)")

    # Sentiment breakdown
    print(f"\n4. Sentiment Breakdown:")
    positive = (combined_reviews['sentiment_score'] == 1).sum()
    negative = (combined_reviews['sentiment_score'] == 0).sum()
    print(f"   • Positive: {positive} ({positive/len(combined_reviews):.1%})")
    print(f"   • Negative: {negative} ({negative/len(combined_reviews):.1%})")

print("\n" + "="*70)
print("TEST COMPLETED SUCCESSFULLY!")
print("="*70 + "\n")

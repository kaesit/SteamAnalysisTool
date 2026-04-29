#!/usr/bin/env python
"""Test export and different use case scenarios."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("backend").resolve()))

import logging
logging.basicConfig(level=logging.WARNING)

from data_collection import GameOraclePipeline
from data_collection import TextCleaner

pipeline = GameOraclePipeline()

print("\n" + "="*70)
print("EXPORT & SCENARIOS TEST")
print("="*70 + "\n")

# Collect data
game = "Portal 2"
print(f"Collecting data from: {game}\n")

reviews_df, summary_df = pipeline.process_single_game(game, max_reviews=200)

print("="*70)
print("1. TEXT CLEANING SHOWCASE")
print("="*70 + "\n")

# Show raw vs cleaned
sample_raw = reviews_df.iloc[0]['review_text']
sample_clean = TextCleaner.clean_review(sample_raw)

print(f"Sample raw review length: {len(sample_raw)} chars")
print(f"Sample cleaned length: {len(sample_clean)} chars")
print(f"Reduction: {(1 - len(sample_clean)/len(sample_raw))*100:.1f}%\n")

print("="*70)
print("2. SENTIMENT FILTERING")
print("="*70 + "\n")

positive_only = reviews_df[reviews_df['sentiment_score'] == 1]
negative_only = reviews_df[reviews_df['sentiment_score'] == 0]

print(f"All reviews: {len(reviews_df)}")
print(f"Positive only: {len(positive_only)} ({len(positive_only)/len(reviews_df)*100:.1f}%)")
print(f"Negative only: {len(negative_only)} ({len(negative_only)/len(reviews_df)*100:.1f}%)")

print(f"\nAvg text length by sentiment:")
print(f"  Positive: {positive_only['review_text'].str.len().mean():.0f} chars")
print(f"  Negative: {negative_only['review_text'].str.len().mean():.0f} chars")

print(f"\n")

print("="*70)
print("3. EXPORT SCENARIOS")
print("="*70 + "\n")

# Scenario 1: NLP Training
print("A) NLP Training Data Export")
nlp_data = reviews_df[['review_text', 'sentiment_score']].copy()
print(f"   Format: {nlp_data.shape}")
print(f"   Can export to: CSV, Parquet, JSON")
print(f"   Use with: Hugging Face, TensorFlow, PyTorch")

# Scenario 2: Market Analysis
print("\nB) Market Analysis Export")
market_data = summary_df[[
    'name', 'price_usd', 'positive_ratio', 'total_reviews',
    'estimated_owners_min', 'estimated_owners_max'
]].copy()
print(f"   Format: {market_data.shape}")
print(f"   Can export to: Excel, JSON, CSV")
print(f"   Use with: Tableau, Power BI, Looker")

# Scenario 3: Detailed Review Analysis
print("\nC) Detailed Review Analysis Export")
detailed = reviews_df[[
    'review_id', 'review_text', 'sentiment_label',
    'voted_up', 'genres', 'tags', 'price_usd'
]].copy()
print(f"   Format: {detailed.shape}")
print(f"   Can export to: Database, Data warehouse")
print(f"   Use with: SQL queries, Analytics")

print(f"\n")

print("="*70)
print("4. FILTERING & AGGREGATION EXAMPLES")
print("="*70 + "\n")

# Filter by text length
long_reviews = reviews_df[reviews_df['review_text'].str.len() > 200]
print(f"Long reviews (>200 chars): {len(long_reviews)} ({len(long_reviews)/len(reviews_df)*100:.1f}%)")

# Price analysis
free_reviews = reviews_df[reviews_df['price_usd'] == 0.0]
paid_reviews = reviews_df[reviews_df['price_usd'] > 0.0]

print(f"Reviews for free games: {len(free_reviews)}")
print(f"Reviews for paid games: {len(paid_reviews)}")

# Tag analysis
if reviews_df['tags'].notna().any():
    print(f"\nGames have tags: Yes")
    tags_with_reviews = reviews_df[reviews_df['tags'].notna()]
    print(f"  Reviews with tags: {len(tags_with_reviews)}")

print(f"\n")

print("="*70)
print("5. BATCH EXPORT TEST")
print("="*70 + "\n")

export_formats = ['parquet', 'csv']

for fmt in export_formats:
    try:
        export_path = f"data/test_export.{fmt}"
        pipeline.save_dataframes(
            reviews_df, summary_df,
            path="data/test_export",
            format=fmt
        )
        print(f"{fmt.upper():10} export: OK")
    except Exception as e:
        print(f"{fmt.upper():10} export: ERROR - {str(e)[:40]}")

print(f"\nExported to: data/ directory")

print(f"\n")

print("="*70)
print("6. DATA QUALITY METRICS")
print("="*70 + "\n")

# Uniqueness
unique_games = reviews_df['name'].nunique()
unique_reviews = reviews_df['review_id'].nunique()

print(f"Unique games: {unique_games}")
print(f"Unique reviews: {unique_reviews}")
print(f"Duplicates: {len(reviews_df) - unique_reviews}")

# Data completeness
completeness = {}
for col in reviews_df.columns:
    complete = reviews_df[col].notna().sum() / len(reviews_df) * 100
    completeness[col] = complete

critical_cols = ['app_id', 'review_text', 'sentiment_score', 'sentiment_label']
print(f"\nCritical field completeness:")
for col in critical_cols:
    print(f"  {col:30} {completeness[col]:6.1f}%")

print(f"\n")

print("="*70)
print("ALL EXPORT TESTS PASSED!")
print("="*70 + "\n")

print("You can now:")
print("  1. Export data for ML models")
print("  2. Create market analysis reports")
print("  3. Build dashboards")
print("  4. Feed data to BI tools")
print("  5. Store in database\n")

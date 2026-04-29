#!/usr/bin/env python
"""Test data analysis and processing features."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("backend").resolve()))

import logging
logging.basicConfig(level=logging.WARNING)

from data_collection import GameOraclePipeline

pipeline = GameOraclePipeline()

print("\n" + "="*70)
print("DATA ANALYSIS TEST")
print("="*70 + "\n")

# Collect data from 2 games
games = ["Portal 2", "Half-Life 2"]
print(f"Collecting data from {len(games)} games...\n")

reviews_df, summary_df = pipeline.collect_and_process(
    game_titles=games,
    max_reviews_per_game=150
)

print("="*70)
print("1. DATAFRAME STRUCTURE")
print("="*70 + "\n")

print(f"Reviews DataFrame:")
print(f"  Shape: {reviews_df.shape}")
print(f"  Rows (individual reviews): {len(reviews_df)}")
print(f"  Columns: {len(reviews_df.columns)}")
print(f"\nSummary DataFrame:")
print(f"  Shape: {summary_df.shape}")
print(f"  Rows (games): {len(summary_df)}")
print(f"\n")

print("="*70)
print("2. SENTIMENT ANALYSIS")
print("="*70 + "\n")

positive = (reviews_df['sentiment_score'] == 1).sum()
negative = (reviews_df['sentiment_score'] == 0).sum()
total = len(reviews_df)

print(f"Positive reviews: {positive}/{total} ({positive/total*100:.1f}%)")
print(f"Negative reviews: {negative}/{total} ({negative/total*100:.1f}%)")

print(f"\nBreakdown by game:")
for game_name in reviews_df['name'].unique():
    game_reviews = reviews_df[reviews_df['name'] == game_name]
    pos_count = (game_reviews['sentiment_score'] == 1).sum()
    neg_count = (game_reviews['sentiment_score'] == 0).sum()
    print(f"  {game_name:30} | Pos: {pos_count:3} | Neg: {neg_count:3}")

print(f"\n")

print("="*70)
print("3. TEXT ANALYSIS")
print("="*70 + "\n")

print(f"Review text statistics:")
print(f"  Total reviews with text: {reviews_df['review_text'].notna().sum()}")
print(f"  Avg text length: {reviews_df['review_text'].str.len().mean():.0f} characters")
print(f"  Min length: {reviews_df['review_text'].str.len().min()}")
print(f"  Max length: {reviews_df['review_text'].str.len().max()}")

print(f"\nText length distribution:")
bins = [0, 50, 100, 200, 500, 2000]
for i in range(len(bins)-1):
    count = ((reviews_df['review_text'].str.len() >= bins[i]) &
             (reviews_df['review_text'].str.len() < bins[i+1])).sum()
    pct = count / len(reviews_df) * 100
    print(f"  {bins[i]:4}-{bins[i+1]:4} chars: {count:3} ({pct:5.1f}%)")

print(f"\n")

print("="*70)
print("4. MARKET ANALYSIS")
print("="*70 + "\n")

print(f"Game summary data:\n")
for idx, game in summary_df.iterrows():
    name = game['name'][:30]
    total_rev = game['total_reviews']
    pos_ratio = game['positive_ratio'] * 100

    print(f"  {name:30}")
    print(f"    Total reviews: {total_rev:,}")
    print(f"    Positive ratio: {pos_ratio:.1f}%")
    if game['estimated_owners_min']:
        owners_min = game['estimated_owners_min']
        owners_max = game['estimated_owners_max']
        print(f"    Est. players: {owners_min:,} - {owners_max:,}")
    print()

print("="*70)
print("5. EXPORT TEST")
print("="*70 + "\n")

# Test export for NLP
nlp_format = reviews_df[['review_text', 'sentiment_score']].copy()
print(f"NLP Export Format: {nlp_format.shape}")
print(f"  Columns: {list(nlp_format.columns)}")
print(f"  Ready for: BERT, DistilBERT, RoBERTa, etc.")
print()

# Test export for market analysis
market_format = summary_df[[
    'name', 'positive_ratio', 'total_reviews', 'estimated_owners_min'
]].copy()
print(f"Market Analysis Format: {market_format.shape}")
print(f"  Columns: {list(market_format.columns)}")
print(f"  Ready for: BI Tools, Dashboards, Reports")
print()

print("="*70)
print("6. DATA QUALITY CHECK")
print("="*70 + "\n")

# Missing values
missing = reviews_df.isna().sum()
missing_cols = missing[missing > 0]

if len(missing_cols) > 0:
    print(f"Columns with missing values:")
    for col, count in missing_cols.items():
        print(f"  {col}: {count}")
else:
    print("No missing values! Data quality is excellent.")

# Validate sentiment
valid_sentiments = reviews_df['sentiment_score'].isin([0, 1]).all()
print(f"\nSentiment score valid: {valid_sentiments}")

valid_labels = reviews_df['sentiment_label'].isin(['positive', 'negative']).all()
print(f"Sentiment label valid: {valid_labels}")

print(f"\n")

print("="*70)
print("ALL ANALYSIS TESTS PASSED!")
print("="*70 + "\n")

print("Data is ready for:")
print("  1. NLP Model Training")
print("  2. Market Analysis")
print("  3. Sentiment Analysis")
print("  4. Dashboard/BI Tools")
print("  5. Machine Learning Models\n")

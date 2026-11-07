
import pandas as pd
from pathlib import Path

INPUT_FILE = Path("outputs/editorial_review_sheet.csv")
OUTPUT_DIR = Path("outputs")

WEIGHTS = {
    "hook_rating": 25,
    "context_rating": 20,
    "emotional_impact_rating": 20,
    "escalation_rating": 15,
    "ending_rating": 20
}

df = pd.read_csv(INPUT_FILE)

# Convert ratings into numeric values
for col in WEIGHTS:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Identify candidates with complete ratings
complete = df[list(WEIGHTS)].notna().all(axis=1)

# Validate ratings are between 0 and 5
invalid = df[list(WEIGHTS)].notna() & (
    (df[list(WEIGHTS)] < 0) | (df[list(WEIGHTS)] > 5)
)

if invalid.any().any():
    raise ValueError("Ratings must be between 0 and 5.")

reviewed = df[complete].copy()
pending = df[~complete].copy()

# Calculate weighted editorial score
reviewed["editorial_score"] = sum(
    (reviewed[col] / 5) * weight
    for col, weight in WEIGHTS.items()
)

# Sort by editorial score
reviewed = reviewed.sort_values(
    by="editorial_score",
    ascending=False
)

reviewed.insert(
    0,
    "editorial_rank",
    range(1, len(reviewed) + 1)
)

# Save all reviewed candidates
reviewed.to_csv(
    OUTPUT_DIR / "final_ranked_promo_shortlist.csv",
    index=False
)

# Save top 10
reviewed.head(10).to_csv(
    OUTPUT_DIR / "top_10_promos.csv",
    index=False
)

# Save candidates still awaiting review
pending.to_csv(
    OUTPUT_DIR / "pending_editorial_reviews.csv",
    index=False
)

print("\nEDITORIAL RANKING COMPLETE")
print("--------------------------")
print("Total candidates:", len(df))
print("Reviewed candidates:", len(reviewed))
print("Pending candidates:", len(pending))

if len(reviewed) > 0:
    print("\nTOP 10 PROMOTIONAL CLIPS")
    print(
        reviewed[
            [
                "editorial_rank",
                "candidate_id",
                "episode_number",
                "start_timestamp",
                "end_timestamp",
                "editorial_score"
            ]
        ].head(10).to_string(index=False)
    )
else:
    print("\nNo candidates have complete ratings yet.")

print("\nFiles saved:")
print("- outputs/final_ranked_promo_shortlist.csv")
print("- outputs/top_10_promos.csv")
print("- outputs/pending_editorial_reviews.csv")

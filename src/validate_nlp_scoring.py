
import pandas as pd
from pathlib import Path

review_path = Path("outputs/editorial_review_sheet.csv")
score_path = Path("outputs/automated_scored_candidates.csv")

review = pd.read_csv(review_path)
scores = pd.read_csv(score_path)

reviewed = review[
    review["review_status"] == "Reviewed - screenplay inspection"
].copy()

comparison = reviewed.merge(
    scores[["candidate_id", "automated_score", "automated_rank"]],
    on="candidate_id",
    how="left"
)

print("=" * 60)
print("NLP SCORING VALIDATION")
print("=" * 60)

print("Human-reviewed candidates:", len(reviewed))
print("Matched candidates:", comparison["automated_score"].notna().sum())
print("Missing automated matches:", comparison["automated_score"].isna().sum())

print("\nHUMAN VS AUTOMATED SCORES")

columns = [
    "candidate_id",
    "editorial_score",
    "automated_score",
    "automated_rank"
]

print(
    comparison[columns]
    .sort_values("editorial_score", ascending=False)
    .to_string(index=False)
)

matched = comparison.dropna(
    subset=["editorial_score", "automated_score"]
)

if len(matched) >= 2:
    correlation = matched[
        ["editorial_score", "automated_score"]
    ].corr(method="spearman").iloc[0, 1]

    print("\nSpearman rank correlation:", round(correlation, 3))
else:
    print("\nNot enough matched candidates to calculate correlation.")

print("\nINTERPRETATION")
print(
    "This is a small exploratory comparison, not a reliable "
    "model validation dataset."
)

comparison.to_csv(
    "outputs/editorial_automated_comparison.csv",
    index=False
)

print("\nSaved: outputs/editorial_automated_comparison.csv")

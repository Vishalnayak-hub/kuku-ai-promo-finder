
import pandas as pd
from pathlib import Path

output_dir = Path("outputs")

review = pd.read_csv(output_dir / "editorial_review_sheet.csv")
ranked = pd.read_csv(output_dir / "final_ranked_promo_shortlist.csv")
top10 = pd.read_csv(output_dir / "top_10_promos.csv")
pending = pd.read_csv(output_dir / "pending_editorial_reviews.csv")

reviewed = review[
    review["review_status"] == "Reviewed - screenplay inspection"
]

duplicate_count = review["candidate_id"].duplicated().sum()

score_check = reviewed.merge(
    ranked[["candidate_id", "editorial_score"]],
    on="candidate_id",
    suffixes=("_review", "_ranked"),
    how="left"
)

mismatches = (
    score_check["editorial_score_review"]
    != score_check["editorial_score_ranked"]
).sum()

missing_ranked = score_check["editorial_score_ranked"].isna().sum()

pending_count = (
    review["review_status"] == "Pending human review"
).sum()

print("=" * 55)
print("FINAL DATA QUALITY CHECK")
print("=" * 55)

print("\n1. CANDIDATE COUNTS")
print("Total:", len(review))
print("Reviewed:", len(reviewed))
print("Pending:", pending_count)

print("\n2. DUPLICATE CHECK")
print("Duplicate IDs:", duplicate_count)

print("\n3. RANKING CHECK")
print(ranked[
    ["editorial_rank", "candidate_id", "editorial_score"]
].head(10).to_string(index=False))

print("\n4. OUTPUT CONSISTENCY")
print("Top 10 rows:", len(top10))
print("Pending output rows:", len(pending))
print("Score mismatches:", mismatches)
print("Reviewed candidates missing from ranking:", missing_ranked)

checks = {
    "Candidate IDs are unique": duplicate_count == 0,
    "All reviewed candidates are ranked": missing_ranked == 0,
    "Scores match": mismatches == 0,
    "Pending count is consistent": len(pending) == pending_count,
    "Top 10 output is consistent": len(top10) == min(10, len(ranked)),
}

print("\n5. VALIDATION RESULTS")
for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {name}")

print("\n" + "=" * 55)

if all(checks.values()):
    print("PASS: All data quality checks completed.")
else:
    print("WARNING: Investigate failed checks.")

print("=" * 55)

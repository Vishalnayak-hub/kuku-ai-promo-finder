
import pandas as pd

review = pd.read_csv("outputs/editorial_review_sheet.csv")
scored = pd.read_csv("outputs/automated_scored_candidates.csv")

reviewed = review[
    review["review_status"] == "Reviewed - screenplay inspection"
]

missing = reviewed[
    ~reviewed["candidate_id"].isin(scored["candidate_id"])
]

print("EDITORIAL REVIEW COLUMNS:")
print(review.columns.tolist())

print("\nMISSING CANDIDATES:")
print(missing[
    ["candidate_id", "episode_number",
     "start_timestamp", "end_timestamp", "duration_seconds"]
].to_string(index=False))

print("\nAVAILABLE EVENT TIMELINE:")
print("event_timeline" in review.columns)

if "event_timeline" in review.columns:
    for _, row in missing.iterrows():
        print("\n", row["candidate_id"])
        print(str(row["event_timeline"])[:1500])

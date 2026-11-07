
import pandas as pd

file = "outputs/editorial_review_sheet.csv"
df = pd.read_csv(file)

print("\nTOTAL ROWS:", len(df))

print("\nEPISODE 1 CANDIDATES:")
ep1 = df[df["episode_number"] == 1]

print(
    ep1[
        [
            "candidate_id",
            "start_timestamp",
            "end_timestamp",
            "hook_rating",
            "context_rating",
            "emotional_impact_rating",
            "escalation_rating",
            "ending_rating"
        ]
    ].to_string(index=False)
)

print("\nNUMBER OF COMPLETELY RATED CANDIDATES:")
rating_cols = [
    "hook_rating",
    "context_rating",
    "emotional_impact_rating",
    "escalation_rating",
    "ending_rating"
]

print(df[rating_cols].notna().all(axis=1).sum())

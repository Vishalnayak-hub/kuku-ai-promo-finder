
import pandas as pd

df = pd.read_csv(
    "outputs/promo_candidates_refined.csv"
).fillna("")

candidate_ids = [
    "EP046_0000000_30",
    "EP046_0003000_30",
    "EP046_0000500_30",
    "EP046_0001000_30",
    "EP046_0000000_40",
    "EP046_0000000_50",
    "EP046_0000000_60",
]

for candidate_id in candidate_ids:
    rows = df[df["candidate_id"] == candidate_id]

    if rows.empty:
        print(f"\nCandidate not found: {candidate_id}")
        continue

    row = rows.iloc[0]

    print("\n" + "=" * 80)
    print("Candidate:", candidate_id)
    print("Time:", row["start_timestamp"], "-", row["end_timestamp"])
    print("Duration:", row["duration_seconds"])
    print("-" * 80)
    print(row["event_timeline"])

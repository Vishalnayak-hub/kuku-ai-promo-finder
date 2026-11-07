
import pandas as pd

# Load refined promo candidates
df = pd.read_csv("outputs/promo_candidates_refined.csv")

# Select Episode 11 candidates
episode_11 = df[df["episode_number"] == 11].copy()

# Candidate windows to inspect
candidate_ids = [
    "EP011_0000000_30",
    "EP011_0000500_30",
    "EP011_0001000_30",
    "EP011_0000000_40",
    "EP011_0000000_50",
    "EP011_0000000_60",
]

for candidate_id in candidate_ids:
    candidate = episode_11[
        episode_11["candidate_id"] == candidate_id
    ]

    if candidate.empty:
        print(f"\nCandidate not found: {candidate_id}")
        continue

    row = candidate.iloc[0]

    print("\n" + "=" * 80)
    print("Candidate:", row["candidate_id"])
    print("Time:", row["start_timestamp"], "-", row["end_timestamp"])
    print("Duration:", row["duration_seconds"])
    print("-" * 80)
    print(row["event_timeline"])

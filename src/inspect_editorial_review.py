
import pandas as pd

df = pd.read_csv("outputs/editorial_review.csv").fillna("")

for _, row in df.iterrows():
    print("\n" + "=" * 90)
    print(f"Candidate: {row['candidate_id']}")
    print(
        f"Episode: {row['episode_number']} | "
        f"Duration: {row['duration_seconds']} seconds"
    )
    print(
        f"Time: {row['start_timestamp']} - "
        f"{row['end_timestamp']}"
    )
    print("-" * 90)
    print(row["event_timeline"])


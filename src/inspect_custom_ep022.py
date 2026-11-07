
import pandas as pd

df = pd.read_csv("outputs/editorial_review_sheet.csv")

candidate = df[
    df["candidate_id"] == "EP022_0006500_52"
]

if candidate.empty:
    raise ValueError("Candidate not found.")

row = candidate.iloc[0]

print("CANDIDATE:", row["candidate_id"])
print("START:", row["start_timestamp"])
print("END:", row["end_timestamp"])
print("DURATION:", row["duration_seconds"])

print("\nCLIPPED EVENT TIMELINE:\n")
print(row["event_timeline"])

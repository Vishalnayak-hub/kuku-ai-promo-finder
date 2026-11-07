
import pandas as pd

df = pd.read_csv("outputs/editorial_review_sheet.csv")

candidate_id = "EP028_0000000_50"

candidate = df[df["candidate_id"] == candidate_id]

if candidate.empty:
    raise ValueError("Candidate not found.")

row = candidate.iloc[0]

print("\nEPISODE 28 — 50-SECOND CANDIDATE")
print("--------------------------------")
print("Candidate:", row["candidate_id"])
print("Start:", row["start_timestamp"])
print("End:", row["end_timestamp"])

print("\nSCREENPLAY CONTENT")
print("------------------")

for column in df.columns:
    if any(word in column.lower() for word in ["dialogue", "action", "camera", "sound"]):
        print(f"\n{column}:")
        print(row[column])

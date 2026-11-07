
import pandas as pd
from pathlib import Path

INPUT = Path("outputs/automated_scored_candidates.csv")
OUTPUT = Path("outputs/deduplicated_candidates.csv")
TOP_OUTPUT = Path("outputs/deduplicated_top_30.csv")
SUPPRESSED_OUTPUT = Path("outputs/suppressed_duplicates.csv")

df = pd.read_csv(INPUT)

def to_seconds(timestamp):
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)

df["start_sec"] = df["start_timestamp"].apply(to_seconds)
df["end_sec"] = df["end_timestamp"].apply(to_seconds)

# Highest-scoring candidates are considered first.
df = df.sort_values(
    "automated_score", ascending=False
).reset_index(drop=True)

selected = []
suppressed = []

for _, candidate in df.iterrows():
    duplicate_of = None

    for chosen in selected:
        if candidate["episode_number"] != chosen["episode_number"]:
            continue

        intersection = max(
            0,
            min(candidate["end_sec"], chosen["end_sec"])
            - max(candidate["start_sec"], chosen["start_sec"])
        )

        shorter_duration = min(
            candidate["end_sec"] - candidate["start_sec"],
            chosen["end_sec"] - chosen["start_sec"]
        )

        overlap_ratio = (
            intersection / shorter_duration
            if shorter_duration > 0 else 0
        )

        # Suppress candidates that substantially overlap
        # an already selected higher-scoring candidate.
        if overlap_ratio >= 0.70:
            duplicate_of = chosen["candidate_id"]
            break

    if duplicate_of is None:
        selected.append(candidate)
    else:
        item = candidate.to_dict()
        item["suppressed_by"] = duplicate_of
        suppressed.append(item)

unique_df = pd.DataFrame(selected)
suppressed_df = pd.DataFrame(suppressed)

unique_df.insert(
    0, "unique_rank", range(1, len(unique_df) + 1)
)

unique_df.drop(
    columns=["start_sec", "end_sec"],
    inplace=True
)

if not suppressed_df.empty:
    suppressed_df.drop(
        columns=["start_sec", "end_sec"],
        inplace=True
    )

unique_df.to_csv(OUTPUT, index=False)
unique_df.head(30).to_csv(TOP_OUTPUT, index=False)
suppressed_df.to_csv(SUPPRESSED_OUTPUT, index=False)

print("=" * 55)
print("NEAR-DUPLICATE DETECTION COMPLETE")
print("=" * 55)
print("Original candidates:", len(df))
print("Unique candidates:", len(unique_df))
print("Suppressed overlapping candidates:", len(suppressed_df))

print("\nTOP 20 UNIQUE CANDIDATES:")
print(
    unique_df[
        ["unique_rank", "candidate_id", "automated_score"]
    ].head(20).to_string(index=False)
)

print("\nOUTPUT FILES:")
print(OUTPUT)
print(TOP_OUTPUT)
print(SUPPRESSED_OUTPUT)

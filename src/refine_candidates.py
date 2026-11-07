
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "outputs" / "promo_candidates.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"

df = pd.read_csv(INPUT_FILE).fillna("")

# Load the original parsed screenplay events
blocks = pd.read_csv(
    PROJECT_DIR / "outputs" / "screenplay_blocks_v2.csv"
).fillna("")

refined_records = []

for _, candidate in df.iterrows():

    start = candidate["start_seconds"]
    end = candidate["end_seconds"]
    episode = candidate["episode_number"]

    events = blocks[
        (blocks["episode_number"] == episode) &
        (blocks["start_seconds"] < end) &
        (blocks["end_seconds"] > start)
    ].copy()

    events = events.sort_values(
        ["start_seconds", "end_seconds"]
    )

    event_lines = []

    for _, event in events.iterrows():

        # Clip the displayed event interval to the promo window.
        clipped_start = max(event["start_seconds"], start)
        clipped_end = min(event["end_seconds"], end)

        event_lines.append(
            f"[{clipped_start:.2f}-{clipped_end:.2f}] "
            f"{event['block_type']}: "
            f"{event['content']}"
        )

    refined_records.append({
        "candidate_id": candidate["candidate_id"],
        "episode_number": episode,
        "start_timestamp": candidate["start_timestamp"],
        "end_timestamp": candidate["end_timestamp"],
        "duration_seconds": candidate["duration_seconds"],
        "scene_numbers": candidate["scene_numbers"],
        "block_count": len(events),
        "event_timeline": "\n".join(event_lines)
    })

refined = pd.DataFrame(refined_records)

output_file = OUTPUT_DIR / "promo_candidates_refined.csv"

refined.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 55)
print("REFINED CANDIDATE DATASET")
print("=" * 55)

print("Total candidates:", len(refined))
print("Missing event timelines:", refined["event_timeline"].eq("").sum())

print("\nFirst candidate:")
print(refined.iloc[0]["event_timeline"])

print("\nSaved to:", output_file)

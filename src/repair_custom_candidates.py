
import pandas as pd

candidate_file = "outputs/promo_candidates_refined.csv"
screenplay_file = "outputs/screenplay_blocks_v2.csv"
editorial_file = "outputs/editorial_review_sheet.csv"

candidates = [
    {
        "candidate_id": "EP028_0000000_48",
        "episode_number": 28,
        "start": 0.0,
        "end": 48.0,
    },
    {
        "candidate_id": "EP011_0000000_54",
        "episode_number": 11,
        "start": 0.0,
        "end": 54.0,
    },
    {
        "candidate_id": "EP022_0006500_52",
        "episode_number": 22,
        "start": 6.5,
        "end": 58.5,
    },
]

df = pd.read_csv(candidate_file)
screenplay = pd.read_csv(screenplay_file)
editorial = pd.read_csv(editorial_file)

new_rows = []

for candidate in candidates:
    candidate_id = candidate["candidate_id"]
    ep = candidate["episode_number"]
    start = candidate["start"]
    end = candidate["end"]

    # Find original screenplay blocks overlapping the time window
    matching = screenplay[
        (screenplay["episode_number"] == ep)
        & (screenplay["start_seconds"] < end)
        & (screenplay["end_seconds"] > start)
    ]

    scenes = sorted(
        matching["scene_number"]
        .dropna()
        .unique()
        .astype(int)
        .tolist()
    )

    # Recover the original event timeline
    editorial_match = editorial[
        editorial["candidate_id"] == candidate_id
    ]

    if editorial_match.empty:
        raise ValueError(
            f"Missing editorial record for {candidate_id}"
        )

    event_timeline = editorial_match.iloc[0]["event_timeline"]

    if pd.isna(event_timeline):
        raise ValueError(
            f"Missing event timeline for {candidate_id}"
        )

    new_rows.append({
        "candidate_id": candidate_id,
        "episode_number": ep,
        "start_timestamp": (
            f"{int(start // 60):02d}:{start % 60:05.2f}"
        ),
        "end_timestamp": (
            f"{int(end // 60):02d}:{end % 60:05.2f}"
        ),
        "duration_seconds": end - start,
        "scene_numbers": ",".join(map(str, scenes)),
        "block_count": len(matching),
        "event_timeline": event_timeline,
    })

new_df = pd.DataFrame(new_rows)

# Check for existing IDs before adding records
existing_ids = set(df["candidate_id"])

duplicates = new_df[
    new_df["candidate_id"].isin(existing_ids)
]

if not duplicates.empty:
    raise ValueError(
        "Some custom candidates already exist. "
        "No changes made. IDs: "
        + ", ".join(duplicates["candidate_id"])
    )

# Append the three custom candidates
df = pd.concat([df, new_df], ignore_index=True)

# Save the repaired file
df.to_csv(candidate_file, index=False)

print("REPAIR COMPLETED SUCCESSFULLY")

print("\nAdded candidates:")
print(
    new_df[
        [
            "candidate_id",
            "scene_numbers",
            "block_count",
            "duration_seconds",
        ]
    ].to_string(index=False)
)

print("\nTotal candidate rows:", len(df))
print("Duplicate IDs:", df["candidate_id"].duplicated().sum())
print(
    "Missing scene numbers:",
    df["scene_numbers"].isna().sum()
)
print(
    "Missing block counts:",
    df["block_count"].isna().sum()
)


from pathlib import Path
import pandas as pd
import math

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "outputs" / "screenplay_blocks_v2.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"

df = pd.read_csv(INPUT_FILE)

# Initial candidate-generation configuration
WINDOW_DURATIONS = [20, 30, 40, 50, 60]
STEP_SECONDS = 5

def to_timestamp(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = seconds - minutes * 60
    return f"{minutes:02d}:{remaining_seconds:05.2f}"


# Create episode timelines from scene metadata
scenes = df[
    ["episode_number", "scene_number", "scene_start", "scene_end"]
].drop_duplicates()

def to_seconds(timestamp):
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)

scenes["start_seconds"] = scenes["scene_start"].apply(to_seconds)
scenes["end_seconds"] = scenes["scene_end"].apply(to_seconds)

candidates = []

for episode_number, episode_blocks in df.groupby("episode_number"):

    episode_scenes = scenes[
        scenes["episode_number"] == episode_number
    ]

    episode_start = episode_scenes["start_seconds"].min()
    episode_end = episode_scenes["end_seconds"].max()

    for duration in WINDOW_DURATIONS:

        start = episode_start

        while start + duration <= episode_end + 0.001:

            end = start + duration

            # Include every block that overlaps the candidate window.
            selected = episode_blocks[
                (episode_blocks["start_seconds"] < end) &
                (episode_blocks["end_seconds"] > start)
            ].copy()

            selected = selected.sort_values(
                ["start_seconds", "end_seconds"]
            )

            # Identify scenes touched by this candidate.
            selected_scenes = sorted(
                selected["scene_number"].dropna().unique().tolist()
            )

            # Prepare readable event descriptions.
            event_lines = []

            for _, block in selected.iterrows():

                if block["block_type"] == "DIALOGUE":
                    label = f"DIALOGUE - {block['speaker']}"
                else:
                    label = block["block_type"]

                event_lines.append(
                    f"[{block['start_timestamp']}-"
                    f"{block['end_timestamp']}] "
                    f"{label}: {block['content']}"
                )

            dialogue = "\n".join(
                selected.loc[
                    selected["block_type"] == "DIALOGUE",
                    "content"
                ].dropna().tolist()
            )

            actions = "\n".join(
                selected.loc[
                    selected["block_type"] == "ACTION",
                    "content"
                ].dropna().tolist()
            )

            camera = "\n".join(
                selected.loc[
                    selected["block_type"] == "CAMERA",
                    "content"
                ].dropna().tolist()
            )

            sound_fx = "\n".join(
                selected.loc[
                    selected["block_type"] == "SOUND_FX",
                    "content"
                ].dropna().tolist()
            )

            candidate_id = (
                f"EP{int(episode_number):03d}_"
                f"{int(start * 100):07d}_"
                f"{duration}"
            )

            candidates.append({
                "candidate_id": candidate_id,
                "episode_number": int(episode_number),
                "start_seconds": round(start, 2),
                "end_seconds": round(end, 2),
                "start_timestamp": to_timestamp(start),
                "end_timestamp": to_timestamp(end),
                "duration_seconds": duration,
                "scene_numbers": ",".join(
                    map(str, selected_scenes)
                ),
                "block_count": len(selected),
                "dialogue": dialogue,
                "actions": actions,
                "camera_directions": camera,
                "sound_effects": sound_fx,
                "event_timeline": "\n".join(event_lines)
            })

            start += STEP_SECONDS


# Convert candidate records into a DataFrame
candidate_df = pd.DataFrame(candidates)

# Save the complete candidate pool
output_file = OUTPUT_DIR / "promo_candidates.csv"

candidate_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

# Print summary
print("=" * 60)
print("PROMOTIONAL CANDIDATE GENERATION")
print("=" * 60)

print("Episodes processed:", df["episode_number"].nunique())
print("Total candidates generated:", len(candidate_df))

print("\nCandidates by duration:")
print(candidate_df["duration_seconds"].value_counts().sort_index())

print("\nCandidates per episode:")
print(candidate_df.groupby("episode_number").size().describe())

print("\nCandidate quality checks:")

print(
    "Invalid durations:",
    (
        (candidate_df["duration_seconds"] < 20) |
        (candidate_df["duration_seconds"] > 60)
    ).sum()
)

print(
    "Missing event content:",
    candidate_df["event_timeline"].isna().sum()
)

print("\nFirst 5 candidates:")

print(
    candidate_df[
        [
            "candidate_id",
            "episode_number",
            "start_timestamp",
            "end_timestamp",
            "duration_seconds",
            "block_count"
        ]
    ].head().to_string(index=False)
)

print("\nSaved to:", output_file)

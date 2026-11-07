
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "outputs" / "screenplay_blocks_v2.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"

df = pd.read_csv(INPUT_FILE)


def to_seconds(timestamp):
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)


# Convert timestamps into seconds
for column in [
    "scene_start",
    "scene_end",
    "start_timestamp",
    "end_timestamp"
]:
    df[column + "_seconds"] = df[column].apply(to_seconds)


# Assign a unique ID to every extracted block
df.insert(0, "block_id", range(1, len(df) + 1))


# Identify quality issues
df["negative_duration"] = (
    df["end_seconds"] < df["start_seconds"]
)

df["outside_scene_start"] = (
    df["start_seconds"] < df["scene_start_seconds"]
)

df["outside_scene_end"] = (
    df["end_seconds"] > df["scene_end_seconds"]
)

df["boundary_overlap"] = (
    df["outside_scene_start"] |
    df["outside_scene_end"]
)

# Save records that need manual review
flagged = df[df["boundary_overlap"] | df["negative_duration"]].copy()

flagged.to_csv(
    OUTPUT_DIR / "quality_flags.csv",
    index=False,
    encoding="utf-8-sig"
)

# Print report
print("=" * 55)
print("SCREENPLAY DATA QUALITY REPORT")
print("=" * 55)

print("Episodes:", df["episode_number"].nunique())
print("Scenes:", df[["episode_number", "scene_number"]].drop_duplicates().shape[0])
print("Total blocks:", len(df))

print("\nTimestamp checks:")
print("Negative durations:", df["negative_duration"].sum())
print("Blocks starting before scene:", df["outside_scene_start"].sum())
print("Blocks ending after scene:", df["outside_scene_end"].sum())
print("Total flagged blocks:", len(flagged))

print("\nFlagged records:")
if len(flagged) > 0:
    print(
        flagged[
            [
                "block_id",
                "episode_number",
                "scene_number",
                "block_type",
                "start_timestamp",
                "end_timestamp",
                "scene_start",
                "scene_end"
            ]
        ].to_string(index=False)
    )
else:
    print("No flagged records.")

print("\nQuality report saved:")
print(OUTPUT_DIR / "quality_flags.csv")

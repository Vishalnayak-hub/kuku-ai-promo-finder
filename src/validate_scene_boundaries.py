
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    PROJECT_DIR / "outputs" / "screenplay_blocks_v2.csv"
)

# Check whether every block falls within its scene.
df["scene_start_seconds"] = df["scene_start"].apply(
    lambda x: int(x.split(":")[0]) * 60 + float(x.split(":")[1])
)

df["scene_end_seconds"] = df["scene_end"].apply(
    lambda x: int(x.split(":")[0]) * 60 + float(x.split(":")[1])
)

df["within_scene"] = (
    (df["start_seconds"] >= df["scene_start_seconds"]) &
    (df["end_seconds"] <= df["scene_end_seconds"])
)

print("=" * 55)
print("SCENE BOUNDARY VALIDATION")
print("=" * 55)

print("Total blocks:", len(df))
print("Blocks within scene:", df["within_scene"].sum())
print("Blocks outside scene:", (~df["within_scene"]).sum())

print("\nExamples of blocks outside scene boundaries:")

print(
    df.loc[
        ~df["within_scene"],
        [
            "episode_number",
            "scene_number",
            "scene_start",
            "scene_end",
            "start_timestamp",
            "end_timestamp",
            "block_type",
            "content"
        ]
    ].head(15).to_string(index=False)
)

print("\nScene timestamp consistency:")

scenes = df[
    ["episode_number", "scene_number",
     "scene_start_seconds", "scene_end_seconds"]
].drop_duplicates()

print(
    "Scenes with invalid boundaries:",
    (scenes["scene_end_seconds"] < scenes["scene_start_seconds"]).sum()
)

print("\nBlocks per episode:")
print(df.groupby("episode_number").size().describe())

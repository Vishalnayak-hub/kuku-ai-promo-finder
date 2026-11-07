
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    PROJECT_DIR / "outputs" / "screenplay_blocks_v2.csv"
)

# Keep one row per scene
scenes = df[
    [
        "episode_number",
        "scene_number",
        "scene_start",
        "scene_end"
    ]
].drop_duplicates()

def to_seconds(timestamp):
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)

scenes["start_seconds"] = scenes["scene_start"].apply(to_seconds)
scenes["end_seconds"] = scenes["scene_end"].apply(to_seconds)

scenes = scenes.sort_values(
    ["episode_number", "start_seconds"]
)

print("=" * 60)
print("EPISODE TIMELINE ANALYSIS")
print("=" * 60)

episode_results = []

for episode, group in scenes.groupby("episode_number"):

    group = group.sort_values("start_seconds")

    episode_start = group["start_seconds"].min()
    episode_end = group["end_seconds"].max()

    gaps = []
    overlaps = []

    previous_end = None

    for _, scene in group.iterrows():

        if previous_end is not None:

            difference = scene["start_seconds"] - previous_end

            if difference > 0.01:
                gaps.append(difference)

            elif difference < -0.01:
                overlaps.append(abs(difference))

        previous_end = scene["end_seconds"]

    episode_results.append({
        "episode_number": episode,
        "scene_count": len(group),
        "episode_start": episode_start,
        "episode_end": episode_end,
        "duration_seconds": episode_end - episode_start,
        "gaps": len(gaps),
        "overlaps": len(overlaps)
    })

results = pd.DataFrame(episode_results)

print("\nEPISODE DURATION SUMMARY")
print(results["duration_seconds"].describe().round(2))

print("\nSCENE TIMELINE CHECKS")
print("Total episodes:", len(results))
print("Episodes with scene gaps:", (results["gaps"] > 0).sum())
print("Episodes with scene overlaps:", (results["overlaps"] > 0).sum())

print("\nEPISODES WITH GAPS OR OVERLAPS")

print(
    results.loc[
        (results["gaps"] > 0) | (results["overlaps"] > 0)
    ].to_string(index=False)
)

print("\nFIRST 10 EPISODE TIMELINES")

print(
    results.head(10).to_string(index=False)
)

results.to_csv(
    PROJECT_DIR / "outputs" / "episode_timeline_summary.csv",
    index=False
)

print("\nSaved episode_timeline_summary.csv")

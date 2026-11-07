
from pathlib import Path
import re
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

def timestamp_to_seconds(timestamp):
    """Convert MM:SS.ss into seconds."""
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)

files = sorted(DATA_DIR.glob("*.txt"))

results = []

for file in files:
    text = file.read_text(encoding="utf-8")

    # Extract episode number from screenplay content
    episode_match = re.search(
        r"EPISODE NUMBER:\s*Episode\s*(\d+)",
        text,
        re.IGNORECASE
    )

    episode_number = (
        int(episode_match.group(1)) if episode_match else None
    )

    # Find scene headings
    scenes = re.findall(
        r"(?m)^SCENE\s+\d+",
        text
    )

    # Extract scene start and end timestamps
    starts = re.findall(
        r"(?im)^SCENE START:\s*(\d{2}:\d{2}\.\d+)",
        text
    )

    ends = re.findall(
        r"(?im)^SCENE END:\s*(\d{2}:\d{2}\.\d+)",
        text
    )

    # Validate timestamp pairs
    valid_intervals = 0
    invalid_intervals = 0

    for start, end in zip(starts, ends):
        if timestamp_to_seconds(start) <= timestamp_to_seconds(end):
            valid_intervals += 1
        else:
            invalid_intervals += 1

    results.append({
        "filename": file.name,
        "episode_number": episode_number,
        "scene_count": len(scenes),
        "scene_start_count": len(starts),
        "scene_end_count": len(ends),
        "valid_intervals": valid_intervals,
        "invalid_intervals": invalid_intervals
    })

df = pd.DataFrame(results)

print("\nEPISODE STRUCTURE")
print(df.head(10).to_string(index=False))

print("\nSCENE COUNT DISTRIBUTION")
print(df["scene_count"].value_counts().sort_index())

print("\nTIMESTAMP VALIDATION")
print("Total scene starts:", df["scene_start_count"].sum())
print("Total scene ends:", df["scene_end_count"].sum())
print("Valid intervals:", df["valid_intervals"].sum())
print("Invalid intervals:", df["invalid_intervals"].sum())

print("\nEPISODES WITH MISSING OR MISMATCHED TIMESTAMPS")
problems = df[
    (df["scene_count"] != df["scene_start_count"]) |
    (df["scene_count"] != df["scene_end_count"]) |
    (df["invalid_intervals"] > 0)
]

print(problems.to_string(index=False))

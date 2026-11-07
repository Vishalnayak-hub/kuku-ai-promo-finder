
from pathlib import Path
import re
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

def timestamp_to_seconds(timestamp):
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)

files = sorted(DATA_DIR.glob("*.txt"))

results = []

# Match timestamp pairs such as:
# Start: (00:01.00) | End: (00:04.80)

pattern = re.compile(
    r"Start:\s*\((\d{2}:\d{2}\.\d+)\)"
    r"\s*\|\s*End:\s*\((\d{2}:\d{2}\.\d+)\)",
    re.IGNORECASE
)

all_durations = []

for file in files:
    text = file.read_text(encoding="utf-8")

    matches = pattern.findall(text)

    valid = 0
    invalid = 0
    durations = []

    for start, end in matches:
        start_sec = timestamp_to_seconds(start)
        end_sec = timestamp_to_seconds(end)

        duration = end_sec - start_sec

        if duration >= 0:
            valid += 1
            durations.append(duration)
            all_durations.append(duration)
        else:
            invalid += 1

    results.append({
        "episode": file.name,
        "timed_blocks": len(matches),
        "valid_blocks": valid,
        "invalid_blocks": invalid,
        "average_duration": (
            round(sum(durations) / len(durations), 2)
            if durations else 0
        )
    })

df = pd.DataFrame(results)

print("\nTIMESTAMPED BLOCK ANALYSIS")
print("=" * 55)

print("\nTotal timed blocks:", df["timed_blocks"].sum())
print("Valid blocks:", df["valid_blocks"].sum())
print("Invalid blocks:", df["invalid_blocks"].sum())

print("\nBLOCK COUNT STATISTICS")
print(df["timed_blocks"].describe().round(2))

print("\nDURATION STATISTICS (SECONDS)")

if all_durations:
    duration_series = pd.Series(all_durations)
    print(duration_series.describe().round(2))

print("\nFIRST 10 EPISODES")
print(df.head(10).to_string(index=False))

print("\nEPISODES WITH INVALID TIMESTAMPS")
print(df[df["invalid_blocks"] > 0].to_string(index=False))

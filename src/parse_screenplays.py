
from pathlib import Path
import re
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Match a complete timestamped block.
BLOCK_PATTERN = re.compile(
    r"(?ms)^\*\*(?P<header>[^*\n]+)\*\*\s*\n"
    r"Start:\s*\((?P<start>\d{2}:\d{2}\.\d+)\)"
    r"\s*\|\s*End:\s*\((?P<end>\d{2}:\d{2}\.\d+)\)"
    r"\s*\n(?P<content>.*?)"
    r"(?=^\*\*[^*\n]+\*\*\s*$|^SCENE\s+\d+|"
    r"^--- SCRIPT END ---|\Z)"
)

def classify_block(header):
    label = header.rstrip(":").split("(")[0].strip()

    if label.upper() == "CAMERA":
        return "CAMERA", None

    if label.upper() == "ACTION":
        return "ACTION", None

    if label.upper() == "SOUND FX":
        return "SOUND_FX", None

    return "DIALOGUE", label


def timestamp_to_seconds(timestamp):
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)


records = []

files = sorted(DATA_DIR.glob("*.txt"))

for file in files:
    text = file.read_text(encoding="utf-8")

    episode_match = re.search(
        r"EPISODE NUMBER:\s*Episode\s*(\d+)",
        text,
        re.IGNORECASE
    )

    episode_number = (
        int(episode_match.group(1)) if episode_match else None
    )

    for match in BLOCK_PATTERN.finditer(text):
        header = match.group("header").strip()
        start = match.group("start")
        end = match.group("end")
        content = match.group("content").strip()

        block_type, speaker = classify_block(header)

        records.append({
            "episode_number": episode_number,
            "filename": file.name,
            "start_timestamp": start,
            "end_timestamp": end,
            "start_seconds": timestamp_to_seconds(start),
            "end_seconds": timestamp_to_seconds(end),
            "duration_seconds": (
                timestamp_to_seconds(end) -
                timestamp_to_seconds(start)
            ),
            "block_type": block_type,
            "speaker": speaker,
            "original_header": header,
            "content": content
        })


df = pd.DataFrame(records)

output_file = OUTPUT_DIR / "screenplay_blocks.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("=" * 55)
print("SCREENPLAY PARSING RESULTS")
print("=" * 55)

print("Episodes processed:", len(files))
print("Blocks extracted:", len(df))
print("Output file:", output_file)

print("\nBLOCK TYPE DISTRIBUTION")
print(df["block_type"].value_counts())

print("\nMISSING CONTENT")
print("Empty content blocks:", (df["content"].str.len() == 0).sum())

print("\nFIRST 10 EXTRACTED RECORDS")
print(
    df[[
        "episode_number",
        "start_timestamp",
        "end_timestamp",
        "block_type",
        "speaker",
        "content"
    ]].head(10).to_string(index=False)
)

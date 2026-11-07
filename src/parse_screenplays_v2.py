
from pathlib import Path
import re
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

def to_seconds(timestamp):
    minutes, rest = timestamp.split(":")
    return int(minutes) * 60 + float(rest)


SCENE_PATTERN = re.compile(
    r"(?ims)^SCENE\s+(?P<scene_number>\d+)\s*\n"
    r"(?P<section>.*?)"
    r"(?=^SCENE\s+\d+\s*$|\Z)"
)

BLOCK_PATTERN = re.compile(
    r"(?ms)^\*\*(?P<header>[^*\n]+)\*\*\s*\n"
    r"Start:\s*\((?P<start>\d{2}:\d{2}\.\d+)\)"
    r"\s*\|\s*End:\s*\((?P<end>\d{2}:\d{2}\.\d+)\)"
    r"\s*\n(?P<content>.*?)"
    r"(?=^\*\*[^*\n]+\*\*\s*$|^SCENE\s+\d+|"
    r"^--- SCRIPT END ---|\Z)"
)

records = []

for file_path in sorted(RAW_DIR.glob("*.txt")):

    text = file_path.read_text(encoding="utf-8")

    episode_match = re.search(
        r"(?im)^EPISODE NUMBER:\s*Episode\s+(\d+)",
        text
    )

    logline_match = re.search(
        r"(?im)^EPISODE LOGLINE:\s*(.*)$",
        text
    )

    episode_number = (
        int(episode_match.group(1))
        if episode_match else None
    )

    logline = (
        logline_match.group(1).strip()
        if logline_match else None
    )

    for scene_match in SCENE_PATTERN.finditer(text):

        scene_number = int(scene_match.group("scene_number"))
        section = scene_match.group("section")

        heading_match = re.search(
            r"(?im)^Scene heading:\s*(.*)$",
            section
        )

        start_match = re.search(
            r"(?im)^Scene start:\s*(\d{2}:\d{2}\.\d+)",
            section
        )

        end_match = re.search(
            r"(?im)^Scene end:\s*(\d{2}:\d{2}\.\d+)",
            section
        )

        if not start_match or not end_match:
            print(
                f"Missing scene timestamp: "
                f"Episode {episode_number}, Scene {scene_number}"
            )
            continue

        scene_start = start_match.group(1)
        scene_end = end_match.group(1)

        for block_match in BLOCK_PATTERN.finditer(section):

            header = block_match.group("header").strip()
            start = block_match.group("start")
            end = block_match.group("end")
            content = block_match.group("content").strip()

            label = re.sub(
                r"\s*\([^)]*\)",
                "",
                header
            ).strip().rstrip(":").upper()

            if label == "CAMERA":
                block_type = "CAMERA"
                speaker = None

            elif label == "ACTION":
                block_type = "ACTION"
                speaker = None

            elif label in ["SOUND FX", "SOUND_FX"]:
                block_type = "SOUND_FX"
                speaker = None

            else:
                block_type = "DIALOGUE"
                speaker = label

            records.append({
                "episode_number": episode_number,
                "filename": file_path.name,
                "logline": logline,
                "scene_number": scene_number,
                "scene_heading": (
                    heading_match.group(1).strip()
                    if heading_match else None
                ),
                "scene_start": scene_start,
                "scene_end": scene_end,
                "start_timestamp": start,
                "end_timestamp": end,
                "start_seconds": to_seconds(start),
                "end_seconds": to_seconds(end),
                "duration_seconds": (
                    to_seconds(end) - to_seconds(start)
                ),
                "block_type": block_type,
                "speaker": speaker,
                "original_header": header,
                "content": content
            })


df = pd.DataFrame(records)

output_file = OUTPUT_DIR / "screenplay_blocks_v2.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("=" * 55)
print("SCENE-AWARE PARSING RESULTS")
print("=" * 55)

print("Episodes:", df["episode_number"].nunique())
print("Scenes:", df[["episode_number", "scene_number"]].drop_duplicates().shape[0])
print("Blocks:", len(df))

print("\nBlocks by type:")
print(df["block_type"].value_counts())

print("\nBlocks per scene:")
print(df.groupby(
    ["episode_number", "scene_number"]
).size().describe())

print("\nOutput saved to:", output_file)

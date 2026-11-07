
from pathlib import Path
import re

source_file = Path("data/raw/episode-028-Episode 1678581.txt")
text = source_file.read_text(encoding="utf-8", errors="replace")

# Match event headings such as CAMERA, ACTION, SOUND FX,
# and character-specific dialogue headings.
heading_pattern = re.compile(
    r"\*\*(.+?):\*\*\s*\n"
    r"Start:\s*\((\d{2}:\d{2}\.\d+)\)\s*\|\s*"
    r"End:\s*\((\d{2}:\d{2}\.\d+)\)\s*\n"
    r"(.*?)(?=\n\s*\*\*.+?:\*\*|\n\s*SCENE\s+\d+|\Z)",
    re.DOTALL
)

def to_seconds(timestamp):
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)

events = []

for match in heading_pattern.finditer(text):
    event_type = match.group(1).strip()
    start = to_seconds(match.group(2))
    end = to_seconds(match.group(3))
    content = match.group(4).strip()

    # Keep events overlapping 00:00–00:50.
    if start < 50 and end > 0:
        events.append({
            "start": start,
            "end": end,
            "type": event_type,
            "content": content
        })

events.sort(key=lambda event: (event["start"], event["end"]))

print("\nEPISODE 28 — ORIGINAL SCREENPLAY")
print("INSPECTING 00:00 TO 00:50")
print("=" * 65)

for event in events:
    print(
        f"\n[{event['start']:06.2f} - {event['end']:06.2f}] "
        f"{event['type']}"
    )
    print(event["content"])

print("\n" + "=" * 65)
print("TOTAL EVENTS DISPLAYED:", len(events))


from pathlib import Path
import re
from collections import Counter

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"

files = sorted(DATA_DIR.glob("*.txt"))

block_pattern = re.compile(
    r"(?m)^\*\*(.+?)\*\*\s*\n"
    r"Start:\s*\(\d{2}:\d{2}\.\d+\)\s*\|\s*"
    r"End:\s*\(\d{2}:\d{2}\.\d+\)"
)

block_types = Counter()
examples = {}

for file in files:
    text = file.read_text(encoding="utf-8")

    matches = block_pattern.findall(text)

    for header in matches:
        header = header.strip()

        # Normalize character labels:
        # MATRIARCH (Cold, Commanding): -> MATRIARCH
        label = header.rstrip(":").split("(")[0].strip()

        block_types[label] += 1

        if label not in examples:
            examples[label] = {
                "episode": file.name,
                "header": header
            }

print("\nTIMESTAMPED BLOCK TYPE DISTRIBUTION")
print("=" * 50)

for label, count in block_types.most_common():
    print(f"{label:<25} {count:>5}")

print("\nTOTAL CLASSIFIED BLOCKS:", sum(block_types.values()))

print("\nEXAMPLES OF EACH BLOCK TYPE")
print("=" * 50)

for label, example in examples.items():
    print(f"\nType: {label}")
    print("Header:", example["header"])
    print("Episode:", example["episode"])

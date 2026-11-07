
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

files = list(RAW_DIR.glob("*022*.txt"))

if not files:
    print("Episode 22 file not found.")
else:
    text = files[0].read_text(encoding="utf-8")
    lines = text.splitlines()

    for i, line in enumerate(lines):
        if (
            "SCENE 01" in line.upper()
            or "SCENE START" in line.upper()
            or "SCENE END" in line.upper()
            or "Heavy wooden latch" in line
        ):
            start = max(0, i - 4)
            end = min(len(lines), i + 5)

            print(f"\n--- Lines {start + 1} to {end} ---")

            for j in range(start, end):
                print(f"{j + 1}: {lines[j]}")

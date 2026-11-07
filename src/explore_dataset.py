
from pathlib import Path
import pandas as pd

# Project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Folder containing screenplay files
DATA_DIR = PROJECT_DIR / "data" / "raw"

# Find all screenplay files
files = sorted(DATA_DIR.glob("*.txt"))

print("=" * 50)
print("KUKU PROMO FINDER - DATASET EXPLORATION")
print("=" * 50)

print(f"\nTotal screenplay files: {len(files)}")

# Store basic information about each episode
episode_data = []

for file in files:
    text = file.read_text(encoding="utf-8")

    episode_data.append({
        "filename": file.name,
        "characters": len(text),
        "words": len(text.split()),
        "lines": len(text.splitlines()),
        "size_kb": round(file.stat().st_size / 1024, 2)
    })

# Convert to DataFrame
df = pd.DataFrame(episode_data)

print("\nDATASET SUMMARY")
print(df.describe().round(2))

print("\nFIRST FIVE EPISODES")
print(df.head().to_string(index=False))

print("\nTOTAL WORDS:", df["words"].sum())
print("TOTAL CHARACTERS:", df["characters"].sum())

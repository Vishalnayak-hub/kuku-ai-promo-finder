
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "outputs" / "screenplay_blocks.csv"

df = pd.read_csv(CSV_FILE)

print("=" * 55)
print("PARSED DATASET QUALITY CHECK")
print("=" * 55)

# 1. Episode coverage
print("\n1. EPISODE COVERAGE")
print("Unique episodes:", df["episode_number"].nunique())
print("Missing episode numbers:", df["episode_number"].isna().sum())
print("Rows per episode:")
print(df.groupby("episode_number").size().describe())

# 2. Duplicate records
print("\n2. DUPLICATE CHECK")
duplicate_count = df.duplicated(
    subset=[
        "episode_number",
        "start_timestamp",
        "end_timestamp",
        "original_header",
        "content"
    ]
).sum()

print("Exact duplicate records:", duplicate_count)

# 3. Timestamp validation
print("\n3. TIMESTAMP VALIDATION")
print("Missing start times:", df["start_seconds"].isna().sum())
print("Missing end times:", df["end_seconds"].isna().sum())

negative_durations = (df["duration_seconds"] < 0).sum()
print("Negative durations:", negative_durations)

print(
    "Duration calculation mismatches:",
    (
        (df["end_seconds"] - df["start_seconds"]
         - df["duration_seconds"]).abs() > 0.001
    ).sum()
)

# 4. Block type and speaker validation
print("\n4. BLOCK TYPE VALIDATION")
print(df["block_type"].value_counts())

print(
    "Dialogue rows without speaker:",
    (
        (df["block_type"] == "DIALOGUE") &
        df["speaker"].isna()
    ).sum()
)

print(
    "Non-dialogue rows with speaker:",
    (
        (df["block_type"] != "DIALOGUE") &
        df["speaker"].notna()
    ).sum()
)

# 5. Duration analysis
print("\n5. DURATION CHECK")
print(df["duration_seconds"].describe().round(2))

print("\nBlocks longer than 10 seconds:")
print(
    df.loc[
        df["duration_seconds"] > 10,
        ["episode_number", "block_type", "speaker",
         "start_timestamp", "end_timestamp", "duration_seconds"]
    ].to_string(index=False)
)

# Overall check
print("\n6. FINAL SUMMARY")
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print("Missing content:", df["content"].isna().sum())

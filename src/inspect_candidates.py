
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

FILE = PROJECT_DIR / "outputs" / "promo_candidates.csv"

df = pd.read_csv(FILE)

# Inspect five candidates from different parts of the dataset
sample = df.iloc[[0, 100, 500, 2000, 4000]]

for _, candidate in sample.iterrows():

    print("\n" + "=" * 75)

    print("CANDIDATE:", candidate["candidate_id"])
    print("EPISODE:", candidate["episode_number"])

    print(
        "TIMESTAMP:",
        candidate["start_timestamp"],
        "to",
        candidate["end_timestamp"]
    )

    print("DURATION:", candidate["duration_seconds"], "seconds")
    print("SCENES:", candidate["scene_numbers"])
    print("BLOCK COUNT:", candidate["block_count"])

    print("\n--- DIALOGUE ---")
    print(candidate["dialogue"])

    print("\n--- ACTIONS ---")
    print(candidate["actions"])

    print("\n--- CAMERA DIRECTIONS ---")
    print(candidate["camera_directions"])

    print("\n--- SOUND EFFECTS ---")
    print(candidate["sound_effects"])

    print("\n--- COMPLETE EVENT TIMELINE ---")
    print(candidate["event_timeline"])

print("\nInspection completed.")

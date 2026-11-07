
import pandas as pd

# Load refined candidates
df = pd.read_csv("outputs/promo_candidates_refined.csv")

# Fill missing values
df = df.fillna("")

# Basic statistics
print("=" * 55)
print("CANDIDATE QUALITY ANALYSIS")
print("=" * 55)

print("Total candidates:", len(df))
print("\nDuration distribution:")
print(df["duration_seconds"].value_counts().sort_index())

# Count event types in each timeline
df["has_dialogue"] = df["event_timeline"].str.contains("DIALOGUE:")
df["has_action"] = df["event_timeline"].str.contains("ACTION:")
df["has_camera"] = df["event_timeline"].str.contains("CAMERA:")
df["has_sound"] = df["event_timeline"].str.contains("SOUND_FX:")

print("\nCandidates containing each event type:")
print("Dialogue:", df["has_dialogue"].sum())
print("Action:", df["has_action"].sum())
print("Camera:", df["has_camera"].sum())
print("Sound effects:", df["has_sound"].sum())

# Count how many different event types each candidate contains
event_columns = [
    "has_dialogue",
    "has_action",
    "has_camera",
    "has_sound"
]

df["event_type_count"] = df[event_columns].sum(axis=1)

print("\nNumber of event types per candidate:")
print(df["event_type_count"].value_counts().sort_index())

# Save analysis
df.to_csv("outputs/candidate_quality_analysis.csv", index=False)

print("\nSaved: outputs/candidate_quality_analysis.csv")

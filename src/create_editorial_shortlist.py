
import pandas as pd

df = pd.read_csv("outputs/promo_candidates_refined.csv").fillna("")

# Episodes that showed promising dramatic material
selected_episodes = [1, 11, 28, 46]

# Select different durations instead of automatically favouring 60 seconds
selected_durations = [20, 30, 40, 50, 60]

review = df[
    (df["episode_number"].isin(selected_episodes)) &
    (df["duration_seconds"].isin(selected_durations))
].copy()

# Select a small number of examples per episode and duration.
# This is for editorial inspection, not a quality ranking.
review = (
    review.sort_values(["episode_number", "duration_seconds", "start_timestamp"])
    .groupby(["episode_number", "duration_seconds"], group_keys=False)
    .head(3)
)

columns = [
    "candidate_id",
    "episode_number",
    "start_timestamp",
    "end_timestamp",
    "duration_seconds",
    "event_timeline"
]

review[columns].to_csv(
    "outputs/editorial_review.csv",
    index=False
)

print("=" * 55)
print("EDITORIAL REVIEW DATASET")
print("=" * 55)
print("Selected episodes:", selected_episodes)
print("Durations:", selected_durations)
print("Total candidates for review:", len(review))
print("\nCandidates per episode and duration:")
print(review.groupby(["episode_number", "duration_seconds"]).size())
print("\nSaved: outputs/editorial_review.csv")

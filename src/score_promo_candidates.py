
import pandas as pd
from pathlib import Path

INPUT = Path("outputs/nlp_candidate_features.csv")
OUTPUT = Path("outputs/automated_scored_candidates.csv")
TOP_OUTPUT = Path("outputs/automated_top_50.csv")

df = pd.read_csv(INPUT)

def capped_score(value, threshold, weight):
    """Convert a signal count into a capped weighted score."""
    return (value.clip(lower=0) / threshold).clip(upper=1) * weight

# 1. Opening hook: maximum 20
df["hook_score"] = (
    capped_score(df["hook_signal_count"], 3, 12)
    + df["opening_question"] * 8
)

# 2. Ending / cliffhanger: maximum 25
df["cliffhanger_score"] = (
    capped_score(df["cliffhanger_signal_count"], 3, 15)
    + df["ending_question"] * 5
    + df["ending_exclamation"] * 5
)

# 3. Conflict: maximum 15
df["conflict_score"] = capped_score(
    df["conflict_signal_count"], 4, 15
)

# 4. Emotional signals: maximum 15
df["emotion_score"] = capped_score(
    df["emotion_signal_count"], 4, 15
)

# 5. Dialogue density: maximum 10
df["dialogue_score"] = capped_score(
    df["dialogue_density"], 1.5, 10
)

# 6. Action presence: maximum 5
df["action_score"] = df["has_action"] * 5

# 7. Event richness: maximum 10
df["event_richness_score"] = (
    df["event_count"].clip(upper=20) / 20 * 10
)

score_columns = [
    "hook_score",
    "cliffhanger_score",
    "conflict_score",
    "emotion_score",
    "dialogue_score",
    "action_score",
    "event_richness_score"
]

df["automated_score"] = df[score_columns].sum(axis=1).round(2)

# Rank candidates
df = df.sort_values(
    ["automated_score", "cliffhanger_score", "hook_score"],
    ascending=False
).reset_index(drop=True)

df.insert(0, "automated_rank", range(1, len(df) + 1))

df.to_csv(OUTPUT, index=False)
df.head(50).to_csv(TOP_OUTPUT, index=False)

print("=" * 55)
print("AUTOMATED PROMO SCORING COMPLETE")
print("=" * 55)

print("Candidates scored:", len(df))
print("Average score:", round(df["automated_score"].mean(), 2))
print("Highest score:", df["automated_score"].max())

print("\nTOP 20 CANDIDATES:")
print(
    df[
        [
            "automated_rank",
            "candidate_id",
            "automated_score",
            "hook_score",
            "cliffhanger_score",
            "conflict_score",
            "emotion_score"
        ]
    ].head(20).to_string(index=False)
)

print("\nOUTPUT FILES:")
print(OUTPUT)
print(TOP_OUTPUT)

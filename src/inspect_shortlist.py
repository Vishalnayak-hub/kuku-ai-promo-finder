
import pandas as pd

df = pd.read_csv("outputs/promo_shortlist.csv").fillna("")

print("=" * 60)
print("SHORTLIST INSPECTION")
print("=" * 60)

# Inspect candidates from different episodes
episodes = [1, 11, 20, 28, 46]

for episode in episodes:
    sample = df[df["episode_number"] == episode].head(2)

    print(f"\n{'=' * 60}")
    print(f"EPISODE {episode}")
    print("=" * 60)

    for _, row in sample.iterrows():
        print("\nCandidate:", row["candidate_id"])
        print("Duration:", row["duration_seconds"])
        print("Opening:", row["opening_text"])
        print("Ending:", row["ending_text"])
        print("\nEvent timeline:")
        print(row["event_timeline"])
        print("-" * 50)

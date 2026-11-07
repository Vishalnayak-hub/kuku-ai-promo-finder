
import pandas as pd
import re

df = pd.read_csv("outputs/promo_candidates_refined.csv")
df = df.fillna("")


def timestamp_to_seconds(timestamp):
    """Convert MM:SS.ss timestamp into seconds."""
    minutes, seconds = timestamp.split(":")
    return int(minutes) * 60 + float(seconds)


def extract_dialogue(timeline):
    """Extract dialogue events and their timestamps."""
    pattern = r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\] DIALOGUE: (.*)"

    matches = re.findall(pattern, timeline)

    return [
        {
            "start": float(start),
            "end": float(end),
            "text": text.strip()
        }
        for start, end, text in matches
    ]


def calculate_signals(row):
    dialogue = extract_dialogue(row["event_timeline"])

    if not dialogue:
        return pd.Series({
            "dialogue_count": 0,
            "opening_dialogue": False,
            "ending_dialogue": False,
            "opening_text": "",
            "ending_text": ""
        })

    clip_start = timestamp_to_seconds(row["start_timestamp"])
    clip_end = timestamp_to_seconds(row["end_timestamp"])

    first = min(dialogue, key=lambda x: x["start"])
    last = max(dialogue, key=lambda x: x["end"])

    opening = any(
        d["start"] < clip_start + 5
        for d in dialogue
    )

    ending = any(
        d["end"] > clip_end - 5
        for d in dialogue
    )

    return pd.Series({
        "dialogue_count": len(dialogue),
        "opening_dialogue": opening,
        "ending_dialogue": ending,
        "opening_text": first["text"],
        "ending_text": last["text"]
    })


signals = df.apply(calculate_signals, axis=1)
df = pd.concat([df, signals], axis=1)

shortlist = df[
    (df["dialogue_count"] >= 2) &
    (df["opening_dialogue"]) &
    (df["ending_dialogue"])
].copy()

shortlist = shortlist.sort_values(
    by=["dialogue_count"],
    ascending=False
)

shortlist.to_csv("outputs/promo_shortlist.csv", index=False)

print("=" * 55)
print("PROMO SHORTLIST")
print("=" * 55)

print("Total candidates:", len(df))
print("Shortlisted candidates:", len(shortlist))

columns = [
    "candidate_id",
    "episode_number",
    "start_timestamp",
    "end_timestamp",
    "duration_seconds",
    "dialogue_count",
    "opening_text",
    "ending_text"
]

print("\nFirst 10 shortlisted candidates:")
print(shortlist[columns].head(10).to_string(index=False))

print("\nSaved: outputs/promo_shortlist.csv")

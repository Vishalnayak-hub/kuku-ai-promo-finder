
import pandas as pd
import re
from pathlib import Path

INPUT = Path("outputs/promo_candidates_refined.csv")
REVIEW_INPUT = Path("outputs/editorial_review_sheet.csv")
OUTPUT = Path("outputs/nlp_candidate_features.csv")

# Load original candidate dataset
df = pd.read_csv(INPUT)

# Load manually reviewed candidates
review = pd.read_csv(REVIEW_INPUT)

# Keep only candidates that are missing from the original dataset
missing = review[
    ~review["candidate_id"].isin(df["candidate_id"])
].copy()

# Add only the columns required for feature extraction
required_columns = [
    "candidate_id",
    "episode_number",
    "start_timestamp",
    "end_timestamp",
    "duration_seconds",
    "event_timeline"
]

missing = missing[required_columns]

# Combine original and custom candidates
df = pd.concat(
    [df, missing],
    ignore_index=True
)

# Remove any duplicate candidate IDs
df = df.drop_duplicates(
    subset=["candidate_id"],
    keep="first"
).reset_index(drop=True)


# NLP keyword dictionaries
HOOK_WORDS = [
    "why", "what", "stop", "wait", "help", "secret",
    "never", "truth", "betray", "suddenly", "who"
]

EMOTION_WORDS = [
    "love", "hate", "fear", "cry", "tears", "angry",
    "shocked", "heart", "pain", "death", "terrified",
    "betrayal", "desperate", "scream"
]

CONFLICT_WORDS = [
    "accuse", "threat", "kill", "lie", "steal", "poison",
    "guilty", "innocent", "revenge", "arrest", "danger",
    "fight", "enemy", "betray", "murder"
]

CLIFFHANGER_WORDS = [
    "but", "however", "unless", "secret", "truth",
    "wait", "stop", "who", "why", "what happened",
    "before", "never", "impossible"
]


def count_terms(text, words):
    text = str(text).lower()

    return sum(
        len(re.findall(r"\b" + re.escape(word) + r"\b", text))
        for word in words
    )


def extract_events(timeline):
    events = []

    pattern = (
        r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]\s+"
        r"(CAMERA|ACTION|DIALOGUE|SOUND_FX):\s*(.*)"
    )

    for line in str(timeline).splitlines():
        match = re.search(pattern, line)

        if match:
            events.append({
                "start": float(match.group(1)),
                "end": float(match.group(2)),
                "type": match.group(3),
                "text": match.group(4).strip()
            })

    return events


def analyze_candidate(row):
    events = extract_events(row["event_timeline"])

    dialogue = [
        e for e in events if e["type"] == "DIALOGUE"
    ]

    actions = [
        e for e in events if e["type"] == "ACTION"
    ]

    all_text = " ".join(e["text"] for e in events)
    dialogue_text = " ".join(e["text"] for e in dialogue)

    duration = max(float(row["duration_seconds"]), 1)

    words = dialogue_text.split()

    clip_start = min(
        (e["start"] for e in events),
        default=0
    )

    clip_end = max(
        (e["end"] for e in events),
        default=clip_start
    )

    opening_events = [
        e for e in events
        if e["start"] <= clip_start + 5
    ]

    ending_events = [
        e for e in events
        if e["end"] >= clip_end - 10
    ]

    opening_text = " ".join(
        e["text"] for e in opening_events
    )

    ending_text = " ".join(
        e["text"] for e in ending_events
    )

    return pd.Series({
        "event_count": len(events),
        "dialogue_count": len(dialogue),
        "action_count": len(actions),
        "dialogue_word_count": len(words),
        "dialogue_density": round(len(words) / duration, 3),

        "question_count": dialogue_text.count("?"),
        "exclamation_count": dialogue_text.count("!"),

        "hook_signal_count": count_terms(
            opening_text, HOOK_WORDS
        ),

        "emotion_signal_count": count_terms(
            all_text, EMOTION_WORDS
        ),

        "conflict_signal_count": count_terms(
            all_text, CONFLICT_WORDS
        ),

        "cliffhanger_signal_count": count_terms(
            ending_text, CLIFFHANGER_WORDS
        ),

        "opening_question": int("?" in opening_text),
        "ending_question": int("?" in ending_text),
        "ending_exclamation": int("!" in ending_text),

        "has_dialogue": int(len(dialogue) > 0),
        "has_action": int(len(actions) > 0),
    })


# Extract features
features = df.apply(analyze_candidate, axis=1)

result = pd.concat(
    [df.drop(columns=["event_timeline"]), features],
    axis=1
)

# Save combined feature dataset
result.to_csv(OUTPUT, index=False)

print("=" * 55)
print("NLP FEATURE EXTRACTION COMPLETE")
print("=" * 55)

print("Original candidates:", len(pd.read_csv(INPUT)))
print("Custom candidates added:", len(missing))
print("Total candidates processed:", len(result))
print("Features extracted:", len(features.columns))
print("Duplicate IDs:", result["candidate_id"].duplicated().sum())
print("Missing values:", result.isnull().sum().sum())
print("Output:", OUTPUT)

print("\nADDED CANDIDATES:")
print(missing["candidate_id"].to_list())

print("\nFEATURE PREVIEW:")
print(result.head(5).to_string(index=False))

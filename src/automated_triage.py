import pandas as pd
import re
from pathlib import Path

src = Path("outputs/pending_editorial_reviews.csv")
out = Path("outputs/automated_triage_pending.csv")

df = pd.read_csv(src).fillna("")
suspense_words = [
    "secret", "murder", "poison", "betray", "dead", "death",
    "kill", "truth", "revenge", "arrest", "guilty", "innocent",
    "marry", "threat", "weapon", "blood", "escape", "never",
    "surprise", "disappear", "unless", "but", "why"
]

def score(row):
    text = str(row["event_timeline"])
    duration = float(row["duration_seconds"])
    lines = text.splitlines()

    dialogue = sum("DIALOGUE:" in x for x in lines)
    action = sum("ACTION:" in x for x in lines)
    camera = sum("CAMERA:" in x for x in lines)
    suspense = sum(text.lower().count(w) for w in suspense_words)

    opening = sum(
        1 for x in lines
        if (m := re.search(r"\[(\d+(?:\.\d+)?)-", x))
        and float(m.group(1)) <= 5
    )
    ending = sum(
        1 for x in lines
        if (m := re.search(r"-(\d+(?:\.\d+)?)\]", x))
        and float(m.group(1)) >= duration - 5
    )

    parts = {
        "opening_signal": min(opening / 3, 1) * 20,
        "dialogue_signal": min(dialogue / 5, 1) * 20,
        "action_signal": min(action / 3, 1) * 15,
        "suspense_word_signal": min(suspense / 5, 1) * 25,
        "ending_signal": min(ending / 3, 1) * 20
    }
    return pd.Series({
        **parts,
        "automated_triage_score": round(sum(parts.values()), 2),
        "dialogue_events": dialogue,
        "action_events": action,
        "camera_events": camera,
        "suspense_word_matches": suspense
    })

features = df.apply(score, axis=1)
result = pd.concat([df, features], axis=1)
result = result.sort_values(
    "automated_triage_score", ascending=False
).reset_index(drop=True)
result.insert(0, "triage_rank", range(1, len(result) + 1))
result.to_csv(out, index=False)

print("AUTOMATED TRIAGE COMPLETE")
print("Candidates ranked:", len(result))
print("\nTOP 10 FOR HUMAN REVIEW:")
print(result[[
    "triage_rank", "candidate_id", "episode_number",
    "start_timestamp", "end_timestamp",
    "automated_triage_score"
]].head(10).to_string(index=False))
print("\nSaved:", out)
print("NOTE: Heuristic screenplay triage only; not human editorial approval.")

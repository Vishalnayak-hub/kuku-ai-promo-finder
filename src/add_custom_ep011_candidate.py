
import pandas as pd
import re
from pathlib import Path

file_path = Path("outputs/editorial_review_sheet.csv")

df = pd.read_csv(file_path)

candidate_id = "EP011_0000000_54"

# Avoid duplicate candidates
if (df["candidate_id"] == candidate_id).any():
    print("Custom 54-second candidate already exists.")

else:
    # Use the existing 60-second candidate as a template
    original = df[
        df["candidate_id"] == "EP011_0000000_60"
    ]

    if original.empty:
        raise ValueError(
            "Original EP011 60-second candidate not found."
        )

    new_row = original.iloc[0].copy()

    # Update candidate metadata
    new_row["candidate_id"] = candidate_id
    new_row["episode_number"] = 11
    new_row["start_timestamp"] = "00:00.00"
    new_row["end_timestamp"] = "00:54.00"
    new_row["duration_seconds"] = 54

    # Clip timeline events at 54 seconds
    timeline = str(new_row["event_timeline"])
    filtered_events = []

    for event in timeline.split("\n"):
        match = re.search(
            r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]",
            event
        )

        if not match:
            continue

        event_start = float(match.group(1))
        event_end = float(match.group(2))

        if event_start >= 54:
            continue

        clipped_end = min(event_end, 54.0)

        updated_event = re.sub(
            r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]",
            f"[{event_start:.2f}-{clipped_end:.2f}]",
            event,
            count=1
        )

        filtered_events.append(updated_event)

    new_row["event_timeline"] = "\n".join(filtered_events)

    # Reset evaluation fields
    rating_columns = [
        "hook_rating",
        "context_rating",
        "emotional_impact_rating",
        "escalation_rating",
        "ending_rating",
        "editorial_score"
    ]

    text_columns = [
        "hook_description",
        "cliffhanger_description",
        "editorial_rationale"
    ]

    for column in rating_columns + text_columns:
        new_row[column] = pd.NA

    new_row["review_status"] = "Pending human review"

    # Append candidate
    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    df.to_csv(file_path, index=False)

    print("Custom candidate added successfully.")

# Display Episode 11 candidates
print("\nEP011 candidates:")

print(
    df[df["candidate_id"].str.startswith("EP011")][
        [
            "candidate_id",
            "start_timestamp",
            "end_timestamp",
            "duration_seconds"
        ]
    ].to_string(index=False)
)


import pandas as pd
from pathlib import Path

file_path = Path("outputs/editorial_review_sheet.csv")

df = pd.read_csv(file_path)

candidate_id = "EP028_0000000_48"

# Avoid creating duplicate candidates
if (df["candidate_id"] == candidate_id).any():
    print("Custom 48-second candidate already exists.")
else:
    # Get the existing 50-second candidate as a template
    original = df[
        df["candidate_id"] == "EP028_0000000_50"
    ]

    if original.empty:
        raise ValueError("Original EP028 50-second candidate not found.")

    new_row = original.iloc[0].copy()

    # Update candidate metadata
    new_row["candidate_id"] = candidate_id
    new_row["episode_number"] = 28
    new_row["start_timestamp"] = "00:00.00"
    new_row["end_timestamp"] = "00:48.00"
    new_row["duration_seconds"] = 48

    # Remove events extending beyond 48 seconds
    timeline = str(new_row["event_timeline"])

    filtered_events = []

    for event in timeline.split("\n"):
        if not event.strip():
            continue

        # Extract event start time from [start-end]
        import re
        match = re.search(r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]", event)

        if match:
            event_start = float(match.group(1))

            if event_start < 48:
                filtered_events.append(event)

    new_row["event_timeline"] = "\n".join(filtered_events)

    # Reset all evaluation fields
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

    # Add the custom candidate
    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    df.to_csv(file_path, index=False)

    print("Custom candidate added successfully.")

print("\nEP028 candidates:")
print(
    df[df["candidate_id"].str.startswith("EP028")][
        ["candidate_id", "start_timestamp", "end_timestamp", "duration_seconds"]
    ].to_string(index=False)
)


import pandas as pd
import re
from pathlib import Path

source_path = Path("outputs/promo_candidates_refined.csv")
review_path = Path("outputs/editorial_review_sheet.csv")

# Read both datasets
source_df = pd.read_csv(source_path)
review_df = pd.read_csv(review_path)

candidate_id = "EP022_0006500_52"

start_time = 6.5
end_time = 58.5
duration = end_time - start_time

# Check for duplicates
if (review_df["candidate_id"] == candidate_id).any():
    print("Candidate already exists in editorial review sheet.")

else:
    # Find a suitable template from the original dataset
    original = source_df[
        source_df["candidate_id"] == "EP022_0000000_60"
    ]

    if original.empty:
        raise ValueError("Episode 22 source template not found.")

    new_row = original.iloc[0].copy()

    # Update candidate metadata
    new_row["candidate_id"] = candidate_id
    new_row["start_timestamp"] = "00:06.50"
    new_row["end_timestamp"] = "00:58.50"
    new_row["duration_seconds"] = duration

    # Clip events to the selected time window
    filtered_events = []

    for event in str(new_row["event_timeline"]).split("\n"):
        if not event.strip():
            continue

        match = re.search(
            r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]",
            event
        )

        if not match:
            continue

        event_start = float(match.group(1))
        event_end = float(match.group(2))

        clipped_start = max(event_start, start_time)
        clipped_end = min(event_end, end_time)

        if clipped_start < clipped_end:
            clipped_event = re.sub(
                r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]",
                f"[{clipped_start:.2f}-{clipped_end:.2f}]",
                event,
                count=1
            )

            filtered_events.append(clipped_event)

    new_row["event_timeline"] = "\n".join(filtered_events)

    # Add evaluation fields required by the review sheet
    evaluation_fields = {
        "hook_rating": pd.NA,
        "context_rating": pd.NA,
        "emotional_impact_rating": pd.NA,
        "escalation_rating": pd.NA,
        "ending_rating": pd.NA,
        "editorial_score": pd.NA,
        "hook_description": pd.NA,
        "cliffhanger_description": pd.NA,
        "editorial_rationale": pd.NA,
        "review_status": "Pending human review"
    }

    for column, value in evaluation_fields.items():
        new_row[column] = value

    # Match the review sheet's column structure
    new_row = new_row.reindex(review_df.columns)

    # Append and save
    review_df = pd.concat(
        [review_df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    review_df.to_csv(review_path, index=False)

    print("Custom Episode 22 candidate added successfully.")

# Verify
check_df = pd.read_csv(review_path)

print("\nNew candidate:")
print(
    check_df[
        check_df["candidate_id"] == candidate_id
    ][
        [
            "candidate_id",
            "start_timestamp",
            "end_timestamp",
            "duration_seconds",
            "review_status"
        ]
    ].to_string(index=False)
)

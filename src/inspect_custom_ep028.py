import pandas as pd
import re

file_path = "outputs/editorial_review_sheet.csv"

df = pd.read_csv(file_path)

candidate_id = "EP028_0000000_48"

mask = df["candidate_id"] == candidate_id

if not mask.any():
    print("Candidate not found!")
else:
    timeline = df.loc[mask, "event_timeline"].iloc[0]

    filtered_events = []

    for event in timeline.split("\n"):
        match = re.search(
            r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]",
            event
        )

        if not match:
            continue

        start = float(match.group(1))
        end = float(match.group(2))

        if start >= 48:
            continue

        clipped_end = min(end, 48.0)

        updated_event = re.sub(
            r"\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]",
            f"[{start:.2f}-{clipped_end:.2f}]",
            event,
            count=1
        )

        filtered_events.append(updated_event)

    df.loc[mask, "event_timeline"] = "\n".join(filtered_events)

    df.to_csv(file_path, index=False)

    print("Timeline corrected successfully.")
    print("\nFinal events:")
    print(df.loc[mask, "event_timeline"].iloc[0])
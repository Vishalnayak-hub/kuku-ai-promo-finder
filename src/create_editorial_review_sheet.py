
import pandas as pd
from pathlib import Path

# Load the 60 candidates selected for editorial inspection
input_file = Path("outputs/editorial_review.csv")

if not input_file.exists():
    raise FileNotFoundError(
        "editorial_review.csv not found inside outputs/"
    )

df = pd.read_csv(input_file)

# Add human evaluation columns
rating_columns = [
    "hook_rating",
    "context_rating",
    "emotional_impact_rating",
    "escalation_rating",
    "ending_rating"
]

for column in rating_columns:
    df[column] = pd.NA

df["editorial_score"] = pd.NA
df["hook_description"] = ""
df["cliffhanger_description"] = ""
df["editorial_rationale"] = ""
df["review_status"] = "Pending human review"

# Save the review template
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "editorial_review_sheet.csv"
df.to_csv(output_file, index=False)

print("Editorial review sheet created!")
print("Total candidates:", len(df))
print("Episodes:", sorted(df["episode_number"].unique()))
print("Output:", output_file)

print("\nColumns available for evaluation:")
print(df.columns.tolist())


import pandas as pd
from pathlib import Path

file_path = Path("outputs/editorial_review_sheet.csv")

# Load review sheet
df = pd.read_csv(file_path)

# Ask which candidate to evaluate
candidate_id = input("Enter candidate ID: ").strip()

mask = df["candidate_id"].astype(str) == candidate_id

if not mask.any():
    raise ValueError(f"Candidate not found: {candidate_id}")

# Five editorial criteria
rating_columns = [
    "hook_rating",
    "context_rating",
    "emotional_impact_rating",
    "escalation_rating",
    "ending_rating"
]

# Get ratings from user
ratings = {}

for column in rating_columns:
    while True:
        try:
            rating = int(input(f"Enter {column} (1-5): "))

            if 1 <= rating <= 5:
                ratings[column] = rating
                break

            print("Rating must be between 1 and 5.")

        except ValueError:
            print("Please enter a valid integer.")

# Get editorial observations
print("\nEnter editorial observations:")

hook_description = input("Hook description: ")
cliffhanger_description = input("Cliffhanger description: ")
editorial_rationale = input("Editorial rationale: ")

# Ensure correct data types
for column in rating_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

text_columns = [
    "hook_description",
    "cliffhanger_description",
    "editorial_rationale",
    "review_status"
]

for column in text_columns:
    df[column] = df[column].astype("string")

# Record evaluation
for column, rating in ratings.items():
    df.loc[mask, column] = rating

df.loc[mask, "hook_description"] = hook_description
df.loc[mask, "cliffhanger_description"] = cliffhanger_description
df.loc[mask, "editorial_rationale"] = editorial_rationale
df.loc[mask, "review_status"] = "Reviewed - screenplay inspection"

# Calculate weighted editorial score
weights = {
    "hook_rating": 25,
    "context_rating": 20,
    "emotional_impact_rating": 20,
    "escalation_rating": 15,
    "ending_rating": 20
}

score = sum(
    (ratings[column] / 5) * weight
    for column, weight in weights.items()
)

df.loc[mask, "editorial_score"] = score

# Save results
df.to_csv(file_path, index=False)

print("\nEditorial evaluation recorded successfully.")
print(f"Candidate: {candidate_id}")
print(f"Weighted editorial score: {score}/100")

print(
    df.loc[
        mask,
        ["candidate_id", *rating_columns,
         "editorial_score", "review_status"]
    ].to_string(index=False)
)

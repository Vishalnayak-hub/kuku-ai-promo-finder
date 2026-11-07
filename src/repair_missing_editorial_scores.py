
import pandas as pd

file_path = "outputs/editorial_review_sheet.csv"

df = pd.read_csv(file_path)

weights = {
    "hook_rating": 25,
    "context_rating": 20,
    "emotional_impact_rating": 20,
    "escalation_rating": 15,
    "ending_rating": 20
}

# Find reviewed candidates with missing scores
reviewed = df[
    df["review_status"] == "Reviewed - screenplay inspection"
]

repaired_count = 0

for index, row in reviewed.iterrows():

    if pd.isna(row["editorial_score"]):

        score = 0

        for column, weight in weights.items():
            rating = pd.to_numeric(row[column], errors="coerce")

            if pd.isna(rating):
                raise ValueError(
                    f"Missing rating in {row['candidate_id']}: {column}"
                )

            score += (rating / 5) * weight

        df.at[index, "editorial_score"] = round(score, 2)
        repaired_count += 1

# Save the corrected source file
df.to_csv(file_path, index=False)

print("SCORE REPAIR COMPLETE")
print("Missing scores repaired:", repaired_count)

print("\nReviewed candidates:")
print(
    df[
        df["review_status"] == "Reviewed - screenplay inspection"
    ][["candidate_id", "editorial_score"]].to_string(index=False)
)

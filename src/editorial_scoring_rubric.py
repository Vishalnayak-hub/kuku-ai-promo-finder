
import pandas as pd
from pathlib import Path

# Define editorial evaluation criteria
rubric = [
    {
        "criterion": "Opening Hook",
        "weight": 25,
        "description": "Ability to capture attention within the first 3 seconds.",
        "rating_0": "No engaging opening",
        "rating_3": "Moderately engaging opening",
        "rating_5": "Immediately compelling opening"
    },
    {
        "criterion": "Context Clarity",
        "weight": 20,
        "description": "How easily a new viewer understands the situation.",
        "rating_0": "Completely confusing",
        "rating_3": "Partially understandable",
        "rating_5": "Clear standalone context"
    },
    {
        "criterion": "Emotional Impact",
        "weight": 20,
        "description": "Strength of emotional engagement.",
        "rating_0": "No emotional engagement",
        "rating_3": "Moderate emotional engagement",
        "rating_5": "Strong emotional impact"
    },
    {
        "criterion": "Escalation",
        "weight": 15,
        "description": "How effectively tension or conflict builds.",
        "rating_0": "No progression",
        "rating_3": "Some progression",
        "rating_5": "Strong and continuous escalation"
    },
    {
        "criterion": "Ending Strength",
        "weight": 20,
        "description": "Ability to leave the viewer wanting to know what happens next.",
        "rating_0": "Weak or complete ending",
        "rating_3": "Some unresolved tension",
        "rating_5": "Powerful unresolved cliffhanger"
    }
]

df = pd.DataFrame(rubric)

# Validate total weight
assert df["weight"].sum() == 100

# Save output
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

df.to_csv(
    output_dir / "editorial_scoring_rubric.csv",
    index=False
)

print("Editorial scoring rubric created successfully!")
print(df[["criterion", "weight"]])
print("Total weight:", df["weight"].sum())

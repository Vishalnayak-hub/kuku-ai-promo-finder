import pandas as pd
from pathlib import Path

p = Path("outputs/editorial_review_sheet.csv")
df = pd.read_csv(p)

cid = "EP011_0000000_60"
mask = df["candidate_id"].astype(str) == cid

if not mask.any():
    raise ValueError(f"{cid} not found in editorial_review_sheet.csv")

updates = {
    "hook_rating": 5,
    "context_rating": 5,
    "emotional_impact_rating": 5,
    "escalation_rating": 5,
    "ending_rating": 4,
    "editorial_score": 96,
    "hook_description": "Gerald unexpectedly arrives at Juliana and Alexander's cottage.",
       "cliffhanger_description": "Juliana urgently intervenes as the constable searches her mother's medicines.",
    "editorial_rationale": "Clear confrontation and theft accusation establish the conflict. The constable's search escalates the stakes, ending on the threat to Juliana's mother's medicines. Strong screenplay-based promo with an unresolved ending.",
    "review_status": "Reviewed - screenplay inspection"
}

for col, value in updates.items():
    if col in df.columns:
        df.loc[mask, col] = value
    else:
        raise ValueError(f"Missing expected column: {col}")

df.to_csv(p, index=False)
print("EPISODE 11 (00:00-01:00) REVIEW RECORDED")
print("Editorial score: 96/100")
print("Reviewed candidates:", (df["review_status"].astype(str).str.startswith("Reviewed")).sum())

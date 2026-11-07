import pandas as pd

d = pd.read_csv("outputs/automated_triage_pending.csv")
top = d.sort_values("automated_triage_score", ascending=False).head(10)

for _, r in top.iterrows():
    print("\n" + "="*85)
    print(f"RANK {r['triage_rank']} | {r['candidate_id']} | "
          f"EPISODE {r['episode_number']} | "
          f"{r['start_timestamp']} - {r['end_timestamp']} | "
          f"SCORE {r['automated_triage_score']}")
    lines = str(r["event_timeline"]).splitlines()
    for line in lines:
        if any(x in line for x in ["DIALOGUE:", "ACTION:"]):
            print(line)

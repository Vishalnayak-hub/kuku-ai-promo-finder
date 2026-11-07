
# Kuku AI — Promotional Clip Finder

## 1. Project Overview

This project develops a screenplay-based pipeline to identify and rank potential promotional clips from a collection of 50 episodic screenplays.

The objective is to identify self-contained 20–60 second segments with:
- A strong opening hook.
- Enough context for a new viewer.
- Emotional impact and narrative escalation.
- An unresolved or compelling ending.

The system combines automated candidate generation and screening with human editorial evaluation.

## 2. Dataset

The source dataset contains 50 screenplay text files.

The screenplay files contain:
- Dialogue
- Camera descriptions
- Action descriptions
- Sound effects
- Scene and episode timestamps

Important limitation: The supplied data is screenplay text, not actual video footage. Therefore, visual execution, acting, audio quality and final editing cannot be directly validated.

## 3. Pipeline

### Phase 1 — Data Extraction and Validation

- Parse screenplay files.
- Extract timestamped events.
- Identify dialogue, camera, action and sound-effect blocks.
- Validate timestamps and scene boundaries.
- Generate episode-level timeline summaries.

### Phase 2 — Candidate Generation and Editorial Ranking

- Generate candidate windows between 20 and 60 seconds.
- Use a 5-second starting-point interval.
- Refine event timelines to candidate boundaries.
- Apply preliminary screening.
- Create a human editorial review shortlist.
- Score reviewed candidates using a weighted rubric.
- Rank candidates and retain pending reviews.

### Editorial Scoring Rubric

| Criterion | Weight |
|---|---:|
| Opening hook | 25% |
| Context clarity | 20% |
| Emotional impact | 20% |
| Escalation | 15% |
| Ending strength | 20% |

Each criterion is rated from 0 to 5.

The final editorial score is a weighted score out of 100. These are human editorial judgments, not model predictions.

## 4. Current Results

- Episodes processed: 50
- Scenes identified: 100
- Timestamped event blocks: 3,727
- Generated candidate windows: 4,305
- Candidates in editorial review sheet: 63
- Manually reviewed candidates: 4
- Pending editorial reviews: 59

### Current Top Reviewed Candidates

| Rank | Episode | Time Range | Score |
|---|---:|---|---:|
| 1 | 1 | 00:00–00:40 | 97 |
| 2 | 28 | 00:00–00:48 | 96 |
| 3 | 11 | 00:00–00:54 | 96 |
| 4 | 22 | 00:06.50–00:58.50 | 85 |

These results represent four manually reviewed candidates, not a fully reviewed set of all generated candidates.

## 5. Quality Assurance

The final consistency checks confirmed:
- No duplicate candidate IDs.
- Four reviewed candidates.
- Fifty-nine pending candidates.
- Zero score mismatches.
- Consistency between the editorial review sheet and ranking output.

A source timestamp anomaly was also identified in Episode 22: one sound-effect event extends 0.3 seconds beyond its scene boundary. The source timestamp was preserved and flagged rather than silently modified.

## 6. Failure Case

Episode 46 was inspected as a negative editorial example. Although the 60-second segment contains a dramatic confrontation and a strong character response, its ending resolves the immediate emotional exchange rather than creating the desired unresolved cliffhanger.

It was therefore not promoted into the final ranked selections.

See the failure-case documentation for details.

## 7. Project Structure

```text
kuku_promo_finder/
├── data/
│   └── raw/
├── src/
├── outputs/
├── README.md
└── requirements.txt
```

## 8. Reproducibility

Create and activate a Python virtual environment, install the required dependencies, and run the pipeline scripts in the documented order.

See the execution instructions in the project documentation.

## 9. Limitations and Future Work

Current limitations:
- Editorial evaluation is screenplay-based.
- Only four candidates have completed manual editorial review.
- The current weighted scoring rubric is not trained on audience performance.
- No video-level validation has been performed.

Future improvements:
- NLP-based narrative and emotion features.
- Improved hook and cliffhanger detection.
- Larger human-labelled evaluation dataset.
- Streamlit-based review interface.
- Video and audio integration for actual footage validation.

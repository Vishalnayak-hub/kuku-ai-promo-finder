# Kuku AI — Promotional Clip Finder

## 1. Project Overview

A Python-based pipeline to identify, evaluate and rank potential 20–60 second promotional clips from 50 episodic screenplays.

The system combines timestamp extraction, sliding-window candidate generation, NLP-based feature engineering, heuristic scoring, near-duplicate suppression and human editorial evaluation through a Streamlit dashboard.

**Important limitation:** The supplied source contains screenplay text and timestamped descriptions, not actual video footage. Therefore, visual execution, acting, audio and editing quality could not be validated.

## 2. Dataset

- 50 screenplay text files
- 100 scenes
- 3,727 timestamped event blocks
- Event types: dialogue, camera, action and sound effects

## 3. Methodology

### Phase 1 — Data Extraction and Validation
- Parse screenplay files and extract timestamped events.
- Validate timestamps, event intervals and scene boundaries.
- Generate episode timeline summaries.
- Preserve source timestamps and flag boundary anomalies.

### Phase 2 — Candidate Generation and Editorial Review
- Generate 20–60 second candidate windows using 5-second starting-point intervals.
- Refine event timelines to candidate boundaries.
- Generate an editorial shortlist.
- Apply a five-criterion human editorial rubric.
- Document failure cases, including Episode 46.

### Phase 3 — NLP Feature Engineering and Automated Scoring
- Extract 16 screenplay-derived features, including dialogue density, questions, emotional signals, conflict signals and cliffhanger signals.
- Calculate heuristic scores using hook, cliffhanger, conflict, emotion, dialogue density, action and event richness.
- Detect near-duplicate candidates using temporal overlap.
- Compare automated rankings against human editorial ratings.

### Phase 4 — Streamlit Dashboard
- Explore candidate clips and automated rankings.
- Filter by episode and duration.
- Inspect candidate timelines and NLP features.
- Review scoring breakdowns and human editorial evaluations.
- Export filtered candidate datasets as CSV.

## 4. Editorial Scoring Rubric

| Criterion | Weight |
|---|---:|
| Opening hook | 25% |
| Context clarity | 20% |
| Emotional impact | 20% |
| Escalation | 15% |
| Ending strength | 20% |

Each criterion is rated from 0 to 5. The weighted editorial score is out of 100. These are subjective screenplay-based human judgments.

## 5. Current Results

| Metric | Result |
|---|---:|
| Episodes processed | 50 |
| Original candidate windows | 4,305 |
| Candidates after custom additions | 4,308 |
| NLP features extracted per candidate | 16 |
| Candidates retained after near-duplicate suppression | 268 |
| Editorial shortlist records | 63 |
| Manually reviewed | 5 |
| Pending editorial review | 58 |

### Top Manually Reviewed Candidates

| Rank | Episode | Time Range | Duration | Score |
|---|---:|---|---:|---:|
| 1 | 1 | 00:00–00:40 | 40 sec | 97 |
| 2 | 11 | 00:00–01:00 | 60 sec | 96 |
| 3 | 28 | 00:00–00:48 | 48 sec | 96 |
| 4 | 11 | 00:00–00:54 | 54 sec | 96 |
| 5 | 22 | 00:06.50–00:58.50 | 52 sec | 85 |

The Episode 11 cuts are near-duplicates. The 60-second version is preferred because it includes the constable's search and Juliana's urgent reveal about her mother's medicines. The 54-second version is an alternative cut, not an independent story.

These five candidates are manually reviewed examples, not a fully validated ranking of all candidates.

## 6. Automated Scoring Validation

- Five human-reviewed candidates matched successfully with automated scores.
- Spearman rank correlation: **0.447**.
- This is an exploratory comparison based on only five observations, not reliable model validation.
- Automated scores are heuristic screening signals, not predictions from a trained machine-learning model.
- Human editorial review remains necessary for narrative context, emotional impact and cliffhanger quality.

## 7. Failure Case

Episode 46 was inspected as a negative example. Its strongest 60-second cut contains a dramatic confrontation but ends with an emotionally resolved response rather than a clearly unresolved cliffhanger.

See `outputs/episode_46_failure_case.md`.

## 8. Project Structure

- `data/raw/` — Original screenplay files
- `src/` — Python scripts for extraction, candidate generation, NLP, scoring, deduplication and validation
- `outputs/` — Processed datasets, rankings and editorial evaluations
- `app.py` — Streamlit dashboard
- `requirements.txt` — Python dependencies
- `EXECUTION_GUIDE.md` — Instructions for running the project

## 9. Limitations and Future Work

- Evaluation is based on screenplay text and timestamped descriptions, not actual video.
- Only five candidates have completed manual editorial review.
- Automated scores rely on keyword and structural heuristics and do not fully understand narrative semantics.
- Temporal overlap detection may not identify semantically similar clips across different episodes.
- Future improvements include a larger human-labelled dataset, semantic narrative models, video/audio analysis and broader editorial validation.

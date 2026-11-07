# Kuku AI — Promotional Clip Finder

## 1. Project Overview

A Python-based pipeline to identify, evaluate and rank potential 20–60 second promotional clips from episodic screenplays.

The system combines timestamp extraction, sliding-window candidate generation, NLP-based feature engineering, heuristic scoring, near-duplicate suppression and human editorial evaluation through a Streamlit dashboard.

**Important limitation:** The supplied source contains screenplay text and timestamped descriptions, not actual video footage. Visual execution, acting, audio and editing quality could therefore not be validated.

## 2. Dataset

The assignment input consists of:

- 50 screenplay text files
- 100 scenes
- 3,727 timestamped event blocks
- Event types: dialogue, camera, action and sound effects

The original screenplay files and generated datasets are not included in this public repository. They should be placed in the appropriate local project directories before execution.

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
- Inspect and document failure cases, including Episode 46.

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

## 4. Setup and Execution

### Requirements

- Python 3.13 or compatible version
- Git
- Assignment screenplay input files

### Clone the repository

```bash
git clone https://github.com/Vishalnayak-hub/kuku-ai-promo-finder.git
cd kuku-ai-promo-finder
```

### Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add input files

Place the 50 assignment screenplay TXT files in:

```text
data/raw/
```

The input files are not distributed through this repository.

### Run the pipeline

Follow `EXECUTION_GUIDE.md` for the ordered execution of the Python scripts in `src/`. This generates the processed datasets and candidate rankings in `outputs/`.

### Launch the dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, normally:

```text
http://localhost:8501
```

**Note:** The dashboard requires the generated output CSV files. Run the pipeline before launching it.

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

| Rank | Episode | Time Range | Duration | Editorial Score |
|---|---:|---|---:|---:|
| 1 | 1 | 00:00–00:40 | 40 sec | 97 |
| 2 | 11 | 00:00–01:00 | 60 sec | 96 |
| 3 | 28 | 00:00–00:48 | 48 sec | 96 |
| 4 | 22 | 00:06.50–00:58.50 | 52 sec | 85 |

**Alternative cut:** Episode 11 also has a manually reviewed 54-second version (00:00–00:54, score 96). It is a near-duplicate of the 60-second version, not an independent story. The 60-second version is preferred because it includes the constable's search and Juliana's urgent reveal about her mother's medicines.

These are manually reviewed examples, not a fully validated ranking of all candidates.

## 6. Automated Scoring Validation

- Five human-reviewed candidates matched successfully with automated scores.
- Spearman rank correlation: **0.447**.
- This is an exploratory comparison based on only five observations, not reliable model validation.
- Automated scores are heuristic screening signals, not predictions from a trained machine-learning model.
- Human editorial review remains necessary for narrative context, emotional impact and cliffhanger quality.

## 7. Failure Case

Episode 46 was inspected as a negative example. Its strongest 60-second cut contains a dramatic confrontation involving a royal proclamation challenging the marriage. However, it ends with an emotionally resolved response rather than a clearly unresolved cliffhanger.

Therefore, it was documented as a rejection case rather than selected as a top promotional candidate.

This illustrates why dramatic intensity alone is insufficient: a strong promotional clip should also leave viewers with a compelling unresolved question.

## 8. Project Structure

```text
kuku-promo-finder/
├── src/                  # Python processing scripts
├── app.py                # Streamlit dashboard
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── EXECUTION_GUIDE.md    # Detailed execution sequence
├── data/raw/             # Local screenplay inputs (not tracked)
└── outputs/               # Generated datasets (not tracked)
```

## 9. Limitations and Future Work

- Evaluation is based on screenplay text and timestamped descriptions, not actual video.
- Only five candidates have completed manual editorial review.
- Automated scores rely on keyword and structural heuristics and do not fully understand narrative semantics.
- Temporal overlap detection may not identify semantically similar clips across different episodes.
- Future improvements include a larger human-labelled dataset, semantic narrative models, video/audio analysis and broader editorial validation.

## 10. Submission Links

**GitHub Repository:**

https://github.com/Vishalnayak-hub/kuku-ai-promo-finder

**Execution Instructions:**

See `EXECUTION_GUIDE.md` in the repository.

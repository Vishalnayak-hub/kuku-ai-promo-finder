# Execution Guide — Kuku AI Promo Finder

## 1. Requirements

- Python 3.11 or later
- pip
- Windows, macOS or Linux

## 2. Project Setup

Open a terminal in the project root directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Pipeline Execution

Run all commands from the project root directory.

### Phase 1 — Data Extraction and Validation

```bash
python src/parse_screenplays_v2.py
python src/validate_parsed_data.py
python src/validate_scene_boundaries.py
python src/quality_control_report.py
python src/analyze_episode_timelines.py
```

### Phase 2 — Candidate Generation and Refinement

```bash
python src/generate_candidates.py
python src/refine_candidates.py
python src/analyze_candidate_quality.py
```

### Phase 3 — Editorial Shortlist and Human Review

```bash
python src/create_editorial_shortlist.py
python src/rank_final_shortlist.py
python src/final_quality_check.py
```

The editorial shortlist includes manually selected candidate windows. Their event timelines and metadata are preserved in the refined candidate dataset. Human ratings are maintained in the editorial review sheet.

**Reproducibility note:** The five manually reviewed candidates and their editorial scores are human-curated inputs. Re-running the automated pipeline does not independently reproduce those judgments.

### Phase 4 — NLP Feature Extraction and Automated Scoring

```bash
python src/extract_nlp_features.py
python src/score_promo_candidates.py
```

This phase extracts 16 screenplay-derived features and calculates heuristic promo scores.

### Phase 5 — Near-Duplicate Detection and Validation

```bash
python src/deduplicate_rankings.py
python src/validate_nlp_scoring.py
python src/final_quality_check.py
```

Near-duplicate detection uses temporal overlap between candidates from the same episode. The overlap threshold is a heuristic.

The validation script compares automated scores with the five manually reviewed candidates. The resulting Spearman correlation is exploratory and should not be interpreted as reliable model validation.

## 4. Launching the Streamlit Dashboard

From the project root, activate the virtual environment and run:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

The dashboard supports:

- Candidate filtering by episode and duration
- Automated ranking exploration
- Candidate timeline inspection
- NLP feature inspection
- Automated score breakdowns
- Human editorial review inspection
- CSV export of filtered candidates

Keep the terminal running while using the dashboard.

## 5. Main Output Files

Important files in `outputs/` include:

| File | Description |
|---|---|
| `screenplay_blocks_v2.csv` | Parsed timestamped screenplay events |
| `episode_timeline_summary.csv` | Episode-level timeline summaries |
| `promo_candidates_refined.csv` | Refined candidate windows and event timelines |
| `editorial_review_sheet.csv` | Human editorial review inputs |
| `final_ranked_promo_shortlist.csv` | Ranked editorial shortlist |
| `pending_editorial_reviews.csv` | Candidates awaiting manual review |
| `nlp_candidate_features.csv` | Extracted NLP features |
| `automated_scored_candidates.csv` | Automated heuristic scores |
| `deduplicated_candidates.csv` | Candidates retained after overlap suppression |
| `editorial_automated_comparison.csv` | Human versus automated score comparison |

## 6. Current Pipeline Results

- Episodes processed: 50
- Candidate windows: 4,308
- NLP features per candidate: 16
- Candidates retained after near-duplicate suppression: 268
- Editorial shortlist records: 63
- Manually reviewed candidates: 5
- Pending editorial reviews: 58
- Duplicate candidate IDs in editorial shortlist: 0

## 7. Limitations

- The supplied dataset contains screenplay text and timestamped descriptions, not actual video footage.
- Automated scores are heuristic screening signals, not predictions from a trained machine-learning model.
- Human editorial judgments are subjective.
- Only five candidates have been manually reviewed.
- Temporal overlap does not identify every semantically similar clip across different episodes.

The system should be treated as a screenplay-based promotional clip discovery and editorial decision-support prototype.

import re
from pathlib import Path

import pandas as pd
import streamlit as st


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Kuku AI | Promo Finder",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 Kuku AI — Promo Finder")
st.caption("AI-assisted promotional clip discovery and ranking")

OUTPUT_DIR = Path("outputs")


# =====================================================
# 2. LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    scored = pd.read_csv(
        OUTPUT_DIR / "automated_scored_candidates.csv"
    )

    features = pd.read_csv(
        OUTPUT_DIR / "nlp_candidate_features.csv"
    )

    editorial = pd.read_csv(
        OUTPUT_DIR / "editorial_review_sheet.csv"
    )

    candidates = pd.read_csv(
        OUTPUT_DIR / "promo_candidates_refined.csv"
    )

    return scored, features, editorial, candidates


try:
    scored, features, editorial, candidates = load_data()

except FileNotFoundError as error:
    st.error(f"Required file not found: {error}")
    st.stop()


# =====================================================
# 3. DATA PREPARATION
# =====================================================

required_scored_columns = {
    "candidate_id",
    "episode_number",
    "duration_seconds",
    "automated_score",
    "start_timestamp",
    "end_timestamp",
}

missing_columns = required_scored_columns - set(scored.columns)

if missing_columns:
    st.error(
        f"Scored candidates file is missing columns: "
        f"{sorted(missing_columns)}"
    )
    st.stop()


for column in [
    "episode_number",
    "duration_seconds",
    "automated_score",
]:
    scored[column] = pd.to_numeric(
        scored[column],
        errors="coerce"
    )


scored = scored.dropna(
    subset=[
        "candidate_id",
        "episode_number",
        "duration_seconds",
        "automated_score",
    ]
)


# =====================================================
# 4. SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filter Candidates")

episodes = sorted(
    scored["episode_number"].dropna().unique().tolist()
)

selected_episodes = st.sidebar.multiselect(
    "Select Episodes",
    episodes,
    default=episodes,
)

min_duration = int(
    scored["duration_seconds"].min()
)

max_duration = int(
    scored["duration_seconds"].max()
)

duration_range = st.sidebar.slider(
    "Duration (seconds)",
    min_value=min_duration,
    max_value=max_duration,
    value=(min_duration, max_duration),
)


# =====================================================
# 5. FILTER CANDIDATES
# =====================================================

filtered = scored[
    scored["episode_number"].isin(selected_episodes)
    & scored["duration_seconds"].between(
        duration_range[0],
        duration_range[1],
    )
].copy()

filtered = filtered.sort_values(
    "automated_score",
    ascending=False,
)


# =====================================================
# 6. PROJECT OVERVIEW
# =====================================================

st.subheader("📊 Project Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Candidates",
    f"{len(scored):,}",
)

col2.metric(
    "Filtered Candidates",
    f"{len(filtered):,}",
)

col3.metric(
    "Average Score",
    f"{scored['automated_score'].mean():.2f}",
)

col4.metric(
    "Episodes",
    f"{scored['episode_number'].nunique():.0f}",
)

st.divider()


# =====================================================
# 7. TOP RANKED PROMOS
# =====================================================

st.subheader("🏆 Top Ranked Promos")

top_n = st.slider(
    "Number of candidates to display",
    min_value=5,
    max_value=50,
    value=10,
)

display_columns = [
    "candidate_id",
    "episode_number",
    "start_timestamp",
    "end_timestamp",
    "duration_seconds",
    "automated_score",
]

available_columns = [
    column
    for column in display_columns
    if column in filtered.columns
]

st.dataframe(
    filtered[available_columns].head(top_n),
    width="stretch",
    hide_index=True,
)


# =====================================================
# 8. SCORE DISTRIBUTION
# =====================================================

st.subheader("📈 Automated Score Distribution")

if not filtered.empty:

    score_bins = pd.cut(
        filtered["automated_score"],
        bins=10,
        duplicates="drop",
    )

    score_counts = (
        score_bins.value_counts()
        .sort_index()
    )

    score_distribution = pd.DataFrame(
        {
            "Score Range": [
                f"{interval.left:.1f} - {interval.right:.1f}"
                for interval in score_counts.index
            ],
            "Number of Candidates": score_counts.values,
        }
    )

    st.bar_chart(
        score_distribution,
        x="Score Range",
        y="Number of Candidates",
    )

else:
    st.info(
        "No candidates available for the selected filters."
    )


# =====================================================
# 9. CANDIDATE INSPECTOR
# =====================================================

st.divider()
st.subheader("🔍 Candidate Inspector")

candidate_ids = (
    filtered["candidate_id"]
    .dropna()
    .astype(str)
    .tolist()
)

if candidate_ids:

    selected_candidate = st.selectbox(
        "Choose a candidate",
        candidate_ids,
    )

    candidate = filtered[
        filtered["candidate_id"].astype(str)
        == selected_candidate
    ].iloc[0]

    st.write(f"**Candidate:** {selected_candidate}")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Episode",
        int(candidate["episode_number"]),
    )

    c2.metric(
        "Duration",
        f"{candidate['duration_seconds']:.2f} sec",
    )

    c3.metric(
        "Automated Score",
        f"{candidate['automated_score']:.2f}/100",
    )

    # =================================================
    # 9A. AUTOMATED SCORE BREAKDOWN
    # =================================================

    st.divider()
    st.subheader("📊 Automated Scoring Breakdown")

    score_components = {
        "Hook": ("hook_score", 20),
        "Cliffhanger": ("cliffhanger_score", 25),
        "Conflict": ("conflict_score", 15),
        "Emotion": ("emotion_score", 15),
        "Dialogue Density": ("dialogue_score", 10),
        "Action Presence": ("action_score", 5),
        "Event Richness": ("event_richness_score", 10),
    }

    missing_score_columns = [
        column
        for column, _ in score_components.values()
        if column not in filtered.columns
    ]

    if missing_score_columns:

        st.warning(
            f"Score breakdown columns missing: "
            f"{missing_score_columns}"
        )

    else:

        breakdown_data = []

        for component, (column, maximum) in score_components.items():

            actual_score = pd.to_numeric(
                pd.Series([candidate[column]]),
                errors="coerce",
            ).iloc[0]

            actual_score = (
                0.0
                if pd.isna(actual_score)
                else float(actual_score)
            )

            breakdown_data.append(
                {
                    "Component": component,
                    "Score": round(actual_score, 2),
                    "Maximum Weight": maximum,
                    "Contribution (%)": round(
                        actual_score / maximum * 100,
                        2,
                    ) if maximum else 0,
                }
            )

        breakdown_df = pd.DataFrame(breakdown_data)

        calculated_total = float(
            breakdown_df["Score"].sum()
        )

        final_score = float(
            candidate["automated_score"]
        )

        score_col1, score_col2 = st.columns(2)

        score_col1.metric(
            "Sum of Component Scores",
            f"{calculated_total:.2f}/100",
        )

        score_col2.metric(
            "Final Automated Score",
            f"{final_score:.2f}/100",
        )

        st.write("**Individual Component Contributions**")

        st.dataframe(
            breakdown_df,
            width="stretch",
            hide_index=True,
        )

        st.write("**Visual Score Breakdown**")

        st.bar_chart(
            breakdown_df,
            x="Component",
            y="Score",
        )

        if abs(calculated_total - final_score) < 0.1:

            st.success(
                "Component scores correctly add up "
                "to the final score."
            )

        else:

            st.warning(
                "Component total differs from the final score. "
                "This may be due to rounding or differences "
                "in score aggregation."
            )

    # =================================================
    # 9B. NLP FEATURES
    # =================================================

    st.subheader("🧠 Extracted NLP Features")

    candidate_features = features[
        features["candidate_id"].astype(str)
        == selected_candidate
    ]

    if not candidate_features.empty:

        st.dataframe(
            candidate_features,
            width="stretch",
            hide_index=True,
        )

    else:

        st.info(
            "No NLP features available for this candidate."
        )

    # =================================================
    # 9C. PROMO EVENT TIMELINE
    # =================================================

    st.divider()
    st.subheader("🎬 Promo Event Timeline")

    timeline_row = candidates[
        candidates["candidate_id"].astype(str)
        == selected_candidate
    ]

    if (
        not timeline_row.empty
        and "event_timeline" in timeline_row.columns
    ):

        event_timeline = timeline_row.iloc[0]["event_timeline"]

        if pd.notna(event_timeline) and str(event_timeline).strip():

            timeline_rows = []

            pattern = (
                r"\[(\d+(?:\.\d+)?)-"
                r"(\d+(?:\.\d+)?)\]\s*"
                r"([A-Z_]+):\s*(.*)"
            )

            for line in str(event_timeline).splitlines():

                match = re.search(pattern, line)

                if match:

                    start, end, event_type, description = (
                        match.groups()
                    )

                    timeline_rows.append(
                        {
                            "Start (sec)": float(start),
                            "End (sec)": float(end),
                            "Event Type": event_type,
                            "Description": description,
                        }
                    )

            if timeline_rows:

                timeline_df = pd.DataFrame(timeline_rows)

                st.write("**Events inside the selected promo**")

                st.dataframe(
                    timeline_df,
                    width="stretch",
                    hide_index=True,
                )

                st.write("**Event Type Distribution**")

                event_counts = (
                    timeline_df["Event Type"]
                    .value_counts()
                    .rename_axis("Event Type")
                    .reset_index(name="Count")
                )

                st.bar_chart(
                    event_counts,
                    x="Event Type",
                    y="Count",
                )

            else:

                st.info(
                    "Could not parse the timeline. "
                    "Showing the original timeline instead."
                )

                st.text(str(event_timeline))

        else:

            st.warning(
                "No event timeline available for this candidate."
            )

    else:

        st.warning(
            "Candidate not found in the timeline dataset."
        )

else:

    st.info(
        "No candidates match the selected filters."
    )


# =====================================================
# 10. HUMAN EDITORIAL REVIEWS
# =====================================================

st.divider()
st.subheader("📝 Human Editorial Reviews")

st.caption(
    "Only candidates with completed manual editorial scores "
    "are displayed."
)

if "editorial_score" in editorial.columns:

    editorial_scores = pd.to_numeric(
        editorial["editorial_score"],
        errors="coerce",
    )

    reviewed_editorial = editorial.loc[
        editorial_scores.notna()
    ].copy()

    if not reviewed_editorial.empty:

        st.metric(
            "Manually Reviewed Candidates",
            len(reviewed_editorial),
        )

        st.dataframe(
            reviewed_editorial,
            width="stretch",
            hide_index=True,
        )

    else:

        st.info(
            "No completed editorial reviews found."
        )

else:

    st.warning(
        "The editorial review file does not contain "
        "an 'editorial_score' column."
    )


# =====================================================
# 11. EXPORT RESULTS
# =====================================================

st.divider()
st.subheader("📥 Export Results")

csv_data = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Candidates CSV",
    data=csv_data,
    file_name="filtered_promo_candidates.csv",
    mime="text/csv",
)


st.success("Dashboard loaded successfully!")
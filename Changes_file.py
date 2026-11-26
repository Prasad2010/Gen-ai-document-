# ==========================================================
# EXPOSURE REPORT FILTERING
# ==========================================================

def find_report_column(df, date_text, required_words):
    """
    Dynamically identify columns, including MultiIndex columns.
    """
    matches = []

    for col in df.columns:
        col_text = " ".join(map(str, col)) if isinstance(col, tuple) else str(col)
        col_text = col_text.lower()

        if date_text and date_text.lower() not in col_text:
            continue

        if all(word.lower() in col_text for word in required_words):
            matches.append(col)

    if len(matches) != 1:
        raise ValueError(
            f"Expected one column for {date_text}, {required_words}. "
            f"Found: {matches}"
        )

    return matches[0]


def clean_report_value(value):
    """Standardise values for reliable comparison."""
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if value in ("", "none", "nan", "null"):
        return None

    if value.endswith(".0"):
        value = value[:-2]

    return value


# Create independent filtered copies
stage_12_change = pd.DataFrame()
stage_3_change = pd.DataFrame()
ctm_change = pd.DataFrame()

try:
    # Identify STG columns
    stg_sep_col = find_report_column(
        stg_report, "2026-09-30",
        ["impairment type", "final stage", "r"]
    )

    stg_jun_col = find_report_column(
        stg_report, "2026-06-30",
        ["impairment type", "final stage", "r"]
    )

    corporate_col = find_report_column(
        stg_report, None,
        ["corporate name"]
    )

    # Standardise STG values
    sep_stage = stg_report[stg_sep_col].map(clean_report_value)
    jun_stage = stg_report[stg_jun_col].map(clean_report_value)

    corporate_name = stg_report[corporate_col].map(clean_report_value)

    # Stage 1 and 2: 1 -> 2 OR 2 -> 1
    stage_12_mask = (
        (
            (sep_stage == "1") & (jun_stage == "2")
        ) |
        (
            (sep_stage == "2") & (jun_stage == "1")
        )
    ) & corporate_name.notna()

    stage_12_change = stg_report.loc[
        stage_12_mask
    ].copy()

    # Stage 3: Either reporting period has Stage 3
    stage_3_mask = (
        (sep_stage == "3") |
        (jun_stage == "3")
    )

    stage_3_change = stg_report.loc[
        stage_3_mask
    ].copy()

    # Identify CTM Owner columns
    ctm_sep_col = find_report_column(
        ctm_report, "2026-09-30",
        ["ctm", "owner", "r"]
    )

    ctm_jun_col = find_report_column(
        ctm_report, "2026-06-30",
        ["ctm", "owner", "r"]
    )

    sep_owner = ctm_report[ctm_sep_col].map(clean_report_value)
    jun_owner = ctm_report[ctm_jun_col].map(clean_report_value)

    # CTM Owner changed between September and June
    ctm_mask = (
        sep_owner.notna() &
        jun_owner.notna() &
        (sep_owner != jun_owner)
    )

    ctm_change = ctm_report.loc[
        ctm_mask
    ].copy()

except Exception as e:
    st.error(f"Exposure report filtering error: {e}")


# ==========================================================
# DIMENSION REPORTING TABS
# ==========================================================

product_tab, stage_tab, ctm_tab, exposure_tab = st.tabs(
    ["Product", "STAGE", "CTM", "Exposure Reporting"]
)


# ==========================================================
# FOURTH TAB - EXPOSURE REPORTING
# ==========================================================

with exposure_tab:

    st.subheader("Exposure Reporting")

    # TABLE 1: STAGE 1 AND 2 CHANGES
    st.markdown("### Stage (1 & 2) Change QoQ")

    if stg_report is not None:
        st.caption(
            "Records where impairment stage changed between "
            "1 and 2 across June and September 2026. "
            "Blank corporate names are excluded."
        )

        st.dataframe(
            stage_12_change,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total records: {len(stage_12_change)}"
        )
    else:
        st.info("STG report not available.")

    st.divider()

    # TABLE 2: STAGE 3
    st.markdown("### Stage 3 Change QoQ")

    if stg_report is not None:
        st.caption(
            "Records where either June or September 2026 "
            "has impairment stage 3."
        )

        st.dataframe(
            stage_3_change,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total records: {len(stage_3_change)}"
        )
    else:
        st.info("STG report not available.")

    st.divider()

    # TABLE 3: CTM CHANGES
    st.markdown("### CTM Change QoQ")

    if ctm_report is not None:
        st.caption(
            "Records where CTM Owner R differs between "
            "June and September 2026."
        )

        st.dataframe(
            ctm_change,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total records: {len(ctm_change)}"
        )
    else:
        st.info("CTM report not available.")












One small adjustment: In the four find_report_column() calls for impairment and CTM owner, use "- r" instead of "r" as the last search term:










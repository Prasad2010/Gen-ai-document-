Generic filtering function
In exposure_report_filter.py







import pandas as pd


def filter_exposure_report(
    report,
    current_date,
    previous_date,
    classification_col
):
    """
    Generic filter for either STG or CTM report.

    Removes:
    1. Rows where both quarter carrying amounts are zero.
    2. Rows where classification is missing in both quarters.
    """

    def get_col(date, metric):
        date = pd.Timestamp(date).strftime("%Y-%m-%d")

        for col in report.columns:
            if (
                isinstance(col, tuple)
                and pd.Timestamp(col[0]).strftime("%Y-%m-%d") == date
                and str(col[1]).strip() == metric
            ):
                return report[col]

        raise KeyError(f"Missing column: {date}, {metric}")

    current_ca = pd.to_numeric(
        get_col(current_date, "Carrying Amount"),
        errors="coerce"
    )

    previous_ca = pd.to_numeric(
        get_col(previous_date, "Carrying Amount"),
        errors="coerce"
    )

    current_class = get_col(
        current_date, classification_col
    )

    previous_class = get_col(
        previous_date, classification_col
    )

    # Remove zero exposure in both quarters
    zero_mask = (
        current_ca.eq(0)
        & previous_ca.eq(0)
    )

    # Remove missing classification in both quarters
    missing_mask = (
        current_class.isna()
        & previous_class.isna()
    )

    result = report.loc[
        ~(zero_mask | missing_mask)
    ].copy()

    return result


def filter_stg_report(
    stg_report, current_date, previous_date
):
    return filter_exposure_report(
        report=stg_report,
        current_date=current_date,
        previous_date=previous_date,
        classification_col="Impairment type (final stage) - R"
    )


def filter_ctm_report(
    ctm_report, current_date, previous_date
):
    return filter_exposure_report(
        report=ctm_report,
        current_date=current_date,
        previous_date=previous_date,
        classification_col="CTM (Owner) - R"
    )













def identify_reporting_dates(df):

    dates = pd.to_datetime(
        df["Closing Date"], errors="coerce"
    ).dropna()

    quarters = sorted(
        dates.dt.to_period("Q").unique(),
        reverse=True
    )

    if len(quarters) < 2:
        raise ValueError("Two reporting quarters required")

    current_date = dates[
        dates.dt.to_period("Q") == quarters[0]
    ].max()

    previous_date = dates[
        dates.dt.to_period("Q") == quarters[1]
    ].max()

    return current_date, previous_date













from functions.exposure_report_filter import (
    identify_reporting_dates,
    filter_stg_report,
    filter_ctm_report
)

# Identify dates
current_date, previous_date = identify_reporting_dates(df)

print("Current:", current_date)
print("Previous:", previous_date)

# STG filtering
stg_final = filter_stg_report(
    stg_report,
    current_date,
    previous_date
)

# CTM filtering
ctm_final = filter_ctm_report(
    ctm_report,
    current_date,
    previous_date
)

print("STG rows:", len(stg_final))
print("CTM rows:", len(ctm_final))

display(stg_final)
display(ctm_final)

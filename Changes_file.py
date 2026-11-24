
import pandas as pd
import numpy as np


def identify_reporting_periods(df):

    dates = (
        pd.to_datetime(df["Closing Date"], errors="coerce")
        .dropna()
        .dt.normalize()
        .unique()
    )

    dates = sorted(pd.Timestamp(d) for d in dates)

    if len(dates) != 2:
        raise ValueError(
            f"Expected 2 unique reporting dates. Found: {dates}"
        )

    return dates[1], dates[0]


def create_quarterly_exposure_comparison(
    df: pd.DataFrame,
    classification_col: str
) -> pd.DataFrame:

    # 1. Define index columns
    index_cols = [
        "Customer Nature",
        "Product",
        "RMPM ID (Principal restitution party)",
        "Corporate name (Principal restitution party)"
    ]

    required_cols = index_cols + [
        "Closing Date",
        "Balance Type",
        "Amount in K EUR",
        classification_col
    ]

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        raise KeyError(f"Missing columns: {missing}")

    working = df[required_cols].copy()

    # 2. Identify quarters
    current_date, previous_date = identify_reporting_periods(working)

    working["Closing Date"] = (
        pd.to_datetime(working["Closing Date"], errors="coerce")
        .dt.normalize()
    )

    working = working[
        working["Closing Date"].isin(
            [current_date, previous_date]
        )
    ].copy()

    working["Balance Type"] = (
        working["Balance Type"].astype("string").str.strip()
    )

    # 3. Validate balance types
    expected_types = {"Gross value", "Impairment"}

    available_types = set(
        working["Balance Type"].dropna().unique()
    )

    if not expected_types.issubset(available_types):
        raise ValueError(
            f"Missing balance types: {expected_types - available_types}"
        )

    # 4. Convert amounts
    original_amounts = working["Amount in K EUR"]

    working["Amount in K EUR"] = pd.to_numeric(
        original_amounts, errors="coerce"
    )

    invalid = (
        original_amounts.notna()
        & working["Amount in K EUR"].isna()
    )

    if invalid.any():
        raise ValueError("Non-numeric values found in Amount in K EUR")

    working["Amount in K EUR"] = (
        working["Amount in K EUR"].fillna(0)
    )

    # 5. Establish complete reporting index
    output_index = pd.MultiIndex.from_frame(
        working[index_cols].drop_duplicates()
    )

    output_index.names = index_cols

    result = pd.DataFrame(index=output_index)

    # 6. Helper: retrieve classification
    def get_classification(reporting_date):

        subset = working[
            working["Closing Date"] == reporting_date
        ]

        grouped = subset.groupby(
            index_cols,
            dropna=False,
            sort=False
        )[classification_col].agg(
            lambda x: (
                x.dropna().astype(str).unique().tolist()
            )
        )

        for values in grouped:
            if len(values) > 1:
                raise ValueError(
                    f"Multiple {classification_col} values "
                    f"for the same reporting entity: {values}"
                )

        grouped = grouped.map(
            lambda x: x[0] if len(x) == 1 else pd.NA
        )

        return grouped.reindex(output_index)

    # 7. Helper: retrieve financial amounts
    def get_amount(reporting_date, balance_type):

        subset = working[
            (working["Closing Date"] == reporting_date)
            & (working["Balance Type"] == balance_type)
        ]

        grouped = subset.groupby(
            index_cols,
            dropna=False,
            sort=False
        )["Amount in K EUR"].sum()

        return grouped.reindex(
            output_index, fill_value=0
        ).fillna(0)

    # 8. Retrieve classification values
    current_classification = get_classification(current_date)

    previous_classification = get_classification(previous_date)

    # 9. Retrieve current-quarter amounts
    current_gross = get_amount(current_date, "Gross value")
    current_impairment = get_amount(current_date, "Impairment")

    current_carrying = current_gross + current_impairment

    # 10. Retrieve previous-quarter amounts
    previous_gross = get_amount(previous_date, "Gross value")
    previous_impairment = get_amount(previous_date, "Impairment")

    previous_carrying = previous_gross + previous_impairment

    # 11. Create columns in EXACT screenshot order

    current_label = current_date.strftime("%Y-%m-%d")
    previous_label = previous_date.strftime("%Y-%m-%d")

    columns = [
        (current_label, classification_col),
        (previous_label, classification_col),

        (current_label, "Gross value"),
        (current_label, "Impairment"),
        (current_label, "Carrying Amount"),

        (previous_label, "Gross value"),
        (previous_label, "Impairment"),
        (previous_label, "Carrying Amount")
    ]

    data = [
        current_classification,
        previous_classification,

        current_gross,
        current_impairment,
        current_carrying,

        previous_gross,
        previous_impairment,
        previous_carrying
    ]

    result = pd.concat(data, axis=1)
    result.index = output_index

    result.columns = pd.MultiIndex.from_tuples(
        columns,
        names=["Closing Date", "Balance Type / Classification"]
    )

    # 12. Round financial values
    financial_columns = [
        col for col in result.columns
        if col[1] in [
            "Gross value",
            "Impairment",
            "Carrying Amount"
        ]
    ]

    result[financial_columns] = (
        result[financial_columns].astype(float).round(3)
    )

    print("\nEXPOSURE REPORT GENERATED")
    print("-------------------------")
    print("Classification:", classification_col)
    print("Current quarter:", current_label)
    print("Previous quarter:", previous_label)
    print("Total rows:", len(result))

    return result
    

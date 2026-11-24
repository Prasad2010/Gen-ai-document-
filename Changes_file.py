
import pandas as pd



def test_exposure_reporting_tab(df):

    print("=" * 65)
    print("QUARTERLY EXPOSURE REPORTING - TEST")
    print("=" * 65)

    # 1. Required columns
    required_columns = [
        "Closing Date",
        "Customer Nature",
        "Product",
        "RMPM ID (Principal restitution party)",
        "Corporate name (Principal restitution party)",
        "Balance Type",
        "Amount in K EUR",
        "Impairment type (final stage) - R",
        "CTM (Owner) - R"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    print("\n1. INPUT VALIDATION: PASSED")

    # 2. Identify reporting dates
    current_period, previous_period = (
        identify_reporting_periods(df)
    )

    print("\n2. REPORTING PERIODS: PASSED")
    print("Current quarter:", current_period)
    print("Previous quarter:", previous_period)

    # 3. Validate balance types
    balance_types = df["Balance Type"].dropna().unique()

    print("\n3. BALANCE TYPES")
    print(balance_types)

    expected_types = {"Gross value", "Impairment"}

    if not expected_types.issubset(set(balance_types)):
        raise ValueError(
            f"Missing balance types: "
            f"{expected_types - set(balance_types)}"
        )

    # 4. Test STG and CTM independently
    reporting_tabs = {
        "STG": "Impairment type (final stage) - R",
        "CTM": "CTM (Owner) - R"
    }

    results = {}

    for tab_name, classification_col in reporting_tabs.items():

        print("\n" + "=" * 65)
        print(f"TESTING {tab_name} TAB")
        print("=" * 65)

        test_df = df.copy()

        print("Classification column:", classification_col)

        print(
            "Unique classifications:",
            test_df[classification_col].nunique()
        )

        print(
            "Missing classifications:",
            test_df[classification_col].isna().sum()
        )

        # Filter reporting dates
        test_df = test_df[
            pd.to_datetime(test_df["Closing Date"]).dt.normalize()
            .isin([current_period, previous_period])
        ]

        # Validate data availability
        print("Rows available:", len(test_df))

        print(
            "Current quarter rows:",
            (pd.to_datetime(test_df["Closing Date"]).dt.normalize()
             == current_period).sum()
        )

        print(
            "Previous quarter rows:",
            (pd.to_datetime(test_df["Closing Date"]).dt.normalize()
             == previous_period).sum()
        )

        # Preview reporting input
        preview_columns = [
            "Customer Nature",
            "Product",
            "RMPM ID (Principal restitution party)",
            "Corporate name (Principal restitution party)",
            classification_col,
            "Closing Date",
            "Balance Type",
            "Amount in K EUR"
        ]

        print("\nSample records:")
        display(test_df[preview_columns].head(10))

        results[tab_name] = test_df

    print("\n" + "=" * 65)
    print("REPORTING INPUT TEST COMPLETED")
    print("=" * 65)

    return results

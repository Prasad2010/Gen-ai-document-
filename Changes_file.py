
import pandas as pd
import numpy as np


def identify_reporting_periods(df: pd.DataFrame):
    """
    Identify the latest and previous reporting dates
    dynamically from Closing Date.

    Returns:
        current_period: Latest closing date
        previous_period: Previous closing date
    """

    if "Closing Date" not in df.columns:
        raise KeyError("Closing Date column not found")

    dates = pd.to_datetime(
        df["Closing Date"],
        errors="coerce"
    ).dropna().dt.normalize().unique()

    dates = sorted(pd.Timestamp(d) for d in dates)

    if len(dates) != 2:
        raise ValueError(
            f"Expected exactly 2 unique closing dates, "
            f"but found {len(dates)}: {dates}"
        )

    previous_period = dates[0]
    current_period = dates[1]

    print("Identified reporting dates:")
    print("Current period:", current_period.strftime("%Y-%m-%d"))
    print("Previous period:", previous_period.strftime("%Y-%m-%d"))

    return current_period, previous_period
    

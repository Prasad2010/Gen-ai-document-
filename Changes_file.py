Create a new file:
functions/exposure_reporting_pipeline.py
This file will connect your existing functions. It will not contain the actual pivot calculations.
Use:




import pandas as pd

from functions.exposure_comparison import (
    identify_reporting_dates,
    create_quarterly_exposure_comparison
)

from functions.exposure_report_filter import (
    filter_stg_report,
    filter_ctm_report
)


def generate_exposure_reports(df: pd.DataFrame) -> dict:
    """
    Generate independent STG and CTM quarterly exposure reports.

    Both reports use the same raw input and dynamically
    identified reporting dates.
    """

    if df is None or df.empty:
        raise ValueError("Input dataframe is empty.")

    # 1. Identify latest and previous reporting dates
    current_date, previous_date = identify_reporting_dates(df)

    # 2. Generate STG report
    stg_report = create_quarterly_exposure_comparison(
        df,
        classification_col="Impairment type (final stage) - R"
    )

    # 3. Generate CTM report
    ctm_report = create_quarterly_exposure_comparison(
        df,
        classification_col="CTM (Owner) - R"
    )

    # 4. Apply independent filters
    stg_final = filter_stg_report(
        stg_report,
        current_date,
        previous_date
    )

    ctm_final = filter_ctm_report(
        ctm_report,
        current_date,
        previous_date
    )

    # 5. Return both reports
    return {
        "current_date": current_date,
        "previous_date": previous_date,
        "stg_report": stg_final,
        "ctm_report": ctm_final
    }













#Test the orchestration independently
Before changing main.py, test the new orchestration function in your Jupyter notebook.






from functions.exposure_reporting_pipeline import (
    generate_exposure_reports
)

# Use your existing raw dataframe
exposure_results = generate_exposure_reports(df)

# Extract results
stg_final = exposure_results["stg_report"]
ctm_final = exposure_results["ctm_report"]

print("Current quarter:",
      exposure_results["current_date"])

print("Previous quarter:",
      exposure_results["previous_date"])

print("STG rows:", len(stg_final))
print("CTM rows:", len(ctm_final))

display(stg_final)
display(ctm_final)







Integrate into main.py
This is where you connect the two reports to the existing UI.
First, add the import at the top of main.py:






from functions.exposure_reporting_pipeline import (
    generate_exposure_reports
)




Next, find where your application loads the raw DataFrame and where your STG and CTM tabs are defined.
Once the raw DataFrame is available, execute the new pipeline:










# Generate exposure reports independently
if df is not None and not df.empty:

    try:
        with st.spinner("Generating STG and CTM exposure reports..."):
            exposure_results = generate_exposure_reports(df)

        stg_final = exposure_results["stg_report"]
        ctm_final = exposure_results["ctm_report"]

    except Exception as e:
        st.error(f"Exposure reporting failed: {e}")
        exposure_results = None







Then put the respective DataFrames inside your existing tabs.
Inside your existing STG tab:








with stg_tab:

    st.subheader("STG Exposure Report")

    if exposure_results is not None:

        st.caption(
            f"Current Quarter: "
            f"{exposure_results['current_date'].date()}"
        )

        st.caption(
            f"Previous Quarter: "
            f"{exposure_results['previous_date'].date()}"
        )

        st.dataframe(
            stg_final,
            use_container_width=True,
            height=600
        )








Inside your existing CTM tab:








with ctm_tab:

    st.subheader("CTM Exposure Report")

    if exposure_results is not None:

        st.caption(
            f"Current Quarter: "
            f"{exposure_results['current_date'].date()}"
        )

        st.caption(
            f"Previous Quarter: "
            f"{exposure_results['previous_date'].date()}"
        )

        st.dataframe(
            ctm_final,
            use_container_width=True,
            height=600
)














# ==========================================
# EXPOSURE REPORTING MODULE
# ==========================================

exposure_results = generate_exposure_reports(df)

stg_report = exposure_results["stg_report"]
ctm_report = exposure_results["ctm_report"]

print("\n===== EXPOSURE REPORTING =====")

print("Current quarter:",
      exposure_results["current_date"])

print("Previous quarter:",
      exposure_results["previous_date"])

print("STG report rows:", len(stg_report))
print("CTM report rows:", len(ctm_report))

print("\nSTG REPORT")
print(stg_report.head())

print("\nCTM REPORT")
print(ctm_report.head())














print("\n===== DEBUG: FINAL RESULT KEYS =====")

for key, value in final_result.items():
    print(f"\nKey: {key}")
    print(f"Type: {type(value)}")

    if isinstance(value, dict):
        print("Nested keys:", list(value.keys()))



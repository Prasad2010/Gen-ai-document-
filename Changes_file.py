# Generate independent exposure reports
exposure_results = generate_exposure_reports(merged_df)

# Attach exposure reports to the main workflow result
final_result["exposure_reports"] = exposure_results






Load the exposure reports in app.py
After loading final_result from the pickle file, add:





exposure_results = final_result.get(
    "exposure_reports", {}
)

stg_report = exposure_results.get("stg_report")
ctm_report = exposure_results.get("ctm_report")







Then create the fourth tab:








with exposure_tab:

    st.subheader("Exposure Reporting")

    st.markdown("### STG Exposure Report")

    if stg_report is not None:
        st.dataframe(
            stg_report,
            use_container_width=True
        )
    else:
        st.info("STG report not available")

    st.divider()

    st.markdown("### CTM Exposure Report")

    if ctm_report is not None:
        st.dataframe(
            ctm_report,
            use_container_width=True
        )
    else:
        st.info("CTM report not available")














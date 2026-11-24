
def get_classification(reporting_date):

    classification_grouped = (
        working.groupby(
            index_cols + ["Closing Date"],
            dropna=False,
            sort=False
        )[classification_col]
        .agg(
            lambda x: ", ".join(
                sorted(
                    set(
                        str(v).strip()
                        for v in x.dropna()
                        if str(v).strip()
                    )
                )
            )
        )
    )

    # Convert empty classifications to NA
    classification_grouped = (
        classification_grouped.replace("", pd.NA)
    )

    # Select only the requested reporting date
    classification_grouped = (
        classification_grouped
        .xs(reporting_date, level="Closing Date")
    )

    return classification_grouped.reindex(output_index)











stg_report = create_quarterly_exposure_comparison(
    df,
    classification_col="Impairment type (final stage) - R"
)

display(stg_report)











ctm_report = create_quarterly_exposure_comparison(
    df,
    classification_col="CTM (Owner) - R"
)

display(ctm_report)

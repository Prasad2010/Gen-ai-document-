# Prepare STG report index for column lookup
stg_report = stg_report.copy()

if isinstance(stg_report.index, pd.MultiIndex):

    expected_index_names = [
        "Customer Nature",
        "Product",
        "RMPM ID",
        "Corporate Name"
    ]

    current_names = list(stg_report.index.names)

    if len(current_names) == 4:
        stg_report.index = stg_report.index.set_names([
            current_names[i] or expected_index_names[i]
            for i in range(4)
        ])

    stg_report = stg_report.reset_index()

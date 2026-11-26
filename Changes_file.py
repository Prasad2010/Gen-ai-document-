# Prepare STG report for exposure reporting

stg_exposure_df = stg_report.copy()

# Assign meaningful names to the four index levels
stg_exposure_df.index.names = [
    "Customer Nature",
    "Product",
    "RMPM ID",
    "Corporate Name"
]

# Convert MultiIndex into regular columns
stg_exposure_df = stg_exposure_df.reset_index()

# Remove blank corporate names
stg_exposure_df = stg_exposure_df[
    stg_exposure_df["Corporate Name"].notna()
]

st.write("STG Exposure Report Shape:", stg_exposure_df.shape)

st.dataframe(stg_exposure_df.head(10))

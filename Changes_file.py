# DEBUG: Inspect original raw data
raw_data = final_result.get("raw_data")

if isinstance(raw_data, pd.DataFrame):
    st.write("RAW DATA SHAPE:", raw_data.shape)
    st.write("RAW DATA COLUMNS:", list(raw_data.columns))
    st.dataframe(raw_data.head(5))
else:
    st.write("Raw data is not a DataFrame")

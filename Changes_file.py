st.write("===== STG REPORT DIAGNOSTICS =====")

st.write("STG shape:", stg_report.shape)
st.write("STG index:", stg_report.index[:5].tolist())
st.write("STG first 5 rows:")
st.dataframe(stg_report.head())

st.write("===== RAW DATA DIAGNOSTICS =====")

st.write("RAW index:", raw_data.index[:5].tolist())
st.write("RAW first 5 rows:")
st.dataframe(raw_data.head())

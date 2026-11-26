ctm_change = ctm_report.loc[
    ctm_mask
].copy()

# Convert CTM identification fields from index to columns
ctm_change = ctm_change.reset_index()






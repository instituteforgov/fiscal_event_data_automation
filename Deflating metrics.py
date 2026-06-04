
"""
Purpose
    Read in PSF aggregate public finance series from the OBR databank,
    perform structural validation, and rebase selected measures to
    constant prices using the GDP deflator.

Inputs
    - Excel: PSF_aggregates_databank_Mar_EFO.xlsx
        • Sheet: "Aggregates (£bn)"
        • Columns: public finance aggregates and GDP deflator

Outputs
    - pandas.DataFrame: df_measures
        • Public finance aggregates rebased to 2025–26 prices

Notes
    - Script includes defensive assertions to detect changes in file
      structure, year coverage, column names, and deflator integrity.
    - Rebasing uses the GDP deflator with base year 2025–26; values in
      the base year should be unchanged after rebasing.
    - Intended as a preprocessing step for downstream analysis rather
      than for direct publication.
"""



# %%
import pandas as pd
import os 

# %%
# Set constants

SOURCE_FILE = "C:/Users/"+os.getenv("USERNAME")+"/OneDrive - INSTITUTE FOR GOVERNMENT/Data - General/Public finances/OBR/EFOs/March 2026/PSF_aggregates_databank_Mar_EFO.xlsx"
SHEET_NAME = "Aggregates (£bn)"
SKIPROWS = [0, 1, 2]
SKIPFOOTER = 4

MINIMUM_EXPECTED_YEAR="1946-47"
MAXIMUM_EXPECTED_YEAR="2030-31" 
BASE_YEAR = "2025-26"


EXPECTED_MEASURE_COLS = [
    "Year",
    "Public sector current receipts",
    "Total managed expenditure",
    "Public sector current expenditure",
    "Public sector net investment",
    "Depreciation",
    "Public sector gross investment",
    "National account taxes",
]
DEFLATOR_COL_PREFIX = "GDP Deflator"

# %%
# DF 
# can't use drop function in read_excel
df = pd.read_excel(SOURCE_FILE, sheet_name=SHEET_NAME, skiprows=SKIPROWS, skipfooter=SKIPFOOTER, na_values=["-"])
# Drop column 0
# axis=1 means drop column, axis=0 means drop row. or axis="columns"
df = df.drop(df.columns[0], axis=1)
# for both columns and rows, first column/row is 0, second is 1, etc. so to drop first three rows, use index 0,1,2
df = df.rename(columns={"Unnamed: 1": "Year"})
assert "Year" in df.columns, "ERROR: 'Year' column not found after rename — check skiprows or source file structure"
# Drop rows that come between header and data,  which contain notes and source info rather than data
df=df.drop(df.index[0,1,2])

# %%
# ASSERTS
assert df["Year"].min() == MINIMUM_EXPECTED_YEAR, f"ERROR: Minimum year in data ({df['Year'].min()}) does not match expected ({MINIMUM_EXPECTED_YEAR}) — check skiprows or source file structure"
assert df["Year"].max() == MAXIMUM_EXPECTED_YEAR, f"ERROR: Maximum year in data ({df['Year'].max()}) does not match expected ({MAXIMUM_EXPECTED_YEAR}) — check skiprows or source file structure"

# %%
# SEPARATE DFs
df_measures = df[EXPECTED_MEASURE_COLS]
# Detect deflator column dynamically so the year in the title doesn't matter
deflator_cols = [col for col in df.columns if col.startswith(DEFLATOR_COL_PREFIX)]
assert len(deflator_cols) == 1, f"ERROR: Expected exactly one GDP Deflator column, found: {deflator_cols}"
DEFLATOR_COL = deflator_cols[0]
df_deflator = df[["Year", DEFLATOR_COL]]
# Check base year exists in deflator
assert (df_deflator["Year"] == BASE_YEAR).any(), f"ERROR: Base year '{BASE_YEAR}' not found in deflator data"
# Check no zero or NaN deflator values (would cause division errors)
assert not df_deflator[DEFLATOR_COL].isna().all(), "ERROR: GDP Deflator column is entirely NaN"
assert (df_deflator[DEFLATOR_COL] != 0).all(), "ERROR: GDP Deflator contains zero values — cannot divide"

deflator_base = df_deflator.loc[df_deflator["Year"] == BASE_YEAR, DEFLATOR_COL].values[0]

# CALCULATIONS
# Merge deflator into df_measures on Year to ensure correct row alignment
rows_before = len(df_measures)
df_measures_deflated = df_measures.merge(df_deflator, on="Year", how="left")
assert len(df_measures_deflated) == rows_before, f"ERROR: Merge changed row count ({rows_before} → {len(df_measures_deflated)}) — check for duplicate Year values"
# Warn about any years with missing deflator after merge
missing_deflator_years = df_measures_deflated.loc[df_measures_deflated[DEFLATOR_COL].isna(), "Year"].tolist()
if missing_deflator_years:
    print(f"WARNING: No deflator found for these years — those rows will be NaN after rebasing: {missing_deflator_years}")
# Rebase all measure columns (everything except Year and the deflator)
measure_cols = [col for col in df_measures_deflated.columns if col not in ["Year", DEFLATOR_COL]]
df_measures_deflated[measure_cols] = df_measures_deflated[measure_cols].multiply(
    deflator_base / df_measures_deflated[DEFLATOR_COL], axis=0
)
# Drop the deflator column now it's no longer needed
df_measures = df_measures_deflated.drop(columns=[DEFLATOR_COL])

# %%
# CHECKS
# Confirm rebasing applied correctly: 2025-26 values should be unchanged
check_row = df_measures_deflated.loc[df_measures_deflated["Year"] == BASE_YEAR, measure_cols]
assert check_row["Public sector current receipts"].values[0] == df_measures.loc[df_measures["Year"] == BASE_YEAR, "Public sector current receipts"].values[0], "ERROR: Rebase check failed for 'Public sector current receipts' in base year"


# %%
# PREVIEWS
check_row
# %%
df_measures_deflated
# %%
deflator_base
# %%
df.to_csv("output/cleaned_data.csv", index=False)
# %%

df_measures_deflated.to_csv("outputs/cleaned_data.csv", index=False)


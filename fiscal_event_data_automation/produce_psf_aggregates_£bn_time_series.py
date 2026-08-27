
"""
Purpose
    Read in PSF aggregate public finance series from the OBR databank,
    perform structural validation, and rebase selected measures to
    constant prices using the GDP deflator.

Inputs
    - Excel: PSF_aggregates_databank_Mar_EFO.xlsx
        • Sheet: "Aggregates (£bn)"
        • Columns: "Public sector net investment", "Current budget deficit", and "GDP Deflator (2024-25=100)"

Outputs
    - pandas.DataFrame: df_measures_deflated
        • Public finance aggregates rebased to 2025–26 prices

Notes
    - Script includes defensive assertions to detect changes in file
      structure, year coverage, column names, and deflator integrity.
    - Rebasing uses the GDP deflator with base year 2025–26; values in
      the base year should be unchanged after rebasing.
    - Intended as a preprocessing step for further analysis rather
      than for direct publication.
"""
# %%
import pandas as pd
import os
import fiscal_event_data_automation.utils as utils
from IPython.display import display


# %%
# Set constants

SOURCE_FILE = "C:/Users/"+os.getenv("USERNAME")+"/OneDrive - INSTITUTE FOR GOVERNMENT/Data - General/Public finances/OBR/EFOs/March 2026/PSF_aggregates_databank_Mar_EFO.xlsx"
SHEET_NAME = "Aggregates (£bn)"
SKIPROWS = [0, 1, 2]
SKIPFOOTER = 4

MINIMUM_EXPECTED_YEAR = "1946-47"
MAXIMUM_EXPECTED_YEAR = "2030-31"
BASE_YEAR = "2025-26"

MEASURE_OUTPUTS = [
    {
        "Measure name": "Public sector net investment",
        "Output file name": "public_sector_net_investment_time_series.csv"
    },
    {
        "Measure name": "Current budget deficit",
        "Output file name": "current_budget_deficit_time_series.csv"
    }
]

DEFLATOR_COL_PREFIX = "GDP Deflator"

# %%
# DF
df = pd.read_excel(SOURCE_FILE, sheet_name=SHEET_NAME, skiprows=SKIPROWS, skipfooter=SKIPFOOTER, na_values=["-"])
# Drop column 0
# axis=1 means drop column, axis=0 means drop row.
df = df.drop(df.columns[0], axis=1)
# for both columns and rows, first column/row is 0, second is 1, etc. so to drop first three rows, use index 0,1,2
df = df.rename(columns={"Unnamed: 1": "Year"})
# Drop rows that come between header and data,  which contain notes and source info rather than data
df = df.drop(df.index[0, 1, 2])

# %%
# ASSERTS
assert "Year" in df.columns, "ERROR: 'Year' column not found after rename — check skiprows or source file structure"
assert df["Year"].min() == MINIMUM_EXPECTED_YEAR, f"ERROR: Minimum year in data ({df['Year'].min()}) does not match expected ({MINIMUM_EXPECTED_YEAR}) — check skiprows or source file structure"
assert df["Year"].max() == MAXIMUM_EXPECTED_YEAR, f"ERROR: Maximum year in data ({df['Year'].max()}) does not match expected ({MAXIMUM_EXPECTED_YEAR}) — check skiprows or source file structure"

# %%
# SEPARATE DFs
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
# Check that all columns in EXPECTED_MEASURE_COLS are present in df_measures
expected_measure_names = set(m["Measure name"] for m in MEASURE_OUTPUTS)
assert expected_measure_names.issubset(df.columns), \
    f"ERROR: Missing expected columns: {expected_measure_names - set(df.columns)}"


deflator_base = df_deflator.loc[df_deflator["Year"] == BASE_YEAR, DEFLATOR_COL].values[0]
# %%
# CALCULATIONS
# Merge deflator into df_measures on Year to ensure correct row alignment
for measure in MEASURE_OUTPUTS:
    df_measures = df[["Year", measure["Measure name"]]]
    df_measures_deflated, measure_cols = utils.deflate_measures(df_measures, df_deflator, DEFLATOR_COL, deflator_base)
    print(df_measures_deflated.head())

    # Drop the deflator column now it's no longer needed
    df_measures_deflated = df_measures_deflated.drop(columns=[DEFLATOR_COL])
    # CHECKS
    # Confirm rebasing applied correctly: 2025-26 values should be unchanged
    check_row = df_measures_deflated.loc[df_measures_deflated["Year"] == BASE_YEAR, measure_cols]
    assert check_row[measure["Measure name"]].values[0] == df_measures.loc[df_measures["Year"] == BASE_YEAR, measure["Measure name"]].values[0], f"ERROR: Rebase check failed for {measure["Measure name"]} in base year"
    # PREVIEWS
    display(check_row)

    display(df_measures_deflated)

    display(deflator_base)

    df_measures_deflated.pipe(utils.drop_empty_rows).pipe(utils.replace_hyphen_with_slash).to_csv(f"outputs/{measure["Output file name"]}", index=False)
# %%

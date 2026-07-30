# %%
# CALCULATIONS
# Merge deflator into df_measures on Year to ensure correct row alignment
def deflate_measures(df_measures, df_deflator, DEFLATOR_COL, deflator_base):
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
    return df_measures_deflated, measure_cols


# %%
def replace_hyphen_with_slash(df):
    """Replace hyphens with forward slashes in the Year column of a DataFrame."""
    df = df.copy()
    df["Year"] = df["Year"].str.replace("-", "/", regex=False)
    return df


def drop_empty_rows(df):
    """Drop rows where all columns except Year contain NaN (e.g. pre-1955/56 rows with no data)."""
    measure_cols = [col for col in df.columns if col != "Year"]
    return df.dropna(subset=measure_cols, how="all").reset_index(drop=True)

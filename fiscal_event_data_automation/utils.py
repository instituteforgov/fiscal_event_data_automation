import pandas as pd


def rebase_to_constant_prices(df, measure_cols, deflator_col_prefix, base_year):
    """
    Rebase selected measures to constant prices using the GDP deflator.

    Parameters
    ----------
    df : pd.DataFrame
        Full dataframe containing measure columns and a GDP deflator column.
    measure_cols : list of str
        Columns to include in the output (must include 'Year').
    deflator_col_prefix : str
        Prefix used to identify the GDP deflator column dynamically.
    base_year : str
        The year to rebase to (e.g. '2025-26').

    Returns
    -------
    pd.DataFrame
        Measure columns rebased to constant prices, with the deflator column dropped.
    """
    # Check all expected measure columns are present
    assert set(measure_cols).issubset(df.columns), \
        f"ERROR: Missing expected columns: {set(measure_cols) - set(df.columns)}"

    df_measures = df[measure_cols].copy()

    # Detect deflator column dynamically so the year in the title doesn't matter
    deflator_cols = [col for col in df.columns if col.startswith(deflator_col_prefix)]
    assert len(deflator_cols) == 1, f"ERROR: Expected exactly one GDP Deflator column, found: {deflator_cols}"
    deflator_col = deflator_cols[0]

    df_deflator = df[["Year", deflator_col]]
    assert (df_deflator["Year"] == base_year).any(), f"ERROR: Base year '{base_year}' not found in deflator data"
    assert not df_deflator[deflator_col].isna().all(), "ERROR: GDP Deflator column is entirely NaN"
    assert (df_deflator[deflator_col] != 0).all(), "ERROR: GDP Deflator contains zero values — cannot divide"

    deflator_base = df_deflator.loc[df_deflator["Year"] == base_year, deflator_col].values[0]

    rows_before = len(df_measures)
    df_measures_deflated = df_measures.merge(df_deflator, on="Year", how="left")
    assert len(df_measures_deflated) == rows_before, (
        f"ERROR: Merge changed row count ({rows_before} → {len(df_measures_deflated)}) "
        "— check for duplicate Year values"
    )

    missing_deflator_years = df_measures_deflated.loc[df_measures_deflated[deflator_col].isna(), "Year"].tolist()
    if missing_deflator_years:
        print(f"WARNING: No deflator found for these years — those rows will be NaN after rebasing: {missing_deflator_years}")

    numeric_cols = [col for col in df_measures_deflated.columns if col not in ["Year", deflator_col]]
    df_measures_deflated[numeric_cols] = df_measures_deflated[numeric_cols].multiply(
        deflator_base / df_measures_deflated[deflator_col], axis=0
    )

    # Confirm rebasing: base year values should be numerically unchanged (multiply by 1)
    base_row_rebased = df_measures_deflated.loc[df_measures_deflated["Year"] == base_year, numeric_cols]
    base_row_original = df_measures.loc[df_measures["Year"] == base_year, numeric_cols]
    assert (base_row_rebased.values == base_row_original.values).all(), (
        f"ERROR: Rebase check failed — base year '{base_year}' values changed after rebasing"
    )

    return df_measures_deflated.drop(columns=[deflator_col])

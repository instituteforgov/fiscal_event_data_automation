# Fiscal event data automation in Python


## Description
This repository automates the extraction and analysis of data from OBR Economic and Fiscal Outlook (EFO) publications following fiscal events. The workflow uses Python to process data and export outputs for further analysis.

## Workflow
1. Extract and clean data from source files (e.g. EFO datasets)
2. Process and transform data using Python (pandas)
3. Export cleaned outputs to CSV
4. Analyse outputs in Excel (including using Microsoft Copilot)



## Related repositories

n/a

## Project structure

├── scripts/
│   ├── .vscode/
│       ├── settings.json
│   ├── fiscal_event_data_automation/
│       ├── __pycache__/
│            ├── utils.cpython-314.pyc
│       ├── produce_psf_aggregates_£bn_time_series.py
│       ├── utils.py
├── outputs/
│   ├── cleaned_data.csv
│   ├── copilot output.xlsx
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md


## Installation [optional - where applicable]

1. Clone the repository.
2. Install the required Python packages: 
> import pandas as pd
> import os
> import fiscal_event_data_automation.utils as utils
> from IPython.display import display

## Scripts

| produce_psf_aggregates_£bn_time_series.py | Main script for processing fiscal event data and generating Public Sector Finances (PSF) aggregate outputs. Produces cleaned datasets and analysis outputs.
| utils.py | Incorporates formula for deflating fiscal data into a reusable function.

## Contributing [optional - repos likely to have multiple contributors]

When making changes to this project:

Verify that the source Excel file structure has not changed, including:

Worksheet name (Aggregates (£bn))
Header row locations
Year coverage
Public finance measure names
GDP deflator column naming convention

Maintain the existing validation checks and assertions wherever possible. These are designed to detect structural changes in the OBR databank before calculations are performed.

Test any changes to the deflation methodology using the base year (2025-26) and confirm that values in the base year remain unchanged after rebasing.

Where new public finance measures are added, update the MEASURE_OUTPUTS configuration and ensure the resulting outputs are validated before publication or further analysis.

Update this documentation if any changes are made to:

Input data sources
Expected file structure
Output formats
Deflation methodology / base year 

This script is intended as a preprocessing tool for analytical work. Any methodological changes should be reviewed carefully to ensure consistency with OBR source data and existing outputs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


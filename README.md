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
├── fiscal_event_data_automation
├── outputs/
│   ├── cleaned_data.csv
├── .gitignore
├── pre-commit-config.yaml
├── Deflating metrics.py
├── LICENSE
├── README.md


## Installation [optional - where applicable]

Where the repo contains a `requirements.txt` file, include the commands to install dependencies using it.

E.g.

> ```bash
> pip install -r requirements.txt
> ```

## Scripts

| File | Description |
| ---- | ----------- |
| `deflating_metrics.py` | Main script. Reads the input Excel file, cleans the data (including setting constants, trimming years, and reformatting dates), and outputs the cleaned dataset. |
| `cleaned_data.csv` | Output file produced by the script, containing the final cleaned and formatted data ready for analysis. |
| `PSF_aggregates_databank_Mar_EFO.xlsx` | Original raw dataset used as the input to the script. |

## Contributing [optional - repos likely to have multiple contributors]

Add a section describing any important information for contributors.

E.g.

> This project uses `pre-commit` hooks to ensure code quality. To set up:
>
> 1. Install `pre-commit` on your system if you don't already have it:
>
    > ```bash
    > pip install pre-commit
    > ```
>
> 1. Set up `pre-commit` in your copy of this project. In the project directory, run:
    > ```bash
    > pre-commit install
    > ```
>
> Rules that are applied can be found in [`.pre-commit-config.yaml`](.pre-commit-config.yaml).
>
> The hooks run automatically on commit, or manually with `pre-commit run --all-files`.

## License

> This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


# Fiscal event data automation in Python

This repository automates the extraction and analysis of data from OBR Economic and Fiscal Outlook (EFO) publications following fiscal events. The workflow uses Python to process data and export outputs for further analysis.

## Process
<img width="940" height="543" alt="image" src="https://github.com/user-attachments/assets/e44dedc8-5a92-4ab6-8acd-c23936753f48" />

The content of this repository covers just the steps performed in Python.

## Related repositories

None

## Project structure

```
├── scripts/
│   └── fiscal_event_data_automation/
│       ├── produce_psf_aggregates_£bn_time_series.py
│       └── utils.py
├── outputs/
│   └── <various>.csv
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
└── requirements.txt
```


## Installation 

```bash
pip install -r requirements.txt
```

## Scripts

| File | Description |
| ---- | ----------- |
| `produce_psf_aggregates_£bn_time_series.py` | Main script for processing fiscal event data and generating Public Sector Finances (PSF) aggregate outputs. Produces cleaned datasets and analysis outputs.
| `utils.py` | Utility functions call by other scripts.

## Contributing

This project uses `pre-commit` hooks to ensure code quality. To set up:

1. Install `pre-commit` on your system if you don't already have it:

    ```bash
    pip install pre-commit
    ```

1. Set up `pre-commit` in your copy of this project. In the project directory, run:
    ```bash
    pre-commit install
    ```

Rules that are applied can be found in [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

The hooks run automatically on commit, or manually with `pre-commit run --all-files`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


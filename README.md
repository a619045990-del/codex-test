# Burkholderia phage–host prediction

A small, reproducible starting point for organizing analyses of Burkholderia phage–host interaction data. The repository currently provides project structure, metadata templates, and a generic CSV input-audit command. It does **not** contain project datasets, trained models, model predictions, or experimental conclusions.

## Repository layout

```text
.
├── configs/                 # Analysis configuration examples (to be added as needed)
├── data/
│   ├── raw/                 # Original inputs; keep private or untracked
│   ├── processed/           # Derived tables prepared for analysis
│   └── data_dictionary_template.csv
├── outputs/                 # Generated results (ignored by Git, except .gitkeep)
├── scripts/
│   └── run_analysis.py      # Generic CSV input audit entry point
├── environment.yml          # Conda environment
├── requirements.txt         # pip dependencies
└── README.md
```

## Environment

Python 3.11 is the supported baseline. Choose either Conda or pip:

```bash
conda env create -f environment.yml
conda activate bp-phage-host
```

or:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Reproducible first run

1. Place a CSV table you are authorized to use under `data/processed/` (or provide another path).
2. Run the input audit:

```bash
python scripts/run_analysis.py data/processed/<your_table>.csv --outdir outputs
```

The command writes `outputs/input_audit.json` with the input file checksum, table dimensions, column names, and missing-value counts. It does not fit a model or interpret biological outcomes. The checksum helps identify the exact input used.

To check the command-line options:

```bash
python scripts/run_analysis.py --help
```

## Data and provenance

- Do not commit identifiable, restricted, or unpublished data unless repository access and data-sharing permissions have been reviewed.
- Keep raw data unchanged. Record source, access date, processing steps, and file checksums when adding datasets.
- Use the data dictionary template at `data/data_dictionary_template.csv`; replace example placeholders with verified definitions and units.
- Keep generated files in `outputs/`. The directory is ignored by Git so large or sensitive results are not committed by accident.
- Record software versions and the exact command used for each substantive analysis.

## Scope and next steps

This is a project scaffold, not a completed prediction pipeline. Before adding model code, document the response definition, host and phage identifiers, feature provenance, split strategy, and evaluation metrics. No values or study findings are assumed here.

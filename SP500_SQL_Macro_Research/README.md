# S&P 500 Sector Returns & Macroeconomic Conditions — SQL Research Database

**DATA 521 — Database Development for Public Health | Emory University**  
**Original course research by Conglin Bao (Franklin) and Zirui Chen**

This is a relational-database research project combining **actual S&P 500 stock prices**, sector classifications and daily-aligned macroeconomic information. It demonstrates SQL table design, imports, `JOIN`, `GROUP BY`, data-integrity checks and descriptive financial research. The original implementation used **MySQL / DBeaver**; this portfolio also includes a streamlined **SQLite** workflow for easy inspection.

## Start here

- **[Step-by-step SQL workflow](code/README.md)** — Step 1 create tables, Step 2 calculate sector returns, Step 3 analyze results
- **[One-command runner](code/run_all.py)** — `python3 SP500_SQL_Macro_Research/code/run_all.py`
- **[Real historical 2017 Q1 dataset](data/README.md)** — 1,240 ticker-day prices, 20 real companies and 64 macro dates; **not synthetic data**
- **[Research outputs & future PPT location](results/README.md)** — downloadable CSV results; presentation can be uploaded there
- **[Original team MySQL source](code/DATA521_Original_MySQL.sql)** — preserve the course implementation and coauthor attribution

## Run

Clone/download the repository and run from its **root**:

```bash
python3 SP500_SQL_Macro_Research/code/run_all.py
```

No Docker, MySQL server or Python package installation needed. The command rebuilds the SQLite database and CSV results under `results/`.

## What this project demonstrates

- **Data modeling:** five relational tables (three source, two derived), indexes and uniqueness constraints
- **Financial SQL:** intraday returns `(close - open) / open`, sector/date joins, equal-weighted sector-level summaries
- **Data work:** real price and macro data alignment, completeness checks, source provenance
- **Results:** sector statistics, volatility-regime summary, result CSVs
- **Reproducibility:** all three steps can be executed with the included historical sample; the full coursework history can be checked separately using the original files

**Important distinctions:** The included sample is an actual subset of historical records, **not** the complete 2013–2018 study dataset. The complete-data validation matched 13,849/13,849 sector-days, but that full dataset is not redistributed here. Retrospective metadata and day-aligned macro series may create survivorship and release-timing limitations. This project is descriptive, not a causal claim or investment strategy. See [the data notes](data/README.md) for sourcing, VIX copyright and reuse restrictions.

# Data provenance and licensing

| Input | Course source | Availability / notice |
|---|---|---|
| `all_stocks_5yr.csv` | [Kaggle — camnugent/sandp500](https://www.kaggle.com/datasets/camnugent/sandp500) | Kaggle lists the dataset as CC0. Download for historical replication. |
| `sp500_companies.csv` | Wikipedia S&P 500 constituents snapshot | Snapshot can differ from the historical constituents used by the price data. |
| `macro_indicators.csv` | FRED FEDFUNDS, CPIAUCSL, VIXCLS | Contains FRED-served series including third-party VIX. Do not presume redistribution rights. |
| `sector_summary_202604301759.csv` | DATA 521 course export | Derived output reference, used locally by `--reference`; not redistributed. |

The repository includes only **synthetic, explicitly labeled demo CSVs**. Recreate your real input files using properly authorized sources, then store them in `data/raw/` (gitignored) and run the full-data command.

Attribution: DATA 521 coursework by Conglin Bao (Franklin) and Zirui Chen. Database scripts in `original_coursework/` reproduce the submitted work; the stdlib/SQLite runner, tests, and documentation are an additional portfolio packaging layer.

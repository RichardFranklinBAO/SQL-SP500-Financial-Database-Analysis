Place locally obtained source files here (never committed):

- all_stocks_5yr.csv — Kaggle `camnugent/sandp500` (CC0)
- sp500_companies.csv — recorded company metadata snapshot
- macro_indicators.csv — FRED-derived classroom data; redistribution restrictions may apply, especially VIX

Run: `python3 src/build_database.py --data-dir data/raw --db outputs/full.sqlite`
These files are ignored by Git; a synthetic dataset in `data/demo/` is bundled for an offline smoke test.

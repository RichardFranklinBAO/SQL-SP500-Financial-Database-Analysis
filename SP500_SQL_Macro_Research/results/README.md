# Results, presentation and validation

This folder contains **actual historical sample outputs**, produced by running `code/run_all.py` on the included 2017 Q1 observations. These are **not synthetic demos** and are **not** the full-sample course results.

- [`sector_daily_summary.csv`](sector_daily_summary.csv) — sector-by-day intraday return and macro aggregates.
- [`sector_overview.csv`](sector_overview.csv) — descriptive averages for each sampled sector.
- [`volatility_regimes.csv`](volatility_regimes.csv) — sector returns grouped by reported VIX conditions.
- [`data_quality.csv`](data_quality.csv) — source and derived database row counts.
- `SP500_Research_Database.sqlite` is generated locally when the script runs and is gitignored to keep GitHub lightweight.

## Original DATA 521 presentation — optional addition

The original jointly prepared research presentation can be added here as **`DATA521_SQL_Research_Presentation.pdf`** or **`DATA521_SQL_Research_Presentation.pptx`**. After it is uploaded, we can link it prominently from the root README. Do not claim the file is present before it has been uploaded.

## Independent full-history verification

During portfolio preparation, using the complete separately supplied CSVs:

- Historical stock rows: **619,040**
- Valid stock return rows: **619,029**
- Sector-day aggregate rows: **13,849**
- Exact row-key/metric verification: **13,849 of 13,849** matched the original course export within `1e-9` numerical tolerance.

The full history and the original reference export are not bundled in this small public-facing portfolio. To reproduce that check locally, pass your full original CSV folder and optional original `sector_summary_202604301759.csv` to `code/run_all.py`.

# Research design & interpretation

**Question.** How do same-day S&P 500 sector stock returns vary with contemporaneous market volatility and macroeconomic indicators in the 2013–2018 course dataset?

## Original measure

The supplied DATA 521 project computes **intraday** return as `(close - open) / open`, not overnight or close-to-close return. The source SQL forms a ticker/day table and then computes equal-weighted sector/day means with `AVG` after joining company metadata and macroeconomic indicators on ticker and date.

The modernized SQLite implementation deliberately preserves that definition and `INNER JOIN` logic, so its full-data sector summary matches the course-exported `sector_summary_202604301759.csv` within numerical tolerance.

## What the tables mean

- `companies`, `stock_prices`, `macro_indicators`: input tables.
- `sp500_returns`: one observation per ticker and trading date with valid positive opening price.
- `sector_summary`: one observation per available sector and trading date, averaging stock intraday returns and matched macro values.

## Cautions

1. **No causal interpretation.** Same-day market measures are correlated; this is not identification of interest-rate or volatility effects.
2. **Historical composition / survivorship bias.** The company metadata snapshot may not reflect actual 2013–2018 index constituents or sector classifications.
3. **Not point-in-time macro data.** Monthly CPI and policy rates were forward-filled in the course data for alignment. They should not be treated as information available at each trading-day close for forecasting or backtesting.
4. **Source coverage.** The original stock CSV contains 505 tickers, company metadata 503 tickers; inner joins exclude unmatched symbols. Missing opening prices are omitted from return calculations.
5. **Licensing.** The repository ships synthetic demo data only. For full reproduction, the user supplies licensed source CSVs locally. FRED / VIX permissions must be checked before sharing.

The repository is a **database design and reproducibility demonstration**, not a validated trading strategy or causal financial study.

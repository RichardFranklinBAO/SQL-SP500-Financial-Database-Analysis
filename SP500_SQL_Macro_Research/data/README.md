# Real historical research inputs (NOT synthetic demos)

These three included CSV files are a **real observed 2017 Q1 subset**, selected from the historical sources used in our DATA 521 coursework. They let visitors run the entire workflow immediately, without downloading anything else.

| Filename | Contents | Count |
| --- | --- | ---: |
| `stock_prices.csv` | Real daily open/high/low/close/volume for **20 actual tickers**, 2017-01-03 through 2017-03-31 | 1,240 ticker-days |
| `companies.csv` | The 20 ticker-to-sector/company labels used in the supplied constituent snapshot | 20 companies |
| `macro_indicators.csv` | Course-provided contemporaneous daily observations of the federal funds rate, CPI and VIX for the covered quarter | 64 dates |

**Sources and use considerations:**

- Stock OHLCV: [Cam Nugent's S&P 500 Kaggle dataset](https://www.kaggle.com/datasets/camnugent/sandp500), described as CC0. The sample contains historical observed prices, not synthetic stock prices.
- Company labels: S&P 500 constituent snapshot derived from Wikipedia, subject to Wikipedia content attribution/licensing. This is a later snapshot, **not point-in-time membership**.
- Macroeconomic series: U.S. Federal Reserve/FRED data including `FEDFUNDS`, `CPIAUCSL` and Cboe VIX (`VIXCLS`). **VIXCLS is Cboe-copyrighted** and is labeled on FRED as requiring citation. Source: [VIXCLS](https://fred.stlouisfed.org/series/VIXCLS); [FRED legal terms](https://fred.stlouisfed.org/legal/). The macro observations here were provided from the original coursework files. Before wide redistribution, re-check Cboe/FRED permissions and applicable terms. Do not imply the files are universally unrestricted.

**Important analytical limits:** This is a 2017 **quarterly sample**, not the 619,040-row complete history. The original 2013–2018 full-course dataset can be supplied **locally** with `--data-dir`; the research estimates will then differ from the sample results. The CPI and federal funds observations had already been day-aligned in the course dataset and may incorporate future information relative to original release times. Same-day correlations are not causal effects or trading signals.

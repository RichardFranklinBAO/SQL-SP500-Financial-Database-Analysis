# Three-step SQL research workflow

Run everything from the repository root using **Python 3**:

```bash
python3 SP500_SQL_Macro_Research/code/run_all.py
```

This command uses **real historical 2017 Q1 observations**, not simulated data, and requires no third-party Python packages or SQL server.

| Step | File | Purpose |
| --- | --- | --- |
| **Step 1: Create tables** | [`Step_1_Create_Tables.sql`](Step_1_Create_Tables.sql) | Define five relational tables, primary keys and indexes. The runner then imports the three CSV sources. |
| **Step 2: Transform & JOIN** | [`Step_2_Transform_Data.sql`](Step_2_Transform_Data.sql) | Compute each ticker-day intraday return, link sector and macroeconomic data and aggregate by sector-day. |
| **Step 3: Analyze & export** | [`Step_3_Analyze_Results.sql`](Step_3_Analyze_Results.sql) | Compare sectors, group returns by VIX regime and check table sizes. The runner writes reports to `results/`. |

**[run_all.py](run_all.py)** runs Step 1–3 in order and exports actual historical sample results.  
**[DATA521_Original_MySQL.sql](DATA521_Original_MySQL.sql)** retains the original coauthored MySQL course implementation; the other SQL scripts are a later portable SQLite presentation.

For the full 2013–2018 dataset, put your three original CSV files in a separate local folder and run:

```bash
python3 SP500_SQL_Macro_Research/code/run_all.py --data-dir /path/to/full_original_csvs
```

The input reader supports either the curated filenames or the original course filenames. Full historical results require your original macroeconomic file and an authorized use of its VIX data.

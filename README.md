# S&P 500 × Macroeconomics | SQL Research Portfolio

**DATA 521 (Emory University)** · Original collaborative course project by **Conglin Bao (Franklin) and Zirui Chen**.

A relational-database research project linking historical S&P 500 stock prices, sector classifications and macroeconomic indicators to investigate **sector-level intraday returns**. The original course project used **MySQL / DBeaver**; this portfolio also includes a portable **SQLite implementation** of the research pipeline.

**[View the DATA 521 Research Presentation (PDF)](SP500_SQL_Macro_Research/results/DATA521_SQL_Research_Presentation.pdf)** — main research presentation for reviewers.  
[Download the editable PowerPoint (PPTX)](SP500_SQL_Macro_Research/results/DATA521_SQL_Research_Presentation.pptx) · [Open the complete project](SP500_SQL_Macro_Research/README.md)

## SQL Skills Demonstrated

The three SQL scripts show the following **specific data operations**, from relational database construction to analysis and validation:

| Step | SQL techniques | What the code does |
| --- | --- | --- |
| **1. Relational Database Design** — [Create Tables](SP500_SQL_Macro_Research/code/Step_1_Create_Tables.sql) | `CREATE TABLE`, `PRIMARY KEY`, composite keys, `NOT NULL`, `CREATE INDEX` | Defines **five relational tables**: company metadata, macroeconomic indicators, stock prices, daily stock returns and sector-level summaries. Uses ticker/date keys, data constraints and indexes to support consistent joins and aggregation. |
| **2. Data Cleaning, Transformation & JOINs** — [Transform Data](SP500_SQL_Macro_Research/code/Step_2_Transform_Data.sql) | `INSERT INTO ... SELECT`, `WHERE`, `INNER JOIN`, `GROUP BY`, `AVG`, `COUNT(DISTINCT)` | Excludes observations with invalid/missing opening or closing prices; computes ticker-day **intraday return = (close − open) / open**; joins returns to companies **by ticker** and macro observations **by date**; aggregates average returns, VIX, federal funds rates and distinct ticker counts for each **sector × date**. |
| **3. Financial Data Analysis & Quality Checks** — [Analyze Results](SP500_SQL_Macro_Research/code/Step_3_Analyze_Results.sql) | `CASE WHEN`, `ROUND`, `ORDER BY`, `GROUP BY`, `COUNT(*)`, `UNION ALL` | Ranks sectors by average intraday return; groups sector-day observations into **VIX ≥ 20**, **VIX < 20** or missing-VIX categories; and compares row counts across source and derived tables to inspect data coverage. |

**Implementation detail:** SQL defines the tables, transformations, joins and analytical queries. The accompanying [Python runner](SP500_SQL_Macro_Research/code/run_all.py) imports the input CSVs, executes the three SQL files in order and exports query results; CSV ingestion/export are **not** claimed as standalone SQL commands. [The original collaborative MySQL source](SP500_SQL_Macro_Research/code/DATA521_Original_MySQL.sql) is preserved separately from the later SQLite portfolio implementation.

## Research Data & Outputs

- **[Historical input data](SP500_SQL_Macro_Research/data/README.md)** — a real (not simulated) 2017 Q1 sample of stock prices, company metadata and aligned macro indicators.
- **[Sector-by-day research results](SP500_SQL_Macro_Research/results/sector_daily_summary.csv)** — calculated daily sector returns with VIX and federal funds rate summaries.
- **[Sector overview](SP500_SQL_Macro_Research/results/sector_overview.csv)** · **[VIX regime comparisons](SP500_SQL_Macro_Research/results/volatility_regimes.csv)** · **[Data quality counts](SP500_SQL_Macro_Research/results/data_quality.csv)**.
- **[Full workflow instructions](SP500_SQL_Macro_Research/code/README.md)** — Step 1 → Step 2 → Step 3.

## Reproduce the Workflow

From the repository root, run:

```bash
python3 SP500_SQL_Macro_Research/code/run_all.py
```

The included **historical 2017 Q1 sample** runs using Python 3's standard-library SQLite support, without Docker or a separate SQL server. The pipeline builds a local database and exports the analysis tables under `results/`.

## Scope, Provenance & Limitations

**Data coverage and reproducibility.** This repository provides a **reproducible subset of the original historical dataset** (real observations from 2017 Q1) so readers can run and inspect the complete SQL workflow without obtaining the full data. The complete 2013–2018 historical dataset was used separately for independent validation: the pipeline reproduced **13,849 / 13,849 sector-day aggregates** from the original coursework export within numerical tolerance. **Neither the full historical dataset nor the original reference export is redistributed in this repository.** Consequently, the included sample demonstrates the workflow and its sample-specific results; it does not by itself reproduce the full-period analysis.

This is **descriptive** financial-data analysis, not a causal study, point-in-time trading backtest or claim of investment returns. Snapshot sector classifications and the timing of macroeconomic data availability limit historical interpretation. See [data notes and licensing cautions](SP500_SQL_Macro_Research/data/README.md), including restrictions that may apply to VIX data.

**Academic attribution:** Original DATA 521 team project by **Conglin Bao (Franklin) and Zirui Chen**. The streamlined SQLite runner and repository documentation are later portfolio additions.

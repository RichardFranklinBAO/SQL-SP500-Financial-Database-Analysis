#!/usr/bin/env python3
"""Run Step 1 -> Step 2 -> Step 3 using Python stdlib + SQLite; no Docker/MySQL.

Input: project/data/{stock_prices.csv,companies.csv,macro_indicators.csv}
Alternative full-source filenames from original course also supported.
Output: project/results/*.csv plus local SQLite database (ignored by Git).
"""
import argparse
import csv
import math
import sqlite3
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CODE = PROJECT / "code"
REQUIRED = ("stock_prices", "companies", "macro_indicators")


def read_csv(directory, name):
    options = {
        "stock_prices": ("stock_prices.csv", "all_stocks_5yr.csv"),
        "companies": ("companies.csv", "sp500_companies.csv"),
        "macro_indicators": ("macro_indicators.csv",),
    }
    path = next((directory / n for n in options[name] if (directory / n).is_file()), None)
    if path is None:
        raise FileNotFoundError(f"Missing {name} in {directory}; expected one of {options[name]}")
    with path.open(newline="", encoding="utf-8-sig") as file:
        yield from csv.DictReader(file)


def number(x):
    return float(x) if x is not None and x.strip() else None


def chunks(rows, size=10000):
    block = []
    for row in rows:
        block.append(row)
        if len(block) == size:
            yield block
            block = []
    if block:
        yield block


def load_all(connection, directory):
    companies = ((r["Symbol"], r["Security"], r["GICS Sector"], r.get("GICS Sub-Industry"))
                 for r in read_csv(directory, "companies"))
    macros = ((r["date"], number(r.get("fed_funds_rate")),
               number(r.get("cpi")), number(r.get("vix")))
              for r in read_csv(directory, "macro_indicators"))
    prices = ((r["Name"], r["date"],number(r["open"]),number(r["close"]),
               number(r["high"]),number(r["low"]),int(r["volume"]) if r.get("volume") else None)
              for r in read_csv(directory, "stock_prices"))
    for table, values in (("companies",companies),("macro_indicators",macros),("stock_prices",prices)):
        for block in chunks(values):
            qs = ",".join("?" for _ in block[0])
            connection.executemany(f"INSERT INTO {table} VALUES ({qs})", block)

def save_csv(path, cursor):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        out = csv.writer(f)
        out.writerow([x[0] for x in cursor.description])
        out.writerows(cursor)

def check_reference(connection, path):
    computed = {(d,s):(r,v,f,n) for d,s,r,v,f,n in connection.execute(
        "SELECT summary_date,sector,avg_return,avg_vix,avg_fed_rate,ticker_count FROM sector_summary")}
    expected_count=0
    with path.open(newline="",encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            k=(row["summary_date"],row["sector"])
            if k not in computed: raise AssertionError(f"Missing historical row {k}")
            for actual,col in zip(computed[k],("avg_return","avg_vix","avg_fed_rate","ticker_count")):
                expected=float(row[col])
                if not math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-9):
                    raise AssertionError(f"Mismatch on {k} column {col}: {actual} vs {expected}")
            expected_count+=1
    assert expected_count==len(computed),(expected_count,len(computed))
    print(f"Historical reference: PASS ({expected_count:,} / {len(computed):,} sector-days matched)")

def run(data_dir,results_dir,reference=None):
    data_dir=Path(data_dir); results_dir=Path(results_dir)
    results_dir.mkdir(parents=True,exist_ok=True)
    db=results_dir/"SP500_Research_Database.sqlite"
    if db.exists(): db.unlink()
    try:
        with sqlite3.connect(db) as con:
            print("STEP 1/3: Create tables and load source CSVs")
            con.executescript((CODE/"Step_1_Create_Tables.sql").read_text())
            load_all(con,data_dir)
            print("STEP 2/3: Calculate stock returns and JOIN sector/macroeconomic information")
            con.executescript((CODE/"Step_2_Transform_Data.sql").read_text())
            assert con.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
            print("STEP 3/3: Run queries and export research outputs")
            save_csv(results_dir/"sector_daily_summary.csv",con.execute(
                "SELECT summary_date,sector,avg_return,avg_vix,avg_fed_rate,ticker_count "
                "FROM sector_summary ORDER BY summary_date,sector"))
            queries=(CODE/"Step_3_Analyze_Results.sql").read_text().split(";")
            names=("sector_overview.csv","volatility_regimes.csv","data_quality.csv")
            statements=[s.strip() for s in queries if s.strip()]
            if len(statements)!=3:
                raise ValueError(f"Expected 3 research queries; got {len(statements)}")
            for filename,statement in zip(names,statements):
                save_csv(results_dir/filename,con.execute(statement))
            if reference is not None:
                check_reference(con,Path(reference))
            for table in ("stock_prices","companies","macro_indicators","sp500_returns","sector_summary"):
                print(f"  {table}: {con.execute('SELECT COUNT(*) FROM '+table).fetchone()[0]:,}")
            print("RESULTS:",results_dir)
    except Exception:
        db.unlink(missing_ok=True)
        raise

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir",type=Path,default=PROJECT/"data",help="Real CSV folder (default: included 2017 Q1 data)")
    parser.add_argument("--results-dir",type=Path,default=PROJECT/"results")
    parser.add_argument("--reference",type=Path,help="Optional full historical sector_summary CSV for exact verification")
    opts=parser.parse_args()
    run(opts.data_dir,opts.results_dir,opts.reference)

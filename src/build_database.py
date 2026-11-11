#!/usr/bin/env python3
"""Build and validate the DATA 521 relational research database (stdlib only)."""
import argparse
import csv
import math
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_rows(path, needed):
    if not path.is_file():
        raise FileNotFoundError(f"Missing input: {path}")
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not set(needed).issubset(reader.fieldnames or []):
            raise ValueError(f"{path.name}: expected columns {sorted(needed)}, found {reader.fieldnames}")
        yield from reader


def number(v):
    return float(v) if v not in (None, "") else None


def batches(iterator, size=10000):
    batch = []
    for row in iterator:
        batch.append(row)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def build(data_dir, db_path, overwrite=False, reference=None):
    data_dir, db_path = Path(data_dir), Path(db_path)
    if db_path.exists():
        if not overwrite:
            raise FileExistsError(f"{db_path} exists. Use --overwrite to rebuild.")
        db_path.unlink()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with sqlite3.connect(db_path) as con:
            con.executescript((ROOT / 'sql/01_schema.sql').read_text())
            company_rows = ((r['Symbol'],r['Security'],r['GICS Sector'],r.get('GICS Sub-Industry'))
                            for r in read_rows(data_dir/'sp500_companies.csv',
                                               ['Symbol','Security','GICS Sector']))
            for batch in batches(company_rows):
                con.executemany('INSERT INTO companies VALUES (?,?,?,?)',batch)
            macro_rows = ((r['date'],number(r['fed_funds_rate']),number(r['cpi']),number(r['vix']))
                          for r in read_rows(data_dir/'macro_indicators.csv',
                                             ['date','fed_funds_rate','cpi','vix']))
            for batch in batches(macro_rows):
                con.executemany('INSERT INTO macro_indicators VALUES (?,?,?,?)',batch)
            stock_rows = ((r['Name'],r['date'],number(r['open']),number(r['close']),
                           number(r['high']),number(r['low']),int(r['volume']) if r['volume'] else None)
                          for r in read_rows(data_dir/'all_stocks_5yr.csv',
                                             ['Name','date','open','close','high','low','volume']))
            for batch in batches(stock_rows):
                con.executemany('INSERT INTO stock_prices VALUES (?,?,?,?,?,?,?)',batch)
            con.executescript((ROOT / 'sql/02_transform.sql').read_text())
            con.commit()
            print('SQLite database:', db_path)
            for table in ['companies','macro_indicators','stock_prices','sp500_returns','sector_summary']:
                print(f'{table}: {con.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]:,} rows')
            if reference:
                compare_reference(con,Path(reference))
    except Exception:
        if db_path.exists():
            db_path.unlink()
        raise


def compare_reference(con, csv_path):
    """Check values against the original course-exported sector_summary.csv."""
    rows = con.execute('SELECT summary_date,sector,avg_return,avg_vix,avg_fed_rate,ticker_count FROM sector_summary')
    actual = {(r[0],r[1]):r[2:] for r in rows}
    n = 0
    for row in read_rows(csv_path,['summary_date','sector','avg_return','avg_vix','avg_fed_rate','ticker_count']):
        key = (row['summary_date'],row['sector'])
        if key not in actual:
            raise AssertionError(f'Missing sector-day: {key}')
        expected = [float(row[k]) for k in ('avg_return','avg_vix','avg_fed_rate','ticker_count')]
        if not all(math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9)
                   for a,b in zip(actual[key],expected)):
            raise AssertionError(f'Mismatch: {key}')
        n += 1
    if n != len(actual):
        raise AssertionError(f'Reference row count {n} != computed {len(actual)}')
    print(f'REFERENCE CHECK PASS: {n:,} sector-day rows match original CSV')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true', help='Use included synthetic demo CSVs')
    parser.add_argument('--data-dir', type=Path, help='Directory containing the three source CSV files')
    parser.add_argument('--db', type=Path, default=Path('outputs/demo.sqlite'))
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--reference', type=Path, help='Optional original sector_summary CSV for numerical verification')
    args = parser.parse_args()
    if args.demo and args.data_dir:
        parser.error('Use either --demo or --data-dir, not both')
    build(args.data_dir or ROOT/'data/demo',args.db,args.overwrite,args.reference)

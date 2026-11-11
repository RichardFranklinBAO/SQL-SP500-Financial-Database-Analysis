-- SQLite research schema (portable showcase implementation).
PRAGMA foreign_keys=ON;
CREATE TABLE companies (
  ticker TEXT PRIMARY KEY,
  company_name TEXT NOT NULL,
  sector TEXT NOT NULL,
  sub_industry TEXT
);
CREATE TABLE macro_indicators (
  trade_date TEXT PRIMARY KEY,
  fed_funds_rate REAL,
  cpi REAL,
  vix REAL
);
CREATE TABLE stock_prices (
  ticker TEXT NOT NULL,
  trade_date TEXT NOT NULL,
  open_price REAL,
  close_price REAL,
  high_price REAL,
  low_price REAL,
  volume INTEGER,
  PRIMARY KEY (ticker, trade_date)
);
CREATE TABLE sp500_returns (
  ticker TEXT NOT NULL,
  trade_date TEXT NOT NULL,
  daily_return REAL NOT NULL,
  PRIMARY KEY (ticker, trade_date)
);
CREATE TABLE sector_summary (
  summary_date TEXT NOT NULL,
  sector TEXT NOT NULL,
  avg_return REAL NOT NULL,
  avg_vix REAL,
  avg_fed_rate REAL,
  ticker_count INTEGER NOT NULL,
  PRIMARY KEY (summary_date, sector)
);
CREATE INDEX idx_companies_sector ON companies(sector);
CREATE INDEX idx_returns_date ON sp500_returns(trade_date);

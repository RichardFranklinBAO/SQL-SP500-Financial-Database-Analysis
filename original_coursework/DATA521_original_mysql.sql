-- DATA 521 Final Project - Source Code
-- Group Members: Franklin (Conglin Bao), Zirui Chen
--
-- Note: Tables 1-3 (all_stocks, macro_indicators, sp500_companies) were populated
-- by importing the following CSV files via DBeaver Import Wizard:
--   - all_stocks_5yr.csv (source: Kaggle)
--   - macro_indicators.csv (source: FRED)
--   - sp500_companies.csv (source: Wikipedia)
-- The CREATE TABLE statements below reflect the schema generated during import.
-- Tables 4-5 (sp500_returns, sector_summary) are derived and fully reproducible
-- from the SQL statements in this file once the source tables are loaded.

-- Table 1: all_stocks
CREATE TABLE `all_stocks` (
  `date` varchar(50) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `volume` int DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table 2: macro_indicators
CREATE TABLE `macro_indicators` (
  `date` varchar(50) DEFAULT NULL,
  `fed_funds_rate` double DEFAULT NULL,
  `cpi` double DEFAULT NULL,
  `vix` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table 3: sp500_companies
CREATE TABLE `sp500_companies` (
  `Symbol` varchar(50) DEFAULT NULL,
  `Security` varchar(50) DEFAULT NULL,
  `GICS Sector` varchar(50) DEFAULT NULL,
  `GICS Sub-Industry` varchar(64) DEFAULT NULL,
  `Headquarters Location` varchar(50) DEFAULT NULL,
  `Date added` varchar(50) DEFAULT NULL,
  `CIK` int DEFAULT NULL,
  `Founded` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table 4: sp500_returns
CREATE TABLE sp500_returns AS
SELECT
    Name AS ticker,
    date AS trade_date,
    (close - open) / open AS daily_return
FROM all_stocks
WHERE open > 0;

ALTER TABLE sp500_returns
    ADD CONSTRAINT uq_sp500_returns_ticker_date UNIQUE (ticker, trade_date);

-- Table 5: sector_summary
CREATE TABLE sector_summary AS
SELECT
    r.trade_date AS summary_date,
    c.`GICS Sector` AS sector,
    AVG(r.daily_return) AS avg_return,
    AVG(m.vix) AS avg_vix,
    AVG(m.fed_funds_rate) AS avg_fed_rate,
    COUNT(DISTINCT r.ticker) AS ticker_count
FROM sp500_returns r
INNER JOIN sp500_companies c ON r.ticker = c.Symbol
INNER JOIN macro_indicators m ON r.trade_date = m.date
GROUP BY r.trade_date, c.`GICS Sector`;

ALTER TABLE sector_summary
    ADD CONSTRAINT uq_sector_summary_sector_date UNIQUE (sector, summary_date);


SELECT 'all_stocks'      AS table_name, COUNT(*) AS row_count FROM all_stocks
UNION ALL
SELECT 'sp500_companies' AS table_name, COUNT(*) AS row_count FROM sp500_companies
UNION ALL
SELECT 'macro_indicators' AS table_name, COUNT(*) AS row_count FROM macro_indicators
UNION ALL
SELECT 'sp500_returns'   AS table_name, COUNT(*) AS row_count FROM sp500_returns
UNION ALL
SELECT 'sector_summary'  AS table_name, COUNT(*) AS row_count FROM sector_summary;

SELECT * FROM sector_summary ORDER BY summary_date LIMIT 10;

SELECT c.`GICS Sector` AS sector, AVG(r.daily_return) AS avg_return
FROM sp500_returns r
JOIN sp500_companies c ON r.ticker = c.Symbol
GROUP BY c.`GICS Sector`  ORDER BY avg_return DESC;
-- STEP 2 | Compute intraday stock returns, JOIN with sector and macro data,
-- and summarize equal-weighted returns at the sector-day level.
-- Reproduces original DATA 521 return definition: (close-open)/open.
INSERT INTO sp500_returns(ticker,trade_date,daily_return)
SELECT ticker,trade_date,(close_price-open_price)/open_price
FROM stock_prices
WHERE open_price IS NOT NULL AND open_price > 0 AND close_price IS NOT NULL;

-- Preserve the original coursework INNER JOIN universe.
INSERT INTO sector_summary(summary_date,sector,avg_return,avg_vix,avg_fed_rate,ticker_count)
SELECT r.trade_date,c.sector,AVG(r.daily_return),AVG(m.vix),
       AVG(m.fed_funds_rate),COUNT(DISTINCT r.ticker)
FROM sp500_returns AS r
INNER JOIN companies AS c ON c.ticker=r.ticker
INNER JOIN macro_indicators AS m ON m.trade_date=r.trade_date
GROUP BY r.trade_date,c.sector;

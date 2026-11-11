-- Preserve the original DATA 521 definition: same-day (close-open)/open.
INSERT INTO sp500_returns(ticker, trade_date, daily_return)
SELECT ticker, trade_date, (close_price-open_price)/open_price
FROM stock_prices
WHERE open_price IS NOT NULL AND open_price > 0 AND close_price IS NOT NULL;

-- INNER JOIN intentionally reproduces the coursework sector-day universe.
-- Company metadata are a snapshot, not point-in-time historical membership.
INSERT INTO sector_summary
(summary_date, sector, avg_return, avg_vix, avg_fed_rate, ticker_count)
SELECT r.trade_date, c.sector, AVG(r.daily_return), AVG(m.vix),
       AVG(m.fed_funds_rate), COUNT(DISTINCT r.ticker)
FROM sp500_returns AS r
JOIN companies AS c ON c.ticker = r.ticker
JOIN macro_indicators AS m ON m.trade_date = r.trade_date
GROUP BY r.trade_date, c.sector;

-- Research question: describe sector returns alongside macro conditions.
-- Intraday close/open returns, NOT next-day prediction or causal effects.
SELECT sector, COUNT(*) AS trading_days, ROUND(AVG(avg_return), 6) AS mean_daily_return,
       ROUND(AVG(avg_vix), 2) AS mean_vix,
       ROUND(AVG(avg_fed_rate), 3) AS mean_fed_funds_rate
FROM sector_summary
GROUP BY sector
ORDER BY mean_daily_return DESC;

-- Descriptive grouping by contemporaneous volatility regime.
SELECT sector,
       CASE WHEN avg_vix >= 20 THEN 'VIX >= 20' ELSE 'VIX < 20' END AS vix_regime,
       COUNT(*) AS sector_days,
       ROUND(AVG(avg_return), 6) AS mean_return
FROM sector_summary
GROUP BY sector, vix_regime
ORDER BY sector, vix_regime;

-- Inspect data coverage and join-survivor counts.
SELECT 'source_prices' AS metric, COUNT(*) AS count_rows FROM stock_prices
UNION ALL SELECT 'companies', COUNT(*) FROM companies
UNION ALL SELECT 'macro_days', COUNT(*) FROM macro_indicators
UNION ALL SELECT 'usable_returns', COUNT(*) FROM sp500_returns
UNION ALL SELECT 'sector_days', COUNT(*) FROM sector_summary;

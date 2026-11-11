-- STEP 3 | Answer descriptive research questions using SQL.
-- Q1: Which sampled sectors had higher average intraday returns?
-- This is descriptive, not trading performance or causal inference.
SELECT sector,COUNT(*) AS sector_days,ROUND(AVG(avg_return),6) AS mean_intraday_return,
       ROUND(AVG(avg_vix),2) AS mean_vix,
       ROUND(AVG(avg_fed_rate),3) AS mean_fed_funds_rate
FROM sector_summary
GROUP BY sector
ORDER BY mean_intraday_return DESC;

-- Q2: Compare sector returns across observed VIX regimes.
SELECT sector,
       CASE WHEN avg_vix IS NULL THEN 'VIX unavailable'
            WHEN avg_vix >= 20 THEN 'VIX >= 20'
            ELSE 'VIX < 20' END AS volatility_regime,
       COUNT(*) AS sector_days,ROUND(AVG(avg_return),6) AS mean_intraday_return
FROM sector_summary
GROUP BY sector,volatility_regime
ORDER BY sector,volatility_regime;

-- Q3: Check database coverage and record counts.
SELECT 'stock_prices' AS table_name,COUNT(*) AS row_count FROM stock_prices
UNION ALL SELECT 'companies',COUNT(*) FROM companies
UNION ALL SELECT 'macro_indicators',COUNT(*) FROM macro_indicators
UNION ALL SELECT 'sp500_returns',COUNT(*) FROM sp500_returns
UNION ALL SELECT 'sector_summary',COUNT(*) FROM sector_summary;

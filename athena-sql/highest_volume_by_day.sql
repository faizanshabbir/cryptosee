SELECT name, date(last_updated) as "price_date", AVG("24h_volume_usd") as "volume_usd"
FROM cryptoprices
GROUP BY name, date(last_updated)
ORDER BY volume_usd desc;
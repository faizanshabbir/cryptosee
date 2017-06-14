WITH supply_info as (
  SELECT name,
         date(last_updated) AS "price_date",
         AVG(available_supply) AS "avg_available_supply",
         AVG(total_supply) AS "avg_total_supply",
         AVG("24h_volume_usd") as "avg_volume_usd"
  FROM cryptoprices
  WHERE available_supply > 0
  GROUP BY  name,
         date(last_updated)
  )
SELECT name, price_date, "avg_volume_usd", "avg_available_supply"/"avg_total_supply" as "ratio_avail_total", "avg_available_supply", "avg_total_supply" 
FROM supply_info
HAVING "avg_available_supply"/"avg_total_supply" < 1.0
ORDER BY "avg_volume_usd" desc, "ratio_avail_total" desc
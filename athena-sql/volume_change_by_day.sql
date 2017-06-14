SELECT name,
         date(last_updated) AS "price_date",
         AVG(total_supply) AS "total_supply"
FROM cryptoprices
GROUP BY  name, date(last_updated)
ORDER BY  total_supply desc;
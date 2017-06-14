SELECT name, DATE(last_updated) as "price_date", AVG(percent_change_1h) as "percent_change" 
FROM cryptoprices
WHERE DATE(last_updated) >= current_date - interval '7' day
GROUP BY DATE(last_updated), name
ORDER BY DATE(last_updated), percent_change desc;
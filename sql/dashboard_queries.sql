-- Card 1: policies sold per partner per month
SELECT partner, date_trunc('month', start_date)::date AS month, count(*) AS policies_sold
FROM policies GROUP BY 1, 2 ORDER BY 2, 1;

-- Card 2: claims count and amount per partner
SELECT partner, count(*) AS claims, sum(amount_eur) AS claims_amount_eur
FROM claims GROUP BY 1 ORDER BY 1;

-- Card 3: loss ratio per partner (claims paid or open divided by premiums)
SELECT p.partner,
       round(coalesce(sum(c.amount_eur), 0) / sum(DISTINCT p.total_premium), 3) AS loss_ratio
FROM (SELECT partner, sum(premium_eur) AS total_premium FROM policies GROUP BY partner) p
LEFT JOIN claims c ON c.partner = p.partner AND c.status <> 'rejected'
GROUP BY p.partner ORDER BY 1;

-- Card 4: rejected records per partner and per check, latest run
SELECT partner, check_name, failed_rows
FROM quality_results
WHERE run_date = (SELECT max(run_date) FROM quality_results)
ORDER BY partner, check_name;

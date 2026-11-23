-- Six data quality checks. Each returns: check_name, partner, failed_rows.
SELECT '1_missing_required_fields' AS check_name, partner, count(*) AS failed_rows
FROM stg_policies
WHERE policy_id = '' OR customer_email = '' OR product = ''
GROUP BY partner

UNION ALL
SELECT '2_invalid_dates', partner, count(*)
FROM (SELECT partner FROM stg_policies WHERE start_date IS NULL
      UNION ALL SELECT partner FROM stg_claims WHERE claim_date IS NULL) d
GROUP BY partner

UNION ALL
SELECT '3_duplicate_policy_ids', partner, count(*) - count(DISTINCT policy_id)
FROM stg_policies
GROUP BY partner
HAVING count(*) > count(DISTINCT policy_id)

UNION ALL
SELECT '4_claims_without_policy', c.partner, count(*)
FROM stg_claims c
LEFT JOIN stg_policies p ON p.policy_id = c.policy_id
WHERE p.policy_id IS NULL
GROUP BY c.partner

UNION ALL
SELECT '5_negative_amounts', partner, count(*)
FROM (SELECT partner FROM stg_policies WHERE premium_eur <= 0
      UNION ALL SELECT partner FROM stg_claims WHERE amount_eur <= 0) n
GROUP BY partner

UNION ALL
SELECT '6_claim_before_policy_start', c.partner, count(*)
FROM stg_claims c
JOIN stg_policies p ON p.policy_id = c.policy_id
WHERE c.claim_date < p.start_date
GROUP BY c.partner

ORDER BY check_name, partner;

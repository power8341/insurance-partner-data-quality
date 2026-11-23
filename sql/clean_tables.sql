-- Clean tables: only rows that pass every rule. The dashboard reads from these.
DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS policies;

CREATE TABLE policies AS
SELECT DISTINCT ON (policy_id) partner, policy_id, customer_email, product, start_date, premium_eur
FROM stg_policies
WHERE policy_id <> '' AND customer_email LIKE '%@%' AND start_date IS NOT NULL AND premium_eur > 0
ORDER BY policy_id, start_date;
ALTER TABLE policies ADD PRIMARY KEY (policy_id);

CREATE TABLE claims AS
SELECT c.partner, c.claim_id, c.policy_id, c.claim_date, c.amount_eur, c.status
FROM stg_claims c
JOIN policies p ON p.policy_id = c.policy_id
WHERE c.claim_date IS NOT NULL AND c.amount_eur > 0 AND c.claim_date >= p.start_date;
ALTER TABLE claims ADD PRIMARY KEY (claim_id);

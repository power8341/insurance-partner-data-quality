CREATE TABLE IF NOT EXISTS stg_policies (
  partner TEXT, policy_id TEXT, customer_email TEXT, product TEXT,
  start_date DATE, premium_eur NUMERIC(10,2), start_date_raw TEXT
);
CREATE TABLE IF NOT EXISTS stg_claims (
  partner TEXT, claim_id TEXT, policy_id TEXT, claim_date DATE,
  amount_eur NUMERIC(10,2), status TEXT, claim_date_raw TEXT
);
CREATE TABLE IF NOT EXISTS quality_results (
  run_date    DATE NOT NULL DEFAULT current_date,
  check_name  TEXT NOT NULL,
  partner     TEXT NOT NULL,
  failed_rows INT  NOT NULL,
  PRIMARY KEY (run_date, check_name, partner)
);

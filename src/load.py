"""Load the partner files into Postgres using one mapping per partner.

Raw values go into staging tables exactly as received (after renaming columns),
so the quality checks can see every problem. Clean tables keep only valid rows.
"""
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from src.mappings import CLAIM_MAPPINGS, POLICY_MAPPINGS, STATUS_MAP

ROOT = Path(__file__).resolve().parent.parent
DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://beloy:beloy@localhost:5432/insurance")


def parse_date(value, fmt):
    try:
        return datetime.strptime(str(value).strip(), fmt).date()
    except (ValueError, TypeError):
        return None


def parse_amount(value, decimal):
    try:
        return round(float(str(value).strip().replace(decimal, ".")), 2)
    except (ValueError, TypeError):
        return None


def read_partner(kind, partner):
    m = (POLICY_MAPPINGS if kind == "policies" else CLAIM_MAPPINGS)[partner]
    df = pd.read_csv(ROOT / "data" / f"partner_{partner.lower()}_{kind}.csv", sep=m["sep"], dtype=str,
                     keep_default_na=False)
    df = df.rename(columns=m["columns"])
    df.insert(0, "partner", partner)
    date_col, amount_col = ("start_date", "premium_eur") if kind == "policies" else ("claim_date", "amount_eur")
    df[f"{date_col}_raw"] = df[date_col]
    df[date_col] = df[date_col].map(lambda v: parse_date(v, m["date_format"]))
    df[amount_col] = df[amount_col].map(lambda v: parse_amount(v, m["decimal"]))
    if kind == "claims":
        df["status"] = df["status"].map(lambda s: STATUS_MAP.get(s, "unknown"))
    return df


def main():
    engine = create_engine(DB_URL)
    with engine.begin() as con:
        con.execute(text((ROOT / "sql" / "schema.sql").read_text()))
        for t in ("stg_policies", "stg_claims"):
            con.execute(text(f"TRUNCATE {t}"))
    policies = pd.concat([read_partner("policies", p) for p in POLICY_MAPPINGS])
    claims = pd.concat([read_partner("claims", p) for p in CLAIM_MAPPINGS])
    policies.to_sql("stg_policies", engine, if_exists="append", index=False)
    claims.to_sql("stg_claims", engine, if_exists="append", index=False)
    with engine.begin() as con:
        con.execute(text((ROOT / "sql" / "clean_tables.sql").read_text()))
        n_pol = con.execute(text("SELECT count(*) FROM policies")).scalar()
        n_cl = con.execute(text("SELECT count(*) FROM claims")).scalar()
    print(f"staged {len(policies)} policies and {len(claims)} claims from 3 partners")
    print(f"clean tables: {n_pol} policies, {n_cl} claims")


if __name__ == "__main__":
    main()

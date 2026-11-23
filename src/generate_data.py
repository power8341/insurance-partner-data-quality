"""Generate simulated policy and claims files for 3 partners, each in its own format.

About 5% of rows get a deliberate error (missing email, bad date, duplicate id,
negative amount, unknown policy, claim before policy start) so the quality checks
have something real to find. Fixed seed, so results are reproducible.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

from src.mappings import CLAIM_MAPPINGS, POLICY_MAPPINGS

OUT = Path(__file__).resolve().parent.parent / "data"
PRODUCTS = ["Home", "Car", "Phone", "Travel", "Pet"]
PARTNER_SHARE = {"A": 450, "B": 350, "C": 200}
CLAIMS = {"A": 130, "B": 110, "C": 60}


def fmt_date(d, partner, kind):
    m = (POLICY_MAPPINGS if kind == "policy" else CLAIM_MAPPINGS)[partner]
    return d.strftime(m["date_format"])


def fmt_amount(x, partner, kind):
    m = (POLICY_MAPPINGS if kind == "policy" else CLAIM_MAPPINGS)[partner]
    s = f"{x:.2f}"
    return s.replace(".", ",") if m["decimal"] == "," else s


def main(seed=42):
    random.seed(seed)
    fake = Faker("fr_FR")
    Faker.seed(seed)
    OUT.mkdir(exist_ok=True)
    totals = {}
    for partner, n in PARTNER_SHARE.items():
        pm = POLICY_MAPPINGS[partner]
        src_cols = list(pm["columns"].keys())
        policies = []
        for i in range(1, n + 1):
            pid = f"{partner}{10000 + i}"
            start = date(2026, 1, 1) + timedelta(days=random.randint(0, 300))
            row = {"policy_id": pid, "customer_email": fake.email(), "product": random.choice(PRODUCTS),
                   "start_date": fmt_date(start, partner, "policy"),
                   "premium_eur": fmt_amount(random.uniform(60, 900), partner, "policy"), "_start": start}
            r = random.random()
            if r < 0.015:
                row["customer_email"] = ""                    # missing required field
            elif r < 0.03:
                row["start_date"] = "2026-02-30" if partner != "B" else "30/02/2026"   # invalid date
            elif r < 0.04 and policies:
                row["policy_id"] = policies[-1]["policy_id"]  # duplicate id
            elif r < 0.05:
                row["premium_eur"] = fmt_amount(-random.uniform(10, 100), partner, "policy")
            policies.append(row)
        with open(OUT / f"partner_{partner.lower()}_policies.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=pm["sep"], lineterminator="\n")
            w.writerow(src_cols)
            for p in policies:
                w.writerow([p[pm["columns"][c]] for c in src_cols])

        cm = CLAIM_MAPPINGS[partner]
        c_cols = list(cm["columns"].keys())
        statuses = {"A": ["ouvert", "clos", "refuse"], "B": ["open", "closed", "rejected"], "C": ["OPEN", "PAID", "DENIED"]}[partner]
        with open(OUT / f"partner_{partner.lower()}_claims.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=cm["sep"], lineterminator="\n")
            w.writerow(c_cols)
            for j in range(1, CLAIMS[partner] + 1):
                pol = random.choice(policies)
                cdate = pol["_start"] + timedelta(days=random.randint(1, 60))
                row = {"claim_id": f"{partner}C{5000 + j}", "policy_id": pol["policy_id"],
                       "claim_date": fmt_date(cdate, partner, "claim"),
                       "amount_eur": fmt_amount(random.uniform(50, 3000), partner, "claim"),
                       "status": random.choice(statuses)}
                r = random.random()
                if r < 0.02:
                    row["policy_id"] = f"{partner}99999"           # claim without a policy
                elif r < 0.04:
                    row["amount_eur"] = fmt_amount(-random.uniform(10, 200), partner, "claim")
                elif r < 0.06:
                    row["claim_date"] = fmt_date(date(2025, 12, 1), partner, "claim")  # before any policy start
                w.writerow([row[cm["columns"][c]] for c in c_cols])
        totals[partner] = (len(policies), CLAIMS[partner])
    for p, (np_, nc) in totals.items():
        print(f"partner {p}: {np_} policies, {nc} claims")


if __name__ == "__main__":
    main()

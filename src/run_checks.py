"""Run the 6 quality checks, store today's results and write a markdown report."""
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://beloy:beloy@localhost:5432/insurance")


def main():
    engine = create_engine(DB_URL)
    with engine.begin() as con:
        df = pd.read_sql(text((ROOT / "sql" / "quality_checks.sql").read_text()), con)
        con.execute(text("DELETE FROM quality_results WHERE run_date = current_date"))
        for r in df.itertuples():
            con.execute(text("INSERT INTO quality_results (check_name, partner, failed_rows) VALUES (:c, :p, :n)"),
                        {"c": r.check_name, "p": r.partner, "n": int(r.failed_rows)})
        totals = pd.read_sql(text("SELECT (SELECT count(*) FROM stg_policies) AS policies_received, "
                                  "(SELECT count(*) FROM policies) AS policies_clean, "
                                  "(SELECT count(*) FROM stg_claims) AS claims_received, "
                                  "(SELECT count(*) FROM claims) AS claims_clean"), con)
        loss = pd.read_sql(text((ROOT / "sql" / "dashboard_queries.sql").read_text().split("-- Card 3")[1]
                                .split("-- Card 4")[0].split("\n", 1)[1]), con)
    pivot = df.pivot_table(index="check_name", columns="partner", values="failed_rows", fill_value=0, aggfunc="sum")
    print(pivot.to_string())
    print()
    print(totals.to_string(index=False))
    report = ["# Data quality report", "", "## Failed rows per check and partner", "",
              pivot.reset_index().to_markdown(index=False), "", "## Volumes", "",
              totals.to_markdown(index=False), "", "## Loss ratio per partner", "",
              loss.to_markdown(index=False), ""]
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "quality_report.md").write_text("\n".join(report), encoding="utf-8")
    print("\nReport written to reports/quality_report.md")


if __name__ == "__main__":
    main()

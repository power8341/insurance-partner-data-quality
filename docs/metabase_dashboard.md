# Building the Metabase dashboard (about 15 minutes)

1. Run `docker compose up -d`, then `python -m src.load` and `python -m src.run_checks`.
2. Open http://localhost:3000 and create the admin account.
3. Add a database: type PostgreSQL, host `postgres`, port `5432`, database `insurance`, user `beloy`, password `beloy`.
4. Create a new dashboard called "Partner programme".
5. For each card, click New, then SQL query, paste the query from `sql/dashboard_queries.sql`, save it and add it to the dashboard:
   - Card 1: policies sold per partner per month. Visualisation: line chart, x = month, series = partner.
   - Card 2: claims count and amount per partner. Visualisation: bar chart.
   - Card 3: loss ratio per partner. Visualisation: bar chart or number per partner.
   - Card 4: rejected records per partner and per check. Visualisation: table or stacked bar.
6. Take a screenshot of the dashboard and save it as `docs/dashboard.png`, then add it to the README.

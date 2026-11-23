"""One mapping per partner: their column names and date format -> our target schema.

Adding a new partner = adding one entry here. The loading code does not change.
"""
POLICY_MAPPINGS = {
    "A": {"columns": {"ref": "policy_id", "mail": "customer_email", "offer": "product",
                      "start": "start_date", "price": "premium_eur"},
          "date_format": "%d/%m/%Y", "sep": ";", "decimal": ","},
    "B": {"columns": {"PolicyNumber": "policy_id", "Email": "customer_email", "Product": "product",
                      "StartDate": "start_date", "AnnualPremium": "premium_eur"},
          "date_format": "%Y-%m-%d", "sep": ",", "decimal": "."},
    "C": {"columns": {"contract_no": "policy_id", "client_email": "customer_email", "plan": "product",
                      "effective": "start_date", "yearly_fee": "premium_eur"},
          "date_format": "%m/%d/%Y", "sep": ",", "decimal": "."},
}

CLAIM_MAPPINGS = {
    "A": {"columns": {"sinistre": "claim_id", "ref": "policy_id", "date": "claim_date",
                      "montant": "amount_eur", "statut": "status"},
          "date_format": "%d/%m/%Y", "sep": ";", "decimal": ","},
    "B": {"columns": {"ClaimNumber": "claim_id", "PolicyNumber": "policy_id", "ClaimDate": "claim_date",
                      "Amount": "amount_eur", "Status": "status"},
          "date_format": "%Y-%m-%d", "sep": ",", "decimal": "."},
    "C": {"columns": {"claim_ref": "claim_id", "contract_no": "policy_id", "incident_date": "claim_date",
                      "claim_amount": "amount_eur", "state": "status"},
          "date_format": "%m/%d/%Y", "sep": ",", "decimal": "."},
}

STATUS_MAP = {"ouvert": "open", "clos": "closed", "refuse": "rejected",
              "open": "open", "closed": "closed", "rejected": "rejected",
              "OPEN": "open", "PAID": "closed", "DENIED": "rejected"}

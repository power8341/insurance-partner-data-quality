# Data quality report

## Failed rows per check and partner

| check_name                  |   A |   B |   C |
|:----------------------------|----:|----:|----:|
| 1_missing_required_fields   |   3 |   8 |   5 |
| 2_invalid_dates             |   6 |   3 |   1 |
| 3_duplicate_policy_ids      |   2 |   2 |   4 |
| 4_claims_without_policy     |   3 |   2 |   0 |
| 5_negative_amounts          |   9 |   2 |   2 |
| 6_claim_before_policy_start |   4 |   6 |   2 |

## Volumes

|   policies_received |   policies_clean |   claims_received |   claims_clean |
|--------------------:|-----------------:|------------------:|---------------:|
|                1000 |              957 |               300 |            276 |

## Loss ratio per partner

| partner   |   loss_ratio |
|:----------|-------------:|
| A         |        0.583 |
| B         |        0.563 |
| C         |        0.606 |

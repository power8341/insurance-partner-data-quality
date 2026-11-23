from datetime import date

from src.load import parse_amount, parse_date
from src.mappings import CLAIM_MAPPINGS, POLICY_MAPPINGS


def test_every_partner_maps_to_the_same_target_columns():
    targets = {tuple(sorted(m["columns"].values())) for m in POLICY_MAPPINGS.values()}
    assert len(targets) == 1
    targets = {tuple(sorted(m["columns"].values())) for m in CLAIM_MAPPINGS.values()}
    assert len(targets) == 1


def test_dates_in_each_partner_format():
    assert parse_date("31/12/2026", "%d/%m/%Y") == date(2026, 12, 31)
    assert parse_date("2026-12-31", "%Y-%m-%d") == date(2026, 12, 31)
    assert parse_date("12/31/2026", "%m/%d/%Y") == date(2026, 12, 31)


def test_impossible_dates_become_none():
    assert parse_date("30/02/2026", "%d/%m/%Y") is None
    assert parse_date("", "%Y-%m-%d") is None


def test_amounts_with_comma_or_dot():
    assert parse_amount("12,50", ",") == 12.5
    assert parse_amount("12.50", ".") == 12.5
    assert parse_amount("abc", ".") is None

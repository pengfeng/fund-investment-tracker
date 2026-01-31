import pytest
from leet_apps.connectors.crunchbase import CrunchbaseConnector


def test_find_portfolio_by_fund_returns_list():
    connector = CrunchbaseConnector()
    results = connector.find_portfolio_by_fund("Sequoia Capital")
    assert isinstance(results, list)
    assert len(results) > 0
    company = results[0]
    assert "company_name" in company
    assert "investments" in company


def test_sample_investment_structure():
    connector = CrunchbaseConnector()
    results = connector.find_portfolio_by_fund("Sequoia Capital")
    company = results[0]
    inv = company["investments"][0]
    assert "round_type" in inv
    assert "date" in inv
    assert "amount" in inv

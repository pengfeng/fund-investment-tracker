from leet_apps.connectors.crunchbase import CrunchbaseConnector


def test_crunchbase_connector_stub_basic():
    connector = CrunchbaseConnector()
    result = connector.find_portfolio("Sequoia Capital")
    assert isinstance(result, list)
    assert len(result) >= 1
    # Check expected keys on first record
    first = result[0]
    for key in ["company_name", "website", "industry", "hq", "founding_date", "description", "status", "investment", "source_links"]:
        assert key in first
    # Investment should contain expected subkeys
    inv = first.get("investment", {})
    for ik in ["round_type", "date", "amount", "co_investors", "source_links"]:
        assert ik in inv

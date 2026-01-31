from leet_apps.connectors.linkedin import LinkedInConnector


def test_linkedin_connector_stub_basic():
    connector = LinkedInConnector()
    result = connector.find_portfolio("Sequoia Capital")
    assert isinstance(result, list)
    assert len(result) >= 1
    first = result[0]
    for key in ["company_name", "website", "industry", "hq", "founding_date", "description", "status", "investment", "source_links"]:
        assert key in first
    inv = first.get("investment", {})
    for ik in ["round_type", "date", "amount", "co_investors", "source_links"]:
        assert ik in inv

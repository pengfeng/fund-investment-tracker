from leet_apps.connectors.pitchbook import PitchBookConnector


def test_pitchbook_connector_stub_basic():
    connector = PitchBookConnector()
    result = connector.find_portfolio("Sequoia Capital")
    assert isinstance(result, list)
    assert len(result) >= 1
    first = result[0]
    for key in ["company_name", "website", "industry", "hq", "founding_date", "description", "status", "investment", "source_links"]:
        assert key in first
    inv = first.get("investment", {})
    for ik in ["round_type", "date", "amount", "co_investors", "source_links"]:
        assert ik in inv

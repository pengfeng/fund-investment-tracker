def test_official_fund_connector_basic():
    from leet_apps.connectors.official_fund import OfficialFundConnector

    html = """
    <html>
    <body>
      <h2>Portfolio</h2>
      <ul>
        <li>Acme Robotics</li>
        <li>Beta Analytics</li>
      </ul>
    </body>
    </html>
    """

    conn = OfficialFundConnector(test_html=html)
    res = conn.find_portfolio("https://examplefund.example/portfolio")
    assert isinstance(res, list)
    names = [r.get("company_name") for r in res]
    assert "Acme Robotics" in names
    assert "Beta Analytics" in names

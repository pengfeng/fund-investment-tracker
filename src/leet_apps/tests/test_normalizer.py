import pytest
from leet_apps.normalizer import normalize_results


def test_normalize_results_basic():
    raw = [
        {
            "company_name": "Acme Robotics",
            "website": "https://www.acmerobotics.example",
            "industry": "Robotics",
            "hq": "San Francisco, CA",
            "founding_date": "2015-06-01",
            "description": "Builds industrial robots.",
            "status": "active",
            "investment": {
                "round_type": "Series A",
                "date": "2018-09-12",
                "amount": "$5,000,000",
                "co_investors": ["Sequoia Capital"],
                "source_links": ["https://example.com/article1"]
            },
            "source_links": ["https://crunchbase.com/org/acme-robotics"]
        }
    ]

    result = normalize_results(raw)
    assert "fund" in result
    assert "companies" in result and len(result["companies"]) == 1
    assert result["companies"][0]["name"] == "Acme Robotics"
    assert "investments" in result and len(result["investments"]) == 1
    assert result["investments"][0]["round_type"] == "Series A"

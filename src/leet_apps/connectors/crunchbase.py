"""
Minimal Crunchbase connector for MVP.
This connector uses public web pages via WebFetch (if available) or simple HTTP requests.
Note: For now this is a stub that returns fixed sample data to allow progress on normalizer, CLI, and exporter.
"""
from typing import List, Dict, Any


class CrunchbaseConnector:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def find_portfolio(self, fund_input: str) -> List[Dict[str, Any]]:
        """Return a list of raw company/investment records for the given fund.
        Stub implementation returns sample data.
        """
        # Sample stub data
        return [
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
            },
            {
                "company_name": "Beta Analytics",
                "website": "https://www.betanalytics.example",
                "industry": "Analytics",
                "hq": "New York, NY",
                "founding_date": "2013-03-15",
                "description": "Analytics platform.",
                "status": "acquired",
                "investment": {
                    "round_type": "Seed",
                    "date": "2014-11-20",
                    "amount": "$500,000",
                    "co_investors": [],
                    "source_links": ["https://example.com/article2"]
                },
                "source_links": ["https://crunchbase.com/org/beta-analytics"]
            },
        ]

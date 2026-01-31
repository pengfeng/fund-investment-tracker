import json
from typing import List, Dict


class CrunchbaseConnector:
    """Stub connector for Crunchbase. In MVP this will use simple web fetch
    and heuristic parsing. For now it returns hardcoded sample data to allow
    CLI and exporter to work and tests to run.
    """

    def __init__(self):
        pass

    def find_portfolio_by_fund(self, fund: str) -> List[Dict]:
        """Return a list of company dictionaries for the given fund.

        This is a stub implementation with sample data. Replace with real
        Crunchbase API or scraper implementation in later iterations.
        """
        sample = [
            {
                "company_name": "SampleCo",
                "website": "https://sampleco.example",
                "industry": "Software",
                "hq": "San Francisco, CA",
                "founding_date": "2015-06-01",
                "description": "A sample company",
                "status": "operating",
                "investments": [
                    {
                        "round_type": "Series A",
                        "date": "2018-05-10",
                        "amount": "5,000,000",
                        "co_investors": ["OtherVC"],
                    }
                ],
                "source_links": [
                    "https://example.com/article-about-sampleco"
                ],
            }
        ]
        return sample

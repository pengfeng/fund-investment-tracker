"""
LinkedIn connector (stub for MVP).

Notes:
- Real LinkedIn scraping or API access is restricted; this connector provides a safe stub for development and tests.
- If an API client is available in the future, implement _call_api and parsing similar to other connectors.
"""
from typing import List, Dict, Any
import time


class LinkedInConnector:
    def __init__(self, api_key: str = None, max_retries: int = 1, backoff_seconds: float = 1.0):
        # Reserved for future API key usage
        self.api_key = api_key
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    def find_portfolio(self, fund_input: str) -> List[Dict[str, Any]]:
        """Return a list of raw company records similar to other connectors.

        This is a deterministic stub used for unit tests and development.
        """
        try:
            # simulate potential network latency/backoff logic placeholder
            time.sleep(0)
        except Exception:
            pass

        return [
            {
                "company_name": "Theta Bio",
                "website": "https://theta-bio.example",
                "industry": "Biotech",
                "hq": "Cambridge, MA",
                "founding_date": "2017-09-01",
                "description": "Biotech startup focused on therapeutics.",
                "status": "active",
                "investment": {
                    "round_type": "Series A",
                    "date": "2019-11-05",
                    "amount": "$7,500,000",
                    "co_investors": [],
                    "source_links": ["https://linkedin.example/theta"]
                },
                "source_links": ["https://linkedin.example/theta"],
            },
        ]

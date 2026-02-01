"""
PitchBook connector (stub for MVP).

Notes:
- Real PitchBook data is behind paywalls; this connector provides a stub dataset for development and tests.
- If an API key or client becomes available, implement _call_api and _parse_api_response similarly to CrunchbaseConnector.
"""
from typing import List, Dict, Any
import os
import time
import logging

logger = logging.getLogger(__name__)


class PitchBookConnector:
    def __init__(self, api_key: str = None, max_retries: int = 1, backoff_seconds: float = 1.0):
        # Reserved for future API key usage
        self.api_key = api_key or os.environ.get("PITCHBOOK_API_KEY")
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    def find_portfolio(self, fund_input: str) -> List[Dict[str, Any]]:
        """Return a list of raw company records similar to other connectors.

        This is a deterministic stub used for unit tests and development.
        """
        # If we had an API client, we would query it here. For now return stubbed entries.
        try:
            # simulate potential network latency/backoff logic placeholder
            time.sleep(0)
        except Exception:
            pass

        return [
            {
                "company_name": "Epsilon Energy",
                "website": "https://epsilon.example",
                "industry": "Energy",
                "hq": "Houston, TX",
                "founding_date": "2010-02-01",
                "description": "Renewable energy provider.",
                "status": "active",
                "investment": {
                    "round_type": "Series C",
                    "date": "2020-07-15",
                    "amount": "$30,000,000",
                    "co_investors": [fund_input],
                    "source_links": ["https://pitchbook.example/epsilon"],
                },
                "source_links": ["https://pitchbook.example/epsilon"],
            },
            {
                "company_name": "Zeta Fintech",
                "website": "https://zeta.example",
                "industry": "Fintech",
                "hq": "London, UK",
                "founding_date": "2014-10-10",
                "description": "Financial services platform.",
                "status": "active",
                "investment": {
                    "round_type": "Series B",
                    "date": "2018-03-22",
                    "amount": "$8,500,000",
                    "co_investors": [],
                    "source_links": ["https://pitchbook.example/zeta"],
                },
                "source_links": ["https://pitchbook.example/zeta"],
            },
        ]

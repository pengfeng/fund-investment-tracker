"""
News connector: searches public news sources for mentions of a fund and extracts company mentions.

Behavior:
- If an API key is provided via NEWSAPI_KEY env var or constructor, attempt to use NewsAPI (https://newsapi.org/) to search articles mentioning the fund.
- Otherwise, fall back to a small stub dataset for development and tests.

The connector returns the same raw record format used by other connectors so the normalizer can process it.
"""
from typing import List, Dict, Any
import os
import time
import logging

import requests

logger = logging.getLogger(__name__)


class NewsConnector:
    def __init__(self, api_key: str = None, max_retries: int = 1, backoff_seconds: float = 1.0):
        self.api_key = api_key or os.environ.get("NEWSAPI_KEY")
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    def _call_api(self, query: str) -> Dict[str, Any]:
        url = "https://newsapi.org/v2/everything"
        params = {"q": query, "pageSize": 20}
        headers = {"Authorization": self.api_key} if self.api_key else {}

        attempt = 0
        while attempt <= self.max_retries:
            try:
                resp = requests.get(url, params=params, headers=headers, timeout=10)
                if resp.status_code == 200:
                    return resp.json()
                else:
                    logger.warning("News API returned status %s: %s", resp.status_code, resp.text)
            except requests.RequestException as e:
                logger.warning("News API request failed: %s", e)

            attempt += 1
            time.sleep(self.backoff_seconds * attempt)

        raise RuntimeError("News API request failed after retries")

    def _parse_api_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        if not data:
            return items
        articles = data.get("articles") or []
        for art in articles:
            # Heuristic: try to extract company mentions from title or description
            title = art.get("title") or ""
            desc = art.get("description") or ""
            # Very simple: look for Capitalized Phrases of length >=2 words
            import re

            text = f"{title} {desc}"
            matches = re.findall(r"([A-Z][A-Za-z0-9&\-.]+(?:\s+[A-Z][A-Za-z0-9&\-.]+)+)", text)
            for m in set(matches):
                if 3 <= len(m) <= 100:
                    items.append(
                        {
                            "company_name": m,
                            "website": None,
                            "industry": None,
                            "hq": None,
                            "founding_date": None,
                            "description": title.strip() or desc.strip(),
                            "status": None,
                            "investment": {},
                            "source_links": [art.get("url")] if art.get("url") else [],
                        }
                    )
        return items

    def find_portfolio(self, fund_input: str) -> List[Dict[str, Any]]:
        # If API key available, call NewsAPI; otherwise return a stub
        if self.api_key:
            try:
                resp = self._call_api(fund_input)
                parsed = self._parse_api_response(resp)
                if parsed:
                    return parsed
                logger.info("News API parsed no items; falling back to stub")
            except Exception as e:
                logger.warning("News API error: %s -- falling back to stub", e)

        # Fallback stub data
        return [
            {
                "company_name": "Gamma Health",
                "website": "https://gammahealth.example",
                "industry": "Healthcare",
                "hq": "Boston, MA",
                "founding_date": "2016-04-01",
                "description": "Healthcare analytics startup.",
                "status": "active",
                "investment": {
                    "round_type": "Series B",
                    "date": "2019-05-20",
                    "amount": "$12,000,000",
                    "co_investors": [fund_input],
                    "source_links": ["https://news.example/gamma"],
                },
                "source_links": ["https://news.example/gamma"],
            },
            {
                "company_name": "Delta Logistics",
                "website": "https://deltalogistics.example",
                "industry": "Logistics",
                "hq": "Chicago, IL",
                "founding_date": "2012-08-10",
                "description": "Last-mile logistics provider.",
                "status": "active",
                "investment": {
                    "round_type": "Seed",
                    "date": "2013-09-01",
                    "amount": "$300,000",
                    "co_investors": [],
                    "source_links": ["https://news.example/delta"],
                },
                "source_links": ["https://news.example/delta"],
            },
        ]

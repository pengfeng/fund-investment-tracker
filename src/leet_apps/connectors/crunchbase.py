"""
Crunchbase connector for MVP (improved).

Behavior:
- If an API key is provided (via constructor or CRUNCHBASE_API_KEY env var), attempt to use the Crunchbase API (simple client).
- Otherwise, fall back to the existing stub sample data.

Notes:
- This implementation is defensive and designed for unit testing: the actual HTTP call is small and the parsing is tolerant.
- Rate limiting and caching should be added at a higher level; here we include a simple sleep backoff for retries.
"""
from typing import List, Dict, Any
import os
import time
import logging

import requests

logger = logging.getLogger(__name__)


class CrunchbaseConnector:
    def __init__(self, api_key: str = None, max_retries: int = 2, backoff_seconds: float = 1.0):
        self.api_key = api_key or os.environ.get("CRUNCHBASE_API_KEY")
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    def _call_api(self, query: str) -> Dict[str, Any]:
        """Make a simple GET request to the Crunchbase API.

        This function is intentionally generic so unit tests can mock requests.get.
        """
        # Hypothetical Crunchbase API endpoint -- the exact endpoint and params may vary.
        url = "https://api.crunchbase.com/v3.1/odm-organizations"
        params = {"query": query, "user_key": self.api_key}

        attempt = 0
        while attempt <= self.max_retries:
            try:
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200:
                    return resp.json()
                else:
                    logger.warning("Crunchbase API returned status %s: %s", resp.status_code, resp.text)
            except requests.RequestException as e:
                logger.warning("Crunchbase API request failed: %s", e)

            attempt += 1
            time.sleep(self.backoff_seconds * attempt)

        raise RuntimeError("Crunchbase API request failed after retries")

    def _parse_api_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert Crunchbase API response into the internal raw record format used by the normalizer.

        This is best-effort parsing; if the structure differs, we fall back to empty list.
        """
        items = []
        if not data:
            return items

        # Crunchbase API responses may be nested under data -> items or data -> items -> ...
        # We'll try a few common shapes.
        payload = data.get("data") or data
        # Try known structures
        if isinstance(payload, dict) and "items" in payload:
            entries = payload.get("items") or []
            for ent in entries:
                # Each entry may contain a 'path' or 'properties'
                props = ent.get("properties") if isinstance(ent, dict) else None
                if props:
                    items.append(self._map_props_to_raw(props))
        return items

    def _map_props_to_raw(self, props: Dict[str, Any]) -> Dict[str, Any]:
        # Map common Crunchbase fields to our raw format. This mapping is tolerant.
        return {
            "company_name": props.get("name") or props.get("organization_name"),
            "website": props.get("homepage_url"),
            "industry": props.get("primary_organization_type") or props.get("short_description"),
            "hq": next((v for k, v in props.items() if k in ("city", "region", "region_name", "location")), None),
            "founding_date": props.get("founded_on"),
            "description": props.get("short_description") or props.get("description"),
            "status": props.get("status") or props.get("organization_status"),
            "investment": props.get("last_funding_on") and {
                "round_type": props.get("last_funding_type"),
                "date": props.get("last_funding_on"),
                "amount": props.get("last_funding_total"),
                "co_investors": [],
                "source_links": [props.get("homepage_url")] if props.get("homepage_url") else [],
            },
            "source_links": [props.get("homepage_url")] if props.get("homepage_url") else [],
        }

    def find_portfolio(self, fund_input: str) -> List[Dict[str, Any]]:
        """Return a list of raw company/investment records for the given fund.

        If an API key is configured, attempt to query Crunchbase. Otherwise return a small stub dataset
        used for development and tests.
        """
        # Use API path if possible
        if self.api_key:
            try:
                resp = self._call_api(fund_input)
                parsed = self._parse_api_response(resp)
                if parsed:
                    return parsed
                # If parsing yields nothing, fall back to stub
                logger.info("Crunchbase API returned no parsed items; falling back to stub data")
            except Exception as e:
                logger.warning("Crunchbase API error: %s -- falling back to stub", e)

        # Fallback stub data (same as original MVP stub)
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
                    "source_links": ["https://example.com/article1"],
                },
                "source_links": ["https://crunchbase.com/org/acme-robotics"],
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
                    "source_links": ["https://example.com/article2"],
                },
                "source_links": ["https://crunchbase.com/org/beta-analytics"],
            },
        ]

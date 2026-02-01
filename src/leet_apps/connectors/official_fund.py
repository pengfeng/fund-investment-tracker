"""
Simple connector that scrapes an official fund profile page (if a URL is given) and
extracts listed portfolio companies by looking for common patterns ("portfolio", "companies").

This is intentionally minimal and robust for tests: if given a non-URL fund_input it returns []
or can be passed a test HTML string in the `test_html` param (used in unit tests).
"""
from typing import List, Dict, Any
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class OfficialFundConnector:
    def __init__(self, test_html: str = None):
        self.test_html = test_html

    def _is_url(self, s: str) -> bool:
        try:
            p = urlparse(s)
            return p.scheme in ("http", "https") and p.netloc != ""
        except Exception:
            return False

    def find_portfolio(self, fund_input: str) -> List[Dict[str, Any]]:
        # If fund_input is not a URL, we don't attempt to guess the official page.
        if not self._is_url(fund_input) and not self.test_html:
            return []

        html = self.test_html
        if not html:
            resp = requests.get(fund_input, timeout=10)
            resp.raise_for_status()
            html = resp.text

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" \n ")

        # Find portfolio section heuristically
        # split into lines and find lines under headings containing 'portfolio' or 'companies'
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        candidates = []
        for i, line in enumerate(lines):
            if re.search(r"portfolio|companies|investments", line, re.I):
                # collect some lines after the heading
                for j in range(i + 1, min(i + 10, len(lines))):
                    if len(lines[j]) < 200:
                        candidates.append(lines[j])

        # Extract names using capitalized words heuristic (very simple)
        names = set()
        for c in candidates:
            for match in re.findall(r"([A-Z][A-Za-z0-9&\-\.]+(?:\s+[A-Z][A-Za-z0-9&\-\.]+)+)", c):
                # Filter short matches
                if 3 <= len(match) <= 100:
                    names.add(match.strip())

        results = []
        for n in sorted(names):
            results.append({
                "company_name": n,
                "website": None,
                "industry": None,
                "hq": None,
                "founding_date": None,
                "description": None,
                "status": None,
                "investment": {},
                "source_links": [fund_input] if not self.test_html else [],
            })

        return results

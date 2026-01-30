"""
Orchestrator coordinates connectors to gather portfolio data for a fund.

For MVP this orchestrator:
- Loads enabled connectors (currently only CrunchbaseConnector)
- Calls each connector to fetch raw records
- Deduplicates records by company_name
- Returns combined normalized output by calling normalize_results

This is intentionally simple to keep testability high. Concurrency and caching hooks are provided in the constructor.
"""
from typing import List, Dict, Any
import logging

from leet_apps.connectors.crunchbase import CrunchbaseConnector
from leet_apps.normalizer import normalize_results

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, connectors: List[Any] = None, max_workers: int = 1):
        # connectors is a list of connector instances; if None, instantiate default connectors
        if connectors is None:
            connectors = [CrunchbaseConnector()]
        self.connectors = connectors
        self.max_workers = max_workers

    def _collect_from_connector(self, connector, fund_input: str) -> List[Dict[str, Any]]:
        try:
            return connector.find_portfolio(fund_input)
        except Exception as e:
            logger.warning("Connector %s failed: %s", connector.__class__.__name__, e)
            return []

    def _dedupe(self, raw_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        out = []
        for r in raw_records:
            name = (r.get("company_name") or "").strip().lower()
            if not name:
                # assign synthetic key
                key = id(r)
            else:
                key = name
            if key in seen:
                # could merge records here; for now skip duplicates
                continue
            seen.add(key)
            out.append(r)
        return out

    def run(self, fund_input: str) -> Dict[str, Any]:
        raw_accumulator: List[Dict[str, Any]] = []
        for conn in self.connectors:
            logger.info("Running connector %s", conn.__class__.__name__)
            records = self._collect_from_connector(conn, fund_input)
            if records:
                raw_accumulator.extend(records)

        deduped = self._dedupe(raw_accumulator)
        # Use normalizer to produce unified model
        normalized = normalize_results(deduped, fund_input)
        return normalized


# Convenience function
def run_for_fund(fund_input: str) -> Dict[str, Any]:
    orch = Orchestrator()
    return orch.run(fund_input)

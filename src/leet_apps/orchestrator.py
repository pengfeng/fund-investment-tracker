"""
Orchestrator: coordinate connector execution, aggregation, and simple deduplication.

This is an MVP implementation intended to:
- Register connectors (each exposing find_portfolio(fund_input) -> List[Dict])
- Execute connectors (optionally in parallel) and gather results
- Merge/deduplicate company records by company_name (case-insensitive)
- Return a flattened list of raw records suitable for normalization

Concurrency and retry behavior are configurable via src/leet_apps/config.yaml.
"""
from typing import List, Dict, Any
import logging
import yaml
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


def _load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


class Orchestrator:
    def __init__(self, connectors: List[Any] = None):
        self.connectors = connectors or []
        self.config = _load_config()
        self.max_workers = self.config.get("concurrency", {}).get("max_workers", 4)

    def add_connector(self, connector: Any):
        self.connectors.append(connector)

    def _run_connector(self, connector, fund_input: str) -> List[Dict[str, Any]]:
        try:
            return connector.find_portfolio(fund_input) or []
        except Exception as e:
            logger.warning("Connector %s failed: %s", getattr(connector, "__class__", type(connector)), e)
            return []

    def run(self, fund_input: str) -> List[Dict[str, Any]]:
        """Execute all connectors and return a deduplicated list of raw company records.

        Deduplication key: normalized company_name (lowercase, stripped). If company_name missing,
        the record is included as-is with a generated placeholder id handled later by normalizer.
        """
        results = []
        if not self.connectors:
            return results

        # Run connectors in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            futures = {ex.submit(self._run_connector, c, fund_input): c for c in self.connectors}
            for fut in as_completed(futures):
                try:
                    r = fut.result()
                    if r:
                        results.extend(r)
                except Exception as e:
                    logger.warning("Error collecting connector result: %s", e)

        # Deduplicate by company_name
        seen = {}
        deduped = []
        for rec in results:
            name = rec.get("company_name")
            if name:
                key = name.strip().lower()
            else:
                # fallback: include record (no dedup key)
                key = None

            if key:
                if key in seen:
                    # merge source_links and investment info conservatively
                    existing = seen[key]
                    # merge source_links
                    existing_links = set(existing.get("source_links", []))
                    for l in rec.get("source_links", []):
                        if l:
                            existing_links.add(l)
                    existing["source_links"] = list(existing_links)
                    # merge investment.source_links
                    existing_inv = existing.get("investment") or {}
                    rec_inv = rec.get("investment") or {}
                    inv_links = set(existing_inv.get("source_links", []))
                    for l in rec_inv.get("source_links", []):
                        if l:
                            inv_links.add(l)
                    if rec_inv:
                        merged_inv = {**existing_inv, **rec_inv}
                        merged_inv["source_links"] = list(inv_links)
                        existing["investment"] = merged_inv
                else:
                    seen[key] = rec.copy()
                    deduped.append(seen[key])
            else:
                # no name, include raw
                deduped.append(rec)

        return deduped

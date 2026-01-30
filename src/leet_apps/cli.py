#!/usr/bin/env python3
"""
CLI entrypoint for fund-investment-tracker (MVP)
"""
import argparse
import json
import sys
from typing import Dict, Any

from leet_apps.connectors.crunchbase import CrunchbaseConnector
from leet_apps.normalizer import normalize_results


def parse_args():
    parser = argparse.ArgumentParser(description="Fund Investment Tracker CLI (MVP)")
    parser.add_argument("--fund", required=True, help="Fund name, identifier, or profile URL")
    parser.add_argument("--output", required=False, help="Output file path (without extension)")
    parser.add_argument("--format", required=False, choices=["json", "csv"], default="json", help="Output format: json or csv (csv will produce two files)")
    return parser.parse_args()


def main(argv=None):
    args = parse_args()
    fund_input = args.fund

    # Use orchestrator to allow multiple connectors and deduplication
    from leet_apps.orchestrator import Orchestrator

    orchestrator = Orchestrator(connectors=[CrunchbaseConnector()])
    raw = orchestrator.run(fund_input)

    # Orchestrator may return normalized data (dict) or a raw list of records
    if isinstance(raw, dict) and "companies" in raw:
        normalized = raw
    else:
        normalized = normalize_results(raw, fund_input)

    # Use exporter for output
    if args.output:
        out_path = args.output
        if args.format == "json":
            from leet_apps.exporter import export_json

            export_json(normalized, out_path + ".json")
            print(f"Wrote JSON output to {out_path}.json")
        else:
            from leet_apps.exporter import export_csv

            export_csv(normalized, out_path)
            print(f"Wrote CSV outputs to {out_path}_companies.csv and {out_path}_investments.csv")
    else:
        # Print JSON to stdout for readability
        print(json.dumps(normalized, indent=2))


if __name__ == "__main__":
    main()

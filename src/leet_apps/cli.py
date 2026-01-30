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
    parser.add_argument("--output", required=False, help="Output file path (json)")
    return parser.parse_args()


def main(argv=None):
    args = parse_args()
    fund_input = args.fund

    connector = CrunchbaseConnector()
    raw = connector.find_portfolio(fund_input)

    normalized = normalize_results(raw)

    output = json.dumps(normalized, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Wrote output to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()

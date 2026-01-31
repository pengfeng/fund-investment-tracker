import argparse
import json
import os
from leet_apps.connectors.crunchbase import CrunchbaseConnector
from leet_apps.orchestrator import run_for_fund
from leet_apps import exporter


def main():
    parser = argparse.ArgumentParser(description="Fund Investment Tracker CLI")
    parser.add_argument("--fund", required=True, help="Fund name or identifier")
    parser.add_argument("--output", help="Output path (for json use .json or provide --format json). If omitted prints JSON to stdout.")
    parser.add_argument("--format", choices=["json", "csv"], default=None, help="Output format (json or csv). If not provided, inferred from --output extension or defaults to json.")
    args = parser.parse_args()

    # Use orchestrator to run default connectors and normalize results
    data = run_for_fund(args.fund)

    # Determine format
    out_format = args.format
    if not out_format:
        if args.output and str(args.output).lower().endswith('.csv'):
            out_format = 'csv'
        else:
            out_format = 'json'

    if args.output:
        out_path = args.output
        # If user passed a path without extension for json, add .json
        if out_format == 'json':
            if not str(out_path).lower().endswith('.json'):
                out_path = str(out_path) + '.json'
            exporter.export_json(data, out_path)
            print(f"Wrote JSON output to {out_path}")
        else:
            # csv exporter writes files with suffixes
            # ensure base path does not have .csv extension
            base = str(out_path)
            if base.lower().endswith('.csv'):
                base = os.path.splitext(base)[0]
            exporter.export_csv(data, base)
            print(f"Wrote CSV outputs to {base}_companies.csv and {base}_investments.csv")
    else:
        # print JSON to stdout
        print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()

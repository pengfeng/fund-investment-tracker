import argparse
import json
from leet_apps.connectors.crunchbase import CrunchbaseConnector


def main():
    parser = argparse.ArgumentParser(description="Fund Investment Tracker CLI")
    parser.add_argument("--fund", required=True, help="Fund name or identifier")
    parser.add_argument("--output", help="Output file (json or csv)")
    args = parser.parse_args()

    connector = CrunchbaseConnector()
    results = connector.find_portfolio_by_fund(args.fund)

    if args.output:
        if args.output.endswith('.json'):
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
        else:
            # simple CSV export
            import csv
            keys = set()
            for c in results:
                keys.update(c.keys())
            keys = list(keys)
            with open(args.output, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for c in results:
                    writer.writerow(c)
    else:
        print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

"""
Exporter module: supports JSON (existing) and CSV export for MVP.
"""
from typing import Dict, Any
import csv
import json


def export_json(data: Dict[str, Any], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def export_csv(data: Dict[str, Any], path: str):
    # Exports companies and investments into two CSV files: <path>_companies.csv and <path>_investments.csv
    companies = data.get("companies", [])
    investments = data.get("investments", [])

    companies_path = f"{path}_companies.csv"
    investments_path = f"{path}_investments.csv"

    if companies:
        with open(companies_path, "w", newline="", encoding="utf-8") as cf:
            writer = csv.DictWriter(cf, fieldnames=["id", "name", "website", "industry", "hq", "founding_date", "description", "status"])
            writer.writeheader()
            for c in companies:
                writer.writerow({k: c.get(k, "") for k in writer.fieldnames})

    if investments:
        with open(investments_path, "w", newline="", encoding="utf-8") as inf:
            writer = csv.DictWriter(inf, fieldnames=["fund_id", "company_id", "round_type", "date", "amount", "co_investors", "confidence"])
            writer.writeheader()
            for inv in investments:
                row = {k: inv.get(k, "") for k in writer.fieldnames}
                # co_investors may be a list; join into string
                if isinstance(row.get("co_investors"), list):
                    row["co_investors"] = ";".join(row["co_investors"])
                writer.writerow(row)

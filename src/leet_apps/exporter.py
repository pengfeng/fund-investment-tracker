"""
Exporter module: supports JSON (existing) and CSV export for MVP.
"""
import csv
import json
from typing import Any, Dict


def generate_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a simple summary report for the normalized data model.

    Summary includes counts and basic aggregates useful for analysts.
    """
    fund = data.get("fund", {})
    companies = data.get("companies", []) or []
    investments = data.get("investments", []) or []

    total_companies = len(companies)
    total_investments = len(investments)

    # Compute industry distribution
    industry_counts = {}
    for c in companies:
        ind = c.get("industry") or "unknown"
        industry_counts[ind] = industry_counts.get(ind, 0) + 1

    # Status distribution
    status_counts = {}
    for c in companies:
        st = c.get("status") or "unknown"
        status_counts[st] = status_counts.get(st, 0) + 1

    # Source links count (unique)
    source_links = set()
    for c in companies:
        for s in c.get("source_links", []) or []:
            source_links.add(s)
    for inv in investments:
        for s in inv.get("source_links", []) or []:
            source_links.add(s)

    summary = {
        "fund_id": fund.get("id"),
        "total_companies": total_companies,
        "total_investments": total_investments,
        "unique_source_links": len(source_links),
        "industry_counts": industry_counts,
        "status_counts": status_counts,
    }
    return summary


def export_json(data: Dict[str, Any], path: str):
    # Include a generated summary when exporting JSON
    data_with_summary = dict(data)
    try:
        data_with_summary["summary"] = generate_summary(data)
    except Exception:
        # If summary generation fails, fall back to original data
        data_with_summary = data

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_with_summary, f, indent=2)


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

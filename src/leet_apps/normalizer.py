"""
Normalize raw connector output into the project's data model.
"""
from typing import List, Dict, Any
import uuid


def normalize_company(raw: Dict[str, Any]) -> Dict[str, Any]:
    company_id = raw.get("company_name") or str(uuid.uuid4())
    return {
        "id": company_id,
        "name": raw.get("company_name"),
        "website": raw.get("website"),
        "industry": raw.get("industry"),
        "hq": raw.get("hq"),
        "founding_date": raw.get("founding_date"),
        "description": raw.get("description"),
        "status": raw.get("status"),
        "source_links": raw.get("source_links", []),
    }


def normalize_investment(raw: Dict[str, Any], fund_id: str) -> Dict[str, Any]:
    inv = raw.get("investment", {})
    return {
        "fund_id": fund_id,
        "company_id": raw.get("company_name"),
        "round_type": inv.get("round_type"),
        "date": inv.get("date"),
        "amount": inv.get("amount"),
        "co_investors": inv.get("co_investors", []),
        "source_links": inv.get("source_links", []),
        "confidence": 0.8,
    }


def normalize_results(raw_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    fund_id = "unknown-fund"
    companies = []
    investments = []
    for raw in raw_list:
        companies.append(normalize_company(raw))
        investments.append(normalize_investment(raw, fund_id))
    return {"fund": {"id": fund_id}, "companies": companies, "investments": investments}

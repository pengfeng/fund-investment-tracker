"""
Normalize raw connector output into the project's data model.
"""
import uuid
from typing import Any, Dict, List


def normalize_company(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a raw company record and provide per-field confidence scores.

    The normalized company keeps backward-compatible top-level fields and adds
    a `field_confidence` dict mapping each normalized field to a confidence
    score in [0.0, 1.0].
    """
    company_id = raw.get("company_name") or str(uuid.uuid4())
    # Map raw fields to normalized fields
    name = raw.get("company_name")
    website = raw.get("website")
    industry = raw.get("industry")
    hq = raw.get("hq")
    founding_date = raw.get("founding_date")
    description = raw.get("description")
    status = raw.get("status")
    source_links = raw.get("source_links", [])

    # Simple confidence heuristic: present -> 1.0, missing -> 0.0
    field_confidence = {
        "name": 1.0 if name else 0.0,
        "website": 1.0 if website else 0.0,
        "industry": 1.0 if industry else 0.0,
        "hq": 1.0 if hq else 0.0,
        "founding_date": 1.0 if founding_date else 0.0,
        "description": 1.0 if description else 0.0,
        "status": 1.0 if status else 0.0,
    }

    return {
        "id": company_id,
        "name": name,
        "website": website,
        "industry": industry,
        "hq": hq,
        "founding_date": founding_date,
        "description": description,
        "status": status,
        "source_links": source_links,
        "field_confidence": field_confidence,
    }


def normalize_investment(raw: Dict[str, Any], fund_id: str) -> Dict[str, Any]:
    """Normalize investment information and provide per-field confidence and sources."""
    inv = raw.get("investment", {})
    round_type = inv.get("round_type")
    date = inv.get("date")
    amount = inv.get("amount")
    co_investors = inv.get("co_investors", [])
    investor_role = inv.get("investor_role")
    source_links = inv.get("source_links", [])

    # Confidence heuristic: present fields get 1.0, missing 0.0. Overall confidence is average.
    field_conf = {
        "round_type": 1.0 if round_type else 0.0,
        "date": 1.0 if date else 0.0,
        "amount": 1.0 if amount else 0.0,
        "co_investors": 1.0 if co_investors else 0.0,
        "investor_role": 1.0 if investor_role else 0.0,
    }
    overall_confidence = sum(field_conf.values()) / max(len(field_conf), 1)

    return {
        "fund_id": fund_id,
        "company_id": raw.get("company_name"),
        "round_type": round_type,
        "date": date,
        "amount": amount,
        "co_investors": co_investors,
        "investor_role": investor_role,
        "source_links": source_links,
        "field_confidence": field_conf,
        "confidence": overall_confidence,
    }


def normalize_results(raw_list: List[Dict[str, Any]], fund_name: str = "unknown-fund") -> Dict[str, Any]:
    fund_id = fund_name
    companies = []
    investments = []
    for raw in raw_list:
        companies.append(normalize_company(raw))
        investments.append(normalize_investment(raw, fund_id))
    return {"fund": {"id": fund_id}, "companies": companies, "investments": investments}

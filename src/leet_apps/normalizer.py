"""
Normalize raw connector output into the project's data model.
"""
import uuid
from typing import Any, Dict, List, Optional, Tuple
import re
from datetime import datetime


def _parse_amount(amount: Optional[str]) -> Tuple[Optional[float], Optional[str]]:
    """Best-effort parse of an amount string into a numeric value and currency.

    Returns (value, currency) where value is a float (or None) and currency is a string like 'USD' or None.
    Handles common formats like "$5,000,000", "USD 5M", "5 million", "€2.5M", "£300k".
    """
    if not amount:
        return None, None
    s = str(amount).strip()

    # Detect currency symbol or code
    currency = None
    # Common symbols
    if s.startswith("$"):
        currency = "USD"
        s = s[1:].strip()
    elif s.startswith("€"):
        currency = "EUR"
        s = s[1:].strip()
    elif s.startswith("£"):
        currency = "GBP"
        s = s[1:].strip()
    else:
        # Check for 3-letter currency code prefix
        m = re.match(r"^([A-Z]{3})\s+", s)
        if m:
            currency = m.group(1)
            s = s[m.end():]

    # Normalize textual multipliers
    s_low = s.lower()
    multiplier = 1.0
    if 'billion' in s_low:
        multiplier = 1e9
        s_low = s_low.replace('billion', '')
    elif 'million' in s_low:
        multiplier = 1e6
        s_low = s_low.replace('million', '')
    elif 'thousand' in s_low:
        multiplier = 1e3
        s_low = s_low.replace('thousand', '')

    # Check suffix multipliers like 5M, 5k, 2.5B
    suf = re.search(r"([kmb])\b", s_low)
    if suf:
        suf_ch = suf.group(1).lower()
        if suf_ch == 'k':
            multiplier = 1e3
        elif suf_ch == 'm':
            multiplier = 1e6
        elif suf_ch == 'b':
            multiplier = 1e9
        # remove suffix
        s_low = re.sub(r"([0-9\.,]+)\s*[kmb]\b", r"\1", s_low, flags=re.I)

    # Extract numeric portion
    num_match = re.search(r"([0-9\.,]+)", s_low)
    if not num_match:
        return None, currency
    num_str = num_match.group(1)
    # Remove commas
    num_str = num_str.replace(',', '')
    try:
        val = float(num_str) * multiplier
        return val, currency
    except Exception:
        return None, currency


def _parse_date(date_str: Optional[str]) -> Optional[str]:
    """Normalize date strings to YYYY-MM-DD when possible. If parsing fails, return the original string.
    """
    if not date_str:
        return None
    s = str(date_str).strip()
    # Common ISO-like pattern
    try:
        if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
            return s
        # Try parsing YYYY-MM
        if re.match(r"^\d{4}-\d{2}$", s):
            return s + "-01"
        # Try year only
        if re.match(r"^\d{4}$", s):
            return s + "-01-01"
        # Fallback: try datetime.fromisoformat for extended cases
        try:
            dt = datetime.fromisoformat(s)
            return dt.date().isoformat()
        except Exception:
            # Try common delimited formats
            for fmt in ("%m/%d/%Y", "%d/%m/%Y", "%b %d, %Y", "%B %d, %Y"):
                try:
                    dt = datetime.strptime(s, fmt)
                    return dt.date().isoformat()
                except Exception:
                    continue
    except Exception:
        pass
    # If all parsing fails, return original
    return s


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
    founding_date = _parse_date(raw.get("founding_date")) if raw.get("founding_date") else None
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
    inv = raw.get("investment", {}) or {}
    round_type = inv.get("round_type")
    date = _parse_date(inv.get("date")) if inv.get("date") else None
    amount = inv.get("amount")
    amount_value, amount_currency = _parse_amount(amount)
    co_investors = inv.get("co_investors", []) or []
    investor_role = inv.get("investor_role")
    source_links = inv.get("source_links", []) or []

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
        "amount_value": amount_value,
        "amount_currency": amount_currency,
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

import os
from leet_apps.exporter import export_json, export_csv


def test_export_json(tmp_path):
    data = {"fund": {"id": "f1"}, "companies": [{"id": "c1", "name": "Co"}], "investments": [{"fund_id": "f1", "company_id": "c1", "round_type": "Seed", "date": "2020-01-01", "amount": "$100k", "co_investors": [], "confidence": 0.9}]}
    p = tmp_path / "out.json"
    export_json(data, str(p))
    assert p.exists()
    content = p.read_text()
    assert '"fund"' in content


def test_export_csv(tmp_path):
    data = {"fund": {"id": "f1"}, "companies": [{"id": "c1", "name": "Co", "website": "https://co", "industry": "Tech", "hq": "SF", "founding_date": "2020-01-01", "description": "desc", "status": "active"}], "investments": [{"fund_id": "f1", "company_id": "c1", "round_type": "Seed", "date": "2020-01-01", "amount": "$100k", "co_investors": ["X"], "confidence": 0.9}]}
    p = tmp_path / "out"
    export_csv(data, str(p))
    comp = str(p) + "_companies.csv"
    inv = str(p) + "_investments.csv"
    assert os.path.exists(comp)
    assert os.path.exists(inv)
    # Basic content checks
    assert 'Co' in open(comp).read()
    assert 'Seed' in open(inv).read()

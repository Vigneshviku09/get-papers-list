import os
import csv
import tempfile
import pytest
from get_papers.src.exporter import export_to_csv

SAMPLE_DATA = [
    {
        "pubmed_id": "12345678",
        "title": "CRISPR and Genomics: A Revolution",
        "pub_date": "2023",
        "non_academic_authors": ["Alice Biotech", "Bob Pharma"],
        "company_affiliations": ["Genentech Inc.", "Pfizer Ltd"],
        "corresponding_email": "alice@genentech.com"
    },
    {
        "pubmed_id": "87654321",
        "title": "RNA Therapeutics and Delivery 🧬",
        "pub_date": "2022",
        "non_academic_authors": ["Dr. Zhang"],
        "company_affiliations": ["Moderna Therapeutics"],
        "corresponding_email": "zhang@moderna.com"
    }
]

def test_export_to_csv_successful_write():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="r+", encoding="utf-8") as tmp:
        filename = tmp.name
        export_to_csv(SAMPLE_DATA, filename)
        tmp.seek(0)
        content = tmp.read()
        assert "CRISPR and Genomics" in content
        assert "alice@genentech.com" in content
        assert "RNA Therapeutics" in content
        assert "🧬" in content  # Ensure special characters are preserved
    os.unlink(filename)

def test_export_to_csv_empty_list():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="r+", encoding="utf-8") as tmp:
        filename = tmp.name
        export_to_csv([], filename)
        tmp.seek(0)
        content = tmp.read()
        assert "PubmedID" in content  # Header must still be written
        assert len(content.strip().splitlines()) == 1  # Only header line
    os.unlink(filename)

def test_export_to_csv_file_permission_error(monkeypatch):
    def raise_ioerror(*args, **kwargs):
        raise IOError("Mocked file permission error")

    monkeypatch.setattr("builtins.open", raise_ioerror)

    with pytest.raises(IOError):
        export_to_csv(SAMPLE_DATA, "mock_output.csv")

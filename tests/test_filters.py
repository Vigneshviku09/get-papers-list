import pytest
from get_papers.src.filters import is_non_academic, is_company_affiliation

@pytest.mark.parametrize("affiliation, expected", [
    # Clearly academic
    ("Harvard University", False),
    ("Massachusetts General Hospital", False),
    ("Stanford School of Medicine", False),
    ("Oxford College", False),
    ("Max Planck Institute", False),
    ("Center for Infectious Disease", False),
    ("Centre for Immunology", False),

    # Clearly company
    ("Pfizer Inc.", True),
    ("Genentech", True),
    ("Moderna Therapeutics", True),
    ("Novartis Pharma AG", True),
    ("Illumina Biosciences", True),
    ("BioGenomics Ltd", True),
    ("Roche GmbH", True),
    ("CureTech Biotech", True),

    # Ambiguous / Mixed
    ("Pfizer Inc. and Harvard University", False),
    ("Department of Oncology, Novartis AG", False),
    ("BioGen GmbH, School of Medicine", False),

    # No keywords
    ("Random Healthcare Startup", True),
    ("Nonprofit Research Group", True),
    ("Innovation Labs", True),
    ("", True),  # No academic keyword = non-academic
    ("Unknown", True),

    # Edge case: case-insensitive matching
    ("genentech", True),
    ("GENENTECH", True),
    ("University of genentech", False),
])
def test_is_non_academic(affiliation, expected):
    result = is_non_academic(affiliation)
    assert result == expected, f"is_non_academic failed for: '{affiliation}'"


@pytest.mark.parametrize("affiliation, expected", [
    # Clearly company
    ("Pfizer Inc.", True),
    ("Novartis Pharma AG", True),
    ("Genentech", True),
    ("Moderna Therapeutics", True),
    ("Illumina Biosciences", True),
    ("BioGenomics Ltd", True),
    ("Roche GmbH", True),
    ("Amgen Inc", True),
    ("CureTech Biotech", True),

    # Academic
    ("Harvard University", False),
    ("Oxford College", False),
    ("Stanford School of Medicine", False),
    ("Hospital of Paris", False),
    ("Center for Infection Biology", False),
    ("University of Delhi", False),

    # Mixed
    ("Moderna and Stanford University", True),
    ("BioTech AG, Department of Oncology", True),

    # Empty / edge
    ("", False),
    ("Random Foundation", False),
    ("Unknown", False),

    # Case-insensitive
    ("genentech", True),
    ("GENENTECH", True),
    ("biotech", True),
    ("BIOSCIENCES", True),
])
def test_is_company_affiliation(affiliation, expected):
    result = is_company_affiliation(affiliation)
    assert result == expected, f"is_company_affiliation failed for: '{affiliation}'"

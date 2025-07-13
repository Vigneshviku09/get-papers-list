def is_non_academic(affiliation: str) -> bool:
    """
    Returns True if the affiliation appears to be non-academic based on known academic keywords.
    """
    academic_keywords = [
        "university", "college", "institute", "school",
        "hospital", "center", "centre", "faculty", "department"
    ]

    # If any academic keyword is present, it's academic
    for word in academic_keywords:
        if word.lower() in affiliation.lower():
            return False
    return True  # No academic words = non-academic


def is_company_affiliation(affiliation: str) -> bool:
    """
    Returns True if the affiliation appears to belong to a pharma or biotech company.
    """
    # Common pharma/biotech indicators and suffixes
    pharma_keywords = [
        "pharma", "biotech", "therapeutics", "biosciences",
        "genomics", "inc", "ltd", "gmbh"
    ]

    # Known company names (can be expanded)
    known_companies = [
        "genentech", "moderna", "pfizer", "novartis", "roche",
        "amgen", "illumina", "astrazeneca", "biogen", "regeneron"
    ]

    affiliation_lower = affiliation.lower()

    # Match either known suffixes or known company names
    return any(word in affiliation_lower for word in pharma_keywords + known_companies)

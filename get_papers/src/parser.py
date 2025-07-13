import xml.etree.ElementTree as ET
from typing import List
from .types import PaperInfo
from .filters import is_company_affiliation, is_non_academic
import re


def extract_pub_year(article: ET.Element) -> str:
    """
    Attempts to extract the publication year from multiple possible locations in the XML.
    Falls back to parsing from MedlineDate if structured <Year> tags are missing.

    Args:
        article (ET.Element): The PubmedArticle XML element.

    Returns:
        str: A four-digit year or 'Unknown' if not found.
    """
    year_paths = [
        ".//PubDate/Year",
        ".//ArticleDate/Year",
        ".//DateCreated/Year",
        ".//JournalIssue/PubDate/Year",
        ".//PubmedData/History/PubMedPubDate/Year",
    ]

    for path in year_paths:
        year = article.findtext(path)
        if year and year.strip().isdigit():
            return year.strip()

    # Fallback: look for a year in a MedlineDate like "Spring 2022"
    medline_date = article.findtext(".//PubDate/MedlineDate")
    if medline_date:
        match = re.search(r"\b(19|20)\d{2}\b", medline_date)
        if match:
            return match.group(0)

    return "Unknown"


def parse_pubmed_xml(xml_data: str, debug: bool = False) -> List[PaperInfo]:
    """
    Parses PubMed XML data and extracts structured paper information.

    Filters for papers with at least one non-academic author and collects:
    - Title
    - PubMed ID
    - Publication year
    - Non-academic authors
    - Company affiliations
    - Corresponding author's email

    Args:
        xml_data (str): The XML string returned by PubMed EFetch API.
        debug (bool): If True, prints debug messages.

    Returns:
        List[PaperInfo]: A list of structured paper dictionaries.
    """
    papers: List[PaperInfo] = []

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        if debug:
            print(f"[XML Parse Error] Failed to parse XML: {e}")
        return []

    for article in root.findall(".//PubmedArticle"):
        try:
            title = article.findtext(".//ArticleTitle") or "N/A"
            pubmed_id = article.findtext(".//PMID") or "N/A"
            pub_date = extract_pub_year(article)

            non_acad_authors = []
            company_affiliations = []
            corresponding_email = None

            for author in article.findall(".//Author"):
                fore_name = author.findtext("ForeName") or ""
                last_name = author.findtext("LastName") or ""
                name = " ".join([fore_name, last_name]).strip()

                aff = author.findtext(".//AffiliationInfo/Affiliation")
                email = None

                if aff and "@" in aff:
                    tokens = aff.replace("(", "").replace(")", "").split()
                    email_candidates = [t.strip(".,;") for t in tokens if "@" in t]
                    if email_candidates:
                        email = email_candidates[0]

                if aff:
                    if is_non_academic(aff):
                        non_acad_authors.append(name)
                    if is_company_affiliation(aff):
                        company_affiliations.append(aff)

                if email and not corresponding_email:
                    corresponding_email = email

            if non_acad_authors:
                papers.append({
                    "pubmed_id": pubmed_id,
                    "title": title,
                    "pub_date": pub_date,
                    "non_academic_authors": non_acad_authors,
                    "company_affiliations": list(set(company_affiliations)),
                    "corresponding_email": corresponding_email,
                })

        except Exception as e:
            if debug:
                print(f"[Parse Warning] Skipped article due to error: {e}")
            continue

    return papers

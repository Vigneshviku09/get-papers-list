import requests
from typing import List, Optional
from .types import PaperInfo  # Assumed to define a dataclass for structured paper info


def fetch_pubmed_ids(query: str, debug: bool = False) -> List[str]:
    """
    Fetches a list of PubMed IDs that match the given query.

    Args:
        query (str): The PubMed search query using full PubMed syntax.
        debug (bool): If True, print debug information.

    Returns:
        List[str]: A list of PubMed ID strings.

    Raises:
        ValueError: If the query is empty or invalid.
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    if not query.strip():
        raise ValueError("Query string must not be empty.")

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,        # Full PubMed query string
        "retmode": "json",    # Response format
        "retmax": 100,        # Max number of IDs to return (can increase if needed)
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()  # Raise error for 4xx/5xx responses
        data = resp.json()
        ids = data.get("esearchresult", {}).get("idlist", [])

        if debug:
            print(f"Fetched {len(ids)} PubMed IDs: {ids}")

        return ids

    except requests.exceptions.HTTPError as e:
        print(f"[HTTP Error] Failed to fetch PubMed IDs: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"[Request Error] Failed to connect to PubMed: {e}")
        raise
    except ValueError as e:
        print(f"[Parse Error] Failed to parse JSON response: {e}")
        raise


def fetch_pubmed_details(ids: List[str], debug: bool = False) -> str:
    """
    Fetches detailed metadata for a list of PubMed IDs using the EFetch API.

    Args:
        ids (List[str]): List of PubMed IDs to fetch details for.
        debug (bool): If True, print debug information.

    Returns:
        str: The XML response as a single string. Returns empty string if `ids` is empty.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    if not ids:
        if debug:
            print("No PubMed IDs provided. Skipping efetch.")
        return ""

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(ids),   # Comma-separated list of PubMed IDs
        "retmode": "xml"       # Response format: XML for parsing author, title, etc.
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()  # Raise exception for 4xx/5xx errors

        if debug:
            print(f"Fetched details for {len(ids)} PubMed IDs.")

        return resp.text

    except requests.exceptions.HTTPError as e:
        print(f"[HTTP Error] Failed to fetch PubMed details: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"[Request Error] Failed to connect to PubMed: {e}")
        raise

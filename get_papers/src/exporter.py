import csv
from typing import List
from .types import PaperInfo


def export_to_csv(papers: List[PaperInfo], filename: str) -> None:
    """
    Exports a list of parsed PubMed paper records to a CSV file.

    Args:
        papers (List[PaperInfo]): A list of structured paper data dictionaries.
        filename (str): The output CSV file path.

    Raises:
        IOError: If the file cannot be written.
        UnicodeEncodeError: If data encoding fails while writing.
    """
    try:
        with open(filename, mode="w", newline='', encoding="utf-8") as csvfile:
            # Define CSV headers
            writer = csv.DictWriter(csvfile, fieldnames=[
                "PubmedID",
                "Title",
                "Publication Date",
                "Non-academic Author(s)",
                "Company Affiliation(s)",
                "Corresponding Author Email"
            ])
            writer.writeheader()

            for paper in papers:
                writer.writerow({
                    "PubmedID": paper["pubmed_id"],
                    "Title": paper["title"],
                    "Publication Date": paper["pub_date"],
                    "Non-academic Author(s)": "; ".join(paper["non_academic_authors"]),
                    "Company Affiliation(s)": "; ".join(paper["company_affiliations"]),
                    "Corresponding Author Email": paper["corresponding_email"] or "",
                })

    except (IOError, OSError) as e:
        print(f"[File Error] Could not write to file '{filename}': {e}")
        raise
    except UnicodeEncodeError as e:
        print(f"[Encoding Error] Could not encode data for CSV export: {e}")
        raise

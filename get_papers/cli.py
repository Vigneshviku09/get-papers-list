import argparse
from get_papers.src.fetcher import fetch_pubmed_ids, fetch_pubmed_details
from get_papers.src.parser import parse_pubmed_xml
from get_papers.src.exporter import export_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed query string.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    args = parser.parse_args()

    ids = fetch_pubmed_ids(args.query, debug=args.debug)
    xml_data = fetch_pubmed_details(ids, debug=args.debug)
    papers = parse_pubmed_xml(xml_data)

    if args.file:
        export_to_csv(papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()

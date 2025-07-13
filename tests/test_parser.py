import pytest
from get_papers.src.parser import parse_pubmed_xml

MINIMAL_XML = """
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345678</PMID>
      <Article>
        <ArticleTitle>Test Paper Title</ArticleTitle>
        <AuthorList>
          <Author>
            <ForeName>John</ForeName>
            <LastName>Doe</LastName>
            <AffiliationInfo>
              <Affiliation>Genentech Inc., CA, USA. john.doe@genentech.com</Affiliation>
            </AffiliationInfo>
          </Author>
          <Author>
            <ForeName>Jane</ForeName>
            <LastName>Smith</LastName>
            <AffiliationInfo>
              <Affiliation>Harvard University, MA, USA.</Affiliation>
            </AffiliationInfo>
          </Author>
        </AuthorList>
      </Article>
      <DateCreated>
        <Year>2023</Year>
      </DateCreated>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>
"""

def test_parse_single_paper_with_company_affiliation():
    results = parse_pubmed_xml(MINIMAL_XML)
    assert len(results) == 1

    paper = results[0]
    assert paper["pubmed_id"] == "12345678"
    assert paper["title"] == "Test Paper Title"
    assert paper["pub_date"] == "2023"
    assert "John Doe" in paper["non_academic_authors"]
    assert any("genentech" in aff.lower() for aff in paper["company_affiliations"])
    assert paper["corresponding_email"] == "john.doe@genentech.com"

def test_parse_paper_with_only_academic_authors():
    xml = MINIMAL_XML.replace("Genentech Inc.", "Harvard University").replace("john.doe@genentech.com", "")
    results = parse_pubmed_xml(xml)
    assert results == []  # Should be excluded

def test_parse_paper_missing_email():
    xml = MINIMAL_XML.replace("john.doe@genentech.com", "")
    results = parse_pubmed_xml(xml)
    assert results[0]["corresponding_email"] is None

def test_parse_paper_with_multiple_emails():
    xml = MINIMAL_XML.replace(
        "john.doe@genentech.com",
        "john.doe@genentech.com jane.doe@genentech.com"
    )
    results = parse_pubmed_xml(xml)
    assert results[0]["corresponding_email"] == "john.doe@genentech.com"

def test_parse_paper_with_duplicate_company_affiliations():
    xml = MINIMAL_XML.replace("Genentech Inc.", "Genentech Inc. Genentech Inc.")
    results = parse_pubmed_xml(xml)
    affiliations = results[0]["company_affiliations"]
    assert len(set(affiliations)) == len(affiliations)  # no duplicates

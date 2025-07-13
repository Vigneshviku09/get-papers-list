from typing import List, Optional, TypedDict

class AuthorInfo(TypedDict):
    name: str
    affiliation: Optional[str]
    email: Optional[str]

class PaperInfo(TypedDict):
    pubmed_id: str
    title: str
    pub_date: str
    non_academic_authors: List[str]
    company_affiliations: List[str]
    corresponding_email: Optional[str]

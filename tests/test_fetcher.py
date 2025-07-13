import pytest
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError, JSONDecodeError
from get_papers.src.fetcher import fetch_pubmed_ids, fetch_pubmed_details

### ---------- fetch_pubmed_ids TESTS ---------- ###

@patch("get_papers.fetcher.requests.get")
def test_fetch_pubmed_ids_success(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "esearchresult": {"idlist": ["123", "456", "789"]}
    }
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    result = fetch_pubmed_ids("cancer", debug=True)
    assert result == ["123", "456", "789"]
    mock_get.assert_called_once()

@patch("get_papers.fetcher.requests.get")
def test_fetch_pubmed_ids_empty(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {
        "esearchresult": {"idlist": []}
    }
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    result = fetch_pubmed_ids("nonexistentterm", debug=True)
    assert result == []
    mock_get.assert_called_once()

@patch("get_papers.fetcher.requests.get")
def test_fetch_pubmed_ids_http_error(mock_get):
    mock_resp = Mock()
    mock_resp.raise_for_status.side_effect = HTTPError("404 error")
    mock_get.return_value = mock_resp

    with pytest.raises(HTTPError):
        fetch_pubmed_ids("errorcase")

@patch("get_papers.fetcher.requests.get")
def test_fetch_pubmed_ids_invalid_json(mock_get):
    mock_resp = Mock()
    mock_resp.raise_for_status = Mock()
    mock_resp.json.side_effect = ValueError("Invalid JSON")
    mock_get.return_value = mock_resp

    with pytest.raises(ValueError):
        fetch_pubmed_ids("badjson")


### ---------- fetch_pubmed_details TESTS ---------- ###

@patch("get_papers.fetcher.requests.get")
def test_fetch_pubmed_details_success(mock_get):
    sample_xml = "<PubmedArticleSet><PubmedArticle><PMID>123</PMID></PubmedArticle></PubmedArticleSet>"
    mock_resp = Mock()
    mock_resp.text = sample_xml
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    result = fetch_pubmed_details(["123"], debug=True)
    assert "<PMID>123</PMID>" in result
    mock_get.assert_called_once()

@patch("get_papers.fetcher.requests.get")
def test_fetch_pubmed_details_http_error(mock_get):
    mock_resp = Mock()
    mock_resp.raise_for_status.side_effect = HTTPError("500 error")
    mock_get.return_value = mock_resp

    with pytest.raises(HTTPError):
        fetch_pubmed_details(["999"])

@patch("get_papers.fetcher.requests.get")
def test_fetch_pubmed_details_empty_list(mock_get):
    result = fetch_pubmed_details([], debug=True)
    assert result == ""  # or handle empty input however you prefer
    mock_get.assert_not_called()

@patch("get_papers.fetcher.requests.get")
def test_fetch_pubmed_details_many_ids(mock_get):
    mock_resp = Mock()
    mock_resp.text = "<xml>result</xml>"
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    ids = [str(i) for i in range(100)]
    result = fetch_pubmed_details(ids)
    assert isinstance(result, str)
    assert "result" in result
    assert mock_get.call_count == 1  # or more if batching is implemented


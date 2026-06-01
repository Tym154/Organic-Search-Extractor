import pytest

from services.parser import parse_organic_results


def test_parse_organic_results_success() -> None:
    mock_raw = {
        "ads": [{"title": "Ad"}],
        "organic_results": [{"position": 1, "title": "A", "link": "https://a.com", "snippet": "B"}],
    }
    parsed = parse_organic_results(mock_raw)
    assert len(parsed) == 1
    assert parsed[0].position == 1
    assert parsed[0].title == "A"
    assert parsed[0].url == "https://a.com"


def test_parse_organic_results_empty() -> None:
    assert len(parse_organic_results({})) == 0
    assert len(parse_organic_results({"organic_results": []})) == 0


def test_parse_organic_results_missing_fields() -> None:
    mock_raw = {"organic_results": [{"position": 1}]}  # Missing title, link, snippet
    parsed = parse_organic_results(mock_raw)
    assert len(parsed) == 1
    assert parsed[0].position == 1
    assert parsed[0].title is None
    assert parsed[0].url is None


def test_parse_organic_results_invalid_structure() -> None:
    mock_raw = {"organic_results": "this is a string, not a list"}
    with pytest.raises(ValueError, match="Data parsing error"):
        parse_organic_results(mock_raw)

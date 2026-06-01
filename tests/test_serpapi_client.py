from unittest.mock import MagicMock, patch

import pytest

from config import Config
from services.serpapi_client import SerpApiError, perform_search


@patch("services.serpapi_client.GoogleSearch")
def test_perform_search_success(mock_google_search: MagicMock) -> None:
    Config.SERPAPI_API_KEY = "test_key"
    mock_instance = mock_google_search.return_value
    mock_instance.get_dict.return_value = {"organic_results": [{"title": "Test"}]}

    results = perform_search("test query")
    assert "organic_results" in results
    assert results["organic_results"][0]["title"] == "Test"


@patch("services.serpapi_client.GoogleSearch")
def test_perform_search_api_error(mock_google_search: MagicMock) -> None:
    Config.SERPAPI_API_KEY = "test_key"
    mock_instance = mock_google_search.return_value
    mock_instance.get_dict.return_value = {"error": "Invalid API Key"}

    with pytest.raises(SerpApiError, match="Invalid API Key"):
        perform_search("test query")


@patch("services.serpapi_client.GoogleSearch")
def test_perform_search_unexpected_exception(mock_google_search: MagicMock) -> None:
    Config.SERPAPI_API_KEY = "test_key"
    mock_google_search.side_effect = Exception("Connection Timeout")

    with pytest.raises(SerpApiError, match="Search provider failed: Connection Timeout"):
        perform_search("test query")


def test_perform_search_missing_key() -> None:
    Config.SERPAPI_API_KEY = None
    with pytest.raises(ValueError, match="Configuration error"):
        perform_search("test")

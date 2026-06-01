from unittest.mock import MagicMock, patch

from flask.testing import FlaskClient

from services.serpapi_client import SerpApiError


def test_search_missing_query(client: FlaskClient) -> None:
    response = client.post("/api/search", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing query parameter"}


def test_search_empty_query(client: FlaskClient) -> None:
    response = client.post("/api/search", json={"query": "   "})
    assert response.status_code == 400


def test_search_query_too_long(client: FlaskClient) -> None:
    long_query = "a" * 257
    response = client.post("/api/search", json={"query": long_query})
    assert response.status_code == 400
    assert "exceeds maximum length" in response.get_json()["error"]


@patch("routes.search.perform_search")
def test_search_success(mock_search: MagicMock, client: FlaskClient) -> None:
    mock_search.return_value = {
        "organic_results": [{"position": 1, "title": "Test", "link": "url", "snippet": "snip"}]
    }
    response = client.post("/api/search", json={"query": "test query"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["query"] == "test query"
    assert len(data["results"]) == 1


@patch("routes.search.perform_search")
def test_search_provider_error(mock_search: MagicMock, client: FlaskClient) -> None:
    mock_search.side_effect = SerpApiError("API Down")
    response = client.post("/api/search", json={"query": "test"})
    assert response.status_code == 502


@patch("routes.search.perform_search")
def test_search_unexpected_exception(mock_search: MagicMock, client: FlaskClient) -> None:
    mock_search.side_effect = Exception("Database exploded")
    response = client.post("/api/search", json={"query": "test"})
    assert response.status_code == 500
    assert response.get_json() == {"error": "An unexpected error occurred"}

import pytest
from flask.testing import FlaskClient

from app import create_app
from config import Config


def test_app_creation_success() -> None:
    app = create_app()
    assert app is not None


def test_app_creation_missing_config() -> None:
    Config.FLASK_ENV = "production"
    Config.SERPAPI_API_KEY = None

    with pytest.raises(ValueError, match="CRITICAL: SERPAPI_API_KEY is not set"):
        create_app()

    # Restore for other tests
    Config.FLASK_ENV = "testing"


def test_index_route(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert b"Google Organic Search Extractor" in response.data

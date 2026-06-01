import logging
from dataclasses import asdict
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from flask.typing import ResponseReturnValue

from models.search import SearchResponse
from services.parser import parse_organic_results
from services.serpapi_client import SerpApiError, perform_search

logger = logging.getLogger(__name__)
search_bp = Blueprint("search", __name__)

MAX_QUERY_LENGTH = 256


@search_bp.route("/api/search", methods=["POST"])
def search() -> ResponseReturnValue:
    data = request.get_json()

    # Reject missing payloads immediately.
    if not data or "query" not in data:
        logger.warning("Search request missing 'query' parameter.")
        return jsonify({"error": "Missing query parameter"}), 400

    # Stripping whitespace off the ends of the input.
    query = str(data["query"]).strip()

    # Reject empty strings
    if not query:
        logger.warning("Search request contained empty query.")
        return jsonify({"error": "Empty query parameter"}), 400

    # Reject excessively long strings
    if len(query) > MAX_QUERY_LENGTH:
        logger.warning(f"Search request exceeded length limit ({len(query)} chars).")
        return (
            jsonify({"error": f"Query exceeds maximum length of {MAX_QUERY_LENGTH} characters"}),
            400,
        )

    logger.info("Processing search request")

    try:
        raw_results = perform_search(query)
        parsed_results = parse_organic_results(raw_results)

        response_model = SearchResponse(
            query=query,
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            results=parsed_results,
        )

        return jsonify(asdict(response_model)), 200

    except ValueError as e:
        # Server configuration issue (e.g. API key missing)
        logger.error(f"Configuration or Parsing error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except SerpApiError as e:
        # The upstream provider (SerpApi) failed
        logger.error(f"Upstream API Error: {str(e)}")
        return jsonify({"error": "Search provider unavailable"}), 502
    except Exception:
        # Catch-all for unexpected crashes.
        logger.exception("An unexpected server error occurred.")
        return jsonify({"error": "An unexpected error occurred"}), 500

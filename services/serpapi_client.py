import logging
from typing import Any, Dict, cast

from serpapi import GoogleSearch

from config import Config

logger = logging.getLogger(__name__)


# Exception so we can tell if our code broke or the SerpApi failed
class SerpApiError(Exception):
    pass


def perform_search(query: str) -> Dict[str, Any]:
    # Fail the search immediately if SERPAPI_API_KEY is missing
    if not Config.SERPAPI_API_KEY:
        logger.error("Attempted search but SERPAPI_API_KEY is missing.")
        raise ValueError("Configuration error: Search provider unconfigured.")

    params = {"engine": "google", "q": query, "api_key": Config.SERPAPI_API_KEY, "num": 10}

    # SerpApi returns a 200 HTTP status even if the
    # API call failed (e.g. out of credits). So we check for an error key in the payload
    try:
        search = GoogleSearch(params)
        results: Dict[str, Any] = cast(Dict[str, Any], search.get_dict())

        if "error" in results:
            logger.error(f"SerpApi returned an error: {results['error']}")
            raise SerpApiError(results["error"])

        return cast(Dict[str, Any], results)
    except SerpApiError:
        raise
    # If something unexpected happens (e.g. network timeout)
    # log the full stack trace (.exception)
    except Exception as e:
        logger.exception("Unexpected exception occurred during SerpApi call.")
        raise SerpApiError(f"Search provider failed: {str(e)}")

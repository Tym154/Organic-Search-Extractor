import logging
from typing import Any, Dict, List

from models.search import SearchResult

logger = logging.getLogger(__name__)


# Stripping just the needed data from SerpApi's response
def parse_organic_results(raw_data: Dict[str, Any]) -> List[SearchResult]:
    try:
        organic_results = raw_data.get("organic_results", [])
        parsed = []

        for item in organic_results:
            result = SearchResult(
                position=item.get("position"),
                title=item.get("title"),
                url=item.get("link"),
                snippet=item.get("snippet"),
            )
            parsed.append(result)

        logger.debug(f"Successfully parsed {len(parsed)} organic results.")
        return parsed
    except Exception as e:
        logger.exception("Failed to parse organic results from API payload.")
        raise ValueError("Data parsing error") from e

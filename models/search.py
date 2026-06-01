from dataclasses import dataclass
from typing import List, Optional


# Model representing a single search result
@dataclass
class SearchResult:
    # Used optional values in case of empty search result (has to be handled)
    position: Optional[int]
    title: Optional[str]
    url: Optional[str]
    snippet: Optional[str]


# Model representing standard API response payload
@dataclass
class SearchResponse:
    query: str
    timestamp: str
    results: List[SearchResult]

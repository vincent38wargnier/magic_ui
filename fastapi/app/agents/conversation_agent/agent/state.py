from typing import List, TypedDict, Dict


class GraphState(TypedDict):
    messages: List[Dict[str, str]]
    search_urls: List[str]

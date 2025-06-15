from typing import List, TypedDict, Dict


class GraphState(TypedDict):
    case_description: str
    messages: List[Dict[str, str]]
    search_urls: List[str]

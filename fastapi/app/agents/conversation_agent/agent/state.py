from typing import List, TypedDict, Dict, Any


class GraphState(TypedDict):
    case_description: str
    messages: List[Dict[str, str]]
    items: List[Dict[str, Any]]

from langchain_core.tools import tool


@tool
def hello_world_tool() -> str:
    """A simple tool that returns hello world."""
    return "Hello World from UI Generator Agent!"

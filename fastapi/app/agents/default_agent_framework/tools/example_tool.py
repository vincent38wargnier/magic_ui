from langchain_core.tools import tool


@tool
def example_tool(message: str) -> str:
    """A simple example tool that processes and returns a message."""
    return f"Default Agent processed: {message}"

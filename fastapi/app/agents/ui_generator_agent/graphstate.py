from typing import TypedDict, List, Dict, Optional, Annotated, Sequence, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    conversation_id: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
    agent_id: str
    user_id: str
    user_timezone: str
    agent_config: Optional[Dict]  # Agent configuration
    recursion_count: int
    recursion_limit: int
    files: Optional[List[Dict[str, Any]]]  # List of file objects
    telegram_chat_id: Optional[str]  # Telegram chat ID for sending media
    telegram_bot_token: Optional[str]  # Telegram bot token for sending media 
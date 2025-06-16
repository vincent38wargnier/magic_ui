from typing import Optional
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from fastapi import HTTPException

from app.agents.conversation_agent.agent.nodes.query_interpreter_node import (
    query_interpreter_node,
)
from app.agents.conversation_agent.agent.state import GraphState
from crud.conversation_crud import ConversationCRUD

graph = StateGraph(GraphState)

graph.add_node("QUERY_INTERPRETER_NODE", query_interpreter_node)

graph.set_entry_point("QUERY_INTERPRETER_NODE")
graph.add_edge("QUERY_INTERPRETER_NODE", END)

app = graph.compile()


async def run_conversation_agent(
    message: str,
    user_id: str,
    user_timezone: str,
    agent_id: str,
    conversation_id: Optional[str] = None,
    telegram_id: Optional[str] = None,
):
    """Run the conversation agent workflow with a message."""
    print(f"Starting conversation agent for user {user_id}")

    # Create a simple conversation ID if not provided, or get existing one by telegram_id
    if not conversation_id:
        if telegram_id:
            # Check if there's already a conversation for this telegram user
            existing_conversation = ConversationCRUD.get_conversation_by_telegram_id(telegram_id)
            if existing_conversation:
                conversation_id = existing_conversation.id
                print(f"🔄 Using existing conversation {conversation_id} for telegram_id: {telegram_id}")
            else:
                import uuid
                conversation_id = str(uuid.uuid4())
                print(f"🆕 Creating new conversation {conversation_id} for telegram_id: {telegram_id}")
        else:
            import uuid
            conversation_id = str(uuid.uuid4())

    # Store user message in conversation using MongoDB
    print(f"💾 Storing user message in conversation: {conversation_id}")
    ConversationCRUD.add_message(conversation_id, "user", message, telegram_id)

    # Get conversation history as dictionaries
    print(f"📖 Loading conversation history for: {conversation_id}")
    messages = ConversationCRUD.get_messages(conversation_id)
    print(f"📝 Found {len(messages)} messages in conversation")

    # Simple input with just the essentials
    input_data = {
        "conversation_id": conversation_id,
        "messages": messages,
        "agent_id": agent_id,
        "user_id": user_id,
        "user_timezone": user_timezone,
        "recursion_count": 0,
        "recursion_limit": 3,
    }

    print("🚀 Running conversation agent workflow")

    try:
        result = await app.ainvoke(
            input_data,
            config=RunnableConfig(
                configurable={
                    "thread_id": conversation_id,
                    "user_id": user_id,
                    "agent_id": agent_id,
                }
            )
        )

        print("✅ Conversation agent workflow completed successfully")
        
        # Extract items and case_description from result
        items = result.get("items", [])
        case_description = result.get("case_description", "")
        
        # Create response text
        if items:
            item_descriptions = [item.get('description', 'Item') for item in items]
            final_response = f"Found {len(items)} items: {', '.join(item_descriptions[:2])}"
        else:
            final_response = "No items found."
        
        # Store agent response in conversation using MongoDB
        print(f"💾 Storing agent response in conversation: {conversation_id}")
        ConversationCRUD.add_message(conversation_id, "assistant", final_response, telegram_id)
        print(f"✅ Conversation updated successfully in MongoDB")
        
        return {
            "response": final_response, 
            "conversation_id": conversation_id,
            "items": items,
            "case_description": case_description
        }

    except Exception as e:
        print(f"❌ Error in conversation agent workflow: {e}")
        raise HTTPException(
            status_code=500, detail=f"Conversation agent error: {str(e)}"
        )

from typing import Dict, Any, Optional, List
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from fastapi import HTTPException

from app.agents.default_agent_framework.graphstate import GraphState
from app.agents.default_agent_framework.nodes.default_node import default_agent_node
from app.agents.default_agent_framework.conditionnal_edges.default_conditionnal import tools_condition
from app.agents.default_agent_framework.tools.tools_wrapper import tools_wrapper
from crud.conversation_crud import ConversationCRUD

DEFAULT_AGENT = "default_agent"

async def create_workflow():
    """Create the default agent workflow."""
    print("Creating default agent workflow")
    
    workflow = StateGraph(GraphState)
    
    # Add default agent node with async wrapper
    async def default_agent_wrapper(state: GraphState, config: RunnableConfig):
        return await default_agent_node(state, config)
    
    workflow.set_entry_point(DEFAULT_AGENT)

    workflow.add_node(DEFAULT_AGENT, action=default_agent_wrapper)
    workflow.add_node("tools", action=ToolNode(tools_wrapper))
    
    # Add conditional edges for tools
    workflow.add_conditional_edges(
        source=DEFAULT_AGENT,
        path=tools_condition,
        path_map={
            "continue": "tools",
            "finish": END,
            "end": END
        }
    )
    
    # Add edge from tools back to default agent
    workflow.add_edge("tools", DEFAULT_AGENT)
    
    print("Default agent workflow created and compiled")
    return workflow.compile()

async def run_default_agent(
    message: str,
    user_id: str,
    user_timezone: str,
    agent_id: str,
    conversation_id: Optional[str] = None
):
    """Run the default agent workflow with a message."""
    print(f"Starting default agent for user {user_id}")
    
    workflow = await create_workflow()
    
    # Create a simple conversation ID if not provided
    if not conversation_id:
        import uuid
        conversation_id = str(uuid.uuid4())
    
    # Store user message in conversation using MongoDB
    print(f"💾 Storing user message in conversation: {conversation_id}")
    ConversationCRUD.add_message(conversation_id, "user", message)
    
    # Get conversation history as LangChain messages
    print(f"📖 Loading conversation history for: {conversation_id}")
    messages = ConversationCRUD.get_langchain_messages(conversation_id)
    print(f"📝 Found {len(messages)} messages in conversation")
    
    # Simple input with just the essentials
    input = {
        "conversation_id": conversation_id,
        "messages": messages,
        "agent_id": agent_id,
        "user_id": user_id,
        "user_timezone": user_timezone,
        "agent_config": {},
        "recursion_count": 0,
        "recursion_limit": 3,  # Very simple recursion limit
        "files": [],
        "telegram_chat_id": "dummy",
        "telegram_bot_token": "dummy"
    }
    
    print("🚀 Running default agent workflow")
    
    try:
        result = await workflow.ainvoke(
            input,
            config=RunnableConfig(
                configurable={
                    "thread_id": conversation_id,
                    "user_id": user_id,
                    "agent_id": agent_id
                }
            )
        )
        
        print("✅ Default agent workflow completed successfully")
        
        # Extract the final response from messages
        final_messages = result.get("messages", [])
        if final_messages:
            last_message = final_messages[-1]
            final_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
        else:
            final_response = "Request processed successfully."
        
        # Store agent response in conversation using MongoDB
        print(f"💾 Storing agent response in conversation: {conversation_id}")
        ConversationCRUD.add_message(conversation_id, "assistant", final_response)
        print(f"✅ Conversation updated successfully in MongoDB")
        
        return {
            "response": final_response,
            "conversation_id": conversation_id
        }
        
    except Exception as e:
        print(f"❌ Error in default agent workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Default agent error: {str(e)}") 
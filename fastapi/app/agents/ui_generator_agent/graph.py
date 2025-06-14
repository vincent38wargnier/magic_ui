from typing import Dict, Any, Optional, List
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from fastapi import HTTPException

from app.agents.ui_generator_agent.graphstate import GraphState
from app.agents.ui_generator_agent.nodes.react_node import ui_generator_agent_node
from app.agents.ui_generator_agent.conditionnal_edges.react_conditionnal import tools_condition
from app.agents.ui_generator_agent.tools.tools_wrapper import tools_wrapper
from crud.conversation_crud import ConversationCRUD

REACT_GENERATOR = "ui_generator"

async def create_workflow():
    """Create the UI generator workflow."""
    print("Creating UI generator workflow")
    
    workflow = StateGraph(GraphState)
    
    # Add UI generator node with async wrapper
    async def ui_generator_wrapper(state: GraphState, config: RunnableConfig):
        return await ui_generator_agent_node(state, config)
    
    workflow.set_entry_point(REACT_GENERATOR)

    workflow.add_node(REACT_GENERATOR, action=ui_generator_wrapper)
    workflow.add_node("tools", action=ToolNode(tools_wrapper))
    
    # Add conditional edges for tools
    workflow.add_conditional_edges(
        source=REACT_GENERATOR,
        path=tools_condition,
        path_map={
            "continue": "tools",
            "finish": END,
            "end": END
        }
    )
    
    # Add edge from tools back to UI generator
    workflow.add_edge("tools", REACT_GENERATOR)
    
    print("UI generator workflow created and compiled")
    return workflow.compile()

async def run_ui_generator_agent(
    message: str,
    user_id: str,
    user_timezone: str,
    agent_id: str,
    conversation_id: Optional[str] = None
):
    """Run the UI generator workflow with a message."""
    print(f"Starting UI generator for user {user_id}")
    
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
    
    print("🚀 Running UI generator workflow")
    
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
        
        print("✅ UI generator workflow completed successfully")
        
        # Extract the final response from messages
        final_messages = result.get("messages", [])
        if final_messages:
            last_message = final_messages[-1]
            final_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
        else:
            final_response = "UI component generated successfully."
        
        # Store agent response in conversation using MongoDB
        print(f"💾 Storing agent response in conversation: {conversation_id}")
        ConversationCRUD.add_message(conversation_id, "assistant", final_response)
        print(f"✅ Conversation updated successfully in MongoDB")
        
        return {
            "response": final_response,
            "conversation_id": conversation_id
        }
        
    except Exception as e:
        print(f"❌ Error in UI generator workflow: {e}")
        raise HTTPException(status_code=500, detail=f"UI generator error: {str(e)}") 
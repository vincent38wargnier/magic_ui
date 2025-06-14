import os
from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from ..graphstate import GraphState
from openai import AsyncOpenAI

async def ui_generator_agent_node(state: GraphState, config: RunnableConfig) -> Dict[str, Any]:
    """Simple UI generator agent node that creates HTML/CSS/JS components."""
    
    print("🎨 UI Generator Agent Started")
    
    # Get all messages for conversation context
    messages = state["messages"]
    
    if not messages:
        print("❌ No messages found")
        return state
    
    print(f"📝 Processing {len(messages)} messages in conversation")
    
    # General AI assistant prompt - can handle any request
    system_prompt = """You are a helpful AI assistant. You can answer questions, generate UI components, provide information, or help with any task the user requests.

For UI-related requests:
- Generate clean, responsive HTML with Tailwind CSS classes
- Include interactive JavaScript when needed
- Make components modern and visually appealing

For general questions:
- Provide accurate, helpful information
- Be concise but thorough
- Use a friendly, professional tone

Always respond directly to what the user is asking for."""

    try:
        # Create OpenAI client
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Convert LangChain messages to OpenAI format
        openai_messages = [{"role": "system", "content": system_prompt}]
        
        for msg in messages:
            if hasattr(msg, 'content'):
                if msg.__class__.__name__ == 'HumanMessage':
                    openai_messages.append({"role": "user", "content": msg.content})
                elif msg.__class__.__name__ == 'AIMessage':
                    openai_messages.append({"role": "assistant", "content": msg.content})
        
        print(f"🤖 Sending {len(openai_messages)} messages to OpenAI (including system message)")
        
        # Create completion with full conversation history
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=openai_messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        generated_response = response.choices[0].message.content
        print("✅ Response Generated")
        
        # Create response message
        response_message = AIMessage(
            content=generated_response
        )
        
        # Update state
        updated_state = state.copy()
        updated_state["messages"] = messages + [response_message]
        updated_state["recursion_count"] = state.get("recursion_count", 0) + 1
        
        return updated_state
        
    except Exception as e:
        print(f"❌ Error generating UI: {e}")
        
        error_message = AIMessage(
            content=f"I encountered an error while generating the UI component: {str(e)}"
        )
        
        updated_state = state.copy()
        updated_state["messages"] = messages + [error_message]
        updated_state["recursion_count"] = state.get("recursion_count", 0) + 1
        
        return updated_state 
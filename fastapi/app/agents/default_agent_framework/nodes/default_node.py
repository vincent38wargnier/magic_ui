import os
from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from ..graphstate import GraphState
from openai import AsyncOpenAI


async def default_agent_node(
    state: GraphState, config: RunnableConfig
) -> Dict[str, Any]:
    """Default agent node that can handle any general-purpose conversation."""

    print("🤖 Default Agent Started")

    # Get all messages for conversation context
    messages = state["messages"]

    if not messages:
        print("❌ No messages found")
        return state

    print(f"📝 Processing {len(messages)} messages in conversation")

    # General AI assistant prompt - can handle any request
    system_prompt = """You are a helpful and intelligent AI assistant. You can assist with a wide variety of tasks including:

CORE CAPABILITIES:
- Answering questions on any topic
- Helping with problem-solving and analysis
- Providing explanations and tutorials
- Creative writing and content generation
- Code assistance and programming help
- Research and information gathering
- Planning and organization
- Mathematical calculations and logic

COMMUNICATION STYLE:
- Be clear, concise, and helpful
- Provide detailed explanations when needed
- Ask clarifying questions if the request is ambiguous
- Offer multiple solutions or approaches when appropriate
- Use examples to illustrate complex concepts

RESPONSE FORMAT:
- Structure your responses clearly with headings when helpful
- Use bullet points or numbered lists for multiple items
- Include code blocks for technical content
- Provide step-by-step instructions for processes

Always aim to be as helpful as possible while being accurate and reliable in your responses."""

    try:
        # Create OpenAI client
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Convert LangChain messages to OpenAI format
        openai_messages = [{"role": "system", "content": system_prompt}]

        for msg in messages:
            if hasattr(msg, "content"):
                if msg.__class__.__name__ == "HumanMessage":
                    openai_messages.append({"role": "user", "content": msg.content})
                elif msg.__class__.__name__ == "AIMessage":
                    openai_messages.append(
                        {"role": "assistant", "content": msg.content}
                    )

        print(
            f"🤖 Sending {len(openai_messages)} messages to OpenAI (including system message)"
        )

        # Create completion with full conversation history
        response = await client.chat.completions.create(
            model="gpt-4o", messages=openai_messages, temperature=0.7, max_tokens=2000
        )

        generated_response = response.choices[0].message.content
        print("✅ Response Generated")

        # Create response message
        response_message = AIMessage(content=generated_response)

        # Update state
        updated_state = state.copy()
        updated_state["messages"] = messages + [response_message]
        updated_state["recursion_count"] = state.get("recursion_count", 0) + 1

        return updated_state

    except Exception as e:
        print(f"❌ Error generating response: {e}")

        error_message = AIMessage(
            content=f"I encountered an error while processing your request: {str(e)}"
        )

        updated_state = state.copy()
        updated_state["messages"] = messages + [error_message]
        updated_state["recursion_count"] = state.get("recursion_count", 0) + 1

        return updated_state

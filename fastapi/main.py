from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import requests

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB connection
from db.mongodb import connect_to_mongo
from app.agents.ui_generator_agent.graph import run_ui_generator_agent
from app.agents.default_agent_framework.graph import run_default_agent
from app.agents.anthropic_no_lanngshit.agent import run_claude_ui_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    connect_to_mongo()
    print("🚀 FastAPI server started with MongoDB connection")
    yield
    # Shutdown (if needed)
    pass


app = FastAPI(
    title="mcpmyapi Agents API",
    description="FastAPI endpoints for running LangGraph agents",
    version="1.0.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str
    agent: str = "ui_generator"  # Which agent to talk to
    conversation_id: Optional[str] = None
    user_id: str = "test_user"
    user_timezone: str = "UTC"


@app.get("/")
async def root():
    return {"message": "mcpmyapi Agents API is running"}


@app.get("/furniture/{furniture_type}/{color}", response_model=List[Furniture])
async def get_furniture(furniture_type: str, color: str):
    filtered_furniture = [
        furniture
        for furniture in furniture_data
        if furniture["type"].lower() == furniture_type.lower()
        and furniture["color"].lower() == color.lower()
    ]

    if not filtered_furniture:
        raise HTTPException(
            status_code=404,
            detail=f"No furniture found for type '{furniture_type}' in color '{color}'",
        )

    return filtered_furniture


@app.post("/conversation_agent")
async def conversation_agent(request: ChatRequest):
    result = await run_conversation_agent(
        message=request.message,
        user_id=request.user_id,
        user_timezone=request.user_timezone,
        agent_id=request.agent,
        conversation_id=request.conversation_id,
    )
    
    search_urls = result["search_urls"]
    print(f"Search URLs: {search_urls}")
    
    # Collect all furniture results via direct function calls
    all_furniture = []
    
    for search_param in search_urls:
        if "/" in search_param:
            try:
                furniture_type, color = search_param.split("/", 1)
                furniture_result = await get_furniture(furniture_type, color)
                all_furniture.extend(furniture_result)
                print(f"Found {len(furniture_result)} items for {search_param}")
            except HTTPException as e:
                print(f"No furniture found for {search_param}: {e.detail}")
            except Exception as e:
                print(f"Error processing {search_param}: {e}")
    
    return {
        "search_params": search_urls,
        "products": all_furniture,
        "conversation_id": result["conversation_id"]
    }


@app.get("/test")
async def test():
    return {
        "message": "Generic AI Chat API is working!",
        "examples": [
            {
                "description": "Chat with UI Generator Agent",
                "method": "POST",
                "url": "/chat",
                "body": {
                    "message": "Create a simple button component",
                    "agent": "ui_generator",
                },
            },
            {
                "description": "General Question with Default Agent",
                "method": "POST",
                "url": "/chat",
                "body": {
                    "message": "who is the president of france",
                    "agent": "default_agent",
                },
            },
            {
                "description": "Continue Conversation",
                "method": "POST",
                "url": "/chat",
                "body": {
                    "message": "Tell me more about him",
                    "agent": "ui_generator",
                    "conversation_id": "your-conversation-id-here"
                }
            },
            {
                "description": "Claude UI Agent - Generate UI and post to endpoint",
                "method": "POST",
                "url": "/chat",
                "body": {
                    "message": "Create a voting app for IKEA furniture",
                    "agent": "anthropic_no_lanngshit"
                }
            }
        ]
    }


@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """Generic chat endpoint - talk to any agent"""
    try:
        # Route to different agents based on agent parameter
        if request.agent == "ui_generator":
            result = await run_ui_generator_agent(
                message=request.message,
                user_id=request.user_id,
                user_timezone=request.user_timezone,
                agent_id=request.agent,
                conversation_id=request.conversation_id,
            )
            return {"success": True, "result": result}
        elif request.agent == "default_agent":
            result = await run_default_agent(
                message=request.message,
                user_id=request.user_id,
                user_timezone=request.user_timezone,
                agent_id=request.agent,
                conversation_id=request.conversation_id,
            )
            return {"success": True, "result": result}
        elif request.agent == "anthropic_no_lanngshit":
            result = await run_claude_ui_agent(request.message)
            return result
        else:
            raise HTTPException(
                status_code=400, detail=f"Unknown agent: {request.agent}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB connection
from db.mongodb import connect_to_mongo
from app.agents.ui_generator_agent.graph import run_ui_generator_agent

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
    lifespan=lifespan
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
                    "agent": "ui_generator"
                }
            },
            {
                "description": "General Question",
                "method": "POST", 
                "url": "/chat",
                "body": {
                    "message": "who is the president of france",
                    "agent": "ui_generator"
                }
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
                conversation_id=request.conversation_id
            )
            return {"success": True, "result": result}
        else:
            raise HTTPException(status_code=400, detail=f"Unknown agent: {request.agent}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
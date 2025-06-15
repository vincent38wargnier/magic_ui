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
from app.agents.conversation_agent.agent.graph import run_conversation_agent


class Furniture(BaseModel):
    id: int
    description: str
    img_url: str
    type: str
    color: str


furniture_data = [
    # Blue furniture
    {
        "id": 1,
        "description": "HYLTARP Sofa, Kilanda pale blue",
        "img_url": "https://www.ikea.com/us/en/images/products/hyltarp-sofa-kilanda-pale-blue__1193800_pe901645_s5.jpg?f=xxs",
        "type": "sofa",
        "color": "blue",
    },
    {
        "id": 2,
        "description": "UPPLAND Sofa, Kilanda dark blue",
        "img_url": "https://www.ikea.com/us/en/images/products/uppland-sofa-kilanda-dark-blue__1194843_pe902111_s5.jpg?f=xxs",
        "type": "sofa",
        "color": "blue",
    },
    {
        "id": 3,
        "description": "KLIPPAN Loveseat, Långban bright blue",
        "img_url": "https://www.ikea.com/us/en/images/products/klippan-loveseat-langban-bright-blue__1315052_pe940371_s5.jpg?f=xxs",
        "type": "loveseat",
        "color": "blue",
    },
    {
        "id": 4,
        "description": "MORABO Sofa, Djuparp dark blue/wood",
        "img_url": "https://www.ikea.com/us/en/images/products/morabo-sofa-djuparp-dark-blue-wood__0990602_pe819086_s5.jpg?f=xxs",
        "type": "sofa",
        "color": "blue",
    },
    {
        "id": 5,
        "description": "SKÖNABÄCK Sleeper sofa, Knisa bright blue",
        "img_url": "https://www.ikea.com/us/en/images/products/skoenabaeck-sleeper-sofa-knisa-bright-blue__1360567_pe954475_s5.jpg?f=xxs",
        "type": "sleeper-sofa",
        "color": "blue",
    },
    # Blue chairs
    {
        "id": 11,
        "description": "TEODORES Chair, blue",
        "img_url": "https://www.ikea.com/us/en/images/products/teodores-chair-blue__1114279_pe871735_s5.jpg?f=xxs",
        "type": "chair",
        "color": "blue",
    },
    {
        "id": 12,
        "description": "DYVLINGE Swivel chair, Kelinge orange",
        "img_url": "https://www.ikea.com/us/en/images/products/dyvlinge-swivel-chair-kelinge-orange__1322501_pe942192_s5.jpg?f=xxs",
        "type": "chair",
        "color": "blue",
    },
    {
        "id": 13,
        "description": "KRYLBO Chair, Tonerud blue",
        "img_url": "https://www.ikea.com/us/en/images/products/krylbo-chair-tonerud-blue__1208500_pe908601_s5.jpg?f=xxs",
        "type": "chair",
        "color": "blue",
    },
    {
        "id": 14,
        "description": "TOBIAS Chair, blue/chrome plated",
        "img_url": "https://www.ikea.com/us/en/images/products/tobias-chair-blue-chrome-plated__0727333_pe735605_s5.jpg?f=xxs",
        "type": "chair",
        "color": "blue",
    },
    {
        "id": 15,
        "description": "GENESÖN Chair, metal/blue",
        "img_url": "https://www.ikea.com/us/en/images/products/genesoen-chair-metal-blue__1185917_pe898620_s5.jpg?f=xxs",
        "type": "chair",
        "color": "blue",
    },
    # Yellow/Green furniture
    {
        "id": 6,
        "description": "JÄTTEBO Sectional, 3-seat, Samsala dark yellow-green",
        "img_url": "https://www.ikea.com/us/en/images/products/jaettebo-sectional-3-seat-samsala-dark-yellow-green__1109636_pe870121_s5.jpg?f=xxs",
        "type": "sectional",
        "color": "green",
    },
    {
        "id": 7,
        "description": "UPPLAND Sofa, Hakebo gray/green",
        "img_url": "https://www.ikea.com/us/en/images/products/uppland-sofa-hakebo-gray-green__1194851_pe902101_s5.jpg?f=xxs",
        "type": "sofa",
        "color": "green",
    },
    {
        "id": 8,
        "description": "JÄTTEBO 4-seat mod sofa w chaise, right/Samsala dark yellow-green",
        "img_url": "https://www.ikea.com/us/en/images/products/jaettebo-4-seat-mod-sofa-w-chaise-right-samsala-dark-yellow-green__1109638_pe870128_s5.jpg?f=xxs",
        "type": "sofa",
        "color": "green",
    },
    {
        "id": 9,
        "description": "JÄTTEBO 2.5-seat mod sofa w chaise, left/Samsala dark yellow-green",
        "img_url": "https://www.ikea.com/us/en/images/products/jaettebo-2-5-seat-mod-sofa-w-chaise-left-samsala-dark-yellow-green__1109585_pe870075_s5.jpg?f=xxs",
        "type": "sofa",
        "color": "green",
    },
    {
        "id": 10,
        "description": "HYLTARP Sofa, Tallmyra dark green",
        "img_url": "https://www.ikea.com/us/en/images/products/hyltarp-sofa-tallmyra-dark-green__1193802_pe901629_s5.jpg?f=xxs",
        "type": "sofa",
        "color": "green",
    },
    # Yellow chairs
    {
        "id": 16,
        "description": "STRANDMON Wing chair, Skiftebo yellow",
        "img_url": "https://www.ikea.com/us/en/images/products/strandmon-wing-chair-skiftebo-yellow__0325450_pe517970_s5.jpg?f=xxs",
        "type": "chair",
        "color": "yellow",
    },
    {
        "id": 17,
        "description": "EKERÖ Armchair, Skiftebo yellow",
        "img_url": "https://www.ikea.com/us/en/images/products/ekeroe-armchair-skiftebo-yellow__0204753_pe359787_s5.jpg?f=xxs",
        "type": "chair",
        "color": "yellow",
    },
    {
        "id": 18,
        "description": "SOTENÄS Armchair, Hakebo red",
        "img_url": "https://www.ikea.com/us/en/images/products/sotenaes-armchair-hakebo-red__1322509_pe942197_s5.jpg?f=xxs",
        "type": "chair",
        "color": "yellow",
    },
    {
        "id": 19,
        "description": "STRANDMON Armchair and ottoman, Skiftebo yellow",
        "img_url": "https://www.ikea.com/us/en/images/products/strandmon-armchair-and-ottoman-skiftebo-yellow__1094844_pe863644_s5.jpg?f=xxs",
        "type": "chair",
        "color": "yellow",
    },
    {
        "id": 20,
        "description": "POÄNG Armchair, birch veneer/Skiftebo yellow",
        "img_url": "https://www.ikea.com/us/en/images/products/poaeng-armchair-birch-veneer-skiftebo-yellow__0936990_pe793502_s5.jpg?f=xxs",
        "type": "chair",
        "color": "yellow",
    },
]


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
                    "conversation_id": "your-conversation-id-here",
                },
            },
        ],
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
        else:
            raise HTTPException(
                status_code=400, detail=f"Unknown agent: {request.agent}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

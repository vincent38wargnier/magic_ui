import requests
import json
from app.agents.conversation_agent.agent.state import GraphState


def query_interpreter_node(state: GraphState) -> GraphState:

    messages = state["messages"]

    url = "https://api.gmi-serving.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": (
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJpZCI6IjY2ZjY4ZGNiLTc2MjYtNDU1YS04MTJlLWNjZWQ0NGM1MmFmMSIs"
            "InR5cGUiOiJpZV9tb2RlbCJ9."
            "wSR0pMUfjAfTijf8jJSaiec1FutdKCcCJq6RlJo62uM"
        ),
    }

    payload = {
        "model": "deepseek-ai/DeepSeek-Prover-V2-671B",
        "messages": [
            {
                "role": "system",
                "content": (
                    """
You are an expert assistant specialized in understanding customer queries 
and returning relevant objects from our database.

When you receive a query about furniture, return matching furniture objects 
with their full details.
When you receive a query about events, return event objects with their 
full details.

IMPORTANT: Return the COMPLETE object structure, not search parameters. 
The objects are already defined in the data above - just return the 
complete matching objects.

For furniture queries: Find products that match type, color, or description.
For event queries: Find events that match the request.

Your response should be a JSON object with:
- suggestions: array of complete object(s) matching the query
- case_description: brief description of what the user is looking for

Return 1-5 most relevant objects based on the query.

Available furniture:
- Types: chair, sofa, loveseat, sleeper-sofa, sectional
- Colors: blue, yellow, green

Furniture Rules:
1. Consider conversation context (if they mentioned colors/types before)
2. If they say "5-6 sofas" → return multiple sofa variations
3. If they compare colors → return both colors
4. Return format: "type/color" (e.g., "sofa/blue", "sofa/yellow")

## EVENT REQUESTS:
When user asks about events/meetings/activities, return built-in event data.

Built-in Events:
- San Francisco events: "luma_sf_event_1", "luma_sf_event_2", "luma_sf_event_3"  
- General events: "general_event_1", "general_event_2", "general_event_3"
- Tech meetups: "tech_meetup_1", "tech_meetup_2", "tech_meetup_3"

Event Rules:
1. If they mention San Francisco → return SF events
2. If they mention tech/programming → return tech meetups  
3. Otherwise → return general events

## EXAMPLES:

**Furniture:**
User: "I'm deciding between yellow and blue sofa"
Output: [sofa objects with yellow and blue colors from Available Data]

User: "Show me 5 different chairs"  
Output: [mix of chair objects from Available Data]

**Events:**
User: "Show me 3 interesting meetings in San Francisco"
Output: [all 3 event objects from EVENTS DATA]

User: "What tech events are happening?"
Output: [AI-related event objects from EVENTS DATA]

**IMPORTANT**: Return complete objects from Available Data, not just IDs or params. Select the most relevant items based on user's query.

Create case_description describing what type of frontend app this would be.
                    
                    
Available Data:
                    
                    furniture_data = [
                        
                    ### Blue furniture
                    {
                        "id": 1,
                        "description": "HYLTARP Sofa, Kilanda pale blue",
                        "img_url": "https://www.ikea.com/us/en/images/products/hyltarp-sofa-kilanda-pale-blue__1193800_pe901645_s5.jpg?f=xxs",
                        "type": "sofa",
                        "color": "blue"
                    },
                    {
                        "id": 2,
                        "description": "UPPLAND Sofa, Kilanda dark blue",
                        "img_url": "https://www.ikea.com/us/en/images/products/uppland-sofa-kilanda-dark-blue__1194843_pe902111_s5.jpg?f=xxs",
                        "type": "sofa",
                        "color": "blue"
                    },
                    {
                        "id": 3,
                        "description": "KLIPPAN Loveseat, Långban bright blue",
                        "img_url": "https://www.ikea.com/us/en/images/products/klippan-loveseat-langban-bright-blue__1315052_pe940371_s5.jpg?f=xxs",
                        "type": "loveseat",
                        "color": "blue"
                    },
                    {
                        "id": 4,
                        "description": "MORABO Sofa, Djuparp dark blue/wood",
                        "img_url": "https://www.ikea.com/us/en/images/products/morabo-sofa-djuparp-dark-blue-wood__0990602_pe819086_s5.jpg?f=xxs",
                        "type": "sofa",
                        "color": "blue"
                    },
                    {
                        "id": 5,
                        "description": "SKÖNABÄCK Sleeper sofa, Knisa bright blue",
                        "img_url": "https://www.ikea.com/us/en/images/products/skoenabaeck-sleeper-sofa-knisa-bright-blue__1360567_pe954475_s5.jpg?f=xxs",
                        "type": "sleeper-sofa",
                        "color": "blue"
                    },
                    ### Blue chairs
                    {
                        "id": 11,
                        "description": "TEODORES Chair, blue",
                        "img_url": "https://www.ikea.com/us/en/images/products/teodores-chair-blue__1114279_pe871735_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "blue"
                    },
                    {
                        "id": 12,
                        "description": "DYVLINGE Swivel chair, Kelinge orange",
                        "img_url": "https://www.ikea.com/us/en/images/products/dyvlinge-swivel-chair-kelinge-orange__1322501_pe942192_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "blue"
                    },
                    {
                        "id": 13,
                        "description": "KRYLBO Chair, Tonerud blue",
                        "img_url": "https://www.ikea.com/us/en/images/products/krylbo-chair-tonerud-blue__1208500_pe908601_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "blue"
                    },
                    {
                        "id": 14,
                        "description": "TOBIAS Chair, blue/chrome plated",
                        "img_url": "https://www.ikea.com/us/en/images/products/tobias-chair-blue-chrome-plated__0727333_pe735605_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "blue"
                    },
                    {
                        "id": 15,
                        "description": "GENESÖN Chair, metal/blue",
                        "img_url": "https://www.ikea.com/us/en/images/products/genesoen-chair-metal-blue__1185917_pe898620_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "blue"
                    },
                    ### Green furniture
                    {
                        "id": 6,
                        "description": "JÄTTEBO Sectional, 3-seat, Samsala dark yellow-green",
                        "img_url": "https://www.ikea.com/us/en/images/products/jaettebo-sectional-3-seat-samsala-dark-yellow-green__1109636_pe870121_s5.jpg?f=xxs",
                        "type": "sectional",
                        "color": "green"
                    },
                    {
                        "id": 7,
                        "description": "UPPLAND Sofa, Hakebo gray/green",
                        "img_url": "https://www.ikea.com/us/en/images/products/uppland-sofa-hakebo-gray-green__1194851_pe902101_s5.jpg?f=xxs",
                        "type": "sofa",
                        "color": "green"
                    },
                    {
                        "id": 8,
                        "description": "JÄTTEBO 4-seat mod sofa w chaise, right/Samsala dark yellow-green",
                        "img_url": "https://www.ikea.com/us/en/images/products/jaettebo-4-seat-mod-sofa-w-chaise-right-samsala-dark-yellow-green__1109638_pe870128_s5.jpg?f=xxs",
                        "type": "sofa",
                        "color": "green"
                    },
                    {
                        "id": 9,
                        "description": "JÄTTEBO 2.5-seat mod sofa w chaise, left/Samsala dark yellow-green",
                        "img_url": "https://www.ikea.com/us/en/images/products/jaettebo-2-5-seat-mod-sofa-w-chaise-left-samsala-dark-yellow-green__1109585_pe870075_s5.jpg?f=xxs",
                        "type": "sofa",
                        "color": "green"
                    },
                    {
                        "id": 10,
                        "description": "HYLTARP Sofa, Tallmyra dark green",
                        "img_url": "https://www.ikea.com/us/en/images/products/hyltarp-sofa-tallmyra-dark-green__1193802_pe901629_s5.jpg?f=xxs",
                        "type": "sofa",
                        "color": "green"
                    },
                    ### Yellow chairs
                    {
                        "id": 16,
                        "description": "STRANDMON Wing chair, Skiftebo yellow",
                        "img_url": "https://www.ikea.com/us/en/images/products/strandmon-wing-chair-skiftebo-yellow__0325450_pe517970_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "yellow"
                    },
                    {
                        "id": 17,
                        "description": "EKERÖ Armchair, Skiftebo yellow",
                        "img_url": "https://www.ikea.com/us/en/images/products/ekeroe-armchair-skiftebo-yellow__0204753_pe359787_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "yellow"
                    },
                    {
                        "id": 18,
                        "description": "SOTENÄS Armchair, Hakebo red",
                        "img_url": "https://www.ikea.com/us/en/images/products/sotenaes-armchair-hakebo-red__1322509_pe942197_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "yellow"
                    },
                    {
                        "id": 19,
                        "description": "STRANDMON Armchair and ottoman, Skiftebo yellow",
                        "img_url": "https://www.ikea.com/us/en/images/products/strandmon-armchair-and-ottoman-skiftebo-yellow__1094844_pe863644_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "yellow"
                    },
                    {
                        "id": 20,
                        "description": "POÄNG Armchair, birch veneer/Skiftebo yellow",
                        "img_url": "https://www.ikea.com/us/en/images/products/poaeng-armchair-birch-veneer-skiftebo-yellow__0936990_pe793502_s5.jpg?f=xxs",
                        "type": "chair",
                        "color": "yellow"
                    }
                ]
                
                EVENTS DATA:
                [
                    {
                        "id": 1,
                        "description": "​You probably already know that AI is changing the world. Come learn about some of the awesome AI dev tools being worked on.",
                        "image_url": "https://cdn.lu.ma/cdn-cgi/image/format=auto,fit=cover,dpr=2,background=white,quality=75,width=400,height=400/event-defaults/1-1/retro3.png",
                        "location": "San Francisco"
                    },
                    {
                        "id": 2,
                        "description": "​We're hosting this mixer to bring together AI founders, researchers and investors in the Bay Area who are building AI ecosystems. Join us for happy hour! Food & drinks provided.",
                        "image_url": "https://images.lumacdn.com/cdn-cgi/image/format=auto,fit=cover,dpr=2,background=white,quality=75,width=400,height=400/event-covers/gd/a4c1f55a-b52c-44b2-94f8-8546e69f3545.png",
                        "location": "San Francisco"
                    },
                    {
                        "id": 3,
                        "description": "Experts in the Loop     Advanced Training Techniques for Agents and Frontier Models",
                        "image_url": "https://images.lumacdn.com/cdn-cgi/image/format=auto,fit=cover,dpr=2,background=white,quality=75,width=400,height=400/event-covers/ih/af166777-3548-47a5-ab10-53dbf7dc5f8b.png",
                        "location": "San Francisco"
                    }
                ]
                    """
                ),
            },
        ]
        + messages,
        "temperature": 0,
        "max_tokens": 500,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "suggestions_list",
                "schema": {
                    "type": "object",
                    "properties": {
                        "suggestions": {"type": "array", "items": {"type": "object"}},
                        "case_description": {"type": "string"}
                    },
                    "required": ["suggestions", "case_description"],
                    "additionalProperties": False,
                },
            },
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()

    # Print just the AI's response content
    if "choices" in response_data and len(response_data["choices"]) > 0:
        content = response_data["choices"][0]["message"]["content"]
        print(f"🔍 Raw API response: {content}")
        try:
            parsed_content = json.loads(content)
            suggestions = parsed_content.get("suggestions", [])
            returned_case_description = parsed_content.get("case_description", "")
            print(f"🔍 Parsed suggestions: {len(suggestions)} items")
            print(f"🔍 Case description: {returned_case_description}")
            # Update state with results
            state["items"] = suggestions
            state["case_description"] = returned_case_description
            return state
        except json.JSONDecodeError as e:
            print("Error parsing JSON response:")
            print(content)
            print(f"JSON Error: {e}")
    else:
        print("Error: No response content found")
        print(json.dumps(response_data, indent=2))
    
    # Return state with empty results on error
    state["items"] = []
    state["case_description"] = ""
    return state

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
                    You are an expert assistant that extracts furniture search parameters from natural language input.

                    Your job is to:
                    1. Parse user requests and return furniture API parameters in the format "type/color"
                    2. Create a brief case_description summarizing what the user is looking for overall, but if you were to describe an frontend application.

                    Available furniture types:
                    - chair
                    - sofa  
                    - loveseat
                    - sleeper-sofa
                    - sectional

                    Available colors:
                    - blue
                    - yellow
                    - green

                    Rules:
                    1. Extract the furniture type and color from user input
                    2. Return in format "type/color" (e.g., "chair/blue")
                    3. If multiple items are mentioned, return multiple strings
                    4. If color is not specified, try to infer or ask for clarification
                    5. If type is not available in our list, suggest the closest match
                    6. Only use the exact types and colors from the lists above

                    Examples:

                    User: "I need a blue chair"
                    Output: "chair/blue"

                    User: "Show me yellow sofas"  
                    Output: "sofa/yellow"

                    User: "I want a green sectional"
                    Output: "sectional/green"

                    User: "Looking for blue chairs and yellow loveseats"
                    Output: "chair/blue", "loveseat/yellow"

                    User: "I need a navy armchair"
                    Output: "chair/blue" (navy -> blue)

                    User: "Show me a beige sofa"
                    Output: "sofa/yellow" (beige -> closest available color)

                    User: "I want a sleeper couch in green"
                    Output: "sleeper-sofa/green" (sleeper couch -> sleeper-sofa)

                    Respond ONLY with the parameter strings, separated by commas if multiple items.
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
                        "suggestions": {"type": "array", "items": {"type": "string"}},
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
        try:
            parsed_content = json.loads(content)
            suggestions = parsed_content.get("suggestions", [])
            returned_case_description = parsed_content.get("case_description", "")
            return {"search_urls": suggestions, "case_description": returned_case_description}
        except json.JSONDecodeError:
            print("Error parsing JSON response:")
            print(content)
    else:
        print("Error: No response content found")
        print(json.dumps(response_data, indent=2))
    return {"search_urls": [], "case_description": ""}

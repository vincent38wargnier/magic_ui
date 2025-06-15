import os
import json
import asyncio
import httpx
from anthropic import Anthropic
from typing import Dict, Any, Optional


class ClaudeUIAgent:
    """Simple Claude Sonnet 4 agent that generates UI code and posts to endpoint"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
        self.endpoint_url = "http://localhost:3000/api/ui"
        
    def _create_ui_prompt(self, user_message: str) -> str:
        """Create a prompt for UI generation based on user message"""
        return f"""
You are a UI generator that creates interactive web applications. Based on the user's request, create a complete HTML page with inline CSS and JavaScript that includes interactive elements like buttons, forms, and real-time updates.

User Request: {user_message}

CRITICAL REQUIREMENTS:
- Create a complete HTML document with DOCTYPE
- Include all CSS inline in <style> tags  
- Include all JavaScript inline in <script> tags
- MUST include interactive elements (buttons, forms, inputs, etc.)
- Use modern, professional styling (cards, gradients, animations, hover effects)
- Include real-time updates and dynamic content

MANDATORY INTERACTIVE FEATURES:
- Add clickable buttons with onclick handlers
- Include forms or input fields where relevant
- Add hover effects and transitions
- Create dynamic content that updates based on user actions
- Include counters, voting, or other interactive elements

STATE MANAGEMENT (CRITICAL):
- Use getState(key, defaultValue) to retrieve stored data
- Use saveState(object) to save data to backend
- Always initialize state with default values
- Update UI immediately after state changes
- Handle state synchronization with: window.onStateSync = function(newState) {{ updateAllDisplays(); }}

JAVASCRIPT STRUCTURE EXAMPLE:
```javascript
// Initialize state
function initializeState() {{
    if (getState('example_key') === null) {{
        saveState({{ 'example_key': 0 }});
    }}
}}

// Interactive functions
function handleClick(action) {{
    const currentValue = getState('example_key', 0);
    const newValue = currentValue + 1;
    saveState({{ 'example_key': newValue }});
    updateDisplay();
}}

// Update displays
function updateDisplay() {{
    const value = getState('example_key', 0);
    document.getElementById('display').textContent = value;
}}

// Handle sync from other users
window.onStateSync = function(newState) {{
    updateDisplay();
}};

// Initialize on load
setTimeout(() => {{
    initializeState();
    updateDisplay();
}}, 1000);
```

STYLING REQUIREMENTS (MOBILE-FIRST FOR SMALL SMARTPHONES):
- CRITICAL: Optimize for very small smartphone screens (320px-375px width)
- Use minimal margins and paddings (4px-8px max) to maximize screen space
- Make buttons finger-friendly (min 44px height/width)
- Use modern CSS with flexbox/grid for compact layouts
- Add touch-friendly hover effects and smooth transitions
- Use professional color schemes with high contrast for small screens
- Include compact cards with minimal shadows and tight spacing
- MANDATORY: Make it fully responsive and mobile-first
- Use small font sizes but ensure readability (14px-16px)
- Minimize white space - pack content efficiently
- Use full-width layouts where possible
- Add loading states and feedback optimized for touch

IMAGE DESIGN REQUIREMENTS:
- ALWAYS use object-fit: cover for images to maintain aspect ratio
- Add rounded corners to all images (border-radius: 8px-12px)
- Use proper image containers with overflow: hidden
- Include hover effects and smooth transitions on images
- Make images responsive with max-width: 100%
- Add subtle shadows or borders to enhance image presentation
- Use placeholder backgrounds while images load
- Optimize image sizes for mobile screens
- Include alt text for accessibility

MOBILE CSS REQUIREMENTS:
```css
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ margin: 4px; padding: 4px; font-size: 14px; }}
.container {{ max-width: 100%; padding: 4px 8px; }}
button {{ min-height: 44px; padding: 8px 12px; border-radius: 4px; }}
.card {{ margin: 4px 0; padding: 8px; border-radius: 8px; }}
img {{ 
    width: 100%; 
    height: auto; 
    object-fit: cover; 
    border-radius: 8px; 
    transition: transform 0.3s ease;
}}
.image-container {{ 
    overflow: hidden; 
    border-radius: 12px; 
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}
@media (max-width: 375px) {{ /* Extra optimizations for tiny screens */ }}
```

Return ONLY the complete HTML code with embedded CSS and JavaScript, no explanations or markdown formatting.
"""

    async def generate_ui_code(self, user_message: str) -> str:
        """Generate UI code using Claude Sonnet 4"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": self._create_ui_prompt(user_message)
                    }
                ]
            )
            
            # Extract the text content from the response
            content = message.content[0].text if message.content else ""
            return content.strip()
            
        except Exception as e:
            raise Exception(f"Failed to generate UI code: {str(e)}")
    
    async def post_to_endpoint(self, content: str) -> Dict[str, Any]:
        """Post the generated content to the UI endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.endpoint_url,
                    json={"content": content},
                    headers={"Content-Type": "application/json"},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            raise Exception(f"Failed to post to endpoint: {str(e)}")
    
    async def process_request(self, user_message: str) -> Dict[str, Any]:
        """Main method to process user request and return URL"""
        try:
            # Step 1: Generate UI code
            ui_code = await self.generate_ui_code(user_message)
            
            # Step 2: Post to endpoint
            endpoint_response = await self.post_to_endpoint(ui_code)
            
            # Step 3: Return the result
            return {
                "success": True,
                "message": "UI generated and posted successfully!",
                "ui_id": endpoint_response.get("id"),
                "url": endpoint_response.get("url"),
                "endpoint_message": endpoint_response.get("message"),
                "generated_code_preview": ui_code[:200] + "..." if len(ui_code) > 200 else ui_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate UI or post to endpoint"
            }


# Simple function to run the agent
async def run_claude_ui_agent(user_message: str) -> Dict[str, Any]:
    """Simple function to run the Claude UI agent"""
    agent = ClaudeUIAgent()
    return await agent.process_request(user_message) 
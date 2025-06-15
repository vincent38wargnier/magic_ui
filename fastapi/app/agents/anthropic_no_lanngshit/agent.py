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
You are a UI generator. Based on the user's request, create a complete HTML page with inline CSS and JavaScript.

User Request: {user_message}

Requirements:
- Create a complete HTML document with DOCTYPE
- Include all CSS inline in <style> tags
- Include all JavaScript inline in <script> tags
- Make it visually appealing and functional
- Use modern web standards
- Include interactive elements where appropriate
- Use professional styling similar to modern web apps

Return ONLY the HTML code, no explanations or markdown formatting.
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
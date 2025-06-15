import os
import json
import asyncio
import httpx
from anthropic import Anthropic
from typing import Dict, Any, Optional, List


class ClaudeUIAgent:
    """Simple Claude Sonnet 4 agent that generates UI code and posts to endpoint"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-opus-4-20250514"
        self.endpoint_url = "http://localhost:3000/api/ui"
        
    def _create_ui_prompt(self, user_message: str) -> str:
        """Create a prompt for UI generation based on user message"""
        return f"""
You are a UI generator that creates interactive web applications. Based on the user's request, create a complete HTML page with inline CSS and JavaScript that includes interactive elements like buttons, forms, and real-time updates.

User Request: {user_message}

🏗️ PLACEHOLDER STRATEGY: Use placeholder content for images and data - real content will be injected later.

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

🚨🚨🚨 TOP PRIORITY - STATE MANAGEMENT (ABSOLUTELY CRITICAL) 🚨🚨🚨
⚠️ THIS IS THE MOST IMPORTANT REQUIREMENT - DO NOT SKIP THIS! ⚠️

MANDATORY STATE MANAGEMENT REQUIREMENTS:
- Use getState(key, defaultValue) to retrieve stored data
- Use saveState(object) to save data to backend  
- Always initialize state with default values
- Update UI immediately after state changes
- Handle state synchronization with: window.onStateSync = function(newState) {{ updateAllDisplays(); }}

🔥 FAILURE TO IMPLEMENT STATE MANAGEMENT = BROKEN APPLICATION 🔥

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

MOBILE CSS REQUIREMENTS:
```css
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ margin: 4px; padding: 4px; font-size: 14px; }}
.container {{ max-width: 100%; padding: 4px 8px; }}
button {{ min-height: 44px; padding: 8px 12px; border-radius: 4px; }}
.card {{ margin: 4px 0; padding: 8px; border-radius: 8px; }}
@media (max-width: 375px) {{ /* Extra optimizations for tiny screens */ }}
```

🏗️ PLACEHOLDER CONTENT GUIDELINES:
- Use placeholder images: https://via.placeholder.com/400x300
- Sample titles: "Sample Event", "Loading...", "Product Name"
- Create proper structure for real data injection later
- Make cards/containers ready for real content replacement

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
    
    async def process_request(self, user_message: str, validation_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Main method to process user request and return URL"""
        try:
            # Step 1: Generate basic UI structure (without images)
            print("🏗️ Step 1: Generating basic UI structure...")
            ui_code = await self.generate_ui_code(user_message)
            print("✅ Basic UI structure generated")
            
            # Step 2: Add images to the generated UI if validation data provided
            if validation_data:
                print("🖼️ Step 2: Adding images to UI...")
                
                # Check if original has JavaScript functions
                has_register_function = "function registerEvent" in ui_code
                has_addcart_function = "function addToCart" in ui_code
                print(f"🔍 Original HTML has registerEvent: {has_register_function}")
                print(f"🔍 Original HTML has addToCart: {has_addcart_function}")
                
                image_injector = ImageInjector()
                ui_code = await image_injector.inject_images_into_html(ui_code, validation_data)
                
                # Check if functions survived injection
                still_has_register = "function registerEvent" in ui_code
                still_has_addcart = "function addToCart" in ui_code
                print(f"🔍 After injection has registerEvent: {still_has_register}")
                print(f"🔍 After injection has addToCart: {still_has_addcart}")
                
                # If functions were lost, use validator to restore them
                if (has_register_function and not still_has_register) or (has_addcart_function and not still_has_addcart):
                    print("⚠️ JavaScript functions were lost during injection! Using validator to restore...")
                    validator = HTMLValidator()
                    ui_code = await validator.validate_and_fix_html(ui_code, validation_data)
                    print("🔧 JavaScript functions restored")
                
                print("✅ Images injected into UI")
            
            # Step 3: Post to endpoint
            print("📤 Step 3: Posting to endpoint...")
            endpoint_response = await self.post_to_endpoint(ui_code)
            print("✅ Posted to endpoint successfully")
            
            # Step 4: Return the result
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


class ImageInjector:
    """Second agent that injects specific images into existing HTML structure"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
    
    async def inject_images_into_html(self, html_code: str, required_data: Dict[str, Any]) -> str:
        """Inject specific images and data into existing HTML"""
        
        # Extract required elements
        image_urls = required_data.get('image_urls', [])
        descriptions = required_data.get('descriptions', [])
        locations = required_data.get('locations', [])
        
        injection_prompt = f"""
🚨🚨🚨 CRITICAL: DO NOT REWRITE THE HTML - ONLY REPLACE PLACEHOLDER CONTENT! 🚨🚨🚨

You are an HTML content replacer. Your job is to find placeholder text and images, and replace them with real data.

EXISTING HTML (DO NOT CHANGE STRUCTURE):
{html_code}

REAL DATA TO USE:
- Image URLs: {image_urls}
- Descriptions: {descriptions}
- Locations: {locations}

🔧 REPLACEMENT RULES:
1. Find placeholder images like "https://via.placeholder.com/400x300" → Replace with real image URLs
2. Find placeholder text like "Sample Event", "Loading...", "Sample Description" → Replace with real descriptions
3. Find placeholder locations like "Sample Location" → Replace with real locations
4. DO NOT touch any <script> tags - keep JavaScript 100% intact
5. DO NOT touch any <style> tags - keep CSS 100% intact  
6. DO NOT change onclick attributes - keep them exactly as they are
7. DO NOT change HTML structure - only replace content inside existing tags

🚨 FORBIDDEN ACTIONS:
- DO NOT rewrite the entire HTML
- DO NOT modify JavaScript functions
- DO NOT change CSS styles
- DO NOT alter HTML structure
- DO NOT remove or add new HTML elements

✅ ALLOWED ACTIONS:
- Replace placeholder image src with real URLs
- Replace placeholder text with real descriptions
- Replace placeholder locations with real locations

EXAMPLE - ONLY change the content:
Before: <img src="https://via.placeholder.com/400x300" alt="Event">
After:  <img src="{image_urls[0] if image_urls else 'https://via.placeholder.com/400x300'}" alt="Event">

Before: <h3>Sample Event Title</h3>
After:  <h3>{descriptions[0] if descriptions else 'Sample Event Title'}</h3>

🔥 CRITICAL: Return the SAME HTML structure with ONLY content replaced!
"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": injection_prompt
                    }
                ]
            )
            
            # Extract the text content from the response
            injected_html = message.content[0].text if message.content else html_code
            return injected_html.strip()
            
        except Exception as e:
            print(f"❌ Image injection failed: {str(e)}")
            return html_code  # Return original if injection fails


class HTMLValidator:
    """Validates that generated HTML contains all required images and data"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"
    
    async def validate_and_fix_html(self, html_code: str, required_data: Dict[str, Any]) -> str:
        """Validate HTML and fix missing elements"""
        
        # Extract required elements
        image_urls = required_data.get('image_urls', [])
        descriptions = required_data.get('descriptions', [])
        locations = required_data.get('locations', [])
        
        validation_prompt = f"""
You are an HTML validator. Your job is to fix JavaScript errors and create clean Apple-style design.

REQUIRED ELEMENTS TO CHECK:
- Image URLs that MUST be in HTML: {image_urls}
- Descriptions that MUST be visible: {descriptions}
- Locations that MUST be shown: {locations}

CRITICAL JAVASCRIPT FIXES:
1. Find ALL onclick="functionName()" calls
2. For EACH onclick function, create the corresponding JavaScript function
3. Example: if you see onclick="addToCart(1)", you MUST add:

<script>
function addToCart(productId) {{
    alert('Added product ' + productId + ' to cart!');
    // Simple cart logic
}}
</script>

4. Example: if you see onclick="registerEvent(1)", you MUST add:

<script>
function registerEvent(eventId) {{
    alert('Registered for event ' + eventId + '!');
    // Simple registration logic
}}
</script>

5. NO undefined functions allowed - every onclick must have a working function

APPLE-STYLE DESIGN REQUIREMENTS:
- Clean, minimal white background
- Subtle shadows and rounded corners (border-radius: 12px)
- Elegant typography (system fonts)
- Plenty of white space
- Simple, elegant buttons with subtle hover effects
- No bright colors - use grays, whites, and one accent color
- Cards with clean borders and subtle shadows
- Professional, minimalist layout like Apple's website

HTML CODE TO VALIDATE:
{html_code}

TASK:
1. Check if ALL image URLs are present as <img src="URL"> tags
2. Check if ALL descriptions are visible as text content  
3. Check if ALL locations are displayed (if provided)
4. CRITICAL: Find every onclick="functionName()" and create function functionName()
5. Apply clean Apple-style design with minimal colors and elegant spacing
6. Make sure ALL JavaScript functions are defined and working

Return the corrected HTML with working JavaScript and Apple-style design.
Return ONLY the complete HTML code, no explanations.
"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": validation_prompt
                    }
                ]
            )
            
            # Extract the text content from the response
            validated_html = message.content[0].text if message.content else html_code
            return validated_html.strip()
            
        except Exception as e:
            print(f"❌ HTML validation failed: {str(e)}")
            return html_code  # Return original if validation fails


# Simple function to run the agent
async def run_claude_ui_agent(user_message: str, validation_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Simple function to run the Claude UI agent"""
    agent = ClaudeUIAgent()
    return await agent.process_request(user_message, validation_data) 
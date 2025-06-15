import aiohttp
import json
import os
from langchain_core.tools import tool

@tool
async def store_ui_component(content: str) -> str:
    """
    Stores a UI component in the database and returns the display URL.
    
    Args:
        content: Complete HTML content with inline CSS and JavaScript
        
    Returns:
        The URL where the UI component can be viewed
    """
    try:
        # Get the base URL from environment or use default
        base_url = os.getenv("NEXT_PUBLIC_BASE_URL", "http://localhost:3000")
        api_endpoint = f"{base_url}/api/ui"
        
        # Prepare the payload
        payload = {
            "content": content
        }
        
        print(f"📤 Storing UI component to: {api_endpoint}")
        
        # Make async HTTP request to store the component
        async with aiohttp.ClientSession() as session:
            async with session.post(
                api_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 201:
                    result = await response.json()
                    display_url = result.get("url")
                    component_id = result.get("id")
                    
                    print(f"✅ UI component stored successfully!")
                    print(f"🆔 Component ID: {component_id}")
                    print(f"🔗 Display URL: {display_url}")
                    
                    return f"UI component stored successfully! 🎉\n\n🔗 **View your component here**: {display_url}\n\n📝 Component ID: {component_id}"
                    
                else:
                    error_data = await response.json()
                    error_msg = error_data.get("error", "Unknown error")
                    print(f"❌ Failed to store UI component: {response.status} - {error_msg}")
                    return f"❌ Failed to store UI component: {error_msg}"
                    
    except aiohttp.ClientError as e:
        print(f"❌ Network error: {e}")
        return f"❌ Network error while storing component: {str(e)}"
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return f"❌ Unexpected error: {str(e)}" 
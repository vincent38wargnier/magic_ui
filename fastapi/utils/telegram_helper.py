import aiohttp
from typing import Dict, Any, Optional
from .magic_print import magic_print

async def send_telegram_message(
    bot_token: str,
    chat_id: str,
    text: str,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Send a text message to a Telegram chat.
    
    Args:
        bot_token: The Telegram bot token
        chat_id: The chat ID to send the message to
        text: The message text to send
        options: Additional options for the message (optional)
    
    Returns:
        The response from the Telegram API
    
    Raises:
        ValueError: If required parameters are missing
        Exception: If the API request fails
    """
    magic_print(f"📤 Sending Telegram message to chat: {chat_id}", "blue")
    
    # Input validation
    if not bot_token or not chat_id or not text:
        missing = []
        if not bot_token: missing.append("bot_token")
        if not chat_id: missing.append("chat_id")
        if not text: missing.append("text")
        error_msg = f"Missing required fields: {', '.join(missing)}"
        magic_print(f"❌ Validation Error: {error_msg}", "red")
        raise ValueError(error_msg)
    
    try:
        # Prepare request
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        
        payload = {
            'chat_id': chat_id,
            'text': text,
            **(options or {})
        }
        
        magic_print(f"Message length: {len(text)} characters", "yellow")
        
        # Make request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                status = response.status
                magic_print(f"Response Status: {status}", "yellow")
                
                if status != 200:
                    error_text = await response.text()
                    magic_print(f"❌ HTTP Error: {status} - {error_text}", "red")
                    response.raise_for_status()
                
                data = await response.json()
                
                if not data.get('ok'):
                    error_msg = data.get('description') or 'Failed to send message'
                    magic_print(f"❌ Telegram API Error: {error_msg}", "red")
                    raise Exception(error_msg)
                
                magic_print("✅ Message sent successfully!", "green")
                return data
                
    except aiohttp.ClientError as e:
        magic_print(f"❌ Network Error: {str(e)}", "red")
        raise
    except Exception as e:
        magic_print(f"❌ Error sending message: {str(e)}", "red")
        raise 
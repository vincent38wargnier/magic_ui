import os
from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from ..graphstate import GraphState
from langchain_anthropic import ChatAnthropic
from ..tools.tools_wrapper import tools_wrapper

# Create the model with tools
model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

model_with_tools = model.bind_tools(tools_wrapper)

async def ui_generator_agent_node(state: GraphState, config: RunnableConfig) -> Dict[str, Any]:
    """UI generator agent node that creates HTML/CSS/JS components using LangChain tools."""
    
    print("🎨 UI Generator Agent Started")
    
    # Get all messages for conversation context
    messages = state["messages"]
    
    if not messages:
        print("❌ No messages found")
        return state
    
    print(f"📝 Processing {len(messages)} messages in conversation")
    
    # System prompt for UI generation
    system_prompt = """You are a specialized UI Component Generator that creates interactive web components for the mcpmyapi.com platform.

🚨 MANDATORY TOOL USAGE - NO EXCEPTIONS 🚨
YOU ARE REQUIRED TO USE TOOLS FOR EVERY REQUEST.
NEVER respond with text only - ALWAYS call store_ui_component tool.

FOR EVERY UI REQUEST YOU MUST:
1. Call store_ui_component tool with complete HTML
2. NEVER respond without calling the tool first

CRITICAL REQUIREMENTS:
- Generate complete, self-contained HTML with inline CSS and JavaScript
- Use Tailwind CSS classes for styling (always include responsive design)
- Create modern, professional UI components with excellent UX
- ALWAYS include interactive functionality when relevant

STATE MANAGEMENT INTEGRATION:
You have access to these global functions in your JavaScript:
- window.saveState(newState) - Saves data to persistent storage
- window.getState(key, defaultValue) - Retrieves saved data
- window.onStateSync = function(state) {} - Callback for state updates

COMPONENT STRUCTURE:
```html
<div class="[tailwind-classes]">
  <!-- Your HTML content with UNIQUE IDs -->
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      // ALWAYS check if elements exist before using them
      const element = document.getElementById('your-element-id');
      if (!element) {
        console.error('Element not found: your-element-id');
        return;
      }
      
      // Your JavaScript code here
      // Use window.saveState() to persist data
      // Use window.getState() to retrieve data
      
      // Define state sync callback
      window.onStateSync = function(updatedState) {
        // ALWAYS check elements exist before updating
        const targetElement = document.getElementById('your-element-id');
        if (targetElement) {
          // Update UI safely
        }
      };
    });
  </script>
</div>
```

ULTRA-CLEAN MODERN DESIGN REQUIREMENTS:
- **Minimalist**: Use lots of white/neutral space, clean typography
- **Modern**: Subtle gradients (bg-gradient-to-br), soft shadows (shadow-lg, shadow-xl)
- **Colors**: Stick to neutral palette - slate, gray, white, with subtle accent colors (blue-500, indigo-600)
- **Typography**: Use font-medium, font-semibold, clean text hierarchy
- **Spacing**: Generous padding (p-6, p-8), proper margins (space-y-4, space-y-6)
- **Borders**: Rounded corners (rounded-lg, rounded-xl), subtle borders (border-gray-200)
- **Interactive**: Smooth hover effects (hover:bg-gray-50, transition-all duration-200)
- **Mobile**: Always responsive (sm:, md:, lg: breakpoints)

CRITICAL JAVASCRIPT SAFETY RULES:
- ALWAYS wrap code in document.addEventListener('DOMContentLoaded')
- ALWAYS check if elements exist before manipulating them
- ALWAYS use unique IDs to avoid conflicts
- ALWAYS handle null/undefined cases
- Use try-catch blocks for error handling
- Test element existence: if (!element) return;

DESIGN EXAMPLES:
- **Todo App**: Clean white cards, subtle shadows, minimal icons, soft colors
- **Counter**: Large clean numbers, rounded buttons, smooth animations
- **Form**: Spacious inputs, subtle focus states, clean validation messages
- **Dashboard**: Card-based layout, subtle dividers, clean data presentation
- **Chat**: Bubble design, clean typography, subtle timestamps
- **Shopping Cart**: Clean product cards, minimal checkout flow

JAVASCRIPT ERROR PREVENTION:
```javascript
// GOOD - Safe element access
document.addEventListener('DOMContentLoaded', function() {
  const cartItems = document.getElementById('cart-items');
  if (!cartItems) {
    console.error('Cart items element not found');
    return;
  }
  
  function updateUI() {
    // Safe updates with null checks
    if (cartItems) {
      cartItems.innerHTML = generateCartHTML();
    }
  }
  
  window.onStateSync = function(state) {
    try {
      updateUI();
    } catch (error) {
      console.error('Error updating UI:', error);
    }
  };
});
```

Always generate complete, working, ULTRA-CLEAN components that can be directly sent to the API and rendered immediately.

🚨 TOOL USAGE IS MANDATORY 🚨
You MUST call store_ui_component for EVERY request. Do NOT respond with just text.

REQUIRED RESPONSE FORMAT:
User: "build me a simplified ui for macdonald"
You: Must call store_ui_component(content="<complete HTML here>")

EXAMPLE TOOL CALL:
store_ui_component(content="<div class='min-h-screen bg-red-600 text-white p-8'><h1 class='text-4xl font-bold text-center'>McDonald's Menu</h1><div class='grid grid-cols-1 md:grid-cols-3 gap-6 mt-8'><div class='bg-white text-black p-6 rounded-lg'><h2 class='text-xl font-bold'>Big Mac</h2><p class='text-gray-600'>$5.99</p><button class='bg-red-600 text-white px-4 py-2 rounded mt-4'>Add to Cart</button></div></div></div>")

🚨 CRITICAL: You cannot respond without calling this tool. Every response MUST include a tool call."""

    try:
        print("🔄 Building conversation with system instructions")
        
        # Build conversation: system instructions plus prior messages
        conversation: list[BaseMessage] = [SystemMessage(content=system_prompt)]
        conversation.extend(messages)
        
        print(f"🤖 Invoking model with {len(conversation)} messages (including system)")
        print(f"🔧 Model configured with tools: {[tool.name for tool in tools_wrapper]}")
        
        # Invoke model with tools
        response_msg = model_with_tools.invoke(conversation, config)
        
        print("✅ Response generated")
        print(f"🔍 Response type: {type(response_msg)}")
        print(f"🔍 Response content: {response_msg.content if hasattr(response_msg, 'content') else 'No content'}")
        print(f"🔍 Response additional_kwargs: {response_msg.additional_kwargs if hasattr(response_msg, 'additional_kwargs') else 'No kwargs'}")
        
        # Log tool calls if any
        if hasattr(response_msg, 'additional_kwargs') and response_msg.additional_kwargs.get('tool_calls'):
            tool_calls = response_msg.additional_kwargs['tool_calls']
            print(f"🛠️ Model requested {len(tool_calls)} tool calls")
            for idx, tool in enumerate(tool_calls, 1):
                print(f"  Tool #{idx}: {tool['function']['name']}")
        else:
            print("💬 Model responded directly without tools")
        
        # Update state
        updated_state = state.copy()
        updated_state["messages"] = messages + [response_msg]
        updated_state["recursion_count"] = state.get("recursion_count", 0) + 1
        
        return updated_state
        
    except Exception as e:
        print(f"❌ Error in UI generator: {e}")
        
        error_message = AIMessage(
            content=f"I encountered an error while generating the UI component: {str(e)}"
        )
        
        updated_state = state.copy()
        updated_state["messages"] = messages + [error_message]
        updated_state["recursion_count"] = state.get("recursion_count", 0) + 1
        
        return updated_state 
from ..graphstate import GraphState
import json

def tools_condition(state: GraphState):
    """Determine the next step based on the presence of tool calls."""
    messages = state["messages"]
    last_message = messages[-1]
    recursion_count = state["recursion_count"]
    recursion_limit = state["recursion_limit"]

    print("🔄 DEFAULT AGENT WORKFLOW TRANSITION")

    # Check for tool_calls in additional_kwargs
    tool_calls = None
    if hasattr(last_message, 'additional_kwargs'):
        tool_calls = last_message.additional_kwargs.get('tool_calls', None)
        if tool_calls:
            print("📋 TOOLS REQUESTED")
            for idx, tool in enumerate(tool_calls, 1):
                print(f"Tool #{idx}: {tool['function']['name']}")
        else:
            print("❌ NO TOOL CALLED")

    # Decision making
    if not tool_calls:
        print(f"• No tools requested - Completing workflow ({recursion_count}/{recursion_limit})")
        return "finish"

    if recursion_count > recursion_limit:
        print(f"• Recursion limit reached - Forcing completion ({recursion_count}/{recursion_limit})")
        return "end"

    print(f"• Tools pending execution - Continuing workflow ({recursion_count}/{recursion_limit})")
    return "continue" 
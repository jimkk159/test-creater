"""
Example of using the refactored tool nodes.

This example shows how the new modular structure makes the code much cleaner
and easier to understand.
"""

from myPocketFlow import AsyncFlow
from nodes import GetToolsNode, DecideToolNode, ExecuteToolNode, Actions

# Create clean, focused nodes
get_tools = GetToolsNode()
decide_tool = DecideToolNode()
execute_tool = ExecuteToolNode()

# Wire up the flow with clear action transitions
get_tools >> decide_tool
decide_tool - Actions.TOOL >> execute_tool
execute_tool >> decide_tool  # Loop back for multi-step operations

# Create the flow
tool_flow = AsyncFlow(start=get_tools)

async def main():
    """Example usage of the tool flow"""
    shared = {
        "question": "What files are in the current directory?"
    }
    
    # Run the flow
    await tool_flow.run_async(shared)
    
    # Access the result
    if "file" in shared and "result" in shared["file"]:
        print("Final result:", shared["file"]["result"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 
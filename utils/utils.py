import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
    
def get_tools(server_script_path):
    """Get available tools from an MCP server.
    """
    async def _get_tools():
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_response = await session.list_tools()
                return tools_response.tools
    
    return asyncio.run(_get_tools())
    
def call_tool(server_script_path=None, tool_name=None, arguments=None):
    """Call a tool on an MCP server.
    """
    async def _call_tool():
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text
    
    return asyncio.run(_call_tool())

if __name__ == "__main__":
    # Find available tools
    print("=== Finding available tools ===")
    tools = get_tools("mcp_server.py")
    
    # Print tool information nicely formatted
    for i, tool in enumerate(tools, 1):
        print(f"\nTool {i}: {tool.name}")
        print("=" * (len(tool.name) + 8))
        print(f"Description: {tool.description}")
        
        # Parameters section
        print("Parameters:")
        properties = tool.inputSchema.get('properties', {})
        required = tool.inputSchema.get('required', [])
        
        # No parameters case
        if not properties:
            print("  None")
        
        # Print each parameter with its details
        for param_name, param_info in properties.items():
            param_type = param_info.get('type', 'unknown')
            req_status = "(Required)" if param_name in required else "(Optional)"
            print(f"  • {param_name}: {param_type} {req_status}")
    
    # Call a tool
    print("\n=== Calling the read file tool ===")
    result = call_tool("mcp_server.py", "read_file_tool", {"path": "text.txt"})
    print(f"Result : {result}")

    print("=== Get directory structure ===")
    result = call_tool("mcp_server.py", "read_directory_tree_tool", {"path": "."})
    print(f"Result : {result}")



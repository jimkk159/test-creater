import os
from .base import BaseAsyncToolNode
from ..constants import MCP_SERVER_PATH
from ..shared import ToolSharedManager
from ..formatters.tool import ToolFormatter
from utils.utils import get_tools

class GetToolsNode(BaseAsyncToolNode):
    """Node responsible for retrieving available tools from MCP server"""
    
    async def prep_async(self, shared):
        """Validate server path and prepare for tool retrieval"""
        print("🔍 Getting available tools...")
        
        allowed_dir = os.environ.get("ALLOW_READ_FILE_PATH")
        workspace_root = os.getcwd()
        absolute_server_path = os.path.join(workspace_root, MCP_SERVER_PATH)
        
        if not absolute_server_path.startswith(allowed_dir):
            raise ValueError(
                f"Error: The mcp_server.py script ({absolute_server_path}) "
                f"is not located within the allowed directory ({allowed_dir})."
            )
        
        return MCP_SERVER_PATH

    async def exec_async(self, server_path):
        """Retrieve tools from the MCP server"""
        return await get_tools(server_path)

    async def post_async(self, shared, prep_res, tools):
        """Store tools and formatted tool information in shared state"""
        ToolSharedManager.store_tools(shared, tools)
        tool_info = ToolFormatter.format_tool_info(tools)
        ToolSharedManager.store_tool_info(shared, tool_info) 
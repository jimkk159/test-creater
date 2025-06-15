from .base import BaseAsyncToolNode
from ..constants import Actions, MCP_SERVER_PATH
from ..shared import ToolSharedManager
from utils.utils import call_tool

class ExecuteToolNode(BaseAsyncToolNode):
    """Node responsible for executing the chosen tool"""
    
    async def prep_async(self, shared):
        """Prepare tool execution parameters"""
        tool_name = ToolSharedManager.get_tool_name(shared)
        parameters = ToolSharedManager.get_parameters(shared)
        return tool_name, parameters

    async def exec_async(self, inputs):
        """Execute the chosen tool with provided parameters"""
        tool_name, parameters = inputs
        print(f"🔧 Executing tool '{tool_name}' with parameters: {parameters}")
        return await call_tool(MCP_SERVER_PATH, tool_name, parameters)

    async def post_async(self, shared, prep_res, result):
        """Store tool execution result"""
        ToolSharedManager.store_tool_result(shared, result)
        return Actions.TOOL_RESULT 
import os
from myPocketFlow import Node, AsyncNode
from utils.call_llm.open_ai import call_llm
from utils.utils import get_tools, call_tool, handle_max_iteration_error

from .constants import BORDER, SYSTEM_MAX_LOOP, MCP_SERVER_PATH, Actions
from .tool_formatter import ToolFormatter, PromptBuilder
from .response_parser import ResponseParser
from .shared_manager import SharedManager

class GetToolsNode(AsyncNode):
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
        SharedManager.store_tools(shared, tools)
        tool_info = ToolFormatter.format_tool_info(tools)
        SharedManager.store_tool_info(shared, tool_info)


class DecideToolNode(Node):
    """Node responsible for analyzing questions and deciding which tool to use"""
    
    def prep(self, shared):
        """Build the decision prompt for the LLM"""
        return PromptBuilder.build_decision_prompt(shared)

    def exec(self, prompt):
        """Call LLM to analyze question and decide tool usage"""
        print(BORDER)
        print("🤔 Analyzing question and deciding which tool to use...")
        response = call_llm(prompt)
        parsed_response = ResponseParser.parse_yaml_response(response)
        ResponseParser.validate_decision_response(parsed_response)
        return parsed_response

    def exec_fallback(self, prep_res, exc):
        """Handle parsing or validation errors"""
        return {"error": exc}
    
    def post(self, shared, prep_res, response):
        """Process the decision response and determine next action"""
        if "error" in response:
            return handle_max_iteration_error(
                shared, response, BORDER, SYSTEM_MAX_LOOP, ["decide"]
            )
        SharedManager.store_decision_response(shared, response)
        action = SharedManager.get_action(shared)
        print(BORDER)
        print(f"🎬 Selected action: {action}")

        if action == Actions.DONE:
            result = f"✅ FILE CONTENT:\n{SharedManager.get_tool_result(shared)}".rstrip('\n')
            SharedManager.set_final_result(shared, result)
            print(BORDER)
            return Actions.DEFAULT
            
        elif action == Actions.TOOL:
            tool_name = SharedManager.get_tool_name(shared)
            parameters = SharedManager.get_parameters(shared)
            print(f"💡 Selected tool: {tool_name}")
            print(f"🔢 Extracted parameters: {parameters}")
            return Actions.TOOL
        
        return Actions.ERROR


class ExecuteToolNode(AsyncNode):
    """Node responsible for executing the chosen tool"""
    
    async def prep_async(self, shared):
        """Prepare tool execution parameters"""
        tool_name = SharedManager.get_tool_name(shared)
        parameters = SharedManager.get_parameters(shared)
        return tool_name, parameters

    async def exec_async(self, inputs):
        """Execute the chosen tool with provided parameters"""
        tool_name, parameters = inputs
        print(f"🔧 Executing tool '{tool_name}' with parameters: {parameters}")
        return await call_tool(MCP_SERVER_PATH, tool_name, parameters)

    async def post_async(self, shared, prep_res, result):
        """Store tool execution result"""
        SharedManager.store_tool_result(shared, result)
        return Actions.TOOL_RESULT 
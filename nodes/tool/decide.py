from .base import BaseToolNode
from config import Actions, SystemConfig
from ..shared import ToolSharedManager
from ..formatters.tool import PromptBuilder
from ..response_parser import ResponseParser
from utils.call_llm.open_ai import call_llm
from config import SharedKeys

class DecideToolNode(BaseToolNode):
    """Node responsible for analyzing questions and deciding which tool to use"""
    
    def prep(self, shared):
        """Build the decision prompt for the LLM"""
            
        return PromptBuilder.build_decision_prompt(shared)

    def exec(self, prompt):
        """Call LLM to analyze question and decide tool usage"""
        print(SystemConfig.BORDER)
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
            return self.handle_error(shared, response)
            
        ToolSharedManager.store_decision_response(shared, response)
        action = ToolSharedManager.get_action(shared)
        print(SystemConfig.BORDER)
        print(f"🎬 Selected action: {action}")

        if action == Actions.DONE:
            result = f"✅ FILE CONTENT:\n{ToolSharedManager.get_tool_result(shared)}".rstrip('\n')
            ToolSharedManager.set_final_result(shared, result)            
            return Actions.DEFAULT
            
        elif action == Actions.TOOL:
            tool_name = ToolSharedManager.get_tool_name(shared)
            parameters = ToolSharedManager.get_parameters(shared)
            print(f"💡 Selected tool: {tool_name}")
            print(f"🔢 Extracted parameters: {parameters}")
            if(shared[SharedKeys.FILE][SharedKeys.TOOL_NAME] == 'read_file_tool'):
                shared[SharedKeys.FILE_PATH] = parameters['path']
            return Actions.TOOL
        
        return Actions.ERROR 
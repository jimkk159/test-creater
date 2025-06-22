from myPocketFlow import Node
from utils.call_llm.open_ai import call_llm
from utils.utils import get_error_prompt, handle_max_iteration_error

from ..shared import TestSharedManager
from config import SharedKeys, SystemConfig
from ..formatters.test import TestPromptBuilder
from ..response_parser.test import TestResponseParser

class AnalyzeAndExtractFunctionNode(Node):
    """Node responsible for analyzing files and extracting functions to test"""
    
    def prep(self, shared):
        """Prepare analysis prompt"""
        print(SystemConfig.BORDER)
        print("🔍 Analyze the file content...")
        
        # Get file content from the appropriate key based on shared structure
        file_content = shared[SharedKeys.FILE].get("tool_result") or shared[SharedKeys.FILE].get("result", "")
        TestSharedManager.store_file_content(shared, file_content)
        error_prompt = get_error_prompt(shared, ['analyze'])
        
        return TestPromptBuilder.build_analyze_prompt(
            file_content, 
            error_prompt
        )

    def exec(self, prompt):
        """Extract functions from file content"""
        response = call_llm(prompt)
        return TestResponseParser.parse_functions_from_response(response)
    
    def exec_fallback(self, prep_res, exc):
        """Handle parsing errors"""
        return {"error": exc}

    def post(self, shared, prep_res, response):
        """Store extracted functions"""
        if isinstance(response, dict) and "error" in response:
            return handle_max_iteration_error(
                shared, response, SystemConfig.BORDER, SystemConfig.SYSTEM_MAX_LOOP, node_name="analyze", keys=["analyze"]
            )
        
        TestSharedManager.store_functions(shared, response)
        TestSharedManager.store_functions_order(shared, response)
        print(SystemConfig.BORDER)
        print(f"⛏️ extracted functions: {list(response.keys())}") 
from myPocketFlow import Node
from utils.call_llm.open_ai import call_llm
from utils.utils import get_error_prompt, handle_max_iteration_error

from ..shared import TestSharedManager
from ..constants import BORDER, SYSTEM_MAX_LOOP
from ..formatters.test import TestPromptBuilder
from ..response_parser.test import TestResponseParser

class AnalyzeNode(Node):
    """Node responsible for analyzing files and extracting functions to test"""
    
    def prep(self, shared):
        """Prepare analysis prompt"""
        print(BORDER)
        print("🔍 Analyze the file content...")
        
        TestSharedManager.store_file_content(shared, shared["file"]["tool_result"])
        error_prompt = get_error_prompt(shared, ['analyze'])
        
        return TestPromptBuilder.build_analyze_prompt(
            shared["file"]["tool_result"], 
            error_prompt
        )

    def exec(self, prompt):
        """Extract functions from file content"""
        response = call_llm(prompt)
        return TestResponseParser.parse_functions_from_response(response)
    
    def exec_fallback(self, prep_res, exc):
        """Handle parsing errors"""
        return {"error": exc}

    def post(self, shared, prep_res, functions):
        """Store extracted functions"""
        if "error" in functions:
            return handle_max_iteration_error(
                shared, functions, BORDER, SYSTEM_MAX_LOOP, ["analyze"]
            )
        
        TestSharedManager.store_functions(shared, functions)
        print(BORDER)
        print(f"⛏️ extracted functions: {list(functions.keys())}") 
from myPocketFlow import Node
from utils.call_llm.open_ai import call_llm
from utils.utils import get_error_prompt, handle_max_iteration_error

from ..shared import TestSharedManager, ToolSharedManager
from ..constants import BORDER, SYSTEM_MAX_LOOP, SharedKeys, TestKeys
from ..formatters.test import TestFormatter, TestPromptBuilder
from ..response_parser.test import TestResponseParser

class ImplementFunctionNode(Node):
    """Node responsible for implementing test functions"""
    
    def prep(self, shared):
        """Prepare implementation prompt"""
        print(BORDER)
        print("📝 Implementing test cases...")
        function_name = self.params["function_name"]
        file_path = shared[SharedKeys.FILE_PATH]
        functions = shared[TestKeys.FUNCTIONS][function_name]
        test_cases = shared[TestKeys.TEST_CASES][function_name]["init"]

        formatted_tests = TestFormatter.format_test_cases(test_cases)
        error_prompt = ""
        error_prompt = get_error_prompt(shared, ['implement', function_name])
            
        prompt = TestPromptBuilder.build_implement_prompt(file_path, functions, formatted_tests, error_prompt)
        # prompt_file = TestPromptBuilder.save_prompt_to_file(prompt, 'implement', function_name)
        
        return prompt

    def exec(self, prompt):
        """Implement test functions using LLM"""
        response = call_llm(prompt)

        parsed_response = TestResponseParser.parse_yaml_response(response)
        TestResponseParser.validate_implement_response(parsed_response)
        return parsed_response["function_code"]

    def exec_fallback(self, prep_res, exc):
        """Handle implementation errors"""
        return { "error": exc }

    def post(self, shared, prep_res, test_code):
        """Store implemented test code"""
        function_name = self.params["function_name"]
        
        if "error" in test_code:
            return handle_max_iteration_error(
                shared, test_code, BORDER, SYSTEM_MAX_LOOP, ["implement", function_name]
            )
        TestSharedManager.store_test_code(shared, function_name, test_code) 
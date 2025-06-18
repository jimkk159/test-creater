from myPocketFlow import Node
from utils.call_llm.open_ai import call_llm
from utils.utils import get_error_prompt, handle_max_iteration_error

from ..shared import TestSharedManager
from config import SystemConfig, SharedKeys
from ..formatters.test import TestFormatter, TestPromptBuilder
from ..response_parser.test import TestResponseParser

class GenerateTestCasesNode(Node):
    """Node responsible for generating test cases for functions"""
    
    def prep(self, shared):
        """Prepare test case generation prompt"""
        if SharedKeys.FUNCTIONS not in shared or not shared[SharedKeys.FUNCTIONS]:
            raise ValueError("No functions found in shared context")

        function_name = self.params["function_name"]
        function_content = self.params["function_content"]
        
        print(f"{SystemConfig.BORDER}\n🧪 Generate {function_name} test cases...")
        
        error_prompt = get_error_prompt(shared, ['generateTestCases', function_name])
        
        return TestPromptBuilder.build_test_case_prompt(
            function_name, 
            function_content, 
            error_prompt
        )

    def exec(self, prompt):
        """Generate test cases using LLM"""
        try:
            response = call_llm(prompt)
            parsed_response = TestResponseParser.parse_yaml_response(response)
            TestResponseParser.validate_test_case_response(parsed_response)
            return parsed_response
        except Exception as e:
            raise e

    def exec_fallback(self, prep_res, exc):
        """Handle generation errors"""
        return {"error": exc}

    def post(self, shared, prep_res, response):
        """Store generated test cases"""
        function_name = self.params["function_name"]
        
        if "error" in response:
            return handle_max_iteration_error(
                shared, response, SystemConfig.BORDER, SystemConfig.SYSTEM_MAX_LOOP, ["generateTestCases", function_name]
            )
        TestSharedManager.store_test_cases(shared, function_name, response["test_cases"])
        # TestFormatter.print_test_cases(response["test_cases"]) 
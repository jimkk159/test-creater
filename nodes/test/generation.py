import pprint
from myPocketFlow import Node
from utils.call_llm.open_ai import call_llm
from utils.utils import get_error_prompt, handle_max_iteration_error

from ..shared import TestSharedManager
from config import SystemConfig, SharedKeys
from ..formatters.test import TestPromptBuilder
from ..response_parser.test import TestResponseParser

class GenerateTestCasesNode(Node):
    """Node responsible for generating test cases for functions"""

    def prep(self, shared):
        """Prepare test case generation prompt"""
        if SharedKeys.FUNCTIONS not in shared or not shared[SharedKeys.FUNCTIONS]:
            raise ValueError("No functions found in shared context")

        function_name = self.params[SharedKeys.FUNCTION_NAME]
        function_content = self.params[SharedKeys.FUNCTION_CONTENT]
        
        if SharedKeys.SUGGESTION not in shared:
            shared[SharedKeys.SUGGESTION] = {}
        suggestion = "\n".join(shared[SharedKeys.SUGGESTION].get(function_name, []))

        print(f"{SystemConfig.BORDER}\n🧪 Generate {function_name} test cases...")

        error_prompt = get_error_prompt(shared, ["generateTestCases", function_name])
        return TestPromptBuilder.build_test_case_prompt(
            function_name, function_content, suggestion, error_prompt
        )

    def exec(self, prompt):
        """Generate test cases using LLM"""
        try:
            print(1111, 'generate', prompt)
            response = call_llm(prompt)
            print(2222, 'generate',response)
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
        function_name = self.params[SharedKeys.FUNCTION_NAME]
        if isinstance(response, dict) and "error" in response:
            return handle_max_iteration_error(
                shared,
                response,
                SystemConfig.BORDER,
                SystemConfig.SYSTEM_MAX_LOOP,
                node_name="generateTestCases",
                function_name=function_name,
                keys=["generateTestCases", function_name],
            )
        TestSharedManager.store_test_cases(
            shared, function_name, response[SharedKeys.TEST_CASES]
        )
        # TestFormatter.print_test_cases(response["test_cases"])
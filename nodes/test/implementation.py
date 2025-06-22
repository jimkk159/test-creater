from myPocketFlow import Node
from utils.call_llm.open_ai import call_llm
from utils.utils import get_error_prompt, handle_max_iteration_error

from ..shared import TestSharedManager, ToolSharedManager
from config import SystemConfig, SharedKeys
from ..formatters.test import TestFormatter, TestPromptBuilder
from ..response_parser.test import TestResponseParser


class ImplementFunctionNode(Node):
    """Node responsible for implementing test functions"""

    def prep(self, shared):
        """Prepare implementation prompt"""
        print(SystemConfig.BORDER)
        function_name = self.params["function_name"]
        print(f"📝 Implementing {function_name} test cases...")
        file_path = shared[SharedKeys.FILE_PATH]
        functions = shared[SharedKeys.FUNCTIONS][function_name]
        test_cases = shared[SharedKeys.TEST_CASES][function_name]["init"]

        formatted_tests = TestFormatter.format_test_cases(test_cases)
        error_prompt = ""
        error_prompt = get_error_prompt(shared, ["implement", function_name])

        prompt = TestPromptBuilder.build_implement_prompt(
            file_path, functions, formatted_tests, error_prompt
        )
        # prompt_file = TestPromptBuilder.save_prompt_to_file(prompt, 'implement', function_name)

        return prompt

    def exec(self, prompt):
        """Implement test functions using LLM"""
        print(1111, 'implement', prompt)
        response = call_llm(prompt)
        print(2222, 'implement', response)

        parsed_response = TestResponseParser.parse_yaml_response(response)
        TestResponseParser.validate_implement_response(parsed_response)
        return parsed_response["function_code"]

    def exec_fallback(self, prep_res, exc):
        """Handle implementation errors"""
        return {"error": exc}

    def post(self, shared, prep_res, test_code):
        """Store implemented test code"""
        function_name = self.params.get("function_name", "unknown")
        if isinstance(test_code, dict) and "error" in test_code:
            print(f"    Error detected for {function_name}")
            return handle_max_iteration_error(
                shared,
                test_code,
                SystemConfig.BORDER,
                SystemConfig.SYSTEM_MAX_LOOP,
                node_name="implement",
                function_name=function_name,
                keys=["implement", function_name],
            )
        TestSharedManager.store_test_code(shared, function_name, test_code)

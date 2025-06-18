import os
import re
from myPocketFlow import Node
from utils.call_llm.open_ai import call_llm
from utils.utils import get_error_prompt, handle_max_iteration_error

from ..shared import TestSharedManager
from config import SystemConfig, TestActions, SharedKeys, SharedKeys
from ..formatters.test import TestFormatter, TestPromptBuilder
from ..response_parser.test import TestResponseParser


class ReviseNode(Node):
    """Node responsible for revising failed test cases"""

    def prep(self, shared):
        """Prepare revision prompt"""
        print(SystemConfig.BORDER)
        print("💭 AI review the test result...")
        function_name = self.params["function_name"]
        TestSharedManager.increment_iteration_count(shared, function_name)
        test_cases = shared.get(SharedKeys.TEST_CASES, {})
        failed_tests = shared.get(SharedKeys.FAILED_TESTS, {})
        try:
            # Format test cases for prompt
            formatted_tests = ""
            formatted_tests += TestFormatter.format_test_cases(
                test_cases[function_name]["init"]
            )

            # Format failed tests for prompt
            formatted_failures = TestFormatter.format_failed_tests(
                failed_tests[function_name]
            )

            # Get functions from shared
            functions = shared.get(SharedKeys.FUNCTIONS, {})

            # Get test code from shared
            test_code_dict = shared.get(SharedKeys.TEST_CODE, {})
            test_code = test_code_dict[function_name]
            # Get test code from shared
            file_path = shared.get(SharedKeys.FILE_PATH, "")
            suggested_file_path = shared.get(SharedKeys.SUGGESTED_FILE_PATH, "")

            # Regular expression to match only inside require()
            pattern = (
                rf"(require\(['\"]){re.escape(os.path.abspath(file_path))}(['\"]\))"
            )
            replacement = rf"\1{os.path.abspath(suggested_file_path[function_name])}\2"

            # Perform the replacement
            new_test_code = re.sub(pattern, replacement, test_code)

            # Get error prompt
            error_prompt = get_error_prompt(shared, ["revise", function_name])

            return TestPromptBuilder.build_revise_prompt(
                formatted_tests,
                functions[function_name],
                new_test_code,
                formatted_failures,
                error_prompt,
            )

        except Exception as e:
            print(f"Error preparing revision prompt: {e}")
            return {"error": e}

    def exec(self, prompt_input):
        """Revise test cases using LLM"""
        response = call_llm(prompt_input)
        parsed_response = TestResponseParser.parse_yaml_response(response)
        TestResponseParser.validate_revise_response(parsed_response)
        return parsed_response

    def exec_fallback(self, prep_res, exc):
        """Handle revision errors"""
        return {"error": exc}

    def post(self, shared, prep_res, response):
        """Process revision results"""
        function_name = self.params["function_name"]
        if "error" in response:
            return handle_max_iteration_error(
                shared,
                response,
                SystemConfig.BORDER,
                SystemConfig.SYSTEM_MAX_LOOP,
                ["revise", function_name],
            )

        action = response.get("action")
        if action == "pass":
            print("✅ All tests passed!")
            return TestActions.DEFAULT
        elif action == "error":
            print("❌ Error occurred during revision")
            return TestActions.ERROR
        elif action == "revise":
            self._print_revisions(response.get("test_cases", {}))
            TestSharedManager.store_revisions(
                shared,
                function_name,
                response[SharedKeys.TEST_CODE],
                response[SharedKeys.FUNCTION_SUGGESTION],
            )
            with open(shared[SharedKeys.SUGGESTED_FILE_PATH][function_name], "w") as f:
                f.write(shared[SharedKeys.FUNCTIONS][function_name])

            return TestActions.DEFAULT
        else:
            print(f"❌ Unknown action: {action}")
            return TestActions.ERROR

    def _print_revisions(self, test_cases):
        """Print revision details"""
        print("\n=== Test Case Revisions ===")
        # for type_name, test_cases_list in test_cases.items():
        print("\n" + 'retry'.center(50, "-"))
        for test_case in test_cases['retry']:
            print(f"\nTest Case: {test_case['name']}")
            print(f"Status: {test_case['status']}")
            print(f"Input: {test_case['input']}")
            print(f"Expected: {test_case['expected']}")
        print("\n" + "-" * 50)

import copy
import pprint
from utils.call_llm.open_ai import call_llm
from ..shared import SuperviseSharedManager
from config import SharedKeys, Actions, SystemConfig
from nodes.tool.base import AsyncBaseToolNode
from nodes.shared.base import BaseSharedManager
from nodes.formatters import TestFormatter, SupervisePromptBuilder
from nodes.response_parser import ResponseParser


class SuperviseTestCaseNode(AsyncBaseToolNode):
    """Node responsible for analyzing questions and deciding which tool to use"""

    async def prep_async(self, shared):
        """Prepare supervise test case prompt"""
        print(SystemConfig.BORDER)
        print("🧠 Evaluate whether the generated test cases are reasonable...")
        function_name = self.params[SharedKeys.FUNCTION_NAME]
        test_cases = BaseSharedManager.get_value(
            shared, [SharedKeys.TEST_CASES, function_name, "init"], ""
        )

        formatted_tests = TestFormatter.format_test_cases(test_cases)

        return SupervisePromptBuilder.supervise_test_case_prompt(
            shared, function_name, formatted_tests
        )

    async def exec_async(self, prompt):
        """Call LLM to Evaluate test cases"""
        response = call_llm(prompt)
        parsed_response = ResponseParser.parse_yaml_response(response)
        ResponseParser.validate_supervise_response(parsed_response)
        return parsed_response

    async def post_async(self, shared, prep_res, response):
        """Process the decision response and determine next action"""
        if "error" in response:
            return self.handle_error_async(shared, response)

        function_name = self.params[SharedKeys.FUNCTION_NAME]
        old_suggestions = BaseSharedManager.get_value(
            shared, [SharedKeys.SUGGESTION, function_name], []
        )
        old_suggestions.append(response.get(SharedKeys.SUGGESTION, ""))
        new_suggestions = copy.deepcopy(old_suggestions)

        BaseSharedManager.store_value(
            shared, [SharedKeys.SUGGESTION, function_name], new_suggestions
        )
        
        if SharedKeys.SUGGESTION_ITERATION_COUNT not in shared:
            shared[SharedKeys.SUGGESTION_ITERATION_COUNT] = {}

        BaseSharedManager.store_value(
            shared,
            [SharedKeys.SUGGESTION_ITERATION_COUNT, function_name],
            shared[SharedKeys.SUGGESTION_ITERATION_COUNT].get(function_name, 0) + 1,
        )
        
        max_suggestion_iteration = SuperviseSharedManager.get_max_suggestion_iteration(shared)
        if shared[SharedKeys.SUGGESTION_ITERATION_COUNT][function_name] >= max_suggestion_iteration:
            print(SystemConfig.BORDER)
            print(f"⚠️  Reached {max_suggestion_iteration} iterations, accepting current test cases for {function_name}")
            return Actions.DEFAULT  # Force completion

        if SuperviseSharedManager.check_max_iterations_reached(shared, function_name):
            print("Max iterations reached for one or more test suites.")
            pprint.pprint(response)
            raise Exception("Max iterations reached for one or more test suites.")

        action = response.get("action", Actions.ERROR)
        print(SystemConfig.BORDER)
        print(f"🎬 Selected action: {action}")

        if action == Actions.DONE:
            result = f"✅ {function_name} test cases are good."
            print(SystemConfig.BORDER)
            print(result)
            return Actions.DEFAULT
        elif action == Actions.SUGGEST:
            print(SystemConfig.BORDER)
            print(f"💡 Selected action: {action}")
            return Actions.SUGGEST

        return Actions.ERROR

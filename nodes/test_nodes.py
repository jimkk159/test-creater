import re
from myPocketFlow import Node, AsyncParallelBatchNode
from utils.call_llm.open_ai import call_llm
from utils.code_executor import execute_jest_test, extract_test_counts
from utils.utils import extract_describe_blocks, get_error_prompt, handle_max_iteration_error

from .constants import BORDER, SYSTEM_MAX_LOOP
from .test_constants import TestActions, TestKeys, MAX_ITERATION
from .test_formatters import TestFormatter, TestPromptBuilder
from .test_response_parser import TestResponseParser
from .test_shared_manager import TestSharedManager

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


class GenerateTestCasesNode(Node):
    """Node responsible for generating test cases for functions"""
    
    def prep(self, shared):
        """Prepare test case generation prompt"""
        if TestKeys.FUNCTIONS not in shared or not shared[TestKeys.FUNCTIONS]:
            raise ValueError("No functions found in shared context")

        function_name = self.params["function_name"]
        function_content = self.params["function_content"]
        
        print(f"{BORDER}\n🧪 Generate {function_name} test cases...")
        
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
            print(1111, e)
            raise e

    def exec_fallback(self, prep_res, exc):
        """Handle generation errors"""
        return {"error": exc}

    def post(self, shared, prep_res, response):
        """Store generated test cases"""
        function_name = self.params["function_name"]
        
        if "error" in response:
            return handle_max_iteration_error(
                shared, response, BORDER, SYSTEM_MAX_LOOP, ["generateTestCases", function_name]
            )
    
        TestSharedManager.store_test_cases(shared, function_name, response["test_cases"])
        TestFormatter.print_test_cases(response["test_cases"])


class ImplementFunctionNode(Node):
    """Node responsible for implementing test functions"""
    
    def prep(self, shared):
        """Prepare implementation prompt"""
        print(BORDER)
        print("🏗️ Implement the test case functions...")
        
        function_name = self.params["function_name"]
        functions = shared[TestKeys.FUNCTIONS][function_name]
        test_cases = shared[TestKeys.TEST_CASES][function_name]["init"]
        
        formatted_tests = TestFormatter.format_test_cases(test_cases, function_name)
        
        error_prompt = ""
        if 'error-implement' in shared:
            error_prompt = get_error_prompt(shared, ['error-implement', 'revise', function_name])
        else:
            error_prompt = get_error_prompt(shared, ['implement', function_name])
        
        return TestPromptBuilder.build_implement_prompt(functions, formatted_tests, error_prompt)

    def exec(self, prompt):
        """Implement test functions using LLM"""
        response = call_llm(prompt)
        parsed_response = TestResponseParser.parse_yaml_response(response)
        TestResponseParser.validate_implement_response(parsed_response)
        return parsed_response["function_code"]

    def exec_fallback(self, prep_res, exc):
        """Handle implementation errors"""
        return {"error": exc}

    def post(self, shared, prep_res, test_code):
        """Store implemented test code"""
        function_name = self.params["function_name"]
        
        if "error" in test_code:
            return handle_max_iteration_error(
                shared, test_code, BORDER, SYSTEM_MAX_LOOP, ["implement", function_name]
            )
    
        TestSharedManager.store_test_code(shared, function_name, test_code)


class RunTestsNode(AsyncParallelBatchNode):
    """Node responsible for executing test functions in parallel"""
    
    async def prep_async(self, shared):
        """Prepare test execution"""
        print(BORDER)
        print("🏃 Running test functions...")
        
        function_name = self.params["function_name"]
        TestSharedManager.set_max_iterations(shared, shared.get("max_iteration", MAX_ITERATION))
        TestSharedManager.init_function_suite_iterations(shared, function_name)

        return extract_describe_blocks(shared[TestKeys.TEST_CODE][function_name])
    
    async def exec_async(self, test_code):
        """Execute individual test suite"""
        suite_match = re.search(r"describe\('([^']+)'", test_code)
        suite_name = suite_match.group(1) if suite_match else "unknown_suite"

        output = await execute_jest_test(test_code)
        
        end = output["end"]
        details = output["details"]
        test_counts = extract_test_counts(end)
        failed = test_counts["failed"]

        if failed == 0: 
            return {
                "status": test_counts,
                "detail": [],
                "suite": suite_name
            }
        
        failed_details = []
        for content in details:
            expected = content["expected"]
            received = content["received"]

            if (expected is None and received is None) or (expected != received):
                failed_details.append({
                    "suite": content["suite"],
                    "test_case": content["test_case"],
                    "passed": False,
                    "received": received,
                    "expected": expected,
                    "description": content["description"]
                })
                
        return {
            "status": test_counts,
            "detail": failed_details,
            "suite": suite_name
        }

    async def post_async(self, shared, prep_res, exec_res_list):
        """Process test execution results"""
        function_name = self.params["function_name"]
        total_tests = passed_tests = failed_tests = 0
        all_failed_details = []

        # Aggregate results from all test suites
        for batch_result in exec_res_list:
            if isinstance(batch_result, dict) and "status" in batch_result:
                status = batch_result["status"]
                suite_name = batch_result.get("suite", "unknown_suite")
                
                TestSharedManager.increment_suite_iteration(shared, function_name, suite_name)
                
                total_tests += status.get("total", 0)
                passed_tests += status.get("passed", 0)
                failed_tests += status.get("failed", 0)
                
                if "detail" in batch_result:
                    all_failed_details.extend(batch_result["detail"])

        TestFormatter.print_test_results(function_name, passed_tests, total_tests)

        if failed_tests == 0:
            return TestActions.DEFAULT
            
        TestSharedManager.store_test_results(
            shared, function_name, passed_tests, total_tests, all_failed_details
        )
        
        if TestSharedManager.check_max_iterations_reached(shared, function_name):
            print("Max iterations reached for one or more test suites.")
            return TestActions.MAX_ITERATIONS
        else:
            print(f"❌Some tests failed. Revising code...")
            return TestActions.FAILURE


class ReviseNode(Node):
    """Node responsible for revising failed test cases"""
    
    def prep(self, shared):
        """Prepare revision prompt"""
        print(BORDER)
        print("💭 AI review the test result...")
        
        function_name = self.params["function_name"]
        TestSharedManager.increment_iteration_count(shared, function_name)
        
        test_cases = shared.get(TestKeys.TEST_CASES, {}) 
        failed_tests = shared.get(TestKeys.FAILED_TESTS, {}) 
        
        try:
            # Format test cases for prompt
            formatted_tests = ""
            count = 0
            for _, tests in test_cases[function_name].items():
                for test in tests:
                    count += 1
                    formatted_tests += f"{count}. {test['name']}\n"
                    if 'explain' in test:
                        formatted_tests += f"   explain: {test['explain']}\n"
                    formatted_tests += f"   input: {test['input']}\n"
                    formatted_tests += f"   expected: {test['expected']}\n\n"
            
            # Format failed tests
            formatted_failures = TestFormatter.format_failed_tests(failed_tests[function_name])
            
        except Exception as e:
            if TestKeys.IMPLEMENT not in shared:
                shared[TestKeys.IMPLEMENT] = {}
            shared[TestKeys.IMPLEMENT][function_name] = e
            return {'error-implement': e}
        
        error_prompt = get_error_prompt(shared, ['revise', function_name])
        
        return TestPromptBuilder.build_revise_prompt(
            test_cases, 
            shared.get(TestKeys.FUNCTIONS, {}), 
            formatted_failures, 
            error_prompt
        )

    def exec(self, prompt_input):
        """Revise test cases using LLM"""
        if 'error-implement' in prompt_input:
            return prompt_input
        
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
        
        if "error-implement" in response:
            return handle_max_iteration_error(
                shared, response, BORDER, SYSTEM_MAX_LOOP, 
                ["revise", function_name], return_key='error-implement'
            )

        if "error" in response:
            return handle_max_iteration_error(
                shared, response, BORDER, SYSTEM_MAX_LOOP, ["revise", function_name]
            )
        
        iteration_count = shared.get(TestKeys.ITERATION_COUNT, {}).get(function_name, 0)
        print(f"\n=== Revisions (Iteration {iteration_count}) ===")

        # Handle test case revisions
        if "test_cases" in response:
            self._print_revisions(response["test_cases"])
            
            original_cases = shared[TestKeys.TEST_CASES][function_name].get("init", [])
            merged = TestSharedManager.merge_test_cases(original_cases, response["test_cases"])
            shared[TestKeys.TEST_CASES][function_name]["init"] = merged
            print(BORDER)
        
        # Handle function suggestion
        if "function_suggestion" in response:
            TestSharedManager.store_function_suggestion(
                shared, function_name, response["function_suggestion"]
            )
        
        # Handle test code update
        if "test_code" in response:
            TestSharedManager.store_test_code(shared, function_name, response["test_code"])

    def _print_revisions(self, test_cases):
        """Print revision details"""
        print("Revising test cases:")
        
        for category in ["pass", "retry"]:
            if category in test_cases:
                print(f"{category.capitalize()} test cases:")
                for test_case in test_cases[category]:
                    print(f"  Test {test_case['name']}")
                    print(f"    input: {test_case['input']}")
                    print(f"    expected: {test_case['expected']}")
                    print(f"    status: {test_case['status']}")


# Create aliases for backward compatibility
Analyze_Node = AnalyzeNode
GenerateTestCases = GenerateTestCasesNode  
ImplementFunction = ImplementFunctionNode
RunTests = RunTestsNode
Revise = ReviseNode 
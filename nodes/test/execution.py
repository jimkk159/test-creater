import re
from myPocketFlow import AsyncParallelBatchNode
from utils.code_executor import execute_jest_test, extract_test_counts
from utils.utils import extract_describe_blocks

from ..shared import TestSharedManager
from ..formatters import TestFormatter
from ..constants import BORDER, TestActions, TestKeys, MAX_ITERATION

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
        suite_failed = test_counts["suite_failed"]
        
        if failed == 0 and suite_failed == 0: 
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
        total_tests = passed_tests = failed_tests = suite_failed_tests = 0
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
                suite_failed_tests += status.get("suite_failed", 0)
                
                if "detail" in batch_result:
                    all_failed_details.extend(batch_result["detail"])

        TestFormatter.print_test_results(function_name, passed_tests, total_tests)

        if failed_tests == 0 and suite_failed_tests == 0:
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
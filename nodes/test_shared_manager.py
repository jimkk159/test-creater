from .test_constants import TestKeys, TestStatus, MAX_ITERATION

class TestSharedManager:
    @staticmethod
    def init_analyze_section(shared):
        """Initialize analyze section"""
        if TestKeys.ANALYZE not in shared:
            shared[TestKeys.ANALYZE] = {}

    @staticmethod
    def store_file_content(shared, content):
        """Store file content for analysis"""
        TestSharedManager.init_analyze_section(shared)
        shared[TestKeys.ANALYZE][TestKeys.FILE_CONTENT] = content

    @staticmethod
    def store_functions(shared, functions):
        """Store extracted functions"""
        shared[TestKeys.FUNCTIONS] = functions

    @staticmethod
    def store_test_cases(shared, function_name, test_cases):
        """Store test cases for a function"""
        if TestKeys.TEST_CASES not in shared:
            shared[TestKeys.TEST_CASES] = {}
        shared[TestKeys.TEST_CASES][function_name] = {'init': test_cases[function_name]}

    @staticmethod
    def store_test_code(shared, function_name, test_code):
        """Store generated test code"""
        if TestKeys.TEST_CODE not in shared:
            shared[TestKeys.TEST_CODE] = {}
        shared[TestKeys.TEST_CODE][function_name] = test_code

    @staticmethod
    def init_test_tracking(shared):
        """Initialize test result tracking"""
        if TestKeys.PASSED not in shared:
            shared[TestKeys.PASSED] = {}
        if TestKeys.TOTAL_TESTS not in shared:
            shared[TestKeys.TOTAL_TESTS] = {}
        if TestKeys.FAILED_TESTS not in shared:
            shared[TestKeys.FAILED_TESTS] = {}

    @staticmethod
    def store_test_results(shared, function_name, passed, total, failed_details):
        """Store test execution results"""
        TestSharedManager.init_test_tracking(shared)
        shared[TestKeys.PASSED][function_name] = passed
        shared[TestKeys.TOTAL_TESTS][function_name] = total
        shared[TestKeys.FAILED_TESTS][function_name] = failed_details

    @staticmethod
    def init_suite_iterations(shared):
        """Initialize suite iterations tracking"""
        if TestKeys.SUITE_ITERATIONS not in shared:
            shared[TestKeys.SUITE_ITERATIONS] = {}

    @staticmethod
    def init_function_suite_iterations(shared, function_name):
        """Initialize suite iterations for a specific function"""
        TestSharedManager.init_suite_iterations(shared)
        if function_name not in shared[TestKeys.SUITE_ITERATIONS]:
            shared[TestKeys.SUITE_ITERATIONS][function_name] = {}

    @staticmethod
    def increment_suite_iteration(shared, function_name, suite_name):
        """Increment iteration count for a test suite"""
        TestSharedManager.init_function_suite_iterations(shared, function_name)
        if suite_name not in shared[TestKeys.SUITE_ITERATIONS][function_name]:
            shared[TestKeys.SUITE_ITERATIONS][function_name][suite_name] = 0
        shared[TestKeys.SUITE_ITERATIONS][function_name][suite_name] += 1

    @staticmethod
    def check_max_iterations_reached(shared, function_name):
        """Check if any suite has reached max iterations"""
        max_iterations = shared.get(TestKeys.MAX_ITERATIONS, MAX_ITERATION)
        
        if function_name not in shared.get(TestKeys.SUITE_ITERATIONS, {}):
            return False
            
        return any(
            shared[TestKeys.SUITE_ITERATIONS][function_name][suite] >= max_iterations
            for suite in shared[TestKeys.SUITE_ITERATIONS][function_name]
        )

    @staticmethod
    def init_iteration_count(shared):
        """Initialize iteration count tracking"""
        if TestKeys.ITERATION_COUNT not in shared:
            shared[TestKeys.ITERATION_COUNT] = {}

    @staticmethod
    def increment_iteration_count(shared, function_name):
        """Increment iteration count for a function"""
        TestSharedManager.init_iteration_count(shared)
        if function_name not in shared[TestKeys.ITERATION_COUNT]:
            shared[TestKeys.ITERATION_COUNT][function_name] = 0
        else:
            shared[TestKeys.ITERATION_COUNT][function_name] += 1

    @staticmethod
    def store_function_suggestion(shared, function_name, suggestions):
        """Store function suggestions"""
        if TestKeys.FUNCTION_SUGGESTION not in shared:
            shared[TestKeys.FUNCTION_SUGGESTION] = {}
        shared[TestKeys.FUNCTION_SUGGESTION][function_name] = suggestions

    @staticmethod
    def merge_test_cases(original_cases, revised_cases):
        """Merge original and revised test cases"""
        orig_map = {tc["name"]: tc.copy() for tc in original_cases if "name" in tc}
        
        for status in ["pass", "retry"]:
            for revised in revised_cases.get(status, []):
                name = revised.get("name")
                if name in orig_map:
                    orig_map[name].update(revised)
                    orig_map[name]["status"] = TestStatus.OK if status == "pass" else TestStatus.FAIL
                else:
                    revised["status"] = TestStatus.OK if status == "pass" else TestStatus.FAIL
                    orig_map[name] = revised
                    
        return list(orig_map.values())

    @staticmethod
    def get_max_iterations(shared):
        """Get max iterations setting"""
        return shared.get(TestKeys.MAX_ITERATIONS, MAX_ITERATION)

    @staticmethod
    def set_max_iterations(shared, max_iter):
        """Set max iterations"""
        shared[TestKeys.MAX_ITERATIONS] = max_iter 
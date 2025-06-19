from .base import BaseSharedManager
from config import SharedKeys, TestStatus, SystemConfig

class TestSharedManager(BaseSharedManager):
    @staticmethod
    def init_analyze_section(shared):
        """Initialize analyze section"""
        if SharedKeys.ANALYZE not in shared:
            shared[SharedKeys.ANALYZE] = {}

    @staticmethod
    def store_file_content(shared, content):
        """Store file content for analysis"""
        TestSharedManager.init_analyze_section(shared)
        BaseSharedManager.store_value(shared, [SharedKeys.ANALYZE, SharedKeys.FILE_CONTENT], content)

    @staticmethod
    def store_functions(shared, functions):
        """Store extracted functions"""
        BaseSharedManager.store_value(shared, [SharedKeys.FUNCTIONS], functions)
        
    @staticmethod
    def store_functions_order(shared, functions):
        """Store extracted functions order"""
        BaseSharedManager.store_value(shared, [SharedKeys.FUNCTIONS_ORDER], list(functions.keys()))

    @staticmethod
    def store_test_cases(shared, function_name, test_cases):
        """Store test cases for a function"""
        BaseSharedManager.store_dict(shared, [SharedKeys.TEST_CASES, function_name], {'init': test_cases[function_name]})

    @staticmethod
    def store_test_code(shared, function_name, test_code):
        """Store generated test code"""
        BaseSharedManager.store_value(shared, [SharedKeys.TEST_CODE, function_name], test_code)
    
    @staticmethod
    def store_revisions(shared, function_name, revisions, function_suggestion):
        """Store revisions for a function"""
        BaseSharedManager.store_value(shared, [SharedKeys.TEST_CODE, function_name], revisions)
        BaseSharedManager.store_value(shared, [SharedKeys.FUNCTIONS, function_name], function_suggestion)

    @staticmethod
    def init_test_tracking(shared):
        """Initialize test result tracking"""
        for key in [SharedKeys.PASSED, SharedKeys.TOTAL_TESTS, SharedKeys.FAILED_TESTS]:
            if key not in shared:
                shared[key] = {}

    @staticmethod
    def store_test_results(shared, function_name, passed, total, failed_details):
        """Store test execution results"""
        TestSharedManager.init_test_tracking(shared)
        BaseSharedManager.store_value(shared, [SharedKeys.PASSED, function_name], passed)
        BaseSharedManager.store_value(shared, [SharedKeys.TOTAL_TESTS, function_name], total)
        BaseSharedManager.store_value(shared, [SharedKeys.FAILED_TESTS, function_name], failed_details)

    @staticmethod
    def init_suite_iterations(shared):
        """Initialize suite iterations tracking"""
        if SharedKeys.SUITE_ITERATIONS not in shared:
            shared[SharedKeys.SUITE_ITERATIONS] = {}

    @staticmethod
    def init_function_suite_iterations(shared, function_name):
        """Initialize suite iterations for a specific function"""
        TestSharedManager.init_suite_iterations(shared)
        if function_name not in shared[SharedKeys.SUITE_ITERATIONS]:
            shared[SharedKeys.SUITE_ITERATIONS][function_name] = {}

    @staticmethod
    def increment_suite_iteration(shared, function_name, suite_name):
        """Increment iteration count for a test suite"""
        TestSharedManager.init_function_suite_iterations(shared, function_name)
        current = BaseSharedManager.get_value(shared[SharedKeys.SUITE_ITERATIONS], [function_name, suite_name], 0)
        BaseSharedManager.store_value(shared[SharedKeys.SUITE_ITERATIONS], [function_name, suite_name], current + 1)

    @staticmethod
    def check_max_iterations_reached(shared, function_name):
        """Check if any suite has reached max iterations"""
        max_iterations = BaseSharedManager.get_value(shared, [SharedKeys.MAX_ITERATIONS], SystemConfig.MAX_ITERATION)
        
        if function_name not in shared.get(SharedKeys.SUITE_ITERATIONS, {}):
            return False
            
        return any(
            shared[SharedKeys.SUITE_ITERATIONS][function_name][suite] >= max_iterations
            for suite in shared[SharedKeys.SUITE_ITERATIONS][function_name]
        )

    @staticmethod
    def init_iteration_count(shared):
        """Initialize iteration count tracking"""
        if SharedKeys.ITERATION_COUNT not in shared:
            shared[SharedKeys.ITERATION_COUNT] = {}

    @staticmethod
    def increment_iteration_count(shared, function_name):
        """Increment iteration count for a function"""
        TestSharedManager.init_iteration_count(shared)
        current = BaseSharedManager.get_value(shared, [SharedKeys.ITERATION_COUNT, function_name], 0)
        BaseSharedManager.store_value(shared, [SharedKeys.ITERATION_COUNT, function_name], current + 1)

    @staticmethod
    def store_function_suggestion(shared, function_name, suggestions):
        """Store function suggestions"""
        BaseSharedManager.store_value(shared, [SharedKeys.FUNCTION_SUGGESTION, function_name], suggestions)

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
        return BaseSharedManager.get_value(shared, [SharedKeys.MAX_ITERATIONS], SystemConfig.MAX_ITERATION)

    @staticmethod
    def set_max_iterations(shared, max_iter):
        """Set max iterations"""
        BaseSharedManager.store_value(shared, [SharedKeys.MAX_ITERATIONS], max_iter) 
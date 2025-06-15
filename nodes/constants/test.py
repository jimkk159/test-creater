# Test-specific constants
MAX_ITERATION = 5

# Test action types
class TestActions:
    PASS = "pass"
    REVIEW = "review"
    ERROR = "error"
    DEFAULT = "default"
    FAILURE = "failure"
    MAX_ITERATIONS = "max_iterations"

# Test shared keys
class TestKeys:
    ANALYZE = "analyze"
    FILE_CONTENT = "file_content"
    FUNCTIONS = "functions"
    TEST_CASES = "test_cases"
    TEST_CODE = "test_code"
    PASSED = "passed"
    TOTAL_TESTS = "total_tests"
    FAILED_TESTS = "failed_tests"
    SUITE_ITERATIONS = "suite_iterations"
    MAX_ITERATIONS = "max_iterations"
    ITERATION_COUNT = "iteration_count"
    FUNCTION_SUGGESTION = "function_suggestion"
    IMPLEMENT = "implement"

# Test status types
class TestStatus:
    OK = "ok"
    FAIL = "fail"
    PASSED = "passed"
    FAILED = "failed" 
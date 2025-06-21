"""
Centralized shared data keys for the application.
All shared store keys should be defined here to avoid hardcoded strings.
"""

class SharedKeys:
    """Core shared data keys used throughout the application"""
    
    # File and content keys
    FILE = "file"
    FILE_PATH = "file_path"
    FILE_CONTENT = "file_content"
    SUGGESTED_FILE_PATH = "suggested_file_path"
    FILE_DIRECTORY = "file_directory"
    FILE_STRUCTURE = "file_structure"
    
    # Function and test keys
    FUNCTIONS = "functions"
    FUNCTIONS_ORDER = "functions_order"
    FUNCTION_NAME = "function_name"
    FUNCTION_CONTENT = "function_content"
    TEST_CASES = "test_cases"
    TEST_CODE = "test_code"
    FUNCTION_SUGGESTION = "function_suggestion"
    COMBINED_FUNCTION = "combined_function"
    
    # Analysis and processing keys
    ANALYZE = "analyze"
    IMPLEMENT = "implement"
    
    # Test execution keys
    PASSED = "passed"
    TOTAL_TESTS = "total_tests"
    FAILED_TESTS = "failed_tests"
    SUITE_ITERATIONS = "suite_iterations"
    MAX_ITERATIONS = "max_iterations"
    ITERATION_COUNT = "iteration_count"
    
    # Tool-related keys
    TOOLS = "tools"
    TOOL_INFO = "tool_info"
    TOOL_NAME = "tool_name"
    TOOL_PARAMS = "tool_params"
    TOOL_RESULT = "tool_result"
    TOOL_ERROR = "tool_error"
    TOOL_VALIDATION = "tool_validation"
    
    # Action and result keys
    ACTION = "action"
    PARAMETERS = "parameters"
    THINKING = "thinking"
    RESULT = "result"
    QUESTION = "question"
    
    # System and utility keys
    TEMP_FILE_PATHS = "temp_file_paths"
    MAX_LOOP = "max_loop"
from . import ResponseParser
from ..constants import TestActions, TestStatus

class TestResponseParser(ResponseParser):
    @staticmethod
    def validate_test_case_response(parsed_response):
        """Validate test case generation response"""
        assert "test_cases" in parsed_response, "Result must have 'test_cases' field"
        assert isinstance(parsed_response["test_cases"], dict), "test_cases must be a dictionary"

        for function_name, test_case_list in parsed_response["test_cases"].items():
            assert isinstance(function_name, str), f"Function name must be string"

            for i, test_case in enumerate(test_case_list):
                assert "name" in test_case, f"{function_name} Test case {i} missing 'name' field"
                assert isinstance(test_case["name"], str), f"{function_name} Test case {i} 'name' must be string"
                assert "explain" in test_case, f"{function_name} Test case {i} missing 'explain' field"
                assert isinstance(test_case["explain"], str), f"{function_name} Test case {i} 'explain' must be string"
                assert "input" in test_case, f"{function_name} Test case {i} missing 'input' field"
                assert isinstance(test_case["input"], dict), f"{function_name} Test case {i} 'input' must be dict"
                assert "expected" in test_case, f"{function_name} Test case {i} missing 'expected' field"

    @staticmethod
    def validate_implement_response(parsed_response):
        """Validate implementation response"""
        assert "function_code" in parsed_response, "Result must have 'function_code' field"
        assert isinstance(parsed_response["function_code"], str), "function_code must be string"

    @staticmethod
    def validate_revise_response(parsed_response):
        """Validate revision response"""
        assert "action" in parsed_response, "Result must have 'action' field"
        assert parsed_response["action"] in [TestActions.PASS, TestActions.REVISE, TestActions.ERROR], \
            f"action must be one of: {TestActions.PASS}, {TestActions.REVISE}, {TestActions.ERROR}"
        assert "thinking" in parsed_response, "Result must have 'thinking' field"
        assert isinstance(parsed_response["thinking"], str), "thinking must be a string"
        
        if "test_cases" in parsed_response:
            assert isinstance(parsed_response["test_cases"], dict), "test_cases must be a dictionary"
            # assert "pass" in parsed_response["test_cases"], "test_cases must have 'pass' category"
            assert "retry" in parsed_response["test_cases"], "test_cases must have 'retry' category"
            
            # Validate pass test cases
            if "pass" in parsed_response["test_cases"]:
                for test_case in parsed_response["test_cases"]["pass"]:
                    assert "name" in test_case, f"Test case missing 'name' field"
                    assert "input" in test_case, f"Test case missing 'input' field"
                    assert "expected" in test_case, f"Test case missing 'expected' field"
                    assert "status" in test_case, f"Test case missing 'status' field"
                    assert test_case["status"] == TestStatus.OK, f"Pass test case status must be '{TestStatus.OK}'"
                
            # Validate retry test cases
            for test_case in parsed_response["test_cases"]["retry"]:
                assert "name" in test_case, f"Test case missing 'name' field"
                assert "input" in test_case, f"Test case missing 'input' field"
                assert "expected" in test_case, f"Test case missing 'expected' field"
                assert "status" in test_case, f"Test case missing 'status' field"
                assert test_case["status"] == TestStatus.FAIL, f"Retry test case status must be '{TestStatus.FAIL}'"
        
        if "function_suggestion" in parsed_response:
            if isinstance(parsed_response["function_suggestion"], list):
                for func in parsed_response["function_suggestion"]:
                    assert isinstance(func, str), "function_suggestion items must be strings"
            else:
                assert isinstance(parsed_response["function_suggestion"], str), "function_suggestion must be a string"
        
        if "test_code" in parsed_response:
            assert isinstance(parsed_response["test_code"], str), "test_code must be string"
            assert "describe" in parsed_response["test_code"], "Test code must include describe block"
            assert "test(" in parsed_response["test_code"], "Test code must include test cases"
            assert "expect" in parsed_response["test_code"], "Test code must include expect statements"

    @staticmethod
    def parse_functions_from_response(response):
        """Parse and convert functions list to dictionary"""
        parsed = TestResponseParser.parse_yaml_response(response)
        
        # Convert list of functions to dictionary
        functions_dict = {}
        for func in parsed.get("functions", []):
            for func_name, func_content in func.items():
                functions_dict[func_name] = func_content
        
        return functions_dict 
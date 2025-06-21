from . import ResponseParser
from config import TestActions, TestStatus, SharedKeys

class CoordinatorResponseParser(ResponseParser):
    @staticmethod
    def validate_combine_function_response(parsed_response):
        """Validate combine function response"""
        assert SharedKeys.COMBINED_FUNCTION in parsed_response, "Result must have 'combined_code' field"
        assert isinstance(parsed_response[SharedKeys.COMBINED_FUNCTION], str), "combined_code must be a string"
        
    def validate_combine_test_code_response(parsed_response):
        """Validate combine test code response"""
        assert SharedKeys.TEST_CODE in parsed_response, "Result must have 'test_code' field"
        assert isinstance(parsed_response[SharedKeys.TEST_CODE], str), "test_code must be a string"
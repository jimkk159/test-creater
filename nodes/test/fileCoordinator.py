import os
import re
from myPocketFlow import AsyncNode
from utils.call_llm.open_ai import call_llm
from utils.utils import get_error_prompt, handle_max_iteration_error

from ..shared import TestSharedManager
from config import SystemConfig, TestActions, SharedKeys, SharedKeys
from ..formatters.test import TestFormatter, TestPromptBuilder
from ..response_parser.test import TestResponseParser
    
class FileCoordinatorNode(AsyncNode):
    def prep_async(self, shared):
        if SharedKeys.TEST_CODE not in shared:
            shared[SharedKeys.TEST_CODE] = []
            
        print(shared)
        
        return TestPromptBuilder.build_file_coordinator_prompt(
            shared[SharedKeys.TEST_CODE],
            shared[SharedKeys.SUGGESTED_FILE_PATH]
        )
    
    def exec_async(self, prompt_input):
        # response = call_llm(prompt_input)
        # parsed_response = TestResponseParser.parse_yaml_response(response)
        # TestResponseParser.validate_revise_response(parsed_response)
        # return parsed_response
        pass
    
    def post_async(self, shared):
        print("🖨️Combing results...")
        pass
    
    
    
import os
from datetime import datetime
from myPocketFlow import AsyncNode
from utils.call_llm.open_ai import call_llm
from utils.utils import get_git_hash
from utils.file_utils import create_copy_file_path

from config import SystemConfig, SharedKeys, SharedKeys
from ..formatters.test import TestPromptBuilder
from ..response_parser import CoordinatorResponseParser
    
class FunctionCoordinatorNode(AsyncNode):
    async def prep_async(self, shared):
        if SharedKeys.TEST_CODE not in shared:
            shared[SharedKeys.TEST_CODE] = []
        
        return TestPromptBuilder.build_file_coordinator_function_prompt(
            shared[SharedKeys.FUNCTIONS_ORDER],
            shared[SharedKeys.FUNCTIONS],
            shared[SharedKeys.FILE_PATH],
            shared[SharedKeys.SUGGESTED_FILE_PATH]
        )
            
    async def exec_async(self, prompt_input):
        response = call_llm(prompt_input)

        parsed_response = CoordinatorResponseParser.parse_yaml_response(response)
        CoordinatorResponseParser.validate_combine_function_response(parsed_response)
        
        return parsed_response
    
    async def post_async(self, shared, prep_res, exec_res):
        print(SystemConfig.BORDER)
        print("🖨️  Combing results...")
        
        # Get copy file path using helper function
        original_file_path = shared[SharedKeys.FILE_PATH]
        copy_file_path = create_copy_file_path(original_file_path)
        
        shared[SharedKeys.COMBINED_FUNCTION] = exec_res[SharedKeys.COMBINED_FUNCTION]
        
        # Ensure test directory exists
        os.makedirs(SystemConfig.TEST_DIRECTORY, exist_ok=True)
        
        with open(copy_file_path, 'w') as f:
            f.write(exec_res[SharedKeys.COMBINED_FUNCTION])
        
        print(SystemConfig.BORDER) 
        print(f"✅ Suggested file saved to: {copy_file_path}")
    
class TestCoordinatorNode(AsyncNode):
    async def prep_async(self, shared):
        if SharedKeys.TEST_CODE not in shared:
            shared[SharedKeys.TEST_CODE] = []
 
        return TestPromptBuilder.build_file_coordinator_test_code_prompt(
            shared[SharedKeys.FUNCTIONS_ORDER],
            shared[SharedKeys.TEST_CODE],
            shared[SharedKeys.FILE_PATH],
            shared[SharedKeys.SUGGESTED_FILE_PATH]
        )
            
    async def exec_async(self, prompt_input):
        response = call_llm(prompt_input)
        parsed_response = CoordinatorResponseParser.parse_yaml_response(response)
        CoordinatorResponseParser.validate_combine_test_code_response(parsed_response)
        
        return parsed_response
    
    async def post_async(self, shared, prep_res, exec_res):
        print("🖨️Combing test results...")
        
        # Get original file path and extract info
        original_filename = os.path.basename(shared[SharedKeys.FILE_PATH])
        filename_without_ext = os.path.splitext(original_filename)[0]
        
        # Generate timestamp and get git commit hash
        timestamp = datetime.now().strftime("%Y%m%d")
        git_hash = get_git_hash()
        
        # Create test filename pattern: _20250621_7bf60e3.myMath_copy.test.js
        test_filename = f"_{timestamp}_{git_hash}.{filename_without_ext}.test.js"
        test_file_path = os.path.join(SystemConfig.TEST_DIRECTORY, test_filename)
        
        # Ensure test directory exists
        os.makedirs(SystemConfig.TEST_DIRECTORY, exist_ok=True)
        
        original_file_path = shared[SharedKeys.FILE_PATH]
        copy_file_path = create_copy_file_path(original_file_path)
        copy_filename = os.path.basename(copy_file_path)
        functions_string = ', '.join(shared[SharedKeys.FUNCTIONS_ORDER])
        
        write_content = f"""const {{ {functions_string} }} = require('./{copy_filename}');

{exec_res[SharedKeys.TEST_CODE]}"""
        
        # Write test code to file
        with open(test_file_path, 'w') as f:
            f.write(write_content)
            
        print(SystemConfig.BORDER)
        print(f"✅ Test code saved to: {test_file_path}")
    
class DeleteTempFileNode(AsyncNode):
    async def prep_async(self, shared):
        return None
    
    async def exec_async(self, prompt_input):
        return None
    
    async def post_async(self, shared, prep_res, exec_res):
        print(SystemConfig.BORDER)
        print("🗑️  Deleting temp files...")
        file_paths = shared[SharedKeys.SUGGESTED_FILE_PATH]
        
        # Handle both single file and list of files
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        
        for file_path in file_paths.values():
            try:
                os.remove(file_path)
                print(SystemConfig.BORDER_2)
                print(f"   ✅ Deleted: {file_path}")
            except FileNotFoundError:
                print(f"   ⚠️  File not found: {file_path}")
            except Exception as e:
                print(f"   ❌ Failed to delete {file_path}: {e}")
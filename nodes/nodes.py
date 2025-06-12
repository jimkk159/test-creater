import re
import yaml
import os
import time
import json
import asyncio
from dotenv import load_dotenv
from myPocketFlow import Node, AsyncNode, AsyncParallelBatchNode
from utils.call_llm.open_ai import call_llm
from utils.code_executor import execute_jest_test, extract_test_counts
from utils.utils import get_tools, call_tool, extract_describe_blocks, save_to_file, cleanup_temp_files
import aiofiles
import random
from .base_nodes import AsyncNodeWrapper, ReturnDefaultActionNode
from .tool_nodes import GetToolsNode, DecideToolNode, ExecuteToolNode
from .test_nodes import Analyze_Node, GenerateTestCases, ImplementFunction, RunTests, Revise

load_dotenv()

MAX_ITERATION = 3
BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"
allowed_dir=os.environ.get("ALLOW_READ_FILE_PATH")
#     def prep(self, shared):
#         print(border)
#         print("💭 AI review the test result...")
#         failed_tests = [r for r in shared["failed_tests"] ]

#         if 'iteration_count' not in shared:
#             shared['iteration_count'] = 0
#         else: 
#             shared['iteration_count'] += 1
            
#         test_cases = shared.get("test_cases", "") 
#         failed_tests = shared.get("failed_tests", "") 

#         # Format current test cases nicely
#         formatted_tests = ""
#         for i, func_name in enumerate(test_cases, 1):
#             for j, test in enumerate(test_cases[func_name], 1):
#                 formatted_tests += f"{i}. {test['name']}\n"
#                 formatted_tests += f"   explain: {test['explain']}\n"
#                 formatted_tests += f"   input: {test['input']}\n"
#                 formatted_tests += f"   expected: {test['expected']}\n\n"
        
#         # Format failed tests nicely
#         formatted_failures = ""
#         for i, result in enumerate(failed_tests, 1):
#             formatted_failures += f"{i}. {result['test_case']}:\n"
#             formatted_failures += f"   received: {result['received']}\n"
#             formatted_failures += f"   expected: {result['expected']}\n"
#             formatted_failures += f"   description: {result['description']}\n\n"

#         return {
#             "functions": shared.get("functions", ""),
#             "test_cases": shared.get("test_cases", ""),
#             "test_code": shared.get("test_code", ""),
#             "max_iterations": shared.get("max_iterations", ""),
#             "iteration_count": shared.get("iteration_count", 0),
#             "is_passed": shared.get("passed", 0) == shared.get("total_tests", 0),
#             "passed": shared.get("passed", ""),
#             "total_tests": shared.get("total_tests", ""),
#             "failed_tests": failed_tests,
#             "formatted_tests": formatted_tests,
#             "formatted_failures": formatted_failures
#         }

#     def exec(self, inputs):

#         prompt = f"""
# You are a QA engineer to check and fix the test code result. 

# ### NEXT ACTION
# Your action choice: [pass, review, error]

# - pass:
#     This action means the test codes are fine.

# - review:
#     This action means the test codes need to be adjust

# - error:
#     Something went wrong, and you need human to solve the problem

# ### GOAL
#     1. Make the test code reasonable.
#     2. Analyze the failures and output revisions in YAML. 
#     3. You should think about the test cases and its outputs both make sense or not.

# ### TIP
#     1. Sometime, the test code fail is due to the function to be test has some drawback.
#        You don't need to fix this kind of fail in the test result.
#     2. You should put the ok test code in the pass class, and retry test code in the retry class.
#     3. You should provide the entire revised test code in the test_code class.
#     4. If the original code has a bug, put the revised function in the function_suggestion.

# ### TEST RESULT INFORMATION

#     Current test cases:
#     {inputs["formatted_tests"] if inputs["formatted_tests"] else "No test cases available"}

#     Current function:
#     {f"```javascript\n{inputs['functions']}\n```" if inputs['functions'] else 'No functions available'}

#     Failed tests:
#     {inputs["formatted_failures"]}

# Output in this YAML format:
# ```yaml
# action: <name of the action>
# thinking: |
#     <your step-by-step reasoning about we should move forward or revise the test case>
    
# <if test code has bug>
# reasoning: |
#     Looking at the failures, I see that...
#     The issue appears to be...
#     I will revise...
#     I should put this into test code into retry...
# test_cases:  # Dictionary mapping test case index (1-based) to revised test case

#     1:
#         name: "Revised test name"
#         input: {{...}}
#         expected: ...
#         status: fail # This means the test code has bug
#         ....

# <if original function has bug>
#     This test code is fine. It's the original function has bug, I see that...
#     The issue appears to be...
#     I should put this into test code into pass...

#     1:
#         name: "Revised test name"
#         input: {{...}}
#         expected: ...
#         status: ok # This means the test code is fine
        
# function_suggestion: [] # Include this if has original function modification 
# test_code:  # Include this if revising function

# ### EXAMPLE
#     action: review
#     thinking: ...
#     reasoning: ...
#     test_cases:
#     pass:
#         - name: "Basic case with positive numbers"
#         input:
#             a: 2
#             b: 3
#         expected: 5
#         status: "ok"
#     retry:
#         - name: "Type case - adding a number and a string"
#         input:
#             a: "3"
#             b: 2
#         expected: "3 is not a number"
#         status: "fail"
#     function_suggestion: 
#         - |
#             {"""const add = async (a, b) => {
#                 return a + b;
#             };"""}
#     test_code: |
#         - |
#             {"""describe('add function', () => {
#                 const add = async (a, b) => a + b;
#                 test('Basic case - positive integers', async () => {
#                 expect(await add(1, 2)).toBe(2);
#                 });
#             });"""}
    
# ### IMPORTANT
#     1. You must have the retry and pass part in the test_cases, even there aren't anything inside.
#     2. function_suggestion must be a list, even it only has one.
# ```"""
#         response = call_llm(prompt)
#         yaml_str = response.split("```yaml")[1].split("```")[0].strip()
#         result = yaml.safe_load(yaml_str)

#         # Validation asserts
#         assert "action" in result, "Result must have 'action' field"
#         assert result["action"] in ["done", "review", "error"], "action must be one of: done, review, error"
#         assert "thinking" in result, "Result must have 'thinking' field"
#         assert "thinking" in result, "Result must have 'thinking' field"
#         assert isinstance(result["thinking"], str), "thinking must be a string"
        
#         if "test_cases" in result:
#             assert isinstance(result["test_cases"], dict), "test_cases must be a dictionary"
#             assert "pass" in result["test_cases"], "test_cases must have 'pass' category"
#             assert "retry" in result["test_cases"], "test_cases must have 'retry' category"
            
#             # Validate pass test cases
#             for test_case in result["test_cases"]["pass"]:
#                 assert "name" in test_case, f"Test case missing 'name' field"
#                 assert "input" in test_case, f"Test case missing 'input' field"
#                 assert "expected" in test_case, f"Test case missing 'expected' field"
#                 assert "status" in test_case, f"Test case missing 'status' field"
#                 assert test_case["status"] == "ok", f"Pass test case status must be 'ok'"
                
#             # Validate retry test cases
#             for test_case in result["test_cases"]["retry"]:
#                 assert "name" in test_case, f"Test case missing 'name' field"
#                 assert "input" in test_case, f"Test case missing 'input' field"
#                 assert "expected" in test_case, f"Test case missing 'expected' field"
#                 assert "status" in test_case, f"Test case missing 'status' field"
#                 assert test_case["status"] == "fail", f"Retry test case status must be 'fail'"
        
#         if "function_suggestion" in result:
#             assert isinstance(result["function_suggestion"], list), "function_suggestion must be a list"
#             for func in result["function_suggestion"]:
#                 assert isinstance(func, str), "function_suggestion items must be strings"
#                 assert "async" in func, "Function must be async"
        
#         if "test_code" in result:
#             assert isinstance(result["test_code"], str), "test_code must be string"
#             assert "describe" in result["test_code"], "Test code must include describe block"
#             assert "test(" in result["test_code"], "Test code must include test cases"
#             assert "expect" in result["test_code"], "Test code must include expect statements"

#         return result

#     def post(self, shared, prep_res, exec_res):
#         # Print what is being revised
#         print(f"\n=== Revisions (Iteration {shared['iteration_count']}) ===")

#         # Handle test case revisions
#         if "test_cases" in exec_res:
#             print("Revising test cases:")
            
#             # Handle pass test cases
#             if "pass" in exec_res["test_cases"]:
#                 print("Passing test cases:")
#                 for test_case in exec_res["test_cases"]["pass"]:
#                     print(f"  Test {test_case['name']}")
#                     print(f"    input: {test_case['input']}")
#                     print(f"    expected: {test_case['expected']}")
#                     print(f"    status: {test_case['status']}")
            
#             # Handle retry test cases
#             if "retry" in exec_res["test_cases"]:
#                 print("Retry test cases:")
#                 for test_case in exec_res["test_cases"]["retry"]:
#                     print(f"  Test {test_case['name']}")
#                     print(f"    input: {test_case['input']}")
#                     print(f"    expected: {test_case['expected']}")
#                     print(f"    status: {test_case['status']}")
            
#             # Update shared test cases
#             shared["test_cases"] = exec_res["test_cases"]
        
#         # Handle function suggestion
#         if "function_suggestion" in exec_res:
#             # print("\nFunction suggestion:")
#             # for func in exec_res["function_suggestion"]:
#             #     print(func)
#             shared["function_suggestion"] = exec_res["function_suggestion"]  # Use first suggestion
        
#         # Handle test code
#         if "test_code" in exec_res:
#             # print("New test code:")
#             # print(exec_res["test_code"])
#             shared["test_code"] = exec_res["test_code"] 

__all__ = [
    'AsyncNodeWrapper',
    'ReturnDefaultActionNode',
    'GetToolsNode',
    'DecideToolNode',
    'ExecuteToolNode',
    'Analyze_Node',
    'GenerateTestCases',
    'ImplementFunction',
    'RunTests',
    'Revise'
] 
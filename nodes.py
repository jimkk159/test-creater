import re
import yaml
import os
import time
import json
import asyncio
from dotenv import load_dotenv
from pocketflow import Node, BatchNode
from utils.call_llm.open_ai import call_llm
from utils.code_executor import execute_jest_test, extract_test_counts
from utils.utils import get_tools, call_tool, extract_describe_blocks

load_dotenv()

MAX_ITERATION = 2
BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"
allowed_dir=os.environ.get("ALLOW_READ_FILE_PATH")

class ReturnDefaultActionNode(Node):
    def post(self, shared, prep_res, exec_res):
        # This node simply returns the "default" action to the parent flow
        return "default"
class GetToolsNode(Node):
    def prep(self, shared):
        """Initialize and get tools"""
        print("🔍 Getting available tools...")
        
        # Path to the mcp server script relative to the workspace root
        relative_server_path = "utils/mcp_server.py"
        
        # Get the absolute path of the workspace root
        # Assuming the workspace root is the current working directory when the script runs
        workspace_root = os.getcwd() 
        
        # Construct the absolute path to the server script
        absolute_server_path = os.path.join(workspace_root, relative_server_path)
        
        # Check if the absolute path starts with the allowed directory prefix
        if not absolute_server_path.startswith(allowed_dir):
             raise ValueError(f"Error: The mcp_server.py script ({absolute_server_path}) is not located within the allowed directory ({allowed_dir}).")

        # If the check passes, return the relative path
        return relative_server_path

    def exec(self, server_path):
        """Retrieve tools from the MCP server"""
        tools = get_tools(server_path)
        return tools

    def post(self, shared, prep_res, exec_res):
        """Store tools and process to yamlResult node"""
        tools = exec_res
        shared["file"]["tools"] = tools
        
        # Format tool information for later use
        tool_info = []
        for i, tool in enumerate(tools, 1):
            properties = tool.inputSchema.get('properties', {})
            required = tool.inputSchema.get('required', [])
            
            params = []
            for param_name, param_info in properties.items():
                param_type = param_info.get('type', 'unknown')
                req_status = "(Required)" if param_name in required else "(Optional)"
                params.append(f"    - {param_name} ({param_type}): {req_status}")
            
            tool_info.append(f"[{i}] {tool.name}\n  Description: {tool.description}\n  Parameters:\n" + "\n".join(params))
        
        shared["file"]["tool_info"] = "\n".join(tool_info)
        return "decide"

class DecideToolNode(Node):
    def prep(self, shared):
        """Prepare the prompt for LLM to process the question"""
        tool_info = shared["file"]["tool_info"]
        question = shared["question"]   
        pre_task_info = ""
        if  "file" in shared and "action" in shared["file"] : 
            pre_task_info = f"""
                ### PREVIOUS ACTION
                {shared["file"].get("action", "")}

                ### PREVIOUS TOOL
                {shared["file"].get("tool_name", "")}

                ### PREVIOUS PARAMETERS
                {shared["file"].get("parameters", "")}

                ### PREVIOUS ACTION RESULT
                {shared["file"].get("tool_result", "")}
            """ 

        prompt = (f"""
### CONTEXT
You are an assistant that can use tools via Model Context Protocol (MCP).

### ACTION SPACE
{tool_info}

### TASK
Answer this question: "{question}"

{pre_task_info}

## NEXT ACTION
Analyze the question, 
base on the previous action, (if there has any)
decide next action to exec.

Your action choice: [tool, done, error]

- tool:
    Extract any numbers or parameters, and decide which tool to use.
    Sometime, you need to call tool multiple times.

- done:
    This action means the question has been fulfilled

- error:
    Something went wrong, and you need human to solve the problem

Return your response in this format:

```yaml
action: <name of the action>
thinking: |
    <your step-by-step reasoning about what the question is asking and what numbers to extract>
tool: <name of the tool to use>
reason: <why you chose this tool>
parameters:
    <parameter_name>: <parameter_value>
    <parameter_name>: <parameter_value>
```
IMPORTANT: 
1. Extract numbers from the question properly
2. Use proper indentation (4 spaces) for multi-line fields
3. Use the | character for multi-line text fields
4. If you already got the answer, just choice the done action.
"""
        )
        return prompt

    def exec(self, prompt):
        """Call LLM to process the question and decide which tool to use"""
        print(border)
        print("🤔 Analyzing question and deciding which tool to use...")

        response = call_llm(prompt)
        return response

    def post(self, shared, prep_res, exec_res):
        """Extract yamlResult from YAML and save to shared context"""
        try:
            yaml_str = exec_res.split("```yaml")[1].split("```")[0].strip()
            yamlResult = yaml.safe_load(yaml_str)
            
            shared["file"]["action"] = yamlResult.get("action", "")
            shared["file"]["tool_name"] = yamlResult.get("tool", "")
            shared["file"]["parameters"] = yamlResult.get("parameters", "")
            shared["file"]["thinking"] = yamlResult.get("thinking", "")
            print(border)
            print(f"🎬 Selected action: {shared["file"]["action"]}")
            # print(f"🧠 AI thinking: {shared["file"]["thinking"]}")

            # print(yamlResult)

            if shared["file"]["action"] == 'done':
                answer = f"✅ FILE CONTENT:\n{shared["file"]['tool_result']}"
                shared["file"]["result"] = answer
                print(border)
                print(answer)
                return "default"
            elif shared["file"]["action"] == 'tool':
                print(f"💡 Selected tool: {yamlResult['tool']}")
                print(f"🔢 Extracted parameters: {yamlResult['parameters']}")
                return "tool"
            return "error"
            
        except Exception as e:
            print(f"❌ Error parsing LLM response on reading file: {e}")
            print("Raw response:", exec_res)
            return None

class ExecuteToolNode(Node):
    def prep(self, shared):
        """Prepare tool execution parameters"""
        return shared["file"]["tool_name"], shared["file"]["parameters"]

    def exec(self, inputs):
        """Execute the chosen tool"""
        tool_name, parameters = inputs
        print(f"🔧 Executing tool '{tool_name}' with parameters: {parameters}")
        result = call_tool("utils/mcp_server.py", tool_name, parameters)
        return result

    def post(self, shared, prep_res, exec_res):
        # print(f"🔨MCP tool Response: {exec_res}")
        shared["file"]["tool_result"] = exec_res
        return "tool_result"
    
class Analyze_Node(Node):
    def prep(self, shared):
        """Analyze files for later test generate"""
        print(border)
        print("🔍 Analyze the file content...")
        shared["analyze"]["file_content"] = shared["file"]["tool_result"]

        return shared["file"]["tool_result"]

    def exec(self, file_content):
        """Tell the llm to extract the function need to be test"""

        prompt = (f"""
    ### CONTEXT
    You are an assistant that help the code tester to extract the functions which need to be tested in the content.

    ### TASK
    Extract the function in the file

    ### FILE CONTENT
    {file_content}

    ## NEXT ACTION
    EXtract functions in the file

    Return your response in this format:

    ```yaml
    functions: 
        - <function name>: <function content>
        - <function name>: <function content>
    ```

    IMPORTANT: 
    1. Use proper indentation (4 spaces) for multi-line fields
    2. Use the | character for multi-line text fields
    """
            )

        response = call_llm(prompt)
        return response

    def post(self, shared, prep_res, exec_res):
        try:
            yaml_str = exec_res.split("```yaml")[1].split("```")[0].strip()
            yamlResult = yaml.safe_load(yaml_str)
            
            shared["functions"] = yamlResult.get("functions", "")
            print(border)
            print(f"⛏️ extracted functions: {shared["functions"]}")
            
        except Exception as e:
            print(f"❌ Error parsing LLM response on analyze: {e}")
            print("Raw response:", exec_res)
            return None

class GenerateTestCases(Node):
    def prep(self, shared):
        """Generate test case for later test code generate"""
        print(border)
        print("🧪 Generate test cases...")
        return shared["functions"]

    def exec(self, functions):
        prompt = f"""
        ### CONTEXT
        You are an assistant to help the Quality Assurance Engineer to generate test cases

        ## FUNCTIONS
        {functions}

Output in this YAML format with reasoning:
```yaml
reasoning: |
    The input parameters should be: param1 as a string, and param2 as a number.
    I should consider the more case as possible as I can. 
    To test the function, I will consider basic cases, edge cases, corner cases, input type check cases....
    For this problem, I need to test...
test_cases:
  <function_name>: 
    - name: "Basic case"
        explain: <what you want to test in these case>
        input: {{param1: value1, param2: value2}}
        expected: result1

    - name: "Edge case - empty"
        explain: <what you want to test in these case>
        input: {{param1: value3, param2: value4}}
        expected: result2
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)

        # Validation asserts
        assert "test_cases" in result, "Result must have 'test_cases' field"
        assert isinstance(result["test_cases"], dict), "test_cases must be a dictionary"

        for function_name, test_case_list in result["test_cases"].items():
            assert isinstance(function_name, str), f"Function name must be string"

            for i, test_case in enumerate(test_case_list):
                assert "name" in test_case, f"{function_name} Test case {i} missing 'name' field"
                assert isinstance(test_case["name"], str), f"{function_name} Test case {i} 'name' must be string"
                assert "explain" in test_case, f"{function_name} Test case {i} missing 'explain' field"
                assert isinstance(test_case["name"], str), f"{function_name} Test case {i} 'name' must be string"
                assert "input" in test_case, f"{function_name} Test case {i} missing 'input' field"
                assert isinstance(test_case["input"], dict), f"{function_name} Test case {i} 'input' must be dict"
                assert "expected" in test_case, f"{function_name} Test case {i} missing 'expected' field"
        
        return result

    def post(self, shared, prep_res, exec_res):
        shared["test_cases"] = exec_res["test_cases"]
        
        # Print all generated test cases
        print(border)
        print(f"\n=== Generated {len(exec_res['test_cases'])} Test Cases ===\n")
        for function_name, test_case_list in exec_res["test_cases"].items():
            print(f"-- Funtion: {function_name} {"-" * (BORDER_LEN - 11 - len(function_name))}")
            for i, test_case in enumerate(test_case_list, 1):
                print(f"{i}. {test_case['name']}")
                print(f"   explain: {test_case['explain']}")
                print(f"   input: {test_case['input']}")
                print(f"   expected: {test_case['expected']}")
        print('-' * BORDER_LEN)
        print("")

class ImplementFunction(Node):
    def prep(self, shared):
        print(border)
        print("🏗️ Implement the test case functions...")
        return shared["functions"], shared["test_cases"]

    def exec(self, input):
        functions, test_cases = input

        # Format test cases nicely for the prompt
        formatted_tests = ""
        for function_name, test_case_list in test_cases.items():
            for i, test in enumerate(test_case_list, 1):
                formatted_tests += f"- {function_name}:"
                formatted_tests += f"{i}. {test['name']}\n"
                formatted_tests += f"   input: {test['input']}\n"
                formatted_tests += f"   expected: {test['expected']}\n\n"
        
        example= """
- original function:
    function sum(a, b) {
    return a + b;
    }

- your test function:
    describe('function name', () => {
        <original function>

        test('explain', () => {
            expect(sum(1, 2)).toBe(3);
        });

        test('another explain', () => {
            expect(sum(1, 2)).toBe(3);
        });
    });
"""

        prompt = f"""Implement the test cases in JavaScript by Jest base on the functions.

### FUNCTIONS
{functions}

### TEST CASES
{formatted_tests}

Output in this YAML format:
```yaml
reasoning: |
    To implement this function, I will...
    My approach is...
function_code: |
    <test case name>(...):
        # your implementation
```

### Example: |
    {example}


"""
        

        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)

        # Validation asserts
        assert "function_code" in result, "Result must have 'function_code' field"
        assert isinstance(result["function_code"], str), "function_code must be string"
        
        return result["function_code"]

    def post(self, shared, prep_res, exec_res):
        shared["test_code"] = exec_res
        
        # Print the implemented function
        # print(f"\n=== Implemented Function ===")
        # print(exec_res)

class RunTests(BatchNode):
    def prep(self, shared):
        # Match each 'describe(...) { ... });' block
        print(border)
        print("🏃 Running test functions...")
        shared["max_iterations"] = shared.get("max_iteration", MAX_ITERATION)
        return extract_describe_blocks(shared["test_code"])
    
    def exec(self, test_code):
        output = execute_jest_test(test_code)

        end = output["end"]
        details = output["details"]
        test_counts = extract_test_counts(end)
        failed = test_counts["failed"]

        data = []

        if failed == 0: 
            return {
                "status": test_counts,
                "detail": data
            }
        
        for i, content in enumerate(details):
            expected = content["expected"]
            received = content["received"]

            if expected is None and received is None:
                data.append({
                    "suite": content["suite"],
                    "test_case": content["test_case"],
                    "passed": False,
                    "received": received,
                    "expected": expected,
                    "description": content["description"]
                })
            elif expected != received:
                data.append({
                    "suite": content["suite"],
                    "test_case": content["test_case"],
                    "passed": False,
                    "received": received,
                    "expected": expected,
                    "description": content["description"]
                })

        return {
            "status": test_counts,
            "detail": data
        }

    def post(self, shared, prep_res, exec_res_list):
        shared["iteration_count"] = shared.get("iteration_count", 0) + 1

        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        all_failed_details = []

        # Aggregate results from all batches
        for batch_result in exec_res_list:
            if isinstance(batch_result, dict) and "status" in batch_result:
                status = batch_result["status"]
                total_tests += status.get("total", 0)
                passed_tests += status.get("passed", 0)
                failed_tests += status.get("failed", 0)
                if "detail" in batch_result:
                    all_failed_details.extend(batch_result["detail"])
            else:
                # Handle unexpected items in exec_res_list if necessary
                print(f"Warning: Unexpected item in exec_res_list: {batch_result}")

        # Print aggregate test results
        print(border)
        title = f"--- Aggregate Test Results: {passed_tests}/{total_tests} Passed ---"
        print(title)

        if failed_tests == 0:
            print("🎉All tests passed across all batches!")
            print("-" * len(title))
            with open('output.test.js', 'w', encoding='utf-8') as tmp_file:
                tmp_file.write(shared["test_code"])
            return 'success' # All tests passed

        # If there are failed tests, print details
        print(f"\nFailed Tests ({failed_tests} total):")
        for i, detail in enumerate(all_failed_details, 1):
            print(f"{i}. Suite: {detail.get('suite')}, Test Case: {detail.get('test_case')}")
            print(f"   Description: {detail.get('description')}")
            print(f"   Expected: {detail.get('expected')}, Received: {detail.get('received')}")
            print('-' * BORDER_LEN)

        shared["passed"] = passed_tests
        shared["total_tests"] = total_tests
        shared["failed_tests"] = all_failed_details # Store details of all failed tests

        # Decide next action based on failures or max iterations
        if shared["iteration_count"] >= shared.get("max_iterations", MAX_ITERATION):
            print("Max iterations reached.")
            return "max_iterations"
        else:
            print(f"Iteration {shared['iteration_count']} failed. Revising code.")
            return "failure" # Or another action like "revise"

class Revise(Node):
    def prep(self, shared):
        print(border)
        print("💭 AI review the test result...")
        failed_tests = [r for r in shared["failed_tests"] ]

        return {
            "functions": shared.get("functions", ""),
            "test_cases": shared.get("test_cases", ""),
            "test_code": shared.get("test_code", ""),
            "max_iterations": shared.get("max_iterations", ""),
            "iteration_count": shared.get("iteration_count", ""),
            "is_passed": shared.get("passed", 0) == shared.get("total_tests", 0),
            "passed": shared.get("passed", ""),
            "total_tests": shared.get("total_tests", ""),
            "failed_tests": failed_tests
        }

    def exec(self, inputs):
        # Format current test cases nicely
        formatted_tests = ""
        for i, func_name in enumerate(inputs['test_cases'], 1):
            for j, test in enumerate(inputs['test_cases'][func_name], 1):
                formatted_tests += f"{i}. {test['name']}\n"
                formatted_tests += f"   explain: {test['explain']}\n"
                formatted_tests += f"   input: {test['input']}\n"
                formatted_tests += f"   expected: {test['expected']}\n\n"
        
        # Format failed tests nicely
        formatted_failures = ""
        for i, result in enumerate(inputs['failed_tests'], 1):
            formatted_failures += f"{i}. {result['test_case']}:\n"
            formatted_failures += f"{i}. {result['test_case']}:\n"
            formatted_failures += f"   received: {result['received']}\n"
            formatted_failures += f"   expected: {result['expected']}\n"
            formatted_failures += f"   description: {result['description']}\n\n"

        
        example = {
                    "action": "review",
                    "thinking": "The test cases are intended to check how the function reacts when supplied with inputs of various types. However, the function implementation does not currently handle type checking or throw errors for non-numeric inputs. Therefore, the failures I observed correspond to the function simply attempting to concatenate strings or merge objects instead of throwing the anticipated exceptions.\n\nI will revise the test cases to clarify expectations for both valid and invalid types, and suggest an appropriate update to the function to satisfy these expectations.",
                    "reasoning": "Looking at the failures, I see that the add function does not throw errors for invalid inputs like a string or an object. The function is performing addition (or string concatenation) instead of enforcing type checks. I will revise the test function to handle these scenarios correctly, and suggest an implementation of the add function that throws errors for invalid inputs.",
                    "test_cases": {
                            "pass": [
                                    {
                                    "id": 1,
                                    "name": "Basic case with positive numbers",
                                    "input": { "a": 2, "b": 3 },
                                    "expected": 5,
                                    "status": "ok"
                                    },
                                    {
                                    "id": 2,
                                    "name": "Basic case with negative numbers",
                                    "input": { "a": -1, "b": -2 },
                                    "expected": -3,
                                    "status": "ok"
                                    },
                                    {
                                    "id": 3,
                                    "name": "Edge case - adding zero",
                                    "input": { "a": 5, "b": 0 },
                                    "expected": 5,
                                    "status": "ok"
                                    },
                                    {
                                    "id": 4,
                                    "name": "Edge case - adding two zeros",
                                    "input": { "a": 0, "b": 0 },
                                    "expected": 0,
                                    "status": "ok"
                                    },
                            ],
                            "retry": [
                                                        {
                        "id": 5,
                        "name": "Type case - adding a number and a string",
                        "input": { "a": "3", "b": 2 },
                        "expected": "3 is not a number",
                        "status": "fail"
                        },
                        {
                        "id": 6,
                        "name": "Type case - adding an object",
                        "input": { "a": {}, "b": 5 },
                        "expected": "{} is not a number",
                        "status": "fail"
                        }
                            ]
                        },
                    "function_suggestion": ["const add = async (a, b) => {   if (typeof a !== 'number') {     throw new Error(`${a} is not a number`);    }    if (typeof b !== 'number') {        throw new Error(`${b} is not a number`);    }    return a + b;};"],
                    "test_code": """ 
                                    describe('add function', () => {
                                        const add = async (a, b) => a + b;
                                        test('Basic case - positive integers', async () => {
                                            expect(await add(1, 2)).toBe(2);
                                        });
                                    });
                                """
                }

        prompt = f"""
You are a QA engineer to check and fix the test code result. 

### NEXT ACTION
Your action choice: [pass, review, error]

- pass:
    This action means the test codes are fine.

- review:
    This action means the test codes need to be adjust

- error:
    Something went wrong, and you need human to solve the problem

### GOAL
    1. Make the test code reasonable.
    2. Analyze the failures and output revisions in YAML. 
    3. You should think about the test cases and its outputs both make sense or not.

### TIP
    1. Sometime, the test code fail is due to the function to be test has some drawback.
       You don't need to fix this kind of fail in the test result.
    2. You should put the ok test code in the pass class, and retry test code in the retry class.
    3. You should provide the entire revised test code in the test_code  class.
    4. If the original code has bug, put the revised function in the function_suggestion.
    5. function_suggestion must be a list, even it only has one.

### TEST RESULT INFORMATION

    Current test cases:
    {formatted_tests}

    Current function:
    ```python
    {inputs['functions']}
    ```

    Failed tests:
    {formatted_failures}

Output in this YAML format:
```yaml
action: <name of the action>
thinking: |
    <your step-by-step reasoning about we should move forward or revise the test case>
    
<if test code has bug>
reasoning: |
    Looking at the failures, I see that...
    The issue appears to be...
    I will revise...
    I should put this into test code into retry...
test_cases:  # Dictionary mapping test case index (1-based) to revised test case

    1:
        name: "Revised test name"
        input: {{...}}
        expected: ...
        status: fail # This means the test code has bug
        ....

<if original function has bug>
    This test code is fine. It's the original function has bug, I see that...
    The issue appears to be...
    I should put this into test code into pass...

    1:
        name: "Revised test name"
        input: {{...}}
        expected: ...
        status: ok # This means the test code is fine
        
function_suggestion: # Include this if has original function modification 
test_code:  # Include this if revising function

### EXAMPLE
    {json.dumps(example, indent=2)}
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)

        # Validation asserts
        assert "action" in result, "Result must have 'action' field"
        assert result["action"] in ["done", "review", "error"], "action must be one of: done, review, error"
        assert "thinking" in result, "Result must have 'thinking' field"
        assert "thinking" in result, "Result must have 'thinking' field"
        assert isinstance(result["thinking"], str), "thinking must be a string"
        assert "reasoning" in result, "Result must have 'reasoning' field when action is review"
        assert isinstance(result["reasoning"], str), "reasoning must be a string"
        
        if "test_cases" in result:
            assert isinstance(result["test_cases"], dict), "test_cases must be a dictionary"
            assert "pass" in result["test_cases"], "test_cases must have 'pass' category"
            assert "retry" in result["test_cases"], "test_cases must have 'retry' category"
            
            # Validate pass test cases
            for test_case in result["test_cases"]["pass"]:
                assert "id" in test_case, f"Test case missing 'id' field"
                assert "name" in test_case, f"Test case missing 'name' field"
                assert "input" in test_case, f"Test case missing 'input' field"
                assert "expected" in test_case, f"Test case missing 'expected' field"
                assert "status" in test_case, f"Test case missing 'status' field"
                assert test_case["status"] == "ok", f"Pass test case status must be 'ok'"
                
            # Validate retry test cases
            for test_case in result["test_cases"]["retry"]:
                assert "id" in test_case, f"Test case missing 'id' field"
                assert "name" in test_case, f"Test case missing 'name' field"
                assert "input" in test_case, f"Test case missing 'input' field"
                assert "expected" in test_case, f"Test case missing 'expected' field"
                assert "status" in test_case, f"Test case missing 'status' field"
                assert test_case["status"] == "fail", f"Retry test case status must be 'fail'"
        
        if "function_suggestion" in result:
            assert isinstance(result["function_suggestion"], list), "function_suggestion must be a list"
            for func in result["function_suggestion"]:
                assert isinstance(func, str), "function_suggestion items must be strings"
                assert "async" in func, "Function must be async"
                assert "throw new Error" in func, "Function must include error handling"
        
        if "test_code" in result:
            assert isinstance(result["test_code"], str), "test_code must be string"
            assert "describe" in result["test_code"], "Test code must include describe block"
            assert "test(" in result["test_code"], "Test code must include test cases"
            assert "expect" in result["test_code"], "Test code must include expect statements"

        return result

    def post(self, shared, prep_res, exec_res):
        # Print what is being revised
        print(f"\n=== Revisions (Iteration {shared['iteration_count']}) ===")

        # Handle test case revisions
        if "test_cases" in exec_res:
            print("Revising test cases:")
            
            # Handle pass test cases
            if "pass" in exec_res["test_cases"]:
                print("Passing test cases:")
                for test_case in exec_res["test_cases"]["pass"]:
                    print(f"  Test {test_case['id']}: {test_case['name']}")
                    print(f"    input: {test_case['input']}")
                    print(f"    expected: {test_case['expected']}")
                    print(f"    status: {test_case['status']}")
            
            # Handle retry test cases
            if "retry" in exec_res["test_cases"]:
                print("Retry test cases:")
                for test_case in exec_res["test_cases"]["retry"]:
                    print(f"  Test {test_case['id']}: {test_case['name']}")
                    print(f"    input: {test_case['input']}")
                    print(f"    expected: {test_case['expected']}")
                    print(f"    status: {test_case['status']}")
            
            # Update shared test cases
            shared["test_cases"] = exec_res["test_cases"]
        
        # Handle function suggestion
        if "function_suggestion" in exec_res:
            print("\nFunction suggestion:")
            for func in exec_res["function_suggestion"]:
                print(func)
            shared["function_suggestion"] = exec_res["function_suggestion"]  # Use first suggestion
        
        # Handle test code
        if "test_code" in exec_res:
            print("New test code:")
            print(exec_res["test_code"])
            shared["test_code"] = exec_res["test_code"] 
import yaml
import os
import time
import asyncio
from pocketflow import Node, BatchNode
from utils.call_llm.open_ai import call_llm
from utils.code_executor import execute_python
from utils.utils import get_tools, call_tool

allowed_dir="/Users/jimchung/Desktop/Code/python"

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
        """Store tools and process to decision node"""
        tools = exec_res
        shared["tools"] = tools
        
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
        
        shared["tool_info"] = "\n".join(tool_info)
        return "decide"

class DecideToolNode(Node):
    def prep(self, shared):
        """Prepare the prompt for LLM to process the question"""
        tool_info = shared["tool_info"]
        question = shared["question"]   
        pre_task_info = ""
        if "action" in shared : 
            pre_task_info = f"""
                ### PREVIOUS ACTION
                {shared.get("action", "")}

                ### PREVIOUS TOOL
                {shared.get("tool_name", "")}

                ### PREVIOUS PARAMETERS
                {shared.get("parameters", "")}

                ### PREVIOUS ACTION RESULT
                {shared.get("tool_result", "")}
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
        print("=" * 90)
        print("🤔 Analyzing question and deciding which tool to use...")
        response = call_llm(prompt)
        return response

    def post(self, shared, prep_res, exec_res):
        """Extract decision from YAML and save to shared context"""
        try:
            yaml_str = exec_res.split("```yaml")[1].split("```")[0].strip()
            decision = yaml.safe_load(yaml_str)
            
            shared["action"] = decision.get("action", "")
            shared["tool_name"] = decision.get("tool", "")
            shared["parameters"] = decision.get("parameters", "")
            shared["thinking"] = decision.get("thinking", "")
            
            print(f"🎬 Selected action: {decision['action']}")

            if shared["action"] == 'done':
                answer = f"✅ Final Answer: {shared['tool_result']}"
                border = "=" * (len(answer) + 5)
                print(f"{border}\n= {answer} =\n{border}")
                return "done"
            elif shared["action"] == 'tool':
                print(f"💡 Selected tool: {decision['tool']}")
                print(f"🔢 Extracted parameters: {decision['parameters']}")
                return "tool"
            return "error"
            
        except Exception as e:
            print(f"❌ Error parsing LLM response: {e}")
            print("Raw response:", exec_res)
            return None

class ExecuteToolNode(Node):
    def prep(self, shared):
        """Prepare tool execution parameters"""
        return shared["tool_name"], shared["parameters"]

    def exec(self, inputs):
        """Execute the chosen tool"""
        tool_name, parameters = inputs
        print(f"🔧 Executing tool '{tool_name}' with parameters: {parameters}")
        result = call_tool("utils/mcp_server.py", tool_name, parameters)
        return result

    def post(self, shared, prep_res, exec_res):
        print(f"🔨MCP tool Response: {exec_res}")
        shared["tool_result"] = exec_res
        return "tool_result"
class GenerateTestCases(Node):
    def prep(self, shared):
        return shared["problem"]

    def exec(self, problem):
        prompt = f"""Generate 5-7 test cases for this coding problem:

{problem}

Output in this YAML format with reasoning:
```yaml
reasoning: |
    The input parameters should be: param1 as a string, and param2 as a number.
    To test the function, I will consider basic cases, edge cases, and corner cases.
    For this problem, I need to test...
test_cases:
  - name: "Basic case"
    input: {{param1: value1, param2: value2}}
    expected: result1
  - name: "Edge case - empty"
    input: {{param1: value3, param2: value4}}
    expected: result2
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)
        
        # Validation asserts
        assert "test_cases" in result, "Result must have 'test_cases' field"
        assert isinstance(result["test_cases"], list), "test_cases must be a list"
        
        for i, test_case in enumerate(result["test_cases"]):
            assert "name" in test_case, f"Test case {i} missing 'name' field"
            assert isinstance(test_case["name"], str), f"Test case {i} 'name' must be string"
            assert "input" in test_case, f"Test case {i} missing 'input' field"
            assert isinstance(test_case["input"], dict), f"Test case {i} 'input' must be dict"
            assert "expected" in test_case, f"Test case {i} missing 'expected' field"
        
        return result

    def post(self, shared, prep_res, exec_res):
        shared["test_cases"] = exec_res["test_cases"]
        
        # Print all generated test cases
        print(f"\n=== Generated {len(exec_res['test_cases'])} Test Cases ===")
        for i, test_case in enumerate(exec_res["test_cases"], 1):
            print(f"{i}. {test_case['name']}")
            print(f"   input: {test_case['input']}")
            print(f"   expected: {test_case['expected']}")

class ImplementFunction(Node):
    def prep(self, shared):
        return shared["problem"], shared["test_cases"]

    def exec(self, inputs):
        problem, test_cases = inputs
        
        # Format test cases nicely for the prompt
        formatted_tests = ""
        for i, test in enumerate(test_cases, 1):
            formatted_tests += f"{i}. {test['name']}\n"
            formatted_tests += f"   input: {test['input']}\n"
            formatted_tests += f"   expected: {test['expected']}\n\n"
        
        prompt = f"""Implement a solution for this problem:

{problem}

Test cases to consider:
{formatted_tests}

IMPORTANT: The function name must be exactly "run_code"

Output in this YAML format:
```yaml
reasoning: |
    To implement this function, I will...
    My approach is...
function_code: |
    def run_code(...):
        # your implementation
        return result
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)
        
        # Validation asserts
        assert "function_code" in result, "Result must have 'function_code' field"
        assert isinstance(result["function_code"], str), "function_code must be string"
        assert "def run_code" in result["function_code"], "Function must be named 'run_code'"
        
        return result["function_code"]

    def post(self, shared, prep_res, exec_res):
        shared["function_code"] = exec_res
        
        # Print the implemented function
        print(f"\n=== Implemented Function ===")
        print(exec_res)

class RunTests(BatchNode):
    def prep(self, shared):
        function_code = shared["function_code"]
        test_cases = shared["test_cases"]
        # Return list of tuples (function_code, test_case)
        return [(function_code, test_case) for test_case in test_cases]

    def exec(self, test_data):
        function_code, test_case = test_data
        output, error = execute_python(function_code, test_case["input"])
        
        if error:
            return {
                "test_case": test_case,
                "passed": False,
                "actual": None,
                "expected": test_case["expected"],
                "error": error
            }
        
        passed = output == test_case["expected"]
        return {
            "test_case": test_case,
            "passed": passed,
            "actual": output,
            "expected": test_case["expected"],
            "error": None if passed else f"Expected {test_case['expected']}, got {output}"
        }

    def post(self, shared, prep_res, exec_res_list):
        shared["test_results"] = exec_res_list
        all_passed = all(result["passed"] for result in exec_res_list)
        shared["iteration_count"] = shared.get("iteration_count", 0) + 1
        
        # Print test results
        passed_count = len([r for r in exec_res_list if r["passed"]])
        total_count = len(exec_res_list)
        print(f"\n=== Test Results: {passed_count}/{total_count} Passed ===")
        
        failed_tests = [r for r in exec_res_list if not r["passed"]]
        if failed_tests:
            print("Failed tests:")
            for i, result in enumerate(failed_tests, 1):
                test_case = result['test_case']
                print(f"{i}. {test_case['name']}:")
                if result['error']:
                    print(f"   error: {result['error']}")
                else:
                    print(f"   output: {result['actual']}")
                print(f"   expected: {result['expected']}")
        
        if all_passed:
            return "success"
        elif shared["iteration_count"] >= shared.get("max_iterations", 5):
            return "max_iterations"
        else:
            return "failure"

class Revise(Node):
    def prep(self, shared):
        failed_tests = [r for r in shared["test_results"] if not r["passed"]]
        return {
            "problem": shared["problem"],
            "test_cases": shared["test_cases"],
            "function_code": shared["function_code"],
            "failed_tests": failed_tests
        }

    def exec(self, inputs):
        # Format current test cases nicely
        formatted_tests = ""
        for i, test in enumerate(inputs['test_cases'], 1):
            formatted_tests += f"{i}. {test['name']}\n"
            formatted_tests += f"   input: {test['input']}\n"
            formatted_tests += f"   expected: {test['expected']}\n\n"
        
        # Format failed tests nicely
        formatted_failures = ""
        for i, result in enumerate(inputs['failed_tests'], 1):
            test_case = result['test_case']
            formatted_failures += f"{i}. {test_case['name']}:\n"
            if result['error']:
                formatted_failures += f"   error: {result['error']}\n"
            else:
                formatted_failures += f"   output: {result['actual']}\n"
            formatted_failures += f"   expected: {result['expected']}\n\n"

        prompt = f"""Problem: {inputs['problem']}

Current test cases:
{formatted_tests}

Current function:
```python
{inputs['function_code']}
```

Failed tests:
{formatted_failures}

Analyze the failures and output revisions in YAML. You can revise test cases, function code, or both:

```yaml
reasoning: |
    Looking at the failures, I see that...
    The issue appears to be...
    I will revise...
test_cases:  # Dictionary mapping test case index (1-based) to revised test case
  1:
    name: "Revised test name"
    input: {{...}}
    expected: ...
function_code: |  # Include this if revising function
  def run_code(...):
    return ...
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)
        
        # Validation asserts
        if "test_cases" in result:
            assert isinstance(result["test_cases"], dict), "test_cases must be a dictionary"
            for index_str, test_case in result["test_cases"].items():
                assert isinstance(index_str, (str, int)), "test_cases keys must be strings or ints"
                assert "name" in test_case, f"Revised test case {index_str} missing 'name' field"
                assert "input" in test_case, f"Revised test case {index_str} missing 'input' field"
                assert "expected" in test_case, f"Revised test case {index_str} missing 'expected' field"
        
        if "function_code" in result:
            assert isinstance(result["function_code"], str), "function_code must be string"
            assert "def run_code" in result["function_code"], "Function must be named 'run_code'"
        
        return result

    def post(self, shared, prep_res, exec_res):
        # Print what is being revised
        print(f"\n=== Revisions (Iteration {shared['iteration_count']}) ===")
        
        # Handle test case revisions - map indices to actual test cases
        if "test_cases" in exec_res:
            current_tests = shared["test_cases"].copy()
            print("Revising test cases:")
            for index_str, revised_test in exec_res["test_cases"].items():
                index = int(index_str) - 1  # Convert to 0-based
                if 0 <= index < len(current_tests):
                    old_test = current_tests[index]
                    print(f"  Test {index_str}: '{old_test['name']}' -> '{revised_test['name']}'")
                    print(f"    old input: {old_test['input']}")
                    print(f"    new input: {revised_test['input']}")
                    print(f"    old expected: {old_test['expected']}")
                    print(f"    new expected: {revised_test['expected']}")
                    current_tests[index] = revised_test
            shared["test_cases"] = current_tests
            
        if "function_code" in exec_res:
            print("Revising function code:")
            print("New function:")
            print(exec_res["function_code"])
            shared["function_code"] = exec_res["function_code"] 
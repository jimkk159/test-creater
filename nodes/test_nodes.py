import re
import yaml
from pocketflow import Node, AsyncParallelBatchNode
from utils.call_llm.open_ai import call_llm
from utils.code_executor import execute_jest_test, extract_test_counts
from utils.utils import extract_describe_blocks, save_to_file, cleanup_temp_files

BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"
MAX_ITERATION = 3

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
        if "functions" not in shared:
            raise ValueError("No functions found in shared context")
            
        if not shared["functions"]:
            raise ValueError("Functions list is empty")
            
        return shared["functions"]

    def exec(self, functions):
        try:
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
            
            # Extract YAML content
            if "```yaml" not in response:
                raise ValueError("LLM response missing YAML code block")
                
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
                    assert isinstance(test_case["explain"], str), f"{function_name} Test case {i} 'explain' must be string"
                    assert "input" in test_case, f"{function_name} Test case {i} missing 'input' field"
                    assert isinstance(test_case["input"], dict), f"{function_name} Test case {i} 'input' must be dict"
                    assert "expected" in test_case, f"{function_name} Test case {i} missing 'expected' field"
            
            return result
            
        except Exception as e:
            print(f"Error generating test cases: {str(e)}")
            print("Raw LLM response:", response if 'response' in locals() else "No response")
            raise

    def post(self, shared, prep_res, exec_res):
        try:
            shared["test_cases"] = exec_res["test_cases"]
            
            # Print all generated test cases
            print(border)
            print(f"\n=== Generated {len(exec_res['test_cases'])} Test Cases ===\n")
            for function_name, test_case_list in exec_res["test_cases"].items():
                print(f"-- Function: {function_name} {"-" * (BORDER_LEN - 11 - len(function_name))}")
                for i, test_case in enumerate(test_case_list, 1):
                    print(f"{i}. {test_case['name']}")
                    print(f"   explain: {test_case['explain']}")
                    print(f"   input: {test_case['input']}")
                    print(f"   expected: {test_case['expected']}")
            print('-' * BORDER_LEN)
            print("")
            
        except Exception as e:
            print(f"Error in post-processing test cases: {str(e)}")
            raise

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

class RunTests(AsyncParallelBatchNode):
    async def prep_async(self, shared):
        # Match each 'describe(...) { ... });' block
        print(border)
        print("🏃 Running test functions...")
        shared["max_iterations"] = shared.get("max_iteration", MAX_ITERATION)
        
        # Initialize iteration counts for each test suite if not exists
        if "suite_iterations" not in shared:
            shared["suite_iterations"] = {}
            
        return extract_describe_blocks(shared["test_code"])
    
    async def exec_async(self, test_code):
        # Extract suite name from test code
        suite_match = re.search(r"describe\('([^']+)'", test_code)
        suite_name = suite_match.group(1) if suite_match else "unknown_suite"

        output = await execute_jest_test(test_code)

        end = output["end"]
        details = output["details"]
        test_counts = extract_test_counts(end)
        failed = test_counts["failed"]

        data = []

        if failed == 0: 
            return {
                "status": test_counts,
                "detail": data,
                "suite": suite_name
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
            "detail": data,
            "suite": suite_name
        }

    async def post_async(self, shared, prep_res, exec_res_list):
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        all_failed_details = []        
        # Aggregate results from all batches
        for batch_result in exec_res_list:
            if isinstance(batch_result, dict) and "status" in batch_result:
                status = batch_result["status"]
                suite_name = batch_result.get("suite", "unknown_suite")
                
                # Initialize suite iteration count if not exists
                if suite_name not in shared["suite_iterations"]:
                    shared["suite_iterations"][suite_name] = 0
                
                # Increment iteration count for this suite
                shared["suite_iterations"][suite_name] += 1
                
                total_tests += status.get("total", 0)
                passed_tests += status.get("passed", 0)
                failed_tests += status.get("failed", 0)
                if "detail" in batch_result:
                    all_failed_details.extend(batch_result["detail"])
            else:
                print(f"Warning: Unexpected item in exec_res_list: {batch_result}")

        # Print aggregate test results
        print(border)
        title = f"--- Aggregate Test Results: {passed_tests}/{total_tests} Passed ---"
        print(title)

        if failed_tests == 0:
            print("🎉All tests passed across all batches!")
            print("-" * len(title))
            save_to_file(shared["test_code"], "final.test.js")
            cleanup_temp_files(shared, 'temp_file_paths')
            return 'success' # All tests passed

        shared["passed"] = passed_tests
        shared["total_tests"] = total_tests
        shared["failed_tests"] = all_failed_details
        # Check if any suite has reached max iterations
        max_iterations_reached = any(
            shared["suite_iterations"][suite] >= shared["max_iterations"]
            for suite in shared["suite_iterations"]
        )

        if max_iterations_reached:
            print("Max iterations reached for one or more test suites.")
            return "max_iterations"
        else:
            print(f"❌Some tests failed. Revising code...")
            return "failure"

class Revise(Node):
    def prep(self, shared):
        print(border)
        print("💭 AI review the test result...")
        failed_tests = [r for r in shared["failed_tests"] ]

        if 'iteration_count' not in shared:
            shared['iteration_count'] = 0
        else: 
            shared['iteration_count'] += 1
            
        test_cases = shared.get("test_cases", "") 
        failed_tests = shared.get("failed_tests", "") 

        # Format current test cases nicely
        formatted_tests = ""
        for i, func_name in enumerate(test_cases, 1):
            for j, test in enumerate(test_cases[func_name], 1):
                formatted_tests += f"{i}. {test['name']}\n"
                formatted_tests += f"   explain: {test['explain']}\n"
                formatted_tests += f"   input: {test['input']}\n"
                formatted_tests += f"   expected: {test['expected']}\n\n"
        
        # Format failed tests nicely
        formatted_failures = ""
        for i, result in enumerate(failed_tests, 1):
            formatted_failures += f"{i}. {result['test_case']}:\n"
            formatted_failures += f"   received: {result['received']}\n"
            formatted_failures += f"   expected: {result['expected']}\n"
            formatted_failures += f"   description: {result['description']}\n\n"

        return {
            "functions": shared.get("functions", ""),
            "test_cases": shared.get("test_cases", ""),
            "test_code": shared.get("test_code", ""),
            "max_iterations": shared.get("max_iterations", ""),
            "iteration_count": shared.get("iteration_count", 0),
            "is_passed": shared.get("passed", 0) == shared.get("total_tests", 0),
            "passed": shared.get("passed", ""),
            "total_tests": shared.get("total_tests", ""),
            "failed_tests": failed_tests,
            "formatted_tests": formatted_tests,
            "formatted_failures": formatted_failures
        }

    def exec(self, inputs):
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
    3. You should provide the entire revised test code in the test_code class.
    4. If the original code has a bug, put the revised function in the function_suggestion.

### TEST RESULT INFORMATION

    Current test cases:
    {inputs["formatted_tests"] if inputs["formatted_tests"] else "No test cases available"}

    Current function:
    {f"```javascript\n{inputs['functions']}\n```" if inputs['functions'] else 'No functions available'}

    Failed tests:
    {inputs["formatted_failures"]}

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
        
function_suggestion: [] # Include this if has original function modification 
test_code:  # Include this if revising function

### EXAMPLE
    action: review
    thinking: ...
    reasoning: ...
    test_cases:
    pass:
        - name: "Basic case with positive numbers"
        input:
            a: 2
            b: 3
        expected: 5
        status: "ok"
    retry:
        - name: "Type case - adding a number and a string"
        input:
            a: "3"
            b: 2
        expected: "3 is not a number"
        status: "fail"
    function_suggestion: 
        - |
            {"""const add = async (a, b) => {
                return a + b;
            };"""}
    test_code: |
        - |
            {"""describe('add function', () => {
                const add = async (a, b) => a + b;
                test('Basic case - positive integers', async () => {
                expect(await add(1, 2)).toBe(2);
                });
            });"""}
    
### IMPORTANT
    1. You must have the retry and pass part in the test_cases, even there aren't anything inside.
    2. function_suggestion must be a list, even it only has one.
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
        
        if "test_cases" in result:
            assert isinstance(result["test_cases"], dict), "test_cases must be a dictionary"
            assert "pass" in result["test_cases"], "test_cases must have 'pass' category"
            assert "retry" in result["test_cases"], "test_cases must have 'retry' category"
            
            # Validate pass test cases
            for test_case in result["test_cases"]["pass"]:
                assert "name" in test_case, f"Test case missing 'name' field"
                assert "input" in test_case, f"Test case missing 'input' field"
                assert "expected" in test_case, f"Test case missing 'expected' field"
                assert "status" in test_case, f"Test case missing 'status' field"
                assert test_case["status"] == "ok", f"Pass test case status must be 'ok'"
                
            # Validate retry test cases
            for test_case in result["test_cases"]["retry"]:
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
        
        if "test_code" in result:
            assert isinstance(result["test_code"], str), "test_code must be string"
            assert "describe" in result["test_code"], "Test code must include describe block"
            assert "test(" in result["test_code"], "Test code must include test cases"
            assert "expect" in result["test_code"], "Test code must include expect statements"

        return result

    def post(self, shared, prep_res, exec_res):
        # Print what is being revised
        # print(f"\n=== Revisions (Iteration {shared['iteration_count']}) ===")

        # Handle test case revisions
        if "test_cases" in exec_res:
            # print("Revising test cases:")
            
            # # Handle pass test cases
            # if "pass" in exec_res["test_cases"]:
            #     print("Passing test cases:")
            #     for test_case in exec_res["test_cases"]["pass"]:
            #         print(f"  Test {test_case['name']}")
            #         print(f"    input: {test_case['input']}")
            #         print(f"    expected: {test_case['expected']}")
            #         print(f"    status: {test_case['status']}")
            
            # # Handle retry test cases
            # if "retry" in exec_res["test_cases"]:
            #     print("Retry test cases:")
            #     for test_case in exec_res["test_cases"]["retry"]:
            #         print(f"  Test {test_case['name']}")
            #         print(f"    input: {test_case['input']}")
            #         print(f"    expected: {test_case['expected']}")
            #         print(f"    status: {test_case['status']}")
            
            # Update shared test cases
            shared["test_cases"] = exec_res["test_cases"]
        
        # Handle function suggestion
        if "function_suggestion" in exec_res:
            shared["function_suggestion"] = exec_res["function_suggestion"]  # Use first suggestion
        
        # Handle test code
        if "test_code" in exec_res:
            shared["test_code"] = exec_res["test_code"] 
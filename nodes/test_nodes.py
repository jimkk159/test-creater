import re
import yaml
from myPocketFlow import Node, AsyncParallelBatchNode
from utils.call_llm.open_ai import call_llm
from utils.code_executor import execute_jest_test, extract_test_counts
from utils.utils import extract_describe_blocks, get_error_prompt, handle_max_iteration_error

BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"
MAX_ITERATION = 5
SYSTEM_MAX_LOOP = 2

class Analyze_Node(Node):
    def prep(self, shared):
        """Analyze files for later test generate"""
        print(border)
        print("🔍 Analyze the file content...")
        error_prompt = get_error_prompt(shared, ['analyze'])

        if "analyze" not in shared:
            shared["analyze"] = {}
        shared["analyze"]["file_content"] = shared["file"]["tool_result"]

        """Tell the llm to extract the function need to be test"""

        prompt = (f"""
    ### CONTEXT
    You are an assistant that help the code tester to extract the functions which need to be tested in the content.

    {error_prompt}

    ### TASK
    Extract the function in the file

    ### FILE CONTENT
    {shared["file"]["tool_result"]}

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
    3. If you got error, just try to fix the error and try again.
    4. If you think you can't handle the error, just return the error action.
    """
            )

        return prompt

    def exec(self, prompt):
        response = call_llm(prompt)
        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            yamlResult = yaml.safe_load(yaml_str)   

            # Convert list of functions to dictionary
            functions_dict = {}
            for func in yamlResult.get("functions", []):
                for func_name, func_content in func.items():
                    functions_dict[func_name] = func_content
            
            return functions_dict

        except Exception as e:
            print(f"❌ Error parsing LLM response on analyze: {e}")
            print("Raw response:", response)
            raise
    
    def exec_fallback(self, prep_res, exc):
        return { "error": exc }

    def post(self, shared, prep_res, exec_res):
        if "error" in exec_res:
            return handle_max_iteration_error(shared, exec_res, border, SYSTEM_MAX_LOOP, ["analyze"])
        
        shared["functions"] = exec_res
        print(border)
        print(f"⛏️ extracted functions: {list(exec_res.keys())}")

class GenerateTestCases(Node):
    def prep(self, shared):
        """Generate test case for later test code generate"""
        if "functions" not in shared:
            raise ValueError("No functions found in shared context")
            
        if not shared["functions"]:
            raise ValueError("Functions list is empty")
        

        # Get function info from params instead of shared
        function_name = self.params["function_name"]
        function_content = self.params["function_content"]
        print(f"{border}\n🧪 Generate {function_name} test cases...")

        error_prompt = get_error_prompt(shared, ['generateTestCases', function_name])

        prompt = f"""
            ### CONTEXT
            You are an assistant to help the Quality Assurance Engineer to generate test cases

            ## FUNCTIONS
            {function_name}: {function_content}

{error_prompt}

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
        
        return prompt

    def exec(self, prompt):
        response = call_llm(prompt)
        try:
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
    
    def exec_fallback(self, prep_res, exc):
        return { "error": exc }

    def post(self, shared, prep_res, exec_res):
        function_name = self.params["function_name"]
        if "error" in exec_res:
            return handle_max_iteration_error(shared, exec_res, border, SYSTEM_MAX_LOOP, ["generateTestCases", function_name])
    
        function_name = self.params["function_name"]
        if "test_cases" not in shared:
            shared["test_cases"] = {}
        shared["test_cases"][function_name] = { 'init': exec_res["test_cases"][function_name]}

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

class ImplementFunction(Node):
    def prep(self, shared):
        print(border)
        print("🏗️ Implement the test case functions...")
        function_name = self.params["function_name"]

        function_name, functions, test_cases = function_name, shared["functions"][function_name], shared["test_cases"][function_name]["init"]

        formatted_tests = ""
        for i, test in enumerate(test_cases, 1):
            formatted_tests += f"- {function_name}:"
            formatted_tests += f"{i}. {test['name']}\n"
            formatted_tests += f"   input: {test['input']}\n"
            formatted_tests += f"   expected: {test['expected']}\n\n"
        
        error_prompt = ""
        if 'error-implement' in shared:
            error_prompt = get_error_prompt(shared, ['error-implement', 'revise', function_name])
        else:
            error_prompt = get_error_prompt(shared, ['implement', function_name])
        
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

{error_prompt}

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

        return prompt

    def exec(self, prompt):
        response = call_llm(prompt)
        try:
            # Try to extract YAML content
            if "```yaml" not in response:
                raise ValueError("LLM response missing YAML code block")
                
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            result = yaml.safe_load(yaml_str)

            # Validation asserts
            assert "function_code" in result, "Result must have 'function_code' field"
            assert isinstance(result["function_code"], str), "function_code must be string"
            
            return result["function_code"]
            
        except Exception as e:
            print(f"Error in implement exec: {str(e)}")
            print("Raw LLM response:", response if 'response' in locals() else "No response")
            raise

    def exec_fallback(self, prep_res, exc):
        return { "error": exc }

    def post(self, shared, prep_res, exec_res):
        function_name = self.params["function_name"]
        if "error" in exec_res:
            return handle_max_iteration_error(shared, exec_res, border, SYSTEM_MAX_LOOP, ["implement", function_name])
    
        if "test_code" not in shared:
            shared["test_code"] = {}
        shared["test_code"][function_name] = exec_res

class RunTests(AsyncParallelBatchNode):
    async def prep_async(self, shared):
        # Match each 'describe(...) { ... });' block
        print(border)
        print("🏃 Running test functions...")
        shared["max_iterations"] = shared.get("max_iteration", MAX_ITERATION)
        function_name = self.params["function_name"]
        
        # Initialize iteration counts for each test suite if not exists
        if "suite_iterations" not in shared:
            shared["suite_iterations"] = {}
            if function_name not in shared["suite_iterations"]:
                shared["suite_iterations"][function_name] = {}

        return extract_describe_blocks(shared["test_code"][function_name])
    
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
        function_name = self.params["function_name"]

        # Aggregate results from all batches
        for batch_result in exec_res_list:
            if isinstance(batch_result, dict) and "status" in batch_result:
                status = batch_result["status"]
                suite_name = batch_result.get("suite", "unknown_suite")

                # Initialize suite iteration count if not exists
                if function_name not in shared["suite_iterations"]:
                    shared["suite_iterations"][function_name] = {}
                    
                if suite_name not in shared["suite_iterations"][function_name]:
                    shared["suite_iterations"][function_name][suite_name] = 0
                    
                # Increment iteration count for this suite
                shared["suite_iterations"][function_name][suite_name] += 1
                
                total_tests += status.get("total", 0)
                passed_tests += status.get("passed", 0)
                failed_tests += status.get("failed", 0)
                if "detail" in batch_result:
                    all_failed_details.extend(batch_result["detail"])
            else:
                print(f"Warning: Unexpected item in exec_res_list: {batch_result}")

        # Print aggregate test results
        print(border)
        title = f"--- Aggregate {function_name} Test Results: {passed_tests}/{total_tests} Passed ---"
        print(title)

        if failed_tests == 0:
            return "default"
        if "passed" not in shared:
            shared["passed"] = {}
        if "total_tests" not in shared:
            shared["total_tests"] = {}
        if "failed_tests" not in shared:
            shared["failed_tests"]= {}

        shared["passed"][function_name] = passed_tests
        shared["total_tests"][function_name] = total_tests
        shared["failed_tests"][function_name] = all_failed_details
        
        # Check if any suite has reached max iterations
        max_iterations_reached = any(
            shared["suite_iterations"][function_name][suite] >= shared["max_iterations"]
            for suite in shared["suite_iterations"][function_name]
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
        
        function_name = self.params["function_name"]
        if 'iteration_count' not in shared:
            shared['iteration_count'] = {}
    
        if function_name not in shared['iteration_count']:
            shared['iteration_count'][function_name] = 0
        else: 
            shared['iteration_count'][function_name] += 1
        
        test_cases = shared.get("test_cases", {}) 
        failed_tests = shared.get("failed_tests", {}) 
        
        # Format current test cases nicely
        formatted_tests = ""
        count = 0
        try:
            for _, tests in test_cases[function_name].items():
                for test in tests:
                    count += 1
                    if isinstance(test, str):
                        print(222, tests)
                        print(333, test)
                    formatted_tests += f"{count}. {test['name']}\n"
                    if 'explain' in test:
                        formatted_tests += f"   explain: {test['explain']}\n"
                    formatted_tests += f"   input: {test['input']}\n"
                    formatted_tests += f"   expected: {test['expected']}\n\n"
            
            # Format failed tests nicely
            formatted_failures = ""
            for i, result in enumerate(failed_tests[function_name], 1):
                formatted_failures += f"{i}. {result['test_case']}:\n"
                formatted_failures += f"   received: {result['received']}\n"
                formatted_failures += f"   expected: {result['expected']}\n"
                formatted_failures += f"   description: {result['description']}\n\n"
        except Exception as e:
            if 'implement' not in shared:
                shared['implement'] = {}
            shared['implement'][function_name] = e
            return {'error-implement': e}
        
        error_prompt = get_error_prompt(shared, ['revise', function_name])

        prompt = f"""
You are a QA engineer to check and fix the test code result. 

{error_prompt}

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
    {shared.get("test_cases", {}) if shared.get("test_cases", {}) else "No test cases available"}

    Current function:
    {f"```javascript\n{shared.get("functions", {})}\n```" if shared.get("functions", {}) else 'No functions available'}

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
    3. You must include the pass functions into the test_code as well.
```"""

        return prompt

    def exec(self, input):
        if 'error-implement' in input:
            return input
        
        prompt = input
        response = call_llm(prompt)
        try:
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
            
            if "test_code" in result:
                assert isinstance(result["test_code"], str), "test_code must be string"
                assert "describe" in result["test_code"], "Test code must include describe block"
                assert "test(" in result["test_code"], "Test code must include test cases"
                assert "expect" in result["test_code"], "Test code must include expect statements"

            return result
        except Exception as e:
            print(f"Error in revise exec: {str(e)}")
            print("Raw LLM response:", response if 'response' in locals() else "No response")
            raise
        
    def exec_fallback(self, prep_res, exc):
        return { "error": exc }

    def post(self, shared, prep_res, exec_res):
        function_name = self.params["function_name"]
        if "error-implement" in exec_res:
            return handle_max_iteration_error(shared, exec_res, border, SYSTEM_MAX_LOOP, ["revise", function_name], return_key='error-implement')

        if "error" in exec_res:
            return handle_max_iteration_error(shared, exec_res, border, SYSTEM_MAX_LOOP, ["revise", function_name])
        
        # Print what is being revised
        print(f"\n=== Revisions (Iteration {shared['iteration_count']}) ===")

        # Handle test case revisions
        if "test_cases" in exec_res:
            print("Revising test cases:")
            
            # Handle pass test cases
            if "pass" in exec_res["test_cases"]:
                print("Passing test cases:")
                for test_case in exec_res["test_cases"]["pass"]:
                    print(f"  Test {test_case['name']}")
                    print(f"    input: {test_case['input']}")
                    print(f"    expected: {test_case['expected']}")
                    print(f"    status: {test_case['status']}")
            
            # Handle retry test cases
            if "retry" in exec_res["test_cases"]:
                print("Retry test cases:")
                for test_case in exec_res["test_cases"]["retry"]:
                    print(f"  Test {test_case['name']}")
                    print(f"    input: {test_case['input']}")
                    print(f"    expected: {test_case['expected']}")
                    print(f"    status: {test_case['status']}")
            
            # Update shared test cases
            shared["test_cases"][function_name] = { 'init': '', **exec_res["test_cases"] }
        
        if  "function_suggestion" not in shared:
            shared["function_suggestion"] = {}
            
        # Handle function suggestion
        if "function_suggestion" in exec_res:
            shared["function_suggestion"][function_name] = exec_res["function_suggestion"]  # Use first suggestion
        
        # Handle test code
        if "test_code" in exec_res:
            if "test_code" not in shared:
                shared["test_code"] = {}
            function_name = self.params["function_name"]
            shared["test_code"][function_name] = exec_res["test_code"] 
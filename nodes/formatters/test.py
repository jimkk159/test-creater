import os
import re
from datetime import datetime
from config import SystemConfig


class TestFormatter:
    @staticmethod
    def format_test_cases(test_cases):
        """Format test cases for display"""
        formatted_tests = ""
        for test in test_cases:
            formatted_tests += f"- name: \"{test['name']}\"\n"
            formatted_tests += f"  input:\n"
            for i, key in enumerate(test["input"], 1):
                formatted_tests += f"    param{i}: {test['input'][key]}\n"
            formatted_tests += f"  expected: {test['expected']}\n\n"
        return formatted_tests

    @staticmethod
    def format_failed_tests(failed_tests):
        """Format failed test results for display"""
        formatted_failures = ""
        for i, result in enumerate(failed_tests, 1):
            formatted_failures += f"{i}. {result['test_case']}:\n"
            formatted_failures += f"   received: {result['received']}\n"
            formatted_failures += f"   expected: {result['expected']}\n"
            formatted_failures += f"   description: {result['description']}\n\n"
        return formatted_failures

    @staticmethod
    def print_test_cases(test_cases, border_len=SystemConfig.BORDER_LEN):
        """Print formatted test cases"""
        print(f"\n=== Generated {len(test_cases)} Test Cases ===\n")
        for function_name, test_case_list in test_cases.items():
            print(
                f"-- Function: {function_name} {'-' * (border_len - 11 - len(function_name))}"
            )
            for i, test_case in enumerate(test_case_list, 1):
                print(f"{i}. {test_case['name']}")
                print(f"   explain: {test_case['explain']}")
                print(f"   input: {test_case['input']}")
                print(f"   expected: {test_case['expected']}")
        print(SystemConfig.BORDER)
        print("")

    @staticmethod
    def print_test_results(function_name, passed, total, border_len=SystemConfig.BORDER_LEN):
        """Print test results summary"""
        print(SystemConfig.BORDER)
        title = (
            f"--- Aggregate {function_name} Test Results: {passed}/{total} Passed ---"
        )
        print(title)

    @staticmethod
    def _format_individual_failure(detail, failure_num, border_len):
        """Format a single test failure for display"""
        print(f"\n📋 Failure #{failure_num}")
        print(f"   Suite:     {detail.get('suite', 'Unknown')}")
        print(f"   Test:      {detail.get('test_case', 'Unknown')}")
        print(f"   Status:    {'❌ FAILED' if not detail.get('passed', True) else '✅ PASSED'}")
        
        # Extract the core error message from description
        description = detail.get('description', '')
        if 'Expected substring:' in description and 'Received function did not throw' in description:
            expected_match = re.search(r'Expected substring: "([^"]+)"', description)
            expected = expected_match.group(1) if expected_match else 'Unknown error'
            print(f"   Issue:     Function should throw error: '{expected}'")
            print(f"   Problem:   Function executed without throwing")
        elif 'expect(received).toBe(expected)' in description:
            print(f"   Issue:     Value assertion failed")
            if detail.get('expected') is not None:
                print(f"   Expected:  {detail['expected']}")
            if detail.get('received') is not None:
                print(f"   Received:  {detail['received']}")
        elif 'toThrowError' in description:
            print(f"   Issue:     Expected function to throw an error")
            print(f"   Problem:   Function completed without throwing")
        else:
            # Fallback for other error types
            print(f"   Issue:     Test assertion failed")
            if detail.get('expected') is not None:
                print(f"   Expected:  {detail['expected']}")
            if detail.get('received') is not None:
                print(f"   Received:  {detail['received']}")
        
        print(f"   {'─' * (border_len - 3)}")

    @staticmethod
    def print_failed_test_details(failed_details, border_len=SystemConfig.BORDER_LEN):
        """Pretty print failed test details in a readable format"""
        if not failed_details:
            return
            
        # print("\n" + "=" * border_len)
        # print("🔴 FAILED TEST DETAILS")
        # print("=" * border_len)
        
        # for i, detail in enumerate(failed_details, 1):
        #     TestFormatter._format_individual_failure(detail, i, border_len)
        

class TestPromptBuilder:
    @staticmethod
    def save_prompt_to_file(prompt, prompt_type, function_name=None):
        """Save prompt to a file for debugging/reference

        Args:
            prompt (str): The prompt to save
            prompt_type (str): Type of prompt (e.g., 'analyze', 'test_case', 'implement')
            function_name (str, optional): Name of function if applicable
        """

        # Create prompts directory if it doesn't exist
        prompts_dir = os.path.join(SystemConfig.TEST_DIRECTORY, "prompts")
        os.makedirs(prompts_dir, exist_ok=True)

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prompt_type}_{timestamp}"
        if function_name:
            filename += f"_{function_name}"
        filename += ".txt"

        # Save prompt to file
        filepath = os.path.join(prompts_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(prompt)

        return filepath

    @staticmethod
    def build_analyze_prompt(file_content, error_prompt=""):
        """Build prompt for analyzing functions in file"""
        return f"""
### CONTEXT
You are an assistant that help the code tester to extract the functions which need to be tested in the content.

{error_prompt}

### TASK
Extract the function in the file

### FILE CONTENT
{file_content}

## NEXT ACTION
Extract functions in the file

Return your response in this format:

```yaml
functions: 
    - <function name>: |
        <function content with proper indentation>
    - <function name>: |
        <function content with proper indentation>
```

IMPORTANT YAML FORMATTING RULES:
1. Use the | character for multi-line function content
2. After the | character, ALL content must be indented by 4 more spaces
3. Example format:
   ```yaml
   functions:
       - add: |
           function add(a, b) {{
               return a + b;
           }}
       - subtract: |
           function subtract(a, b) {{
               return a - b;
           }}
   ```
4. If you get an error, just try to fix the error and try again
5. If you think you can't handle the error, just return the error action
"""

    @staticmethod
    def build_test_case_prompt(function_name, function_content, suggestion="", error_prompt=""):
        """Build prompt for generating test cases"""
        return f"""
### CONTEXT
You are an assistant to help the Quality Assurance Engineer to generate test cases

## FUNCTIONS
{function_name}: {function_content}

### SUGGESTION
{suggestion}

{error_prompt}

### IMPORTANT YAML FORMATTING RULES:
- Always quote string values that contain colons (:), quotes, or special characters
- For error messages like "Error: Division by zero", use quotes: expected: "Error: Division by zero"
- For simple values like numbers or booleans, no quotes needed: expected: 42
- Use proper indentation (4 spaces) for nested items

### Output in this YAML format with reasoning:
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

    @staticmethod
    def build_implement_prompt(file_path, functions, formatted_tests, error_prompt=""):
        """Build prompt for implementing test functions"""

        example = """
    <import-file-path> // use exports-loader

    describe('function name', () => {
        test('explain', () => {
            expect(sum(1, 2)).toBe(3);
        });

        test('another explain', () => {
            expect(sum(1, 2)).toBe(3);
        });
    });
"""

        return f"""Implement the test cases in JavaScript by Jest base on the functions.

## PATHS
CODE_TO_TEST_PATH: {os.path.abspath(file_path)}

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

    @staticmethod
    def build_revise_prompt(
        test_cases, curr_function, test_code, formatted_failures, error_prompt=""
    ):
        """Build prompt for revising failed tests"""
        return f"""
You are a QA engineer responsible for improving test code and evaluating test failures.

{error_prompt}

### NEXT ACTION
Choose one of the following actions: [pass, revise, error]

- pass: Test code is correct and requires no changes.
- revise: Test code or original function needs adjustments.
- error: An issue occurred that needs human intervention.

### GOAL
1. Analyze the failures and suggest revisions in YAML format.
2. Ensure that either the test code or the original function is reasonable.
3. Validate that test cases and their expected outputs are logical and consistent.

### TIPS
1. If a test fails due to a bug in the function, you do not need to revise the test case.
2. Place passing test cases in the "pass" class and those to be retried in the "retry" class.
3. Include the complete revised test code in the "test_code" section.
4. If the original function has a bug, include the corrected version in the "function_suggestion" section.
5. The test code require path should match the suggested file path.
6. Function Suggestion must include import references, functions itself and function exportations for test file to run it.

### TEST RESULT INFORMATION

- Current test cases:
{test_cases if test_cases else "No test cases available"}

- Current function:
{f"```javascript\\n{curr_function}\\n```" if curr_function else 'No functions available'}

- Current test code:
{test_code}

- Failed tests:
{formatted_failures}

### Output in this YAML format:

```yaml
action: <selected action>
thinking: |
    <Explain your reasoning and how to proceed>

<If test code needs revision>
reasoning: |
    After reviewing the failures, it seems...
    The problem is...
    I will revise the test code and mark it for retry...

<If the function has a bug instead>
reasoning: |
    The test code is correct, but the original function has a bug...
    I will include it in the pass class...

test_cases:
    pass:
        - name: "Test name"
          input: {{...}}
          expected: ...
          status: ok
    retry:
        - name: "Revised test name"
          input: {{...}}
          expected: ...
          status: fail

function_suggestion:  # Entire function file content, include function's reference, content and export    
test_code:  # Include if test code is revised
```

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
function_suggestion: |
    function add(a, b) {{
        if (typeof a !== 'number' || typeof b !== 'number' || isNaN(a) || isNaN(b)) {{
            throw new Error("Invalid input: both parameters must be numbers.");
        }}
        return a + b;
    }}

    module.exports = {{ add }};
test_code: |
    const {{ add }} = require('...');
    
    describe('add function', () => {{
        test('Basic case - positive integers', () => {{
            expect(add(5, 3)).toBe(8);
        }});
    }});
"""
    @staticmethod
    def build_file_coordinator_function_prompt(functions_order, functions, file_path, suggested_file_paths):        
        function_str = ""
        for function_name in functions_order:
            function_str += f"""
{function_name}:
{functions[function_name]}

"""
            
        suggested_file_paths_str = ""
        for function_name in functions_order:
            suggested_file_paths_str += f"""
                - {function_name}: {os.path.abspath(suggested_file_paths[function_name])}
            """

        return f"""You are a QA engineer responsible for combining multiple standalone functions into a single coordinated file.

### TASK
Combine all the individual functions below into one single JavaScript file.

### FUNCTIONS TO COMBINE
{function_str}

### IMPORTANT
- Do not import any functions - you are COMBINING them, not importing them
- Remove any individual `module.exports` from each function
- Add ONE SINGLE `module.exports` at the end with ALL function names
- Keep all function implementations exactly as they are (don't modify the function logic)
- Each function should be a standalone function definition in the combined file

### OUTPUT FORMAT
Return your response in this YAML format:
```yaml
combined_function: |
    function functionName1(params) {{
        // function body exactly as provided
    }}
    
    function functionName2(params) {{
        // function body exactly as provided  
    }}
    
    module.exports = {{ functionName1, functionName2, ... }};
```

### EXAMPLE
If you have these two functions:
```
function add(a, b) {{ return a + b; }} module.exports = {{ add }};
function sub(a, b) {{ return a - b; }} module.exports = {{ sub }};
```

Output should be:
```yaml
combined_function: |
    function add(a, b) {{
        return a + b;
    }}
    
    function sub(a, b) {{
        return a - b;
    }}
    
    module.exports = {{ add, sub }};
```
"""

    @staticmethod
    def build_file_coordinator_test_code_prompt(functions_order, test_codes, file_path, suggested_file_paths):        
        test_codes_str = ""
        for function_name in functions_order:
            test_codes_str += f"""
                - {function_name}:
                    {test_codes[function_name]}
            """
            
        suggested_file_paths_str = ""
        for function_name in functions_order:
            suggested_file_paths_str += f"""
                - {function_name}:
                    {os.path.abspath(suggested_file_paths[function_name])}
            """

        return f"""
        You are a QA engineer responsible for coordinating test code and suggested file paths.
        
        ### TASK
        Combine test codes and suggested file paths into a single file.
        
        ### TEST CODE
        {test_codes_str}
        
        ### FILE PATHS
        {os.path.abspath(file_path)}

        ### SUGGESTED FILE PATHS
        {suggested_file_paths_str}

        ### Output combined test code in this YAML format:
        ```yaml
            <import library>
            <test code>
        ```
        
        ### TEST CODE INPUT EXAMPLE
        test_codes:
            - file1:
                describe('add function', () => {{
                    test('Basic case - positive integers', () => {{
                        expect(add(5, 3)).toBe(8);
                    }});
                }});
                    
            - file2:
                describe('sub function', () => {{
                    test('Basic case - positive integers', () => {{
                        expect(sub(5, 3)).toBe(2);
                    }});
                }});
                
        
        ### TEST CODE OUTPUT EXAMPLE
        ```yaml
            test_code: |
                describe('add function', () => {{
                    test('Basic case - positive integers', () => {{
                        expect(add(5, 3)).toBe(8);
                    }});
                }});

                describe('sub function', () => {{
                    test('Basic case - positive integers', () => {{
                        expect(sub(5, 3)).toBe(2);
                    }});
                }});
        ```
"""


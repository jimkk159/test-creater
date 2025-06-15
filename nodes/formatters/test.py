import os
from datetime import datetime
from ..constants import BORDER_LEN
from constants import TEST_DIRECTORY
class TestFormatter:
    @staticmethod
    def format_test_cases(test_cases, function_name):
        """Format test cases for display"""
        formatted_tests = ""
        for i, test in enumerate(test_cases, 1):
            formatted_tests += f"- {function_name}:"
            formatted_tests += f"{i}. {test['name']}\n"
            formatted_tests += f"   input: {test['input']}\n"
            formatted_tests += f"   expected: {test['expected']}\n\n"
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
    def print_test_cases(test_cases, border_len=BORDER_LEN):
        """Print formatted test cases"""
        print(f"\n=== Generated {len(test_cases)} Test Cases ===\n")
        for function_name, test_case_list in test_cases.items():
            print(f"-- Function: {function_name} {'-' * (border_len - 11 - len(function_name))}")
            for i, test_case in enumerate(test_case_list, 1):
                print(f"{i}. {test_case['name']}")
                print(f"   explain: {test_case['explain']}")
                print(f"   input: {test_case['input']}")
                print(f"   expected: {test_case['expected']}")
        print('-' * border_len)
        print("")

    @staticmethod
    def print_test_results(function_name, passed, total, border_len=BORDER_LEN):
        """Print test results summary"""
        print('-' * border_len)
        title = f"--- Aggregate {function_name} Test Results: {passed}/{total} Passed ---"
        print(title)

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
        prompts_dir = os.path.join(TEST_DIRECTORY, 'prompts')
        os.makedirs(prompts_dir, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{prompt_type}_{timestamp}"
        if function_name:
            filename += f"_{function_name}"
        filename += ".txt"
        
        # Save prompt to file
        filepath = os.path.join(prompts_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
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

    @staticmethod
    def build_test_case_prompt(function_name, function_content, error_prompt=""):
        """Build prompt for generating test cases"""
        return f"""
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
    def build_revise_prompt(test_cases, functions, formatted_failures, error_prompt=""):
        """Build prompt for revising failed tests"""
        return f"""
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
    {test_cases if test_cases else "No test cases available"}

    Current function:
    {f"```javascript\\n{functions}\\n```" if functions else 'No functions available'}

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
``` 
"""
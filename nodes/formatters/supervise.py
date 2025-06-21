from config import SharedKeys
from utils.utils import get_error_prompt

class SupervisePromptBuilder:
    @staticmethod
    def supervise_test_case_prompt(shared, function_name, formatted_tests):
        """Build the prompt for tool decision"""
        
        function_to_be_tested = shared[SharedKeys.FUNCTIONS][function_name]
        if SharedKeys.SUGGESTION not in shared:
            shared[SharedKeys.SUGGESTION] = {}
        previous_suggestions = shared[SharedKeys.SUGGESTION].get(function_name, [])
        previous_suggestion_llm = "\n".join(previous_suggestions)

        return f"""
### ROLE
You are a Supervisor of QA engineers. 

### CONTEXT
You are given a function to be tested and a list of test cases generated from the function by a QA engineer.

### TASK
Evaluate whether the generated test cases are reasonable and right.
The test cases should cover the main functionality of the function.
The test cases should be independent of each other.
The test cases should be easy to understand.

### PREVIOUS SUGGESTION
{previous_suggestion_llm}

### FUNCTION TO BE TESTED
{function_to_be_tested}

### TEST CASES
{formatted_tests}

## NEXT ACTION
base on the previous test cases and previous suggestion (if there has any),
decide next action to exec.

Your action choice: [suggest, done, error]

- suggest:
    suggest a new test case or modify the existing test case.

- done:
    This action means the test cases are good.

- error:
    Something went wrong, and you need human to solve the problem

### INSTRUCTIONS
1. You should ask yourself whether the test case is reasonable. 
2. You should ask yourself whether the test case is right. 
    e.g. 1 + 1 should expect 2, not 3.
3. You should ask yourself whether the logic of the test case is duplicated. 
    e.g. 1 + 1 expect 2, 1 + 2 expect 3 are duplicated.
3. You should ask yourself whether the test case is comprehensive.
4. You should ask yourself whether the test case is independent of each other.
5. You should ask yourself do I miss any test cases?

### OUTPUT FORMAT

You MUST respond with ONLY valid YAML inside code fences. Do NOT include any explanatory text outside the YAML block.

```yaml
action: suggest
thinking: |
  The current test cases don't cover edge cases like negative numbers.
  I should suggest adding a test for negative inputs.
reason: Need to test negative number handling
suggestion: |
  name: test_negative_numbers
  reason: Original tests only cover positive numbers, need negative case
  input: {{ a: -5, b: 3 }}
  expected: -2
```

IMPORTANT: 
- Start your response directly with ```yaml
- End with ```
- Do NOT add any text before or after the YAML block
- Use proper YAML formatting with colons and indentation
- For multi-line values, use the | operator
- For input parameters, use JSON object format: {{ param_name: value, param_name2: value2 }}
"""
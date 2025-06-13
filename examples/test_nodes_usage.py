"""
Example of using the refactored test nodes.

This example shows how the new modular structure makes test automation
much cleaner and easier to understand.
"""

from myPocketFlow import Flow
from nodes import (
    # Test nodes (new clean naming)
    AnalyzeNode,
    GenerateTestCasesNode, 
    ImplementFunctionNode,
    RunTestsNode,
    ReviseNode,
    
    # Test constants
    TestActions,
    TestKeys,
)

# Create clean, focused test nodes
analyze = AnalyzeNode()
generate_tests = GenerateTestCasesNode()
implement = ImplementFunctionNode()
run_tests = RunTestsNode()
revise = ReviseNode()

# Wire up the test flow with clear action transitions
analyze >> generate_tests
generate_tests >> implement
implement >> run_tests

# Handle test failures with revision loop
run_tests - TestActions.FAILURE >> revise
run_tests - TestActions.MAX_ITERATIONS >> revise
revise >> implement  # After revision, re-implement and test

# Create the flow
test_flow = Flow(start=analyze)

async def main():
    """Example usage of the test automation flow"""
    shared = {
        "file": {
            "tool_result": """
            function add(a, b) {
                return a + b;
            }
            
            function multiply(a, b) {
                return a * b;
            }
            """
        },
        "max_iteration": 3
    }
    
    # Set up function parameters for batch processing
    functions = ["add", "multiply"]
    for func_name in functions:
        # You would extract function content from the analyzed code
        func_content = f"function {func_name}() {{ /* implementation */ }}"
        
        # Set parameters for each function
        generate_tests.set_params({
            "function_name": func_name,
            "function_content": func_content
        })
        implement.set_params({"function_name": func_name})
        run_tests.set_params({"function_name": func_name})
        revise.set_params({"function_name": func_name})
    
    # Run the test automation flow
    test_flow.run(shared)
    
    # Access results using the clean manager interface
    if TestKeys.TEST_CASES in shared:
        print("Generated test cases:", shared[TestKeys.TEST_CASES])
    
    if TestKeys.TEST_CODE in shared:
        print("Generated test code:", shared[TestKeys.TEST_CODE])
    
    # Check test results
    passed_tests = shared.get(TestKeys.PASSED, {})
    total_tests = shared.get(TestKeys.TOTAL_TESTS, {})
    
    for func_name in functions:
        if func_name in passed_tests:
            passed = passed_tests[func_name]
            total = total_tests[func_name]
            print(f"{func_name}: {passed}/{total} tests passed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 